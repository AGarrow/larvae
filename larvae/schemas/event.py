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

        # **name** - A simple name of the event, such as
        # "Fiscal subcommittee hearing on pudding cups"
        "name": { "type": "string" },

        # **description** - A longer description describing the event. As
        # an example, "Topics for discussion include this that and the other
        # thing. In addition, lunch will be served".
        "description": { "type": "string", "required": False },

        # **end** - Ending date / time of the event.
        "end": { "type": ["datetime", "null"] },

        # **when** - Starting date / time of the event.
        "when": { "type": ["datetime"] },

        # **status** - String that denotes the status of the meeting. This is
        # useful for showing the meeting is cancelled in a machine-readable
        # way.
        "status": { "type": ["string", "null"],
                    "enum": ["cancelled", "tentative", "confirmed"] },

        # **location** - Where the event will take place.
        "location": {
            "type": "object",
            "properties": {

                # * **name** - name of the location, such as "City Hall, Boston,
                # MA, USA", or "Room E201, Dolan Science Center, 20700 North
                # Park Blvd University Heights Ohio, 44118"
                "name": { "type": "string" },

                # * **note** - human readable notes regarding the location,
                # something like "The meeting will take place at the
                # Minority Whip's desk on the floor"
                "note": { "type": ["string", "null"] },

                # * **coordinates** - coordinates where this event will take
                # place. This is purely optional.
                "coordinates": {
                    "type": "object",
                    "required": False,
                    "properties": {
                        # * * **latitude** - latitude of the location, if any
                        "latitude": {"type": ["string", "null"]},

                        # * * **longitude** - longitude of the location, if any
                        "longitude": {"type": ["string", "null"]}
                    }
                },
            },
        },

        # == Linked Entities ==

        # **documents** - Links to related documents for the event. Usually,
        # this includes things like pre-written testimony, spreadsheets or
        # a slide deck that a presenter will use.
        "documents": {
            "items": {
                "properties": {
                    # * **note** - name of the document. Something like
                    # "Fiscal Report" or "John Smith's Slides".
                    "name": { "type": "string" },
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
        #        "participant_type": "person", "type": "chair" }
        #
        # Which expresses the chair of the event will be John Q. Smith.
        #
        #     { "participant": "Ways and Means",
        #       "participant_type": "organization", "type": "host" }
        #
        # Which expresses the host of the event is the Ways and Means
        # committee.
        "participants": {
            "items": {
                "properties": {
                    # * **chamber** - Optional field storing the chamber
                    # of the related participant.
                    "chamber": {"type": ["string", "null"]},

                    # * **participant** - Human readable name of the entitity.
                    "participant": { "type": "string" },

                    # * **participant_id** - ID of the participant
                    "participant_id": { "type": "string",
                                        "required": False },

                    # * **participant_type** - What type of entity is this?
                    # `person` may be used if the person is not a Legislator,
                    # butattending the event, such as an invited speaker or one
                    # who is offering testimony.
                    "participant_type": {
                        "enum": [ "organization", "person", ],
                        "type": "string"
                    },

                    # * **votes** - This field may be used if the person is
                    # eligible to vote, and may contain a numerical value
                    # (including decimal points, in some locales) denoting how
                    # many votes they have. This may be ommited.
                    "votes": {
                        "type": "number",
                        "required": False
                    },

                    # * **type** - Role of the entity we're relating to, such
                    # as `chair` for the chair of a meeting.
                    "type": {
                        "enum": [ "host", "chair", "participant" ],
                        "type": "string"
                    },

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
                    # * **description** - Human-readable string that represents
                    # this agenda item. A good example would be something like
                    #
                    # > The Committee will consider SB 2339, HB 100
                    "description": { "type": "string" },
                    "order": {"type": "integer", "required": False },

                    # **subjects** - List of related topics of this agenda
                    # item relates to.
                    "subjects": {
                        "items": { "type": "string" },
                        "type": "array"
                    },

                    # **media** - List of media links this item relates to
                    "media": {
                        "items": {
                            "properties": {
                                "name": { "type": "string" },
                                "type": { "type": "string" },
                                "date": {
                                    "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
                                    "type": ["string", "null"]
                                },
                                "links": {
                                    "items": {
                                        "properties": {
                                            "mimetype": {
                                                "type": ["string", "null"]
                                            },
                                            "url": { "type": "string" },
                                            "offset": {
                                                "type": "integer",
                                                "required": False,
                                            }
                                        },
                                        "type": "object"
                                    },
                                    "type": "array"
                                },
                            },
                            "type": "object"
                        },
                        "type": "array"
                    },

                    # * **notes** - List of notes taken during this agenda item,
                    # may be used to construct meeting minutes.
                    "notes": {
                        "required": False,
                        "items": {
                            "properties": {
                                "description": { "type": "string" },
                            },
                            "type": "object"
                        },
                        "type": "array"
                    },

                    # * **related_entities** - Entities that relate to this
                    # agenda item, such as presenters, legislative instruments,
                    # or committees.
                    "related_entities": {
                        "properties": {

                            # * * **type** - type of relation, such as
                            # `consideration` or `presenter`.
                            "type": { "type": "string" },

                            # * * **id** - ID of the related entity
                            "id": { "type": "string" },

                            # * * **name** - human readable string
                            # representing the entity, such as `John Q. Smith`.
                            "name": { "type": "string" },

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

   },
    "type": "object"
}
