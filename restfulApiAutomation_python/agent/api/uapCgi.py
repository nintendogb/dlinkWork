#!/usr/bin/python3
import time
import requests
import agent.api.openapi as openapi
import agent.config.parameter as parameter
from agent.log.myLog import MyLog
LOGGING = MyLog()


def uap_sign_in(uri, cid, cs, user, pw):
    api = 'REMOVE FOR CREDENTIAL'
    path = '{}?'.format(api)
    myParams = {
        'REMOVE FOR CREDENTIAL': 'REMOVE FOR CREDENTIAL'
    }
    sig = openapi.get_sig(path, myParams, cs)
    myParams['sig'] = sig
    r = requests.get(
        'https://{}{}'.format(uri, api),
        params=myParams,
        allow_redirects=False
    )
    openapi.print_api_res(r)
    return r
