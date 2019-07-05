#!/usr/bin/python3
import glob
import json
import math
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
import agent.config.parameter as parameter


log_bp = Blueprint(
    'log',
    __name__,
    template_folder='./templates',
    static_folder='./static'
)

PAGE_SIZE = 10
LOCAL_TZ = pytz.timezone(parameter.LOCAL_TIMEZONE())
TIME_FORMAT = "%Y-%m-%d %H:%M {}".format(parameter.LOCAL_TIMEZONE())


@log_bp.route('/newest', methods=['GET'])
def newest():
    return render_template(
        'layout.html',
    )


@log_bp.route('/get-redis-log', methods=['GET'])
def log_list():
    site_list = [item['site'] for item in parameter.SITE_CFG()]
    page = request.args.get('page', default=1, type=int)
    r = redis.Redis(
        host=parameter.REDIS_SERVER(),
        port=parameter.REDIS_PORT(),
        decode_responses=True
    )
    log_period = parameter.LOGGING_PERIOD()
    redis_log_list = []
    index, redis_key = r.scan(
        cursor=0,
        match='LOG:*',
        count=parameter.REDIS_SCAN_AMOUNT()
    )
    redis_key.sort(reverse=True)
    log_num = len(redis_key)
    total_page = math.ceil(log_num/PAGE_SIZE)
    if page == 0:
        key_list = redis_key
    else:
        start = (page-1)*PAGE_SIZE
        if page > total_page:
            key_list = []
        elif page == total_page:
            key_list = redis_key[start:]
        else:
            key_list = redis_key[start:(start+PAGE_SIZE)]

    for key in key_list:
        res_data = {}
        for site in site_list:
            res_data[site] = ''
        hash_data = r.hgetall(key)
        timestamp = int(key[4:])
        redislog_time = datetime.fromtimestamp(
            timestamp,
            LOCAL_TZ
        ).strftime(TIME_FORMAT)
        res_data['logTime'] = redislog_time
        for site in hash_data:
            json_data = json.loads(hash_data[site])
            err_item_list = []
            for counter in json_data:
                err_item_list.append(
                    '{} fail {}次'.format(counter[5:], json_data[counter])
                )
            res_data[site] = err_item_list
        redis_log_list.append(res_data)

    return render_template(
        'logList.html',
        redisLogList=redis_log_list,
        totalPage=total_page,
        currentPage=page,
        pageAmount=PAGE_SIZE,
        siteList=site_list,
        logPeriod=log_period
    )


@log_bp.route('/fail-count', methods=['GET'])
def fail_count():
    time_range = request.args.get('range', default=0, type=int)
    time_period = request.args.get('periodUnit', default='days', type=str)
    if time_range == 0:
        return render_template('failCount.html',
                               time_range=time_range, time_period=time_period)

    if time_period == 'min':
        delta_time = timedelta(minutes=time_range)
    elif time_period == 'hr':
        delta_time = timedelta(hours=time_range)
    else:
        delta_time = timedelta(days=time_range)

    site_list = [item['site'] for item in parameter.SITE_CFG()]
    r = redis.Redis(
        host=parameter.REDIS_SERVER(),
        port=parameter.REDIS_PORT(),
        decode_responses=True
    )
    index, redis_key = r.scan(
        cursor=0,
        match='LOG:*',
        count=parameter.REDIS_SCAN_AMOUNT()
    )
    redis_key.sort(reverse=True)

    target_ts = int((datetime.now() - delta_time).timestamp())
    res_data = {}
    for key in redis_key:
        hash_data = r.hgetall(key)
        timestamp = int(key[4:])
        if timestamp < target_ts:
            break

        for site in hash_data:
            json_data = json.loads(hash_data[site])
            if site not in res_data:
                res_data[site] = json_data
            else:
                res_data[site] = dict(
                    Counter(res_data[site])+Counter(json_data)
                )

    for site in res_data:
        err_item_list = []
        for counter in res_data[site]:
            err_item_list.append(
                '{} fail {}次'.format(counter[5:], res_data[site][counter])
            )
        res_data[site] = err_item_list

    return render_template(
        'failCount.html',
        timeRange=time_range,
        timePeriod=time_period,
        redisLog=res_data,
        siteList=site_list
    )


@log_bp.route("/download/<logfile>", methods=['GET'])
@login_required
def download_file(logfile):
    return log_bp.send_static_file('testLog/' + logfile)


@log_bp.route("/download-list", methods=['GET'])
@login_required
def download_list():
    log_list = [
        f for f in glob.glob(
            '/webpage/static/testLog/*.zip'
        )
    ]
    zip_list = [zip_loc.split('/')[-1] for zip_loc in log_list]
    page = request.args.get('page', default=1, type=int)
    zip_list.sort(reverse=True)
    log_num = len(zip_list)
    total_page = math.ceil(log_num/PAGE_SIZE)
    log_period = parameter.LOGGING_PERIOD()
    download_list = []
    if page == 0:
        data_list = zip_list
    else:
        start = (page-1)*PAGE_SIZE
        if page > total_page:
            data_list = []
        elif page == total_page:
            data_list = zip_list[start:]
        else:
            data_list = zip_list[start:(start+PAGE_SIZE)]

    for data in data_list:
        res_data = {}
        timestamp = int(data.split('.')[0])
        log_time = datetime.fromtimestamp(
            timestamp,
            LOCAL_TZ
        ).strftime(TIME_FORMAT)
        res_data['logTime'] = log_time
        res_data['zipName'] = data
        download_list.append(res_data)

    return render_template(
        'downloadLog.html',
        downloadList=download_list,
        totalPage=total_page,
        currentPage=page,
        pageAmount=PAGE_SIZE,
        logPeriod=log_period
    )


@log_bp.route("/get-latest", methods=['GET'])
def get_latest():
    r = redis.Redis(
        host=parameter.REDIS_SERVER(),
        port=parameter.REDIS_PORT(),
        decode_responses=True
    )
    latest = r.hgetall('latest')
    res_dict = {}
    if 'timestamp' not in latest:
        res_dict['date'] = 'No record'
    else:
        res_dict['date'] = datetime.fromtimestamp(
            int(latest['timestamp']), LOCAL_TZ
        ).strftime(TIME_FORMAT)
        site_list = [item['site'] for item in parameter.SITE_CFG()]
        for site in site_list:
            if site in latest:
                if latest[site] == 'NOT RUNNING':
                    res_dict[site] = 'NOT RUNNING'
                    continue

                json_data = json.loads(latest[site])
                err_item_list = []
                for counter in json_data:
                    err_item_list.append(
                        '{} fail {} times'.format(
                            counter[5:],
                            json_data[counter]
                        )
                    )
                res_dict[site] = err_item_list
            else:
                res_dict[site] = 'pass'

    return jsonify(res_dict)
