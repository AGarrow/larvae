schema = {
    "description": "event data",
    "properties": {
        "_type": {
            "enum": [
                "event"
            ],
            "type": "string"
        },
        "all_day": {
            "required": False,
            "type": "boolean"
        },
        "description": {
            "type": "string"
        },
        "documents": {
            "items": {
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "url": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "end": {
            "type": [
                "string",
                "null"
            ]
        },
        "links": {
            "description": "URLs for documents about the event",
            "items": {
                "properties": {
                    "note": {
                        "description": "A note, e.g. 'Wikipedia page'",
                        "required": False,
                        "type": "string"
                    },
                    "url": {
                        "description": "A URL for a document about the event",
                        "format": "uri",
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "required": False,
            "type": "array"
        },
        "location": {
            "type": "string"
        },
        "notes": {
            "required": False,
            "type": "array"
        },
        "participants": {
            "items": {
                "properties": {
                    "chamber": {
                        "required": False,
                        "type": "string"
                    },
                    "participant": {
                        "type": "string"
                    },
                    "participant_type": {
                        "enum": [
                            "committee",
                            "legislator",
                            "person",
                        ],
                        "type": "string"
                    },
                    "type": {
                        "enum": [
                            "host",
                            "chair",
                            "participant"
                        ],
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "record_id": {
            "required": False,
            "type": "string"
        },
        "agenda": {
            "items": {
                "properties": {
                    "note": {
                        "type": "string"
                    },
                    "related_entities": {
                        "properties": {
                            "type": {
                                "type": "string"
                            },
                            "entity_id": {
                                "type": "string"
                            },
                            "name": {
                                "type": "string"
                            },
                            "note": {
                                "type": "string"
                            },
                        },
                        "type": "object"
                    },
                    "minItems": 0,
                    "type": "array",
                },
                "type": "object"
            },
            "minItems": 0,
            "type": "array"
        },
        "sources": {
            "items": {
                "properties": {
                    "url": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "minItems": 1,
            "type": "array"
        },
        "canceled": {
            "required": False,
            "type": "boolean"
        },
        "type": {
            "type": "string"
        },
        "start": {
            "type": "string"
        }
    },
    "type": "object"
}
