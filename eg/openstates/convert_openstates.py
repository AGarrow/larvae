#!/usr/bin/env python

from popolo.organization import Organization
from popolo.membership import Membership
from billy.core import db


def save_objects(payload):
    pass


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
        save_object(committee)


def create_

if __name__ == "__main__":
    create_committee_orgs()
