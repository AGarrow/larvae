#!/usr/bin/env python

from larvae.organization import Organization
from larvae.membership import Membership
from larvae.person import Person
from larvae.bill import Bill

from billy.core import db

from pymongo import Connection
import uuid
import sys

connection = Connection('localhost', 27017)
nudb = connection.larvae  # XXX: Fix the db name


type_tables = {
    Organization: "organizations",
    Membership: "memberships",
    Person: "people",
    Bill: "bills",
}

_hot_cache = {}


def ocd_namer(obj):
    # ocd-person/UUID
    # ocd-organization/UUID
    if obj._type in ["person", "organization"]:
        return "ocd-{type_}/{uuid}".format(type_=obj._type,
                                           uuid=uuid.uuid1())
    return None


def is_ocd_id(string):
    return string.startswith("ocd-")


def save_objects(payload):
    for entry in payload:
        entry.validate()
        what = type_tables[type(entry)]
        table = getattr(nudb, what)

        _id = None
        try:
            _id = entry._id
        except AttributeError:
            pass

        ocd_id = ocd_namer(entry)
        if _id and not is_ocd_id(_id):
            _id = None

        if _id is None and ocd_id:
            entry._id = ocd_id

        eo = entry.as_dict()
        mongo_id = table.save(eo)

        if _id is None and ocd_id is None:
            entry._id = mongo_id

        if hasattr(entry, "openstates_id"):
            _hot_cache[entry.openstates_id] = entry._id

        sys.stdout.write(entry._type[0])
        sys.stdout.flush()


def save_object(payload):
    return save_objects([payload])


def migrate_legislatures():
    for metad in db.metadata.find():
        abbr = metad['abbreviation']
        cow = Organization(metad['legislature_name'])
        cow.openstates_id = abbr

        for post in db.districts.find({"abbr": abbr}):

            cow.add_post(label="Member",
                         role="member",
                         num_seats=post['num_seats'],
                         chamber=post['chamber'],
                         district=post['name'])

        save_object(cow)


def lookup_entry_id(collection, openstates_id):
    hcid = _hot_cache.get(openstates_id, None)
    if hcid:
        return hcid

    org = getattr(nudb, collection).find_one({
        "openstates_id": openstates_id
    })

    if org is None:
        return None

    id_ = str(org['_id'])
    _hot_cache[openstates_id] = id_
    return id_


def migrate_committees():

    def attach_members(committee, org):
        for member in committee['members']:
            osid = member.get('leg_id', None)
            person_id = lookup_entry_id('people', osid)
            if person_id:
                m = Membership(person_id, org._id)
                save_object(m)

    for committee in db.committees.find({"subcommittee": None}):
        # OK, we need to do the root committees first, so that we have IDs that
        # we can latch onto down below.
        org = Organization(committee['committee'])
        org.parent_id = lookup_entry_id('organizations', committee['state'])
        org.openstates_id = committee['_id']
        org.sources = committee['sources']
        # Look into posts; but we can't be sure.
        save_object(org)
        attach_members(committee, org)

    for committee in db.committees.find({"subcommittee": {"$ne": None}}):
        org = Organization(committee['subcommittee'])

        org.parent_id = lookup_entry_id(
            'organizations',
            committee['parent_id']
        ) or lookup_entry_id(
            'organizations',
            committee['state']
        )

        org.openstates_id = committee['_id']
        org.sources = committee['sources']
        # Look into posts; but we can't be sure.
        save_object(org)
        attach_members(committee, org)


def drop_existing_data():
    for entry in type_tables.values():
        print("Dropping %s" % (entry))
        nudb.drop_collection(entry)


def create_or_get_party(what):
    hcid = _hot_cache.get(what, None)
    if hcid:
        return hcid

    org = nudb.organizations.find_one({
        "name": what
    })
    if org:
        return org['_id']

    org = Organization(what)
    save_object(org)

    _hot_cache[what] = org._id

    return org._id


def migrate_people():
    for entry in db.legislators.find():
        who = Person(entry['full_name'])
        who.openstates_id = entry['_id']

        for k, v in {
            "photo_url": "image",
            "chamber": "chamber",
            "district": "district",
        }.items():
            if entry.get(k, None):
                setattr(who, v, entry[k])

        who.sources = entry['sources']

        home = entry.get('url', None)
        if home:
            who.add_link(home, "Homepage")

        blacklist = ["photo_url", "chamber", "district", "url",
                     "roles", "offices", "updated_at", "created_at",
                     "party", "state", "_locked_fields", "sources",
                     "active", "old_roles"]

        for key, value in entry.items():
            if key in blacklist or not value:
                continue
            who.extras[key] = value

        legislature = lookup_entry_id('organizations', entry['state'])
        if legislature is None:
            raise Exception("Someone's in the void.")

        save_object(who)  # gives who an id, btw.

        party = entry.get('party', None)

        if party:
            m = Membership(who._id, create_or_get_party(entry['party']))
            save_object(m)

        m = Membership(who._id, legislature)

        chamber, district = (entry.get(x, None)
                             for x in ['chamber', 'district'])

        if chamber:
            m.chamber = chamber

        if district:
            m.district = district

        for office in entry['offices']:
            note = office['name']
            for key, value in office.items():
                if not value or key in ["name", "type"]:
                    continue

                m.contact_details.append([
                    key,
                    value,
                    note
                ])

        save_object(m)


def migrate_bills():
    bills = db.bills.find()
    for bill in bills:
        b = Bill(bill_id=bill['bill_id'],
                 session=bill['session'],
                 title=bill['title'],
                 type=bill['type'])
        for source in bill['sources']:
            b.add_source(source['url'], note='old-source')

        for document in bill['documents']:
            b.add_document(name=document['name'],
                           links=[{"url": document['url']}])

        for version in bill['versions']:
            link = {"url": version['url']}
            mime = version.get("mimetype", None)
            if mime:
                link['mimetype'] = mime

            b.add_version(name=version['name'],
                          links=[link])

        for subject in bill.get('subjects', []):
            b.add_subject(subject)

        for sponsor in bill['sponsors']:
            type_ = 'people'
            sponsor_id = sponsor.get('leg_id', None)

            if sponsor_id is None:
                type_ = 'organizations'
                sponsor_id = sponsor.get('committee_id', None)

            if sponsor_id:
                objid = lookup_entry_id(type_, sponsor_id)
                etype = {"people": "person",
                         "organizations": "committee"}[type_]
                b.add_sponsor(
                    name=sponsor['name'],
                    sponsorship_type=sponsor['type'],
                    entity_type=etype,
                    primary=sponsor['type'] == 'primary',
                    chamber=sponsor.get('chamber', None),
                )


        b.validate()
        save_object(b)


SEQUENCE = [
    drop_existing_data,
    migrate_legislatures,
    migrate_people,  # depends on legislatures
    migrate_committees,  # depends on people
    migrate_bills,
]


if __name__ == "__main__":
    for seq in SEQUENCE:
        seq()

    print("")
    print("Migration complete.")
