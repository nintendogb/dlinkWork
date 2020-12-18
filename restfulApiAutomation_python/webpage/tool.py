#!/usr/bin/python3
import glob
import json
import math
import re
from datetime import datetime
from datetime import timedelta
from collections import Counter
from flask import jsonify
from flask import render_template
from flask import request
from flask import Blueprint
from flask_login import login_required
import redis
import pytz
from urllib.parse import unquote
from authlib.jose import JsonWebKey

import agent.config.parameter as parameter
import agent.agent as agent


tool_bp = Blueprint(
    'tool',
    __name__,
    template_folder='./templates',
    static_folder='./static'
)

CLIENT_ID = parameter.APP_ID()
CLIENT_SECRET = parameter.APP_SECRET()
URI = 'api.auto.mydlink.com'


@tool_bp.route('/dev-info', methods=['GET'])
@login_required
def dev_info():
    test_account = request.args.get('account', default='no_input', type=str)
    test_password = request.args.get('password', type=str)
    if test_account == 'no_input':
        return render_template(
                               'getDevInfo.html',
                               account=test_account,
                               password=test_password
                              )

    uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)
    uap.get_user_token(test_account, test_password)

    try:
        uap.list_device()
        data = uap.res.json()['data']
        dev_id_list = []
        for dev in data:
            dev_id_list.append(dev["mydlink_id"])



        dev_num = len(dev_id_list)
        start_idx = 0
        dev_data = {}
        while start_idx < dev_num:
            uap.get_device_info(dev_id_list[start_idx:start_idx+3])
            res = uap.res.json()['data']
            for dev in res:
                tmp_list = []
                for key, val in dev.items():
                    tmp_list.append('{}: {}'.format(key, val))
                dev_data[dev['mydlink_id']] = tmp_list
            start_idx += 3

    except KeyError:
        dev_data='NoData'
    

    return render_template(
        'getDevInfo.html',
        account=test_account,
        password=test_password,
        devData=dev_data
    )


@tool_bp.route('/list-event', methods=['GET'])
@login_required
def list_event():
    test_account = request.args.get('account', default='no_input', type=str)
    test_password = request.args.get('password', type=str)
    sTs = request.args.get('start', type=int)
    eTs = request.args.get('end', type=int)
    if test_account == 'no_input':
        return render_template(
                               'listEvent.html',
                               account=test_account,
                              )

    uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)
    uap.get_user_token(test_account, test_password)
    event_data = []
    file_property = []
    event_property = {}
    try:
        uap.cnvr_list_event(sTs, eTs)
        data = uap.res.json()['data']
        for row in data:
            if row['type'] == 'file':
                file_property.append(row)
            else:
                event_property['date'] = row['date']
                event_property['first_event_ts'] = row['first_event_ts']
                event_property['last_event_ts'] = row['last_event_ts']
                event_property['has_more'] = row['has_more']
                event_property['num'] = row['num']
                raw_data = row['data']
                for event in raw_data:
                    tmp_dict = {}
                    for key in event:
                        tmp_dict[key] = json.dumps(event[key])
                    event_data.append(tmp_dict)
    except KeyError:
        event_data='NoData'
    print(file_property)
    

    return render_template(
        'listEvent.html',
        start=sTs,
        end=eTs,
        event=event_data,
        eventProverty=event_property,
        fileProverty=file_property,
        eventNum=len(event_data),
        fileNum=len(file_property),
        account=test_account,
    )


