schema = {
    "$schema": "http://json-schema.org/draft-03/schema#",
    "description": "A real person, alive or dead",
    "id": "http://popoloproject.com/schemas/person.json#",
    "properties": {
        "additional_name": {
            "description": "One or more secondary given names",
            "required": False,
            "type": "string"
        },
        "biography": {
            "description": "An extended account of a person's life",
            "required": False,
            "type": "string"
        },
        "birth_date": {
            "description": "A date of birth",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "required": False,
            "type": "string"
        },
        "death_date": {
            "description": "A date of death",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "required": False,
            "type": "string"
        },
        "email": {
            "description": "An email address",
            "format": "email",
            "required": False,
            "type": "string"
        },
        "family_name": {
            "description": "One or more family names",
            "required": False,
            "type": "string"
        },
        "gender": {
            "description": "A gender",
            "required": False,
            "type": "string"
        },
        "given_name": {
            "description": "One or more primary given names",
            "required": False,
            "type": "string"
        },
        "honorific_prefix": {
            "description": "One or more honorifics preceding a person's name",
            "required": False,
            "type": "string"
        },
        "honorific_suffix": {
            "description": "One or more honorifics following a person's name",
            "required": False,
            "type": "string"
        },
        "id": {
            "description": "The person's unique identifier",
            "required": False,
            "type": "string"
        },
        "image": {
            "description": "A URL of a head shot",
            "format": "uri",
            "required": False,
            "type": "string"
        },
        "links": {
            "description": "URLs for documents about the person",
            "items": {
                "properties": {
                    "note": {
                        "description": "A note, e.g. 'Wikipedia page'",
                        "required": False,
                        "type": "string"
                    },
                    "url": {
                        "description": "A URL for a document about the person",
                        "format": "uri",
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "required": False,
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
            "required": False,
            "type": "array"
        },
        "summary": {
            "description": "A one-line account of a person's life",
            "required": False,
            "type": "string"
        }
    },
    "title": "Person",
    "type": "object"
}
