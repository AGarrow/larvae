#!/usr/bin/env python

from larvae.organization import Organization
from larvae.membership import Membership
from larvae.person import Person

from billy.core import db

from pymongo import Connection
import sys

connection = Connection('localhost', 27017)
nudb = connection.larvae  # XXX: Fix the db name


type_tables = {
    Organization: "organizations",
    Membership: "memberships",
    Person: "people"
}

_hot_cache = {}

def save_objects(payload):
    for entry in payload:
        entry.validate()
        what = type_tables[type(entry)]
        table = getattr(nudb, what)
        eo = entry.as_dict()
        nid = table.save(eo)
        entry.id = str(nid)
        if hasattr(entry, "openstates_id"):
            _hot_cache[entry.openstates_id] = entry.id

        sys.stdout.write(what[0].lower())
        sys.stdout.flush()


def save_object(payload):
    return save_objects([payload])


def migrate_legislatures():
    for metad in db.metadata.find():
        abbr = metad['abbreviation']
        cow = Organization(metad['legislature_name'])
        cow.openstates_id = abbr

        for post in db.districts.find({"abbr": abbr}):
            for seat in range(int(post['num_seats'])):
                sid = "%s.%s" % (post['_id'], seat)

                cow.add_post(sid, post['name'], "Member",
                    chamber=post['chamber'], district=post['name'])

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
                m = Membership(person_id, org.id)
                save_object(m)

    for committee in db.committees.find({"subcommittee": None}):
        # OK, we need to do the root committees first, so that we have IDs that
        # we can latch onto down below.
        org = Organization(committee['committee'])
        org.parent_id = lookup_entry_id('organizations', committee['state'])
        org.openstates_id = committee['_id']
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

    _hot_cache[what] = org.id

    return org.id



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
            m = Membership(who.id, create_or_get_party(entry['party']))
            save_object(m)

        m = Membership(who.id, legislature)
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


SEQUENCE = [
    drop_existing_data,
    migrate_legislatures,
    migrate_people,  # depends on legislatures
    migrate_committees,  # depends on people
]


if __name__ == "__main__":
    for seq in SEQUENCE:
        seq()

    print("")
    print("Migration complete.")
