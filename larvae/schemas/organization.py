schema = {
    "$schema": "http://json-schema.org/draft-03/schema#",
    "description": "A group with a common purpose or reason for existence that goes beyond the set of people belonging to it",
    "id": "http://popoloproject.com/schemas/organization.json#",
    "properties": {
        "classification": {
            "description": "An organization category, e.g. committee",
            "required": False,
            "type": "string"
        },
        "dissolution_date": {
            "description": "A date of dissolution",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "required": False,
            "type": "string"
        },
        "founding_date": {
            "description": "A date of founding",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "required": False,
            "type": "string"
        },

        # **updated_at** - the time that this object was last updated.
        "updated_at": { "type": "string" },

        # **created_at** - the time that this object was first created.
        "created_at": { "type": "string" },

        "id": {
            "description": "The organization's unique identifier",
            "required": False,
            "type": "string"
        },
        "identifiers": {
            "description": "Issued identifiers",
            "items": {
                "properties": {
                    "identifier": {
                        "description": "An issued identifier, e.g. a DUNS number",
                        "type": "string"
                    },
                    "scheme": {
                        "description": "An identifier scheme, e.g. DUNS",
                        "required": False,
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "required": False,
            "type": "array"
        },
        "name": {
            "description": "A primary name, e.g. a legally recognized name",
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
        "parent_id": {
            "description": "An organization that contains this organization",
            "required": False,
            "type": "string"
        },
        "contact_details": {
            "description": "Details regarding how to contact the organization.",
            "required": False,
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
        "posts": {
            "description": "All posts.",
            "items": {
                "description": "A position that exists independent of the person holding it",
                "properties": {
                    "contact_details": {
                        "description": "Details regarding how to contact the holder of this post.",
                        "required": False,
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
                    "end_date": {
                        "description": "Ending date of the post.",
                        "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
                        "required": False,
                        "type": "string"
                    },
                    "id": {
                        "description": "The post's unique identifier",
                        "type": "string",
                        "required": False
                    },
                    "label": {
                        "description": "A label describing the post",
                        "type": "string"
                    },
                    "organization_id": {
                        "description": "The ID of the organization in which the post is held",
                        "required": False,
                        "type": "string"
                    },
                    "role": {
                        "description": "The role that the holder of the post fulfills",
                        "type": "string"
                    },
                    "start_date": {
                        "description": "Startting date of the post.",
                        "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
                        "required": False,
                        "type": "string"
                    }
                },
                "title": "Post",
                "type": "object"
            },
            "required": False,
            "type": "array"
        }
    },
    "title": "Organization",
    "type": "object"
}
