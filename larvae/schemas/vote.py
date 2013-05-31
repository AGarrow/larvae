"""
    Schema for vote objects.
"""

schema = {
    "description": "vote data",
    "type": "object",
    "properties": {

        # == Basics ==

        # **_type** - All vote objects must have a _type field set to vote.
        "_type": { "enum": [ "vote" ], "type": "string" },

        # **session** - Associated with one of jurisdiction's sessions
        "session": { "type": "string" },

        # **chamber** - chamber vote took place in (if legislature is
        # bicameral, otherwise null)
        "chamber": {
            "enum": [ "upper", "lower", "joint" ], "type": ["string", "null"],
        },

        # **date** - date of the action
        "date": { "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$", "type": "string" },

        # **motion** - description of motion (from upstream source)
        "motion": { "type": "string" },

        # **type** - array of types (e.g. passage, veto_override, etc.)
        # [TODO: enum?]
        "type": { "items": { "type": "string" }, "type": "array" },

        # **passed** - boolean indicating passage
        "passed": { "type": "boolean" },

        # == Relationship to Bill ==

        # **bill** - Related bill, votes will have a non-null bill object if
        # they are related to a bill. Bills will have the following fields:
        #

        "bill": {
            "type": "object",
            "required": False,
            "properties": {
                # * **id** - bill's internal id if bill was matched with
                # an object in the database
                "id": { "type": ["string", "null"] },
                # * **name** - bill name (e.g. HB 21)
                "name": { "type": "string" },
                # * **chamber** - bill's chamber if vote was on a bill (and
                # legislature is bicameral, otherwise null)
                "chamber": {
                    "enum": [ "upper", "lower" ], "type": ["string", "null"],
                },
            }
        },



        # == Vote Counts ==

        # **vote_counts** is a list of objects with vote_type and count
        # properties.  vote_type is something like 'yes', 'no', 'not-voting',
        # etc.  TODO: enum?
        "vote_counts": {
            "items": {
                "properties": {
                    "vote_type": { "type": "string" },
                    "count": { "type": "integer", "minimum": 0 }
                },
                "type": "object"
            },
        },

        # **roll_call** is a list of objects with the following fields:
        #
        "roll_call": {
            "items": {
                "type": "object",
                "properties": {
                    # * **vote_type** - type of vote (e.g. yes, no, abstain)
                    "vote_type": { "type": "string" },

                    # * **person** - person object representing the voter,
                    # has the following fields:
                    #     * **name** - person's name as provided by source
                    #     * **id** - person's internal id if they've been
                    #       matched to an entity in the database
                    "person": {
                        "type": "object",
                        "properties": {
                            "name": { "type": "string" },
                            "id": { "type": ["string", "null"] },
                        }
                    }
                }
            }
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
                    "url": { "type": "string" },
                    "note": { "type": "string" },
                },
                "type": "object"
            },
            "minItems": 1,
            "type": "array"
        },
    }
}
