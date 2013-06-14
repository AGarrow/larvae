#!/usr/bin/env python

"""
OK. Let's spot-check a few bills.

"""

from billy.core import db
from pymongo import Connection

connection = Connection('localhost', 27017)
nudb = connection.larvae  # XXX: Fix the db name


pdb = nudb.people


def check_people():
    print "Checking people"
    for person in pdb.find():
        pid, osid = (person.get(x) for x in ('_id', 'openstates_id'))
        refobj = db.legislators.find_one({"_id": osid})
        assert refobj is not None  # OK. We have a valid backref.

        memberships = nudb.memberships.find({"person_id": pid})
        has_juris = False
        has_party = False

        for membership in memberships:
            orgid = membership['organization_id']
            orga = nudb.organizations.find_one({"_id": orgid})
            assert orga is not None
            klass = orga['classification']
            if klass == 'party':
                has_party = True
            if klass == 'jurisdiction':
                assert has_juris is False
                has_juris = True
                # validate state
        assert has_juris, has_party


def check_bills():
    print "Checking bills"
    for bill in nudb.bills.find():
        osbill = db.bills.find_one({"_id": bill['openstates_id']})
        for sponsor in bill['sponsors']:
            ocdid = sponsor.get('id', None)
            if ocdid is None:
                continue

            who = None
            type_ = sponsor['_type']
            if type_ == 'organization':
                who = nudb.organizations.find_one({"_id": ocdid})
            if type_ == 'person':
                who = pdb.find_one({"_id": ocdid})

            assert who

        oactions = [x['description'] for x in bill['actions']]
        for action in osbill['actions']:
            assert action['action'] in oactions

check_bills()
check_people()
