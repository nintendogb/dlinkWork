#!/usr/bin/python3
import hashlib
import time
import urllib
import json
import simplejson
import requests
from agent.log.myLog import MyLog
LOGGING = MyLog()
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
def get_sig(path, my_params, cs):
    cmd = urllib.parse.urlencode(my_params)
    payload = 'REMOVE FOR CREDENTIAL'
    sig = hashlib.md5(payload.encode()).hexdigest()
    LOGGING.debug('sig: {}'.format(sig))
    return sig


def print_api_res(res):
    LOGGING.info('<-------------------------------------------------------------------------')
    LOGGING.info('URL: {}'.format(res.url))
    if res.request.body is not None:
        try:
            LOGGING.info('Json request: \n{}'.format(
                json.dumps(
                    json.loads(res.request.body),
                    indent=3,
                    sort_keys=True
                )
            ))
        except (
            UnicodeDecodeError,
            simplejson.errors.JSONDecodeError,
            json.decoder.JSONDecodeError
        ):
            LOGGING.info('request body: \n{}'.format(res.request.body))
    LOGGING.info('status code: {}'.format(res.status_code))
    LOGGING.info('elapsed time: {}'.format(res.elapsed))
    LOGGING.info('header: {}'.format(res.headers))
    try:
        LOGGING.info('Json return: \n{}'.format(
            json.dumps(
                res.json(),
                indent=3,
                sort_keys=True
            )
        ))
    except simplejson.errors.JSONDecodeError:
        LOGGING.info(str('body: {}'.format(res.text)))
    LOGGING.info('------------------------------------------------------------------------->')


def func_2d1_****(uri, cid, at, account):
    api = 'REMOVE FOR CREDENTIAL'
    my_params = {
         'REMOVE FOR CREDENTIAL': 'REMOVE FOR CREDENTIAL'
    }
    r = requests.get(
        'https://{}{}'.format(uri, api),
        params=my_params,
        allow_redirects=False
    )
    print_api_res(r)
    return r


def func_3a1_****(uri, access_token, user_name, password):
    return_value = ''
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
    print_api_res(r)
    return_value = r.json()
    return return_value
