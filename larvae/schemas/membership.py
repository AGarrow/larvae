schema = {
    "$schema": "http://json-schema.org/draft-03/schema#",
    "description": "A relationship between a person and an organization",
    "id": "http://popoloproject.com/schemas/membership.json#",
    "properties": {
        "end_date": {
            "description": "The date on which the relationship ended",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "type": ["string", "null"],
        },
        # **updated_at** - the time that this object was last updated.
        "updated_at": { "type": "string", "required": False },
        # **created_at** - the time that this object was first created.
        "created_at": { "type": "string", "required": False },
        "organization_id": {
            "description": "The ID of the organization that is a party to the relationship",
            "type": "string"
        },
        "person_id": {
            "description": "The ID of the person who is a party to the relationship",
            "type": "string"
        },
        "post_id": {
            "description": "Post ID key.",
            "type": ["string", "null"],
        },
        "role": {
            "description": "The role that the holder of the post fulfills",
            "type": ["string", "null"],
        },
        "start_date": {
            "description": "The date on which the relationship began",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "type": ["string", "null"],
        },
        "contact_details": {
            "description": "Details regarding how to contact the holder of this membership.",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string"
                    },
                    "value": {
                        "type": "string"
                    },
                    "note": {
                        "type": "string"
                    },
                }
            }
        },
    },
    "title": "Membership",
    "type": "object"
}
