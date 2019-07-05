#!/usr/bin/python3
import re
import smtplib
import glob
import os
import json
import zipfile
from datetime import datetime
from datetime import timedelta
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
            error_count = {}
            for log in log_list:
                log_content = ''
                fail_list = []
                error_list = []
                log_time = get_log_ts(log)
                if datetime.now() < (log_time + timedelta(minutes=parameter.TEST_DURATION_MINUTES())):
                    continue

                with open(log, 'r') as f:
                    log_content = f.read()
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
                            if fail not in error_count:
                                error_count[fail] = 1
                            else:
                                error_count[fail] += 1

                        for error in error_list:
                            if error not in error_count:
                                error_count[error] = 1
                            else:
                                error_count[error] += 1
                    else:
                        os.remove(log)
                        os.remove(get_api_res_record(log))
                else:
                    has_failure = True
                    mail_content += 'Site:{}, at {} unfinished\n\n\n'.format(
                        config['site'],
                        log_time.astimezone(
                            pytz.timezone(parameter.LOCAL_TIMEZONE())
                        )
                    )

            if len(error_count) > 0:
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
            # If a site doesn't have testing log, mark it in NOT RUNNING status
            elif len(log_list) == 0:
                redis_data_field = config['site']
                r.hset('latest', redis_data_field, 'NOT RUNNING')

        if has_failure:
            if send_email:
                self.send_fail_letter(
                    parameter.NOTIF_MAIL_SUB(),
                    mail_content,
                    mail_attach_list
                )

            zip_file = '/webpage/static/testLog/{}.zip'.format(
                redis_log_time
            )
            # Don't make empty zip file
            if len(mail_attach_list) > 0:
                compress_log_to_zip(zip_file, mail_attach_list)

            for rm_log in mail_attach_list:
                os.remove(rm_log)
