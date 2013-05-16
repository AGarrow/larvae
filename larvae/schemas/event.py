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
                "datetime",
                "null"
            ]
        },
        "link": {
            "required": False,
            "type": [
                "string",
                "null"
            ]
        },
        "location": {
            "type": "string"
        },
        "notes": {
            "required": False,
            "type": [
                "string",
                "null"
            ]
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
        "session": {
            "type": "string"
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
        "status": {
            "required": False,
            "type": "string"
        },
        "type": {
            "type": "string"
        },
        "when": {
            "type": "datetime"
        }
    },
    "type": "object"
}
