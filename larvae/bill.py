from larvae.base import LarvaeBase


def _cleanup_list(obj, default):
    if not obj:
        obj = default
    elif isinstance(obj, basestring):
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

    def __init__(self, bill_id, session, title, type='bill', **kwargs):
        super(Bill, self).__init__()

        self.bill_id = bill_id
        self.session = session
        self.title = title
        self.type = type

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

    def add_version(self, name, date=None, type='version', links=None):
        ret = {
            "name": name,
            "type": type,
            "links": links or [],
        }
        if date:
            ret['date'] = date
        self.versions.append(ret)

    def __str__(self):
        return self.bill_id + ' in ' + self.session
    __unicode__ = __str__
