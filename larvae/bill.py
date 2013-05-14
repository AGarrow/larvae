from larvae.base import LarvaeBase


class Bill(LarvaeBase):
    """
    A single OpenCivic bill.
    """

    _type = _schema_name = "bill"
    _seen_links = set()
    __slots__ = ('actions', 'alternate_bill_ids', 'alternate_titles',
                 'related_bills', 'bill_id', 'chamber', 'documents', 'session',
                 'sources', 'sponsors', 'summaries', 'subjects', 'title',
                 'type', 'versions')

    def __init__(self, bill_id, session, title, type=None, **kwargs):
        super(Bill, self).__init__()

        self.bill_id = bill_id
        self.session = session
        self.title = title
        if not isinstance(type, list):
            type = [type]
        self.type = type
        # force'd params

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
            "type": type or [],
            "related_entities": related_entities or []  # validate
        })

    def add_related_bill(self, bill_id, session, chamber, relation):
        self.related_bills.append({
            "bill_id": bill_id,
            "session": session,
            "chamber": chamber,
            "relation_type": relation  # validate
        })

    def add_document(self, name, date=None, type='document', links=None):
        ret = {
            "name": name,
            "type": type,
            "links": links or [],
        }

        if date:
            ret['date'] = date

        self.documents.append(ret)

    def add_sponsor(self, name, sponsorship_type,
                    entity_type, primary, chamber=None):
        ret = {
            "name": name,
            "sponsorship_type": sponsorship_type,
            "entity_type": entity_type,
            "primary": primary,
        }
        if chamber:
            ret['chamber'] = chamber
        self.sponsors.append(ret)

    def add_subject(self, subject):
        self.subjects.append(subject)

    def add_version_link(
        self, name, uri, date=None, type='version',
        mimetype=None, on_duplicate='error'
    ):
        return self._add_associated_link(
            collection='versions',
            name=name,
            uri=uri,
            date=date,
            type=type,
            mimetype=mimetype,
            on_duplicate=on_duplicate)


    def _add_associated_link(self, collection, name, url, date,
                             type, mimetype, on_duplicate):
        versions = getattr(self, collection)
        ver = {
            "name": name,
            "type": type,
            "date": date,
            "links": []
        }
        matches = 0
        for version in versions:
            if False not in (ver[x] == version[x]
                             for x in ["name", "type", "date"]):
                matches =+ 1
                ver = version

        if matches > 1:
            raise ValueError("Something went just very wrong internally")

        if uri in self._seen_links:
            if on_duplicate == 'error':
                raise ValueError("Duplicate bill version URL: `%s'" % (
                    uri))

        self._seen_links.add(uri)


        # OK. This is either new or old. Let's just go for it.
        ver['links'].append({
            "url": uri,
            "mimetype": mimetype
        })
        return version

    def __str__(self):
        return self.bill_id + ' in ' + self.session
    __unicode__ = __str__
