"""
    Schema for vote objects.
"""

schema = {
    "description": "vote data",
    "type": "object",
    "properties": {

        # == Basics ==

        # **_type** - All larvae objects must have a _type field set to bill.
        "_type": { "enum": [ "vote" ], "type": "string" },

        # **session** - Associated with one of jurisdiction's sessions
        "session": { "type": "string" },

        # **chamber** - chamber vote took place in (if legislature is
        # bicameral, otherwise null)
        "chamber": {
            "enum": [ "upper", "lower", "joint" ], "type": ["string", "null"],
        },

        # * **date** - date of the action
        "date": { "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$", "type": "string" },

        # **motion** - description of motion (from upstream source)
        "motion": { "type": "string" },

        # **type** - array of types (e.g. passage, veto_override, etc.)
        # [TODO: enum?]
        "type": { "items": { "type": "string" }, "type": "array" },

        # **passed** - boolean indicating passage
        "passed": { "type": "boolean" },

        # == Relationship to Bill ==

        # Votes will have these fields if they are votes on specific pieces
        # of legislation.

        # **bill_id** - bill's bill_id if vote was on a bill
        "bill_id": { "type": ["string", "null"] },

        # **bill_chamber** - bill's chamber if vote was on a bill (and
        # legislature is bicameral, otherwise null)
        "bill_chamber": {
            "enum": [ "upper", "lower" ], "type": ["string", "null"],
        },

        # == Vote Counts ==

        # **vote_count** is a list of objects with vote_type and count
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

        # **rollcall** is a list of objects with the following fields:
        #
        "rollcall": {
            "items": {
                "properties": {
                    # * **vote_type** - type of vote (e.g. yes, no, abstain)
                    "vote_type": { "type": "string" },
                    # * **person** - name of person, as provided by source
                    "person": { "type": "string" },
                    # * **person_id** - person's internal id if they've been
                    # matched to an entity in the database
                    "person_id": { "type": ["string", "null"] },
                },
                "type": "object"
            },
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
