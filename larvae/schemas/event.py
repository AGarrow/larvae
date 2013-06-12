"""
    Schema for event objects.
"""

# == Reused Schemas ==

# **media_schema** - This "special" schema is used in two places in the
# Event scema, on the top level and inside the agenda item. This is an
# optional component that may be omited entirely from a document.
media_schema = {
    "required": False,
    "items": {
        "properties": {
            # * **name** - name of the media link, such as "Recording of the
            # meeting" or "Discussion of construction near the watershed"
            "name": { "type": "string" },

            # * **type** - type of the set of recordings, such as "recording"
            # or "testimony".
            "type": { "type": "string" },

            # * **date** - date of the recording.
            "date": {
                "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
                "type": ["string", "null"]
            },

            # * **links** - List of links to the same media item, each with
            # a different MIME type.
            "links": {
                "items": {
                    "properties": {
                        # * * **mimetype** - Mimetype of the media, such as
                        # video/mp4 or audio/webm
                        "mimetype": {
                            "type": ["string", "null"]
                        },

                        # * * **url** - URL where this media may be accessed
                        "url": { "type": "string" },

                        # * * **offset** - Offset where the related
                        # part starts. This is optional and may be ommited
                        # entirely.
                        "offset": {
                            "type": "number",
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
}

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

        # **when** - Starting date / time of the event. This should be
        # fully timezone qualified.
        "when": { "type": ["datetime"] },

        # **end** - Ending date / time of the event. This should be fully
        # timezone qualified.
        "end": {
            "required": False,
            "type": ["datetime", "null"]
        },


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
                "note": {
                    "required": False,
                    "type": ["string", "null"],
                },

                # * **coordinates** - coordinates where this event will take
                # place. If the location hasn't (or isn't) geolocated or
                # geocodable, than this should be set to null.
                "coordinates": {
                    "type": ["object", "null"],
                    "properties": {
                        # * * **latitude** - latitude of the location, if any
                        "latitude": {"type": "string"},

                        # * * **longitude** - longitude of the location, if any
                        "longitude": {"type": "string"}
                    }
                },
            },
        },

        # == Linked Entities ==


        # **media** - See the description above for the Media schema.
        "media": media_schema,

        # **documents** - Links to related documents for the event. Usually,
        # this includes things like pre-written testimony, spreadsheets or
        # a slide deck that a presenter will use.
        "documents": {
            "required": False,
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
            "required": False,
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

                    # * **order** - order of this item, useful for re-creating
                    # meeting minutes. This may be ommited entirely.
                    "order": {"type": "integer", "required": False },

                    # **subjects** - List of related topics of this agenda
                    # item relates to.
                    "subjects": {
                        "required": False,
                        "items": { "type": "string" },
                        "type": "array"
                    },

                    # **media** - See the description above for the Media schema.
                    "media": media_schema,

                    # * **notes** - List of notes taken during this agenda item,
                    # may be used to construct meeting minutes.
                    "notes": {
                        "required": False,
                        "items": {
                            "properties": {
                                # * * **description** - simple string containing
                                # the content of the note.
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
                        "required": False,
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
