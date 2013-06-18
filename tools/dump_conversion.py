#!/usr/bin/env python
from larvae.utils import JSONEncoderPlus
from pymongo import Connection
import argparse
import json
import os

connection = Connection('localhost', 27017)
db = connection.larvae  # XXX: Fix the db name

parser = argparse.ArgumentParser(description='Re-convert a state.')
parser.add_argument('state', type=str, help='State to rebuild',
                    default=None, nargs='?')
args = parser.parse_args()
state = args.state


def normalize_person(entry):
    entry['memberships'] = list(db.memberships.find({
        "person_id": entry['_id']
    }))
    return entry


normalizers = {
    "ocd-person": normalize_person
}


def dump(collection, spec):
    for entry in collection.find(spec):
        path = entry['_id']
        path = "%s/%s" % (entry['jurisdiction'], path)
        basename = os.path.dirname(path)
        if not os.path.exists(basename):
            os.makedirs(basename)

        for hook in normalizers:
            if entry['_id'].startswith(hook):
                entry = normalizers[hook](entry)

        with open(path, 'w') as fd:
            print path
            json.dump(entry, fd, cls=JSONEncoderPlus)


spec = {}
if state:
    spec = {"jurisdiction": state}

for collection in [
    db.orgnizations,
    db.people,
    db.bills,
    db.votes,
    db.events
]:
    dump(collection, spec)
