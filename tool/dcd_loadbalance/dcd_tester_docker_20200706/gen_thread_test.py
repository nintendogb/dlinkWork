import json
import os
import shutil
BIN_DIR = 'dcd_tester_docker_20200706'
TEST_CONFIG = [
    {
        'keep_alive-1': {
            'dev_patt': 10000
        },
        'keep_alive-2': {
            'dev_patt': 10000
        },
        'event': {
            'dev_patt': 4500,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'sign_in': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'get_policy': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
        'get_schedule': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
    },
    {
        'keep_alive-1': {
            'dev_patt': 10000
        },
        'keep_alive-2': {
            'dev_patt': 10000
        },
        'event': {
            'dev_patt': 4500,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'sign_in': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'get_policy': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
        'get_schedule': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
    },
    {
        'keep_alive-1': {
            'dev_patt': 10000
        },
        'keep_alive-2': {
            'dev_patt': 10000
        },
        'event': {
            'dev_patt': 4500,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'sign_in': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'get_policy': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
        'get_schedule': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
    },
    {
        'keep_alive-1': {
            'dev_patt': 10000
        },
        'keep_alive-2': {
            'dev_patt': 10000
        },
        'event': {
            'dev_patt': 4500,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'sign_in': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'get_policy': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
        'get_schedule': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
    },
    {
        'keep_alive-1': {
            'dev_patt': 10000
        },
        'keep_alive-2': {
            'dev_patt': 10000
        },
        'event': {
            'dev_patt': 4500,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'sign_in': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
        },
        'get_policy': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
        'get_schedule': {
            'dev_patt': 50,
            'pre_pause': [0, 60],
            'round': 10000,
            'firmware_ver': '1.01.03',
        },
    },
]

ws_url = {
    0: 'qa-us-dcdda-1.auto.mydlink.com:443/SwitchCamera',
    1: 'qa-us-dcdda-1.auto.mydlink.com:443/SwitchCamera',
}

START_DEV = 88000000
def gen_dev_patt():
    global START_DEV
    for cfg in TEST_CONFIG:
        for _, case_cfg in cfg.items():
            count = case_cfg['dev_patt']
            case_cfg['dev_patt'] = f'{START_DEV}_{count}'
            START_DEV += count

gen_dev_patt()
'''
import json
print(json.dumps(TEST_CONFIG, indent=4))
'''        



def test_base():
    return {
        "base_case":{
            "site_prefix": "qa-us",
                "da":{
                    "default": {
                        "delay_connect": [0, 50],
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

def signin_cmd_base():
    return {
        "command":"sign_in"
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
    'sign_in': signin_cmd_base,
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
    'sign_in': 'sign_in.json',
    'keep_alive': 'keep.json',
    'get_policy': 'get_policy.json',
    'get_regular': 'get_regular.json',
    'get_schedule': 'get_schedule.json',
    'get_server_info': 'get_server_info.json',
    'recycle_channel': 'recycle_channel.json',
    'event': 'event.json',
    'start_viewing': 'start_viewing.json',
    'sync_info': 'sync_info.json',
    'unit_change_event': 'unit_change.json',
}
count = 0
for test_cfg in TEST_CONFIG:
    count += 1
    shutil.rmtree(f'/home/dlink/tool/tool/dcd_loadbalance/{BIN_DIR}/dcd_thread_{count}', ignore_errors=True)
    os.makedirs(f'/home/dlink/tool/tool/dcd_loadbalance/{BIN_DIR}/dcd_thread_{count}', exist_ok=True)
    for case, case_cfg in test_cfg.items():
        json_cfg = test_base()
        json_cfg['base_case']['site_prefix'] = ws_url[count % 2]
        if 'firmware_ver' in case_cfg:
            json_cfg['base_case']['da']['default']['step']['0']['request_parameter']['firmware_ver'] = case_cfg['firmware_ver']
        if 'keep_alive' in case:
            json_cfg['base_case']['da'][case_cfg['dev_patt']] = {}
        else:
            tmp_step = step_base()
            if '-' in case:
                tmp_step['step']['1']['request_parameter'] = get_request_parameter[
                    case[0:case.index('-')]
                ]()
            else:
                tmp_step['step']['1']['request_parameter'] = get_request_parameter[case]()
            tmp_step['step']['1']['pre_pause'] = case_cfg['pre_pause']
            tmp_step['step']['1']['round'] = case_cfg['round']
            json_cfg['base_case']['da'][case_cfg['dev_patt']] = tmp_step

        print(f'{case}')
        print(json_cfg)
        with open(f'/home/dlink/tool/tool/dcd_loadbalance/{BIN_DIR}/dcd_thread_{count}/{case}.json', 'w') as outfile:
            #json.dump(json_cfg, outfile, sort_keys=True ,indent=4)
            json.dump(json_cfg, outfile, indent=4)
