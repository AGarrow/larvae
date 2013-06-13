schema = {
    "$schema": "http://json-schema.org/draft-03/schema#",
    "description": "A real person, alive or dead",
    "id": "http://popoloproject.com/schemas/person.json#",
    "properties": {
        # **updated_at** - the time that this object was last updated.
        "updated_at": { "type": "string", "required": False },

        # **created_at** - the time that this object was first created.
        "created_at": { "type": "string", "required": False },

        "contact_details": {
            "description": "Details regarding how to contact this person.",
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
        "biography": {
            "description": "An extended account of a person's life",
            "type": ["string", "null"],
        },
        "birth_date": {
            "description": "A date of birth",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "type": ["string", "null"],
        },
        "death_date": {
            "description": "A date of death",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "type": ["string", "null"],
        },
        "gender": {
            "description": "A gender",
            "type": ["string", "null"],
        },
        # reinstate these?
        #"honorific_prefix": {
        #    "description": "One or more honorifics preceding a person's name",
        #    "type": ["string", "null"],
        #},
        #"honorific_suffix": {
        #    "description": "One or more honorifics following a person's name",
        #    "type": ["string", "null"],
        #},
        "id": {
            "description": "The person's unique identifier",
            "required": False,
            "type": "string"
        },
        "image": {
            "description": "A URL of a head shot",
            "format": "uri",
            "type": ["string", "null"],
        },
        "links": {
            "description": "URLs for documents about the person",
            "items": {
                "properties": {
                    "note": {
                        "description": "A note, e.g. 'Wikipedia page'",
                        "type": ["string", "null"],
                    },
                    "url": {
                        "description": "A URL for a document about the person",
                        "format": "uri",
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "name": {
            "description": "A person's preferred full name",
            "type": "string"
        },
        "other_names": {
            "description": "Alternate or former names",
            "items": {
                "$ref": "http://popoloproject.com/schemas/other_name.json#"
            },
            "type": "array"
        },
        "summary": {
            "description": "A one-line account of a person's life",
            "type": ["string", "null"],
        }
    },
    "title": "Person",
    "type": "object"
}
