#!/usr/bin/python3
import json
import requests
import agent.api.openapi as openapi
from agent.log.myLog import MyLog
LOGGING = MyLog()


def func_cnvr11_****(uri, access_token, mydlink_id, sub_id, start_ts, end_ts):
    api = 'REMOVE FOR CREDENTIAL'
    my_params = {
        'REMOVE FOR CREDENTIAL': 'REMOVE FOR CREDENTIAL'
    }

    data = {
        'REMOVE FOR CREDENTIAL': 'REMOVE FOR CREDENTIAL'
    }

    r = requests.post(
        'https://{}{}'.format(uri, api),
        params=my_params,
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    openapi.print_api_res(r)
    return r


def func_cnvr12_****(uri, session_id):
    api = 'REMOVE FOR CREDENTIAL'
    my_params = {
        'REMOVE FOR CREDENTIAL': 'REMOVE FOR CREDENTIAL'
    }

    r = requests.get('https://{}{}'.format(uri, api), params=my_params)
    openapi.print_api_res(r)
    return r

