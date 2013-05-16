schema = {
    "description": "bill data",
    "properties": {
        "_type": {
            "enum": [
                "bill"
            ],
            "type": "string"
        },
        "actions": {
            "items": {
                "properties": {
                    "action": {
                        "type": "string"
                    },
                    "actor": {
                        "required": False,
                        "type": "string"
                    },
                    "date": {
                        "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
                        "type": "string"
                    },
                    "related_entities": {
                        "items": {
                            "properties": {
                                "id": {
                                    "required": False,
                                    "type": "string"
                                },
                                "name": {
                                    "type": "string"
                                },
                                "type": {
                                    "enum": [
                                        "committee",
                                        "legislator"
                                    ],
                                    "type": "string"
                                }
                            },
                            "type": "object"
                        },
                        "required": True,
                        "type": "array"
                    },
                    "type": {
                        "items": {
                            "enum": [
                                "introduced",
                                "reading:1",
                                "reading:2",
                                "reading:3"
                            ],
                            "type": "string"
                        },
                        "type": "array"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "alternate_bill_ids": {
            "items": {
                "properties": {
                    "bill_id": {
                        "type": "string"
                    },
                    "note": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "alternate_titles": {
            "items": {
                "properties": {
                    "note": {
                        "type": "string"
                    },
                    "title": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "bill_id": {
            "type": "string"
        },
        "chamber": {
            "enum": [
                "upper",
                "lower"
            ],
            "required": False,
            "type": "string"
        },
        "documents": {
            "items": {
                "properties": {
                    "date": {
                        "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
                        "required": False,
                        "type": "string"
                    },
                    "links": {
                        "items": {
                            "properties": {
                                "mimetype": {
                                    "required": False,
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
                    "name": {
                        "type": "string"
                    },
                    "type": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "related_bills": {
            "items": {
                "properties": {
                    "bill_id": {
                        "type": "string"
                    },
                    "chamber": {
                        "enum": [
                            "upper",
                            "lower"
                        ],
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "relation_type": {
                        "enum": [
                            "companion"
                        ],
                        "type": "string"
                    },
                    "session": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "session": {
            "type": "string"
        },
        "sources": {
            "items": {
                "properties": {
                    "note": {
                        "type": "string"
                    },
                    "url": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "minItems": 1,
            "type": "array"
        },
        "sponsors": {
            "items": {
                "properties": {
                    "chamber": {
                        "enum": [
                            "upper",
                            "lower"
                        ],
                        "required": False,
                        "type": "string"
                    },
                    "entity_id": {
                        "required": False,
                        "type": "string"
                    },
                    "entity_type": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    },
                    "primary": {
                        "type": "boolean"
                    },
                    "sponsorship_type": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "subjects": {
            "items": {
                "type": "string"
            },
            "required": False,
            "type": "array"
        },
        "summaries": {
            "items": {
                "properties": {
                    "note": {
                        "type": "string"
                    },
                    "text": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },
        "title": {
            "type": "string"
        },
        "type": {
            "items": {
                "type": "string"
            },
            "type": "array"
        },
        "versions": {
            "items": {
                "properties": {
                    "date": {
                        "pattern": "^[0-9]{4}(-[0-9]{2}){0,2}$",
                        "required": False,
                        "type": "string"
                    },
                    "links": {
                        "items": {
                            "properties": {
                                "mimetype": {
                                    "required": False,
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
                    "name": {
                        "type": "string"
                    },
                    "type": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        }
    },
    "type": "object"
}
