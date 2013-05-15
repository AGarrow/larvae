from larvae.base import LarvaeBase
from six import text_type as str_type


def _cleanup_list(obj, default):
    if not obj:
        obj = default
    elif isinstance(obj, str_type):
        obj = [obj]
    elif not isinstance(obj, list):
        obj = list(obj)
    return obj


class Bill(LarvaeBase):
    """
    A single OpenCivic bill.
    """

    _type = _schema_name = "bill"
    __slots__ = ('actions', 'alternate_bill_ids', 'alternate_titles',
                 'related_bills', 'bill_id', 'chamber', 'documents', 'session',
                 'sources', 'sponsors', 'summaries', 'subjects', 'title',
                 'type', 'versions')

    def __init__(self, bill_id, session, title, type=None, **kwargs):
        super(Bill, self).__init__()

        self.bill_id = bill_id
        self.session = session
        self.title = title
        self.type = _cleanup_list(type, ['bill'])

        self.actions = []
        self.alternate_bill_ids = []
        self.alternate_titles = []
        self.documents = []
        self.related_bills = []
        self.sponsors = []
        self.subjects = []
        self.summaries = []
        self.versions = []

        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_action(self, action, actor, date,
                   type=None, related_entities=None):
        self.actions.append({
            "action": action,
            "actor": actor,
            "date": date,
            "type": _cleanup_list(type, []),
            "related_entities": related_entities or []  # validate
        })

    def add_related_bill(self, bill_id, session, chamber, relation):
        self.related_bills.append({
            "bill_id": bill_id,
            "session": session,
            "chamber": chamber,
            "relation_type": relation  # validate
        })

    def add_sponsor(self, name, sponsorship_type,
                    entity_type, primary,
                    chamber=None, entity_id=None):
        ret = {
            "name": name,
            "sponsorship_type": sponsorship_type,
            "entity_type": entity_type,
            "primary": primary,
        }

        if entity_id:
            ret["entity_id"] = entity_id

        if chamber:
            ret['chamber'] = chamber

        self.sponsors.append(ret)

    def add_subject(self, subject):
        self.subjects.append(subject)

    def add_document_link(
        self, name, url, date=None, type='document',
        mimetype=None, on_duplicate='error'
    ):
        return self._add_associated_link(
            collection='documents',
            name=name,
            url=url,
            date=date,
            type=type,
            mimetype=mimetype,
            on_duplicate=on_duplicate)

    def add_version_link(
        self, name, url, date=None, type='version',
        mimetype=None, on_duplicate='error'
    ):
        return self._add_associated_link(
            collection='versions',
            name=name,
            url=url,
            date=date,
            type=type,
            mimetype=mimetype,
            on_duplicate=on_duplicate)

    def _add_associated_link(self, collection, name, url, date,
                             type, mimetype, on_duplicate):
        """
        """

        if on_duplicate not in ['error', 'ignore']:
            raise TypeError("Sorry; we accept either `error' or `ignore' for "
                            "on_duplicate behavior.")

        versions = getattr(self, collection)
        ver = {
            "name": name,
            "type": type,
            "links": []
        }

        if date:
            ver['date'] = date

        seen_links = set()  # We iterate over everything anyway. Meh. Storing
        # as an instance var is actually non-trivial, since we abuse __slots__
        # for as_dict, and it's otherwise read-only or shared set() instance.

        matches = 0
        for version in versions:
            for link in version['links']:
                seen_links.add(link['url'])

            if False not in (ver.get(x) == version.get(x)
                             for x in ["name", "type", "date"]):
                matches = matches + 1
                ver = version

        if matches > 1:
            raise ValueError("Something went just very wrong internally")

        if url in seen_links:
            if on_duplicate == 'error':
                raise ValueError("Duplicate entry in `%s' - URL: `%s'" % (
                    collection, url
                ))
            else:
                # This means we're in ignore mode. This situation right here
                # means we should *skip* adding this link silently and continue
                # on with our scrape. This should *ONLY* be used when there's
                # a site issue (Version 1 == Version 2 because of a bug) and
                # *NEVER* because "Current" happens to match "Version 3". Fix
                # that in the scraper, please.
                #  - PRT
                return None

        # OK. This is either new or old. Let's just go for it.
        ret = {"url": url}

        if mimetype:
            ret["mimetype"] = mimetype

        ver['links'].append(ret)

        if matches == 0:
            # in the event we've got a new entry; let's just insert it into
            # the versions on this object. Otherwise it'll get thrown in
            # automagically.
            self.versions.append(ver)

        return ver

    def __str__(self):
        return self.bill_id + ' in ' + self.session

    __unicode__ = __str__
