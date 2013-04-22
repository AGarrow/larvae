#!/usr/bin/env python

from popolo.organization import Organization
from popolo.membership import Membership
from popolo.person import Person

from billy.core import db

from pymongo import Connection
import uuid

connection = Connection('localhost', 27017)
nudb = connection.popolo  # XXX: Fix the db name


type_tables = {
    Organization: "organizations",
    Membership: "memberships",
    Person: "people"
}


def save_objects(payload):
    for entry in payload:
        entry.validate()
        table = getattr(nudb, type_tables[type(entry)])
        eo = entry.as_dict()
        eo['_id'] = eo['id']
        table.save(eo)


def save_object(payload):
    return save_objects([payload])


def create_committee_orgs():
    for committee in db.committees.find():
        orga = Organization(committee['_id'],
                            committee['committee'])

        if committee.get("parent_id", None):
            orga.parent_id = committee['parent_id']
        else:
            # the parent is the COW
            cow = nudb.organizations.find_one({"id": committee['state']})
            orga.parent_id = cow['id']

        memberships = []

        for member in committee['members']:
            if not member.get("leg_id", None):
                continue  # XXX: Expected behavior?

            person_id = member["leg_id"]
            cid = committee['_id']
            guid = "{cid}.{person_id}".format(**locals())
            memberships.append(Membership(guid, person_id, orga.id))

        save_objects(memberships)
        save_object(orga)


def create_cow(abbr):
    metad = db.metadata.find_one({"_id": abbr})
    cow = Organization(abbr, metad['legislature_name'])
    for post in db.districts.find({"abbr": abbr}):
        for seat in range(int(post['num_seats'])):
            sid = "%s.%s" % (post['_id'], seat)
            cow.add_post(sid, post['name'], "Member",
                         chamber=post['chamber'], district=post['name'])

    return cow


def convert_people():
    cows = {}  # Committee on the whole
    parties = {}
    people = []
    memberships = []
    allocated_posts = set([])
    person_copy_block = set([
        "district",
        "chamber",
        "country",
        "_scraped_name",
        "state",
        "active",
        "party",
        "updated_at",
        "created_at",
        "full_name",
        "old_roles",
        "roles",
        "email",
        "_locked_fields",
        "photo_url",
        "_all_ids",  # XXX: Need to translate this
        "offices",  # XXX: move to post
        "id", "_id", "leg_id"
    ])

    def allocate_post(person, orga):
        district = person['district']
        for i, post in enumerate(
            filter(lambda x: x['district'] == district, orga.posts)
        ):
            if post['id'] in allocated_posts:
                continue
            break

        pid = post['id']
        allocated_posts.add(pid)
        return pid, i

    def get_party(party):
        party_org = parties.get(party, None)
        if not party_org:
            party_org = Organization(str(uuid.uuid4()),
                                     "{party} Party".format(**locals()))
            parties[party] = party_org
        return parties[party]

    for person in db.legislators.find({"active": True}):
        state = person['state']
        current_role = person['roles'][0]
        person_id = person['_id']

        chamber = current_role['chamber']
        party = current_role['party']
        district = current_role['district']

        cow = cows.get(state, None)
        if not cow:
            cows[state] = cow = create_cow(state)

        party = party.encode('utf-8')
        party_org = get_party(party)

        post_id, post_offset = allocate_post(person, cow)
        post = cow.posts[post_offset]
        addresses = []

        for address in person['offices']:
            for entry in address:
                if entry in ["name", "type"]:
                    continue

                if address[entry]:
                    addresses.append({
                        "key": entry,
                        "value": address[entry]
                    })

        memberships.append(Membership(
            "{cow.id}.{person_id}".format(**locals()),
            person_id,
            cow.id,
            post_id=post_id,
            addresses=addresses))

        memberships.append(Membership(
            "{party}.{person_id}".format(**locals()),
            person_id, party_org.id))  # Party membership

        who = Person(person['full_name'], id=person_id)

        for entry in person:
            # let's copy fields over into extras.
            if entry in person_copy_block:
                continue

            if person[entry]:
                who.extras[entry] = person[entry]

        people.append(who)

    save_objects(people)
    save_objects(memberships)
    save_objects(cows.values())
    save_objects(parties.values())


if __name__ == "__main__":
    for entry in type_tables.values():
        print("Dropping %s" % (entry))
        nudb.drop_collection(entry)

    print("Converting people")
    convert_people()

    print("Converting committees")
    create_committee_orgs()