@tool_bp.route('/get-event-clip', methods=['GET'])
@login_required
def get_event_clip():
    test_account = request.args.get('account', default='no_input', type=str)
    test_password = request.args.get('password', type=str)
    mydlink_id = request.args.get('mydlink_id', type=str)
    timestamp = request.args.get('timestamp', type=int)
    if test_account == 'no_input':
        return render_template(
            'getEventClip.html',
            account=test_account,
            error_info='NO ERROR'
        )

    uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)
    uap.get_user_token(test_account, test_password)
    subs_uid = 'Not exist'
    uap.cnvr_query_subscription()
    try:
        subscription_list = uap.res.json()['data']
        for subscription in subscription_list:
            if mydlink_id in subscription['devices']:
                subs_uid = subscription['subs_uid']
    except KeyError:
        return render_template(
            'getEventClip.html',
            account='no_input',
            error_info='Need to subscribe test DEV first.'
        )
        

    uap.cnvr_init_playlist_session_from_timestamp(
        mydlink_id,
        subs_uid,
        timestamp
    )

    res = uap.res.json()
    sid = 'Not exist'
    try:
        res_json = res['data']
        sid = res_json['session_id']
        uap.cnvr_fetch_playlist(sid)
        url_pattern = re.compile(r'(https://\S*)')
        return_body = uap.res.text
        url_list = url_pattern.findall(return_body)
    except KeyError:
        if 'error' in res:
            return render_template(
                'getEventClip.html',
                error_info=res['error']['message']
            )
        else:
            return render_template(
                'getEventClip.html',
                error_info=f'Something wrong subid[{subs_uid}] sid[{sid}]'
            )
            

    return render_template(
        'getEventClip.html',
        url_list=url_list,
        account=test_account,
        mydlink_id=mydlink_id,
        timestamp=timestamp,
        error_info='NO ERROR'
    )


@tool_bp.route('/get-storyboard', methods=['GET'])
@login_required
def get_storyboard_info():
    test_account = request.args.get('account', default='no_input', type=str)
    test_password = request.args.get('password', type=str)
    mydlink_id = request.args.get('mydlink_id', type=str)
    start_ts = request.args.get('start', type=int)
    end_ts = request.args.get('end', type=int)
    if test_account == 'no_input':
        return render_template(
            'getStoryBoard.html',
            account=test_account,
            error_info='NO ERROR'
        )

    uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)
    uap.get_user_token(test_account, test_password)
    uap.cnvr_get_storyboard_info(mydlink_id, [start_ts, end_ts])        

    res = uap.res.json()
    try:
        res_json = res['data']
    except KeyError:
        if 'error' in res:
            return render_template(
                'getStoryBoard.html',
                error_info=res['error']['message']
            )
        else:
            return render_template(
                'getStoryBoard.html',
                error_info=f'Something wrong subid[{subs_uid}] sid[{sid}]'
            )
            

    return render_template(
        'getStoryBoard.html',
        storyboardProperty=res_json,
        account=test_account,
        mydlink_id=mydlink_id,
        start=start_ts,
        end=end_ts,
        error_info='NO ERROR'
    )


@tool_bp.route('/hook', methods=['GET', 'POST'])
def hook():
    all_args = request.args
    r = redis.Redis(
        host=parameter.REDIS_SERVER(),
        port=parameter.REDIS_PORT(),
        decode_responses=True
    )
    r.delete('hook')
    res_data = {}
    for key, val in request.args.items():
        r.hset('hook', key, unquote(val))
    res_data.update(request.args)
    if request.get_json():
        data = request.get_json()
        for key, val in data.items():
            r.hset('hook', key, json.dumps(val))
            res_data[key] = val
    else:
        data = request.get_data()
        if len(data) > 0:
            res_data['raw_res'] = str(data)

    return jsonify(res_data)


@tool_bp.route('/jwk', methods=['GET'])
def get_jwk():
    def get_timestamp_from_name(key_name):
        start = key_name.rfind('/')
        end = key_name.rfind('.key.pub')
        return key_name[start+1:end]


    jwt_key_res = {'keys': []}
    pub_key_list = glob.glob('/webpage/jwks/*.key.pub')
    for pub_key in pub_key_list:
        with open(pub_key, 'r') as f:
            key = JsonWebKey.import_key(f.read(), {'kty': 'RSA'})
            update_data = {
                'kid': get_timestamp_from_name(pub_key),
                'alg': 'RS256',
                'kty': 'RSA',
                'use': 'sig,'
            }
            key.update(update_data)
            jwt_key_res['keys'].append(key)
        
    return jsonify(jwt_key_res)


@tool_bp.route('/event_token', methods=['GET', 'POST'])
def get_event_token():
    res_data = {
        'access_token': 'tedtest',
        'expires_in': 18300,
    }
    return jsonify(res_data)
