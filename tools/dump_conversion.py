#!/usr/bin/env python
from larvae.utils import JSONEncoderPlus
from contextlib import contextmanager
from pymongo import Connection
import argparse
import json
import os

parser = argparse.ArgumentParser(description='Re-convert a state.')
parser.add_argument('state', type=str, help='State to rebuild',
                    default=None, nargs='?')

parser.add_argument('--server', type=str, help='Mongo Server',
                    default="localhost")

parser.add_argument('--database', type=str, help='Mongo Database',
                    default="larvae")

parser.add_argument('--port', type=int, help='Mongo Server Port',
                    default=27017)

parser.add_argument('--output', type=str, help='Output Directory',
                    default="dump")

args = parser.parse_args()


@contextmanager
def cd(path):
    pop = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(pop)


state = args.state

connection = Connection(args.server, args.port)
db = getattr(connection, args.database)


def normalize_person(entry):
    data = list(db.memberships.find({
        "person_id": entry['_id']
    }))
    for datum in data:
        datum.pop('_id')

    entry['memberships'] = data

    return entry


normalizers = {
    "ocd-person": normalize_person
}


def dump(collection, spec):
    for entry in collection.find(spec):
        path = entry['_id']
        where = entry.get('openstates_id')
        if where:
            where = where[:2]
        else:
            where = 'unknown'

        path = "%s/%s" % (where, path)
        basename = os.path.dirname(path)
        if not os.path.exists(basename):
            os.makedirs(basename)

        for hook in normalizers:
            if entry['_id'].startswith(hook):
                entry = normalizers[hook](entry)

        with open(path, 'w') as fd:
            print path
            json.dump(entry, fd, cls=JSONEncoderPlus)


path = args.output
if not os.path.exists(path):
    os.makedirs(path)

with cd(path):
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
