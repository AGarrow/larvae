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

    def __init__(self, **kwargs):
        super(Bill, self).__init__()
        # set instance vars
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

    def add_document(self, name, date, type, links):
        self.documents.append({
            "name": name,
            "date": date,
            "type": type,
            "links": links,  # validate
        })

    def add_sponsor(self, name, sponsorship_type,
                    entity_type, primary, chamber):

        self.sponsors.append({
            "sponsorship_type": sponsorship_type,
            "entity_type": entity_type,
            "primary": primary,
            "chamber": chamber
        })

    def add_subject(self, subject):
        self.subjects.append(subject)

    def add_version(self, name, date, type, links):
        self.versions.append({
            "name": name,
            "date": date,
            "type": type,
            "links": links
        })

    def __str__(self):
        return self.person_id + ' membership in ' + self.organization_id
    __unicode__ = __str__
