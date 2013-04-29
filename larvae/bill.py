from larvae.base import LarvaeBase


class Bill(LarvaeBase):
    """
    A single OpenCivic bill.
    """

    _type = _schema_name = "bill"
    __slots__ = ('actions', 'alternate_bill_ids', 'alternate_titles',
                 'related_bills', 'bill_id', 'chamber', 'documents', 'session',
                 'sources', 'sponsors', 'subjects', 'title', 'type',
                 'versions')

    def __init__(self, bill_id, session, title, **kwargs):
        super(Bill, self).__init__()

        self.bill_id = bill_id
        self.session = session
        self.title = title
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

    def add_action(self, action, actor, date, related_entities):
        self.actions.append({
            "action": action,
            "actor": actor,
            "date": date,
            "related_entities": related_entities  # validate
        })

    def add_related_bill(self, bill_id, session, chamber, relation):
        self.related_bills.append({
            "bill_id": bill_id,
            "session": session,
            "chamber": chamber,
            "relation_type": relation  # validate
        })

    def add_document(self, name, date, type, links=None):
        if links is None:
            links = []

        self.documents.append({
            "name": name,
            "date": date,
            "type": type,
            "links": links,  # validate
        })

    def add_sponsor(self, name, sponsorship_type,
                    entity_type, primary, chamber=None):
        ret = {
            "sponsorship_type": sponsorship_type,
            "entity_type": entity_type,
            "primary": primary,
        }
        if chamber:
            ret['chamber'] = chamber
        self.sponsors.append(ret)

    def add_subject(self, subject):
        self.subjects.append(subject)

    def add_version(self, name, date, type, links=None):
        if links is None:
            links = []
        self.versions.append({
            "name": name,
            "date": date,
            "type": type,
            "links": links
        })

    def __str__(self):
        return self.person_id + ' membership in ' + self.organization_id
    __unicode__ = __str__
