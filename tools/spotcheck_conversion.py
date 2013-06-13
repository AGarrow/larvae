#!/usr/bin/env python

"""
OK. Let's spot-check a few bills.

"""

from billy.core import db
from pymongo import Connection

connection = Connection('localhost', 27017)
nudb = connection.larvae  # XXX: Fix the db name


pdb = nudb.people

total_people = pdb.find().count()
spotcheck_pct = 0.3


for person in pdb.find().limit(int(total_people * spotcheck_pct)):
    pid, osid = (person.get(x) for x in ('_id', 'openstates_id'))
    refobj = db.legislators.find_one({"_id": osid})
    assert refobj is not None  # OK. We have a valid backref.

    memberships = nudb.memberships.find({"person_id": pid})
    print list(memberships), pid
