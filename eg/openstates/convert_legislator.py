#!/usr/bin/env python

from popolo.person import Person


def convert_legislator_object(person):
    copies = set([  # We use this to copy keys off the person later.
        "full_name",
        "photo_url",
        "offices",
        "roles",
        "state",
        "email",
        "url",
    ])

    who = Person(person['full_name'])

    photo = person.get("photo_url", None)
    if photo:
        who.image = photo

    url = person.get("url", None)
    if url:
        who.add_link("Homepage", url)

    for k, v in person.items():
        if k in copies:
            continue
        if v:
            who.extras[k] = v

    return who


if __name__ == "__main__":
    import json
    import sys
    obj = json.load(open(sys.argv[1], 'r'))
    person = convert_legislator_object(obj)
    print person.as_dict()
