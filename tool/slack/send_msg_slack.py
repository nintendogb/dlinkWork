import argparse
import requests
import subprocess
import json
import redis

'''
parser = argparse.ArgumentParser()
parser.add_argument(
    '-n',
    '--name',
    type=str,
    help='name of aws ec2 instance'
)
parser.add_argument(
    '-p',
    '--target_type',
    type=str,
    help='channel or user'
)
parser.add_argument(
    '-t',
    '--target',
    type=str,
    help='which to send'
)
args = parser.parse_args()
'''
REDIS_URL = '**********************'
REDIS_PORT = 6379
SLACK_TOKEN = '***************************'
MSG = 'ted test:large_blue_circle:\n2nd msg:red_circle:'
SLACK_NOTIF_LIST = [
    '@Ted.Kao',
    '#team-siqad-usqa-usage'
    #'@Laurence.Tsai'
]
URL = 'https://mydlink.slack.com/services/hooks/slackbot'
target_prefix = {
    'user': '@',
    'channel': '#'
}

status_symbol = {
    'running': ':large_blue_circle:',
    'stopped': ':red_circle:'
}

def get_aws_instance_list(name_patt):
    cmd = f"aws ec2 describe-instances --region us-west-1 --filter 'Name=tag:Name,Values={name_patt}'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    res_data = json.loads(output)
    #print(json.dumps(res_data, indent=4))
    return res_data['Reservations']


def send_slack_msg(msg):
    for target in SLACK_NOTIF_LIST:
        my_params = {
            'token': SLACK_TOKEN,
            'channel': target
        }
        r = requests.post(
            URL,
            params=my_params,
            data=msg.encode(),
        )

def get_power_status_of_instances(ins_list):
    power_status = {}
    for instance in ins_list:
        tags = instance['Instances'][0]['Tags']
        power = instance['Instances'][0]['State']['Name']
        for tag in tags:
            if tag['Key'] == 'Name':
                ins_name = tag['Value']
                break
        power_status[ins_name] = power
    return power_status

def send_pw_status2slack(ins_patt, ins_status_dict):
    ins_name_list = ins_status_dict.keys()
    msg = f'USQA {ins_patt}現在狀況\n'
    for ins_name in sorted(ins_name_list):
        if ins_status_dict[ins_name] in status_symbol:
            msg += f'{status_symbol[ins_status_dict[ins_name]]}{ins_name}\n'
        else:
            msg += f':black_circle:{ins_name}:{ins_status_dict[ins_name]}\n'
    send_slack_msg(msg)

def send_redis_croncfg2slack():
    r = redis.Redis(
        host=REDIS_URL,
        port=REDIS_PORT,
        decode_responses=True
    )
    msg = f'目前是否在測試期間[{r.get("in_testing")}]\n'
    server_status_cfg = r.hgetall('server_status_cfg')
    if len(server_status_cfg):
        msg += '目前crontab自動控制aws instance之設定\n'
        for server in sorted(server_status_cfg.keys()):
            server_cfg_list = json.loads(server_status_cfg[server])
            msg += f'*{server}:*\n'
            for server_cfg in server_cfg_list:
                if 'cron' in server_cfg:
                    cron = server_cfg['cron']
                    server_action = server_cfg['action']
                    msg += f':black_small_square:[{cron}]{server_action}\n'
    else:
        msg = '目前沒有crontab自動控制aws instance之設定\n'
    send_slack_msg(msg)
    
def check_instance_status(ins_patt):
    ins_list = get_aws_instance_list(ins_patt)
    pw_dict = get_power_status_of_instances(ins_list)
    send_pw_status2slack(ins_patt, pw_dict)

send_redis_croncfg2slack()
check_instance_status('QA_US_321*')
check_instance_status('SQAD_*')





'''
print(r.status_code)
print(r.request.body)
'''
