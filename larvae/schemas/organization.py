schema = {
    "description": "A group with a common purpose or reason for existence that goes beyond the set of people belonging to it",
    "properties": {
        "classification": {
            "description": "An organization category, e.g. committee",
            "type": ["string", "null"]
        },
        "dissolution_date": {
            "description": "A date of dissolution",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "type": ["string", "null"],
        },
        "founding_date": {
            "description": "A date of founding",
            "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
            "type": ["string", "null"],
        },

        # **updated_at** - the time that this object was last updated.
        "updated_at": { "type": "string", "required": False },

        # **created_at** - the time that this object was first created.
        "created_at": { "type": "string", "required": False },

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
                        "type": "string",
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "name": {
            "description": "A primary name, e.g. a legally recognized name",
            "type": "string"
        },
        "other_names": {
            "description": "Alternate or former names",
            "items": {
                "properties": {
                    "name": { "type": "string" },
                    "start_date": {
                        "type": ["string", "null"],
                        "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$"
                    },
                    "end_date": {
                        "type": ["string", "null"],
                        "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$"
                    },
                    "note": { "type": ["string", "null"] }
                },
                "type": "object",
            },
            "type": "array"
        },
        "parent_id": {
            "description": "An organization that contains this organization",
            "type": ["string", "null"],
        },
        "contact_details": {
            "description": "Details regarding how to contact the organization.",
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
                        "type": ["string", "null"],
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
                                    "type": ["string", "null"],
                                },
                            }
                        }
                    },
                    "end_date": {
                        "description": "Ending date of the post.",
                        "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
                        "type": ["string", "null"],
                    },
                    "id": {
                        "description": "The post's unique identifier",
                        "type": ["string", "null"],
                    },
                    "label": {
                        "description": "A label describing the post",
                        "type": "string"
                    },
                    "organization_id": {
                        "description": "The ID of the organization in which the post is held",
                        "type": ["string", "null"],
                    },
                    "role": {
                        "description": "The role that the holder of the post fulfills",
                        "type": "string"
                    },
                    "start_date": {
                        "description": "Startting date of the post.",
                        "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
                        "type": ["string", "null"],
                    }
                },
                "title": "Post",
                "type": "object"
            },
            "type": "array"
        }
    },
    "title": "Organization",
    "type": "object"
}
