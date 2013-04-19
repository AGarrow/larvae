#!/usr/bin/env python

from popolo.organization import Organization
from popolo.membership import Membership
from popolo.person import Person

from billy.core import db

from pymongo import Connection
connection = Connection('localhost', 27017)
nudb = connection.popolo  # XXX: Fix the db name


type_tables = {
    Organization: "organizations",
    Membership: "memberships",
    Person: "people"
}


def save_objects(payload):
    for entry in payload:
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

        party_org = parties.get(party, None)
        if not party_org:
            party = party.encode('utf-8')
            party_org = Organization("{party}".format(**locals()),
                               "{party} Party".format(**locals()))
            parties[party] = party_org

        memberships.append(Membership(
            "{cow.id}.{person_id}".format(**locals()),
            person_id,
            cow.id))  # COW membership

        memberships.append(Membership(
            "{party}.{person_id}".format(**locals()),
            person_id,
            party_org.id))  # Party membership

        who = Person(person['full_name'],
                     id=person_id)
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
