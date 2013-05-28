"""
    Schema for event objects.
"""

schema = {
    "description": "event data",
    "properties": {

        # == Basics ==

        # **_type** - All larvae events must have a _type field set to one
        # of tne entries in the enum below.
        "_type": { "enum": [ "event" ], "type": "string" },

        # **description** - A simple description describing the event. As
        # an example, "Fiscal subcommittee hearing on pudding cups" is a valid
        # string.
        "description": { "type": "string" },

        # **all_day** - This signals if an event should be considered to be
        # an all-day event, such as a holiday.
        "all_day": { "type": ["boolean", "null"] },

        # **end** - Ending date / time of the event.
        "end": { "type": ["datetime", "null"] },

        # **start** - Starting date / time of the event.
        "start": { "type": ["datetime"] },

        # **canceled** - Simple boolean if this event has been canceled.
        "canceled": { "type": ["boolean", "null"] },

        # **location** - Where the event will take place. This is a
        # Human-readable string, with the best data that can be found as
        # to the location of the event. Good strings include:
        #
        # > Room E201, Dolan Science Center, 20700 North Park Blvd
        # > University Heights Ohio, 44118
        #
        # Or:
        #
        # > Minority Whip's desk, Floor of the House, Nowhere Ohio
        "location": { "type": "string" },

        # == Related Entities ==

        # **documents** - Links to related documents for the event. Usually,
        # this includes things like pre-written testimony, spreadsheets or
        # a slide deck that a presenter will use.
        "documents": {
            "items": {
                "properties": {
                    # * **note** - name of the document. Something like
                    # "Fiscal Report" or "John Smith's Slides".
                    "note": { "type": "string" },
                    # * **url** - URL where the content may be found.
                    "url": { "type": "string" }

                },
                "type": "object"
            },
            "type": "array"
        },

        # **links** - Links related to the event that are not documents
        # or items in the Agenda. This is filled with helpful links for the
        # event, such as a committee's homepage, reference material or
        # links to learn more about subjects related to the event.
        "links": {
            "description": "URLs for documents about the event",
            "items": {
                "properties": {

                    # * **note** - Human-readable name of the link. Something
                    # like "Historical precedent for popsicle procurement"
                    "note": {
                        "description": "A note, e.g. 'Wikipedia page'",
                        "type": ["string", "null"]
                    },

                    # * **url** - URL where the content may be found
                    "url": {
                        "description": "A URL for a link about the event",
                        "format": "uri",
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },

        # **participants** - List of participants in the event. This includes
        # committees invited, legislators chairing the event or people who
        # are attending.
        #
        # Some entries:
        #
        #      { "participant": "John Q. Smith",
        #        "participant_type": "legislator", "type": "chair" }
        #
        # Which expresses the chair of the event will be John Q. Smith.
        #
        #     { "participant": "Ways and Means",
        #       "participant_type": "committee", "type": "host" }
        #
        # Which expresses the host of the event is the Ways and Means
        # committee.
        "participants": {
            "items": {
                "properties": {
                    # * **chamber** - Optional field storing the chamber
                    # of the related participant.
                    "chamber": { "type": ["string", "null"] },

                    # * **participant** - Human readable name of the entitity.
                    "participant": { "type": "string" },

                    # * **participant_id** - ID of the participant
                    "participant_id": { "type": "string" },

                    # * **participant_type** - What type of entity is this?
                    # `person` may be used if the person is not a Legislator,
                    # butattending the event, such as an invited speaker or one
                    # who is offering testimony.
                    "participant_type": {
                        "enum": [ "committee", "legislator", "person", ],
                        "type": "string"
                    },

                    # * **type** - Role of the entity we're relating to, such
                    # as `chair` for the chair of a meeting.
                    "type": {
                        "enum": [ "host", "chair", "participant" ],
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },

        # **agenda** - Agenda of the event, if any. This contains information
        # about the meeting's agenda, such as bills to discuss or people to
        # present.
        "agenda": {
            "items": {
                "properties": {
                    # * **note** - Human-readable string that represents
                    # this agenda item. A good example would be something like
                    #
                    # > The Committee will consider SB 2339, HB 100
                    "note": { "type": "string" },

                    # * **related_entities** - Entities that relate to this
                    # agenda item, such as presenters, legislative instruments,
                    # or committees.
                    "related_entities": {
                        "properties": {

                            # * * **entity_type** - type of relation, such as
                            # `consideration` or `presenter`.
                            "entity_type": { "type": "string" },

                            # * * **entity_id** - ID of the related entity
                            "entity_id": { "type": "string" },

                            # * * **entity** - human readable string
                            # representing the entity, such as `John Q. Smith`.
                            "entity": { "type": "string" },

                            # * * **note** - human readable string (if any)
                            # noting the relationship between the entity and
                            # the agenda item, such as "Jeff will be presenting
                            # on the effects of too much cookie dough"
                            "note": { "type": "string" },

                            "type": "object"
                        },
                        "minItems": 0,
                        "type": "array",
                    },
                },
                "type": "object"
            },
            "minItems": 0,
            "type": "array"
        },

        # == Sources ==

        # **sources** - like all larvae objects, sources is an array of one
        # or more source object.  Each source object has the following
        # properties:
        #
        # * **url** - URL to resource used to collect
        # * **note** - Note about what this URL was used to collect.
        "sources": {
            "items": {
                "properties": {
                    "url": {
                        "type": "string"
                    },
                    "note": {
                        "type": ["null", "string"],
                    }
                },
                "type": "object"
            },
            "minItems": 1,
            "type": "array"
        },

        "type": {
            "type": "string"
        },
    },
    "type": "object"
}
