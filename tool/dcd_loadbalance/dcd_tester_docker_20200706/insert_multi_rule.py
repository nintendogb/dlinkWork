import agent.agent as agent
import agent.config.parameter as parameter
CLIENT_ID = parameter.APP_ID()
CLIENT_SECRET = parameter.APP_SECRET()
URI = 'qa-us-openapi.auto.mydlink.com'

def default_policy(mydlink_id):
    return [
        {
            "active": 1,
            "conditions": [],
            "description": "",
            "icon": "",
            "name": "policy 1",
            "rules": [
               {
                  "act_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "actions": [
                     {
                        "Fx": {
                           "setting": {
                              "idx": 0,
                              "type": 768,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 1
                        }
                     }
                  ],
                  "cond_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "conditions": [
                     {
                        "X": {
                           "status": {
                              "idx": 0,
                              "type": 8,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 0
                        },
                        "op": "gt"
                     }
                  ],
                  "group_id": 0,
                  "type": 1
               }
            ],
            "scene_id": "1"
         },
         {
            "active": 1,
            "conditions": [],
            "description": "",
            "icon": "",
            "name": "policy 2",
            "rules": [
               {
                  "act_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "actions": [
                     {
                        "Fx": {
                           "setting": {
                              "idx": 0,
                              "type": 22,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 1
                        }
                     }
                  ],
                  "cond_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "conditions": [
                     {
                        "X": {
                           "status": {
                              "idx": 0,
                              "type": 8,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 0
                        },
                        "op": "gt"
                     }
                  ],
                  "group_id": 0,
                  "type": 1
               }
            ],
            "scene_id": "2"
         },
         {
            "active": 1,
            "conditions": [],
            "description": "",
            "icon": "",
            "name": "policy 3",
            "rules": [
               {
                  "act_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "actions": [
                     {
                        "Fx": {
                           "setting": {
                              "idx": 0,
                              "type": 768,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 1
                        }
                     }
                  ],
                  "cond_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "conditions": [
                     {
                        "X": {
                           "status": {
                              "idx": 0,
                              "type": 8,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 0
                        },
                        "op": "gt"
                     }
                  ],
                  "group_id": 0,
                  "type": 1
               },
               {
                  "act_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "actions": [
                     {
                        "Fx": {
                           "setting": {
                              "idx": 0,
                              "type": 22,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 1
                        }
                     }
                  ],
                  "cond_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "conditions": [
                     {
                        "X": {
                           "status": {
                              "idx": 0,
                              "type": 8,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 0
                        },
                        "op": "gt"
                     }
                  ],
                  "group_id": 0,
                  "type": 1
               }
            ],
            "scene_id": "3"
         },
         {
            "active": 1,
            "conditions": [],
            "description": "",
            "icon": "",
            "name": "policy 4",
            "rules": [
               {
                  "act_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "actions": [
                     {
                        "Fx": {
                           "setting": {
                              "idx": 0,
                              "type": 22,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 1
                        }
                     }
                  ],
                  "cond_scope": {
                     "devices": [
                        mydlink_id
                     ]
                  },
                  "conditions": [
                     {
                        "X": {
                           "status": {
                              "idx": 0,
                              "type": 8,
                              "uid": 0
                           }
                        },
                        "Y": {
                           "value": 0
                        },
                        "op": "gt"
                     }
                  ],
                  "group_id": 0,
                  "type": 1
               }
            ],
            "scene_id": "4"
         }
      ]


def default_schedule():
    return [
         {
            "active": 1,
            "conditions": [],
            "description": "",
            "icon": "",
            "name": "schedule 1",
            "rules": [
               {
                  "act_scope": {
                     "policies": [
                        "1"
                     ]
                  },
                  "actions": [
                     {
                        "Fx": {},
                        "Y": {
                           "value": 1
                        }
                     }
                  ],
                  "conditions": [
                     {
                        "X": "date",
                        "Y": [
                           "TUE"
                        ],
                        "op": "in"
                     },
                     {
                        "X": "time",
                        "Y": "09:00",
                        "op": "eq"
                     }
                  ],
                  "group_id": 0,
                  "type": 2
               },
               {
                  "act_scope": {
                     "policies": [
                        "1"
                     ]
                  },
                  "actions": [
                     {
                        "Fx": {},
                        "Y": {
                           "value": 0
                        }
                     }
                  ],
                  "conditions": [
                     {
                        "X": "date",
                        "Y": [
                           "TUE"
                        ],
                        "op": "in"
                     },
                     {
                        "X": "time",
                        "Y": "12:00",
                        "op": "eq"
                     }
                  ],
                  "group_id": 1,
                  "type": 3
               }
            ],
            "scene_id": "5"
         }
      ]


def insert_rule(mydlink_id):
    uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)
    uap.get_user_token(f'testqaid+{mydlink_id}@sqadt1.mydlink.com', 'mydlink')
    uap.set_policy('default', default_policy(mydlink_id))
    uap.set_schedule('default', default_schedule())


MYDLINK_ID_LIST = [str(88000000 + i) for i in range(150000)]
for mydlink_id in MYDLINK_ID_LIST:
    insert_rule(mydlink_id)
