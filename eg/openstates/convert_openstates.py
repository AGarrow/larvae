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
        print entry
        table = getattr(nudb, type_tables[type(entry)])
        table.save(entry.as_dict())


def save_object(payload):
    return save_objects([payload])


def create_committee_orgs():
    for committee in db.committees.find():
        orga = Organization(committee['_id'],
                            committee['committee'])
        memberships = []
        # XXX: Fix how we do subcommittees. Pass one to get all committees,
        # then pass over again and assoc as members?

        for member in committee['members']:
            if not member.get("leg_id", None):
                continue  # XXX: Expected behavior?

            person_id = member["leg_id"]
            cid = committee['_id']
            guid = "{cid}.{person_id}".format(**locals())
            memberships.append(Membership(guid, person_id, orga.id))

        save_objects(memberships)
        save_object(orga)


def convert_people():
    cows = {}  # Committee on the whole
    chambers = {}
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
            # XXX: Use metadata to create better name.
            cow = Organization(state, "{state} Legislature".format(**locals()))
            cows[state] = cow

        party_org = parties.get(party, None)
        if not party_org:
            party = party.encode('utf-8')
            party_org = Organization("{state}-{party}".format(**locals()),
                               "{state} {party} Party".format(**locals()))
            parties[party] = party_org

        chamber_org = chambers.get(chamber, None)
        if not chamber_org:
            chamber_org = Organization(
                "{state}-{chamber}".format(**locals()),
                "{state} {chamber} Chamber".format(**locals()))
            chambers[chamber] = chamber_org

        post_id = "{state}-{chamber}-{district}".format(**locals())

        cow.add_post(post_id,
                     "{state} {chamber} {district} district",
                     "Member",)  # XXX Metadata name

        memberships.append(Membership(
            "{post_id}.{person_id}".format(**locals()),
            person_id,
            cow.id))  # COW membership

        memberships.append(Membership(
            "{state}-{chamber}.{person_id}".format(**locals()),
            person_id,
            chamber_org.id))  # COW membership

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
    save_objects(chambers.values())


if __name__ == "__main__":
    convert_people()
    create_committee_orgs()
