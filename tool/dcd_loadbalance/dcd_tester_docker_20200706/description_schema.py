""" The json schema of the description file
"""

SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",

    "definitions":{
        #==
        "request_parameter":{
            "type":"object",
            "properties":{
                "command":{
                    "type":"string"
                }
            },
            "required":["command"]
        },

        #==
        "response_validator":{
            "type":"object"
        },

        #==
        "step_content":{
            "type":"object",
            "properties":{
                "round":{
                    "type":"integer",
                    "minimum":1
                },
                "pre_pause":{
                    "type":"array",
                    "minItems":1,
                    "maxItems":2,
                    "items":{
                        "type":"number"
                    }
                },
                "post_pause":{
                    "type":"array",
                    "minItems":1,
                    "maxItems":2,
                    "items":{
                        "type":"number"
                    }
                },
                "request_parameter":{
                    "$ref":"#/definitions/request_parameter"
                },
                "response_validator":{
                    "$ref":"#/definitions/response_validator"
                }
            },
            "required": ["request_parameter"],
            "additionalProperties":False
        },

        #==
        "step":{
            "type":"object",
            "patternProperties":{
                ".*\\S.*":{
                    "anyOf":[
                        {
                            "$ref":"#/definitions/step_content"
                        },
                        {
                            "type":"array",
                            "items":{
                                "$ref":"#/definitions/step_content"
                            }
                        }
                    ]
                }
            }
        },

        #==
        "predefined_response":{
            "type":"object",
            "patternProperties":{
                ".*\\S.*":{
                    "type":"object",
                    "properties":{
                        "request":{
                            "type":"object",
                            "properties":{
                                "command":{
                                    "type":"string",
                                    "pattern":".*\\S.*"
                                }
                            },
                            "required":["command"]
                        },
                        "response":{"type":"object"}
                    },
                    "required":["request", "response"]
                }
            }
        },

        #running_da or default _da
        "da_inst":{
            "type":"object",
            "properties":{
                "mac_prefix":{
                    "type":"string",
                },
                "key_path":{
                    "type":"string",
                },
                "cert_path":{
                    "type":"string",
                },
                "device_id":{
                    "type":"string",
                },
                "step":{
                    "$ref":"#/definitions/step"
                },
                "predefined_response":{
                    "$ref":"#/definitions/predefined_response"
                },
                "cipher_list":{
                    "type":"string"
                },
                "delay_connect":{
                    "type":"array",
                    "minItems":1,
                    "maxItems":2,
                    "items":{
                        "type":"number"
                    }
                }
            },
            "additionalProperties":False
        },

        # da object
        "da":{
            "type":"object",
            "properties":{
                "default":{
                    "$ref":"#/definitions/da_inst"
                }
            },
            "additionalProperties":{
                "$ref":"#/definitions/da_inst"
            }
        },

        #==
        "ca":{
            "type":"object"
        },

        # a test case
        "case_description":{
            "type":"object",

            # only three properties are leagel.
            "properties":{
                "site_prefix":{"type":"string"},
                "da":{
                    "$ref":"#/definitions/da"
                },
                "ca":{
                    "$ref":"#/definitions/ca"
                }
            },
            "additionalProperties":False
        }
    },

    # the root is an object.
    "type": "object",
    #contains a "selected" properties.
    "properties": {
        "selected": {
            "type": "string",
        }
    },

    #others should be be a test_case object.
    "additionalProperties":{
        "$ref":"#/definitions/case_description"
    }
}
