#!/usr/bin/python3
import hashlib
import time
import urllib
import requests
import agent.api.openapi as openapi
import agent.api.uapCgi as uapCgi
import agent.api.cnvrApi as cnvrApi
import agent.config.parameter as parameter
from agent.log.myLog import MyLog
LOGGING = MyLog()


class Agent:
    def __init__(self, uri, cid, csc):
        self.uri = uri
        self.client_id = cid
        self.client_secret = csc
        self.md5_password = ''

    def get_md5_password(self, pw):
        self.md5_password = 'REMOVE FOR CREDENTIAL'


class Uap(Agent):
    def __init__(self, uri, cid, csc):
        super().__init__(uri, cid, csc)
        self.access_code = ''
        self.refresh_token = ''
        self.access_token = ''
        self.user_token = ''
        self.res = ''

    def uap_user_signin(self, account, password):
        self.get_md5_password(password)
        self.res = uapCgi.uap_sign_in(
            self.uri,
            self.client_id,
            self.client_secret,
            account,
            self.md5_password
        )
        try:
            res = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(
                self.res.headers['Location']).query))
            self.user_token = res['access_token']
        except KeyError:
            print('Get UAP user sign-in failed.')

    def get_user_token(self, account, password):
        self.get_md5_password(password)
        self.account = account
        api = 'REMOVE FOR CREDENTIAL'
        path = '{}?'.format(api)
        myParams = {
            'REMOVE FOR CREDENTIAL': 'REMOVE FOR CREDENTIAL'
        }
        sig = openapi.get_sig(path, myParams, self.client_secret)
        myParams['sig'] = sig
        self.res = requests.get(
            'https://{}{}'.format(self.uri, api),
            params=myParams,
            allow_redirects=False
        )
        openapi.print_api_res(self.res)
        try:
            res = dict(urllib.parse.parse_qsl(
                urllib.parse.urlsplit(self.res.headers['Location']).query
            ))
            self.user_token = res['access_token']
        except KeyError:
            print('Get UAP access token failed.')

    def ****(self, account):
        if self.access_token == '':
            print('Please execute get_access_token() first')
        else:
            self.res = openapi.func_2d1_****(
                self.uri, self.client_id, self.access_token, account)

    def ****(self, account, password):
        if self.access_token == '':
            print('Please execute get_access_token() first')
        else:
            self.res = openapi.func_3a1_****(
                self.uri, self.access_token, account, password)
            if 'data' in self.res:
                if 'access_token' in self.res['data']:
                    self.user_token = self.res['data']['access_token']

    def cnvr_****(self, mydlink_id, subs_id, start_ts, end_ts):
        if self.user_token == '':
            print('Please execute get_user_token() first')
        else:
            self.res = cnvrApi.func_cnvr11_****(
                self.uri,
                self.user_token,
                mydlink_id,
                subs_id,
                start_ts,
                end_ts
            )

    def cnvr_****(self, session_id):
        self.res = cnvrApi.func_cnvr12_****(
            self.uri, session_id)

