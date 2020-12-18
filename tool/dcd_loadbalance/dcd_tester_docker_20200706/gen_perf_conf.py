import json
import os
TEST_CONFIG = [
    {
        'keep_alive': {
            'dev_patt': '8800[0-9][0-9][0-9][0-9]'
        },
        'get_policy': {
            'dev_patt': '880100[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'get_regular': {
            'dev_patt': '880101[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'get_schedule': {
            'dev_patt': '880102[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'get_server_info': {
            'dev_patt': '880103[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'recycle_channel': {
            'dev_patt': '880104[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'event': {
            'dev_patt': '880105[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'start_viewing': {
            'dev_patt': '880106[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'sync_info': {
            'dev_patt': '880107[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'unit_change_event': {
            'dev_patt': '880108[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
    },
    {
        'keep_alive': {
            'dev_patt': '8802[0-9][0-9][0-9][0-9]'
        },
        'get_policy': {
            'dev_patt': '880300[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'get_regular': {
            'dev_patt': '880301[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'get_schedule': {
            'dev_patt': '880302[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'get_server_info': {
            'dev_patt': '880303[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'recycle_channel': {
            'dev_patt': '880304[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'event': {
            'dev_patt': '880305[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'start_viewing': {
            'dev_patt': '880306[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'sync_info': {
            'dev_patt': '880307[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
        'unit_change_event': {
            'dev_patt': '880308[0-9][0-9]',
            'pre_pause': [180],
            'round': 200,
        },
    }
]

ws_url = {
    0: 'qa-us-dcdda-1.auto.mydlink.com:443/SwitchCamera',
    1: 'qa-us-dcdda-2.auto.mydlink.com:443/SwitchCamera',
}

def test_base():
    return {
        "base_case":{
            "site_prefix": "qa-us",
                "da":{
                    "default": {
                        "cipher_list":"ECDHE-RSA-AES128-SHA256",
                        "step":{
                            "0":{
                                "request_parameter":{
                                    "command":"sign_in"
                                }
                            }          
                        }
                    },
                }
        } 
    }

def step_base():
    return {
        "step":{
            "1":{}
            }
    }


def event_cmd_base():
    return {
        "command":"event",
        "event":{
            "type":56,
            "name":"Policy Condition Hit",
            "metadata":{
                "conditions":[
                    {
                        "X":{
                            "status":{"uid":15766853,"type":8,"idx":0}
                        },
                        "op":"ge",
                        "Y":{"value":0},
                        "V":{"value":53}
                    }
                ],
                "actions":[]
            }
        }
    }

def policy_cmd_base():
    return {
        "command":"get_policy"
    }


def regular_cmd_base():
    return {
        "command":"get_regular"
    }


def schedule_cmd_base():
    return {
        "command":"get_schedule",
        "model":"DCS_8300LH"
    }


def server_info_cmd_base():
    return {
        "command":"get_server_info"
    }


def recycle_channel_cmd_base():
    return {
        "command":"recycle_channel",
        "channel_url":"https://rd"
    }


def start_view_cmd_base():
    return {
        "command":"start_viewing",
        "code":0,
        "message":"no error",
        "uid":0,
        "idx":0,
        "client_id":"ddd",
        "channel_url":"https:\/\/rd-rdsg-rcdca",
        "viewing":{"type":1},
        "capability":1
    }


def sync_info_cmd_base():
    return {
        "command":"sync_info",
        "metadata":{
            "type":1,
            "name":"oob change"
        }
    }


def unit_change_event_cmd_base():
    return {
        "command":"event",
            "event":{
                "type":60,
                "name":"Unit Data Change",
                "metadata":[
                    {"uid":0,"model":"DCS-H100","sub_id":"58D56EEE453D","setting":[19,32,33,34,45,256],"status":[7,17,19,23]},
                    {"uid":15615429,"model":"DCS-2800LH","sub_id":"58D56EEE45C5","setting":[21,27,29,30,31,40,41,42,43,44,48,22,513,"39"],"status":[8,16,18,22],"version":"1.05.00B0"},
                    {"uid":15615446,"model":"DCS-2800LH","sub_id":"58D56EEE45D6","setting":[21,27,29,30,31,40,41,42,43,44,48,22,513,39],"status":[8,16,18,22],"version":"1.05.00B0"}
                ]                 
            }
    }


get_request_parameter = {
    'get_policy': policy_cmd_base,
    'get_regular': regular_cmd_base,
    'get_schedule': schedule_cmd_base,
    'get_server_info': server_info_cmd_base,
    'recycle_channel': recycle_channel_cmd_base,
    'event': event_cmd_base,
    'start_viewing': start_view_cmd_base,
    'sync_info': sync_info_cmd_base,
    'unit_change_event': unit_change_event_cmd_base,
}
cfg_name = {
    'keep_alive': 'perf_keep.json',
    'get_policy': 'perf_get_policy.json',
    'get_regular': 'perf_get_regular.json',
    'get_schedule': 'perf_get_schedule.json',
    'get_server_info': 'perf_get_server_info.json',
    'recycle_channel': 'perf_recycle_channel.json',
    'event': 'perf_event.json',
    'start_viewing': 'perf_start_viewing.json',
    'sync_info': 'perf_sync_info.json',
    'unit_change_event': 'perf_unit_change.json',
}
count = 0
for test_cfg in TEST_CONFIG:
    count += 1
    os.makedirs(f'./perf_conf_{count}', exist_ok=True)
    for case, case_cfg in test_cfg.items():
        json_cfg = test_base()
        json_cfg['base_case']['site_prefix'] = ws_url[count % 2]
        if case == 'keep_alive':
            json_cfg['base_case']['da'][case_cfg['dev_patt']] = {}
        else:
            tmp_step = step_base()
            tmp_step['step']['1']['request_parameter'] = get_request_parameter[case]()
            tmp_step['step']['1']['pre_pause'] = case_cfg['pre_pause']
            tmp_step['step']['1']['round'] = case_cfg['round']
            json_cfg['base_case']['da'][case_cfg['dev_patt']] = tmp_step

        print(f'{cfg_name[case]}')
        print(json_cfg)
        with open(f'./perf_conf_{count}/{cfg_name[case]}', 'w') as outfile:
            json.dump(json_cfg, outfile, sort_keys=True ,indent=4)
