#!/usr/bin/python3
import re
import smtplib
import glob
import os
import json
import zipfile
import requests
from datetime import datetime
from datetime import timedelta
from collections import Counter
from collections import defaultdict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import redis
import pytz
import agent.config.parameter as parameter


LOG_TIMEOUT_SECS = parameter.LOG_TIMEOUT_DAYS() * 60 * 60 * 24


def get_log_ts(log):
    split = log.split('_')
    year = int(split[-1][0:4])
    month = int(split[-1][4:6])
    date = int(split[-1][6:8])
    hour = int(split[-1][8:10])
    minute = int(split[-1][10:12])
    log_time = datetime(year, month, date, hour, minute)
    return log_time


def get_api_res_record(log):
    return log.replace('_test_result_', '_api_response_')


def compress_log_to_zip(zip_name, log_list):
    with zipfile.ZipFile(zip_name, 'w') as zf:
        for log_file in log_list:
            zf.write(log_file)


def send_slack_msg(msg):
    for target in parameter.SLACK_NOTIF_LIST():
        my_params = {
            'token': parameter.SLACK_TOKEN(),
            'channel': target
        }
        r = requests.post(
            parameter.SLACK_URL(),
            params=my_params,
            data=msg.encode(),
        )


class LogExamer:
    def __init__(self):
        self.gmail_user = parameter.NOTIF_SENDER_ACCOUNT()
        self.gmail_password = parameter.NOTIF_SENDER_PW()

    def send_fail_letter(self, subject, content, attach_list):
        from_address = self.gmail_user
        to_address = parameter.NOTIF_LIST()
        sub = subject
        contents = content
        attachments = attach_list

        mail = MIMEMultipart()
        mail['From'] = from_address
        mail['To'] = ', '.join(to_address)
        mail['Subject'] = sub
        # Add mail content
        mail.attach(MIMEText(contents))
        # Add mail attachment
        if attach_list:
            for file in attachments:
                if os.path.exists(file):
                    with open(file, 'rb') as fp:
                        add_file = MIMEBase('application', "octet-stream")
                        add_file.set_payload(fp.read())
                    encoders.encode_base64(add_file)
                    add_file.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=file
                    )
                    mail.attach(add_file)

        # Use smtp to send mail
        smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtpserver.ehlo()
        smtpserver.login(self.gmail_user, self.gmail_password)
        smtpserver.sendmail(from_address, to_address, mail.as_string())
        smtpserver.quit()

    def fail_alert(self, send_email=True):
        check_period = parameter.FAIL_ALERT_PERIOD_MINS()
        fail_thres = parameter.FAIL_ALERT_THRESHOLD()
        delta_time = timedelta(minutes=check_period)
        has_failure = False
        mail_content = ''

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
            period_err = 0
            for counter in res_data[site]:
                period_err += res_data[site][counter]
            if period_err >= fail_thres:
                has_failure = True
                mail_content += '{}: hit fail alert threshold\n'.format(site)

        if has_failure:
            if send_email:
                self.send_fail_letter(
                    parameter.FAIL_ALERT_SUB(),
                    mail_content,
                    None
                )

    def check_log(self, send_email=True):
        finish_pattern = re.compile(r'Ran (\d*) tests in (\d*).(\d*)s')
        fail_pattern = re.compile(r'FAIL: (\w*) ')
        error_pattern = re.compile(r'ERROR: (\w*) ')
        site_cfg = parameter.SITE_CFG()

        mail_content = ''
        mail_attach_list = []
        has_failure = False
        r = redis.Redis(host=parameter.REDIS_SERVER(),
                        port=parameter.REDIS_PORT(), decode_responses=True)
        redis_log_time = int(datetime.now().timestamp())

        # clear last latest_redis_log
        r.delete('latest')
        r.hset('latest', 'timestamp', redis_log_time)

        for config in site_cfg:
            log_list = [
                f for f in glob.glob(
                    '/log/' + config['site'] +
                    '_test_result_*.log'
                )]
            error_count = defaultdict(int)
            for log in log_list:
                log_content = ''
                fail_list = []
                error_list = []
                log_time = get_log_ts(log)
                if datetime.now() < (log_time + timedelta(minutes=parameter.TEST_DURATION_MINUTES())):
                    continue

                with open(log, 'r') as f:
                    log_content = f.read()

                # Parsing test which finish successfully
                if len(finish_pattern.findall(log_content)) == 1:
                    fail_list = fail_pattern.findall(log_content)
                    error_list = error_pattern.findall(log_content)
                    if len(fail_list) > 0 or len(error_list) > 0:
                        has_failure = True
                        mail_content += 'Site: {} at {}: fail item\n'.format(
                            config['site'],
                            log_time.astimezone(
                                pytz.timezone(parameter.LOCAL_TIMEZONE())
                            )
                        )
                        mail_content += '    FAIL: {}\n'.format(fail_list)
                        mail_content += '    ERROR: {}\n'.format(error_list)
                        mail_content += '\n'
                        mail_content += '\n'
                        mail_attach_list.append(log)
                        mail_attach_list.append(get_api_res_record(log))

                        for fail in fail_list:
                            error_count[fail] += 1

                        for error in error_list:
                            error_count[error] += 1
                    else:
                        os.remove(log)
                        os.remove(get_api_res_record(log))

                # Record test which hanged for long time.
                else:
                    has_failure = True
                    mail_content += 'Site: {}, at {} unfinished\n\n\n'.format(
                        config['site'],
                        log_time.astimezone(
                            pytz.timezone(parameter.LOCAL_TIMEZONE())
                        )
                    )
                    os.remove(log)
                    os.remove(get_api_res_record(log))

            if error_count:
                mail_content += 'Fail of site {} in check period\n'.format(
                    config['site']
                )
                redis_data_dict = {}
                for key in error_count:
                    mail_content += '{}: {}\n'.format(key, error_count[key])
                    redis_data_dict[key] = error_count[key]
                mail_content += '\n\n'
                redis_data_key = 'LOG:' + str(redis_log_time)
                redis_data_field = config['site']
                r.hset(redis_data_key, redis_data_field, json.dumps(redis_data_dict))
                r.hset('latest', redis_data_field, json.dumps(redis_data_dict))
                r.expire(redis_data_key, time=LOG_TIMEOUT_SECS)

            # If a site doesn't have testing log in recent check period, mark it in NOT RUNNING status
            elif not log_list:
                redis_data_field = config['site']
                r.hset('latest', redis_data_field, 'NOT RUNNING')
                has_failure = True
                mail_content += f'Site: {config["site"]} has no testing result in this checking period.\n\n\n'

        if has_failure:
            try:
                send_slack_msg(mail_content)
            except Exception as e:
                mail_content += f'Send msg to slack fail at: {e}'

            if send_email:
                self.send_fail_letter(
                    parameter.NOTIF_MAIL_SUB(),
                    mail_content,
                    mail_attach_list
                )

            # Backup fail_log for download
            print(f'MA\n{mail_attach_list}')
            if mail_attach_list:
                zip_file = '/webpage/static/testLog/{}.zip'.format(
                    redis_log_time
                )
                compress_log_to_zip(zip_file, mail_attach_list)

                for rm_log in mail_attach_list:
                    os.remove(rm_log)
