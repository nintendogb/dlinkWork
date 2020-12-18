import os
import argparse
import glob
from collections import defaultdict
import subprocess
import send_msg
parser = argparse.ArgumentParser()
parser.add_argument(
    '-t', 
    '--time', 
    type=str,
    help='test start time'
)
parser.add_argument(
    '-s', 
    '--site', 
    type=str,
    help='which site to test'
)
parser.add_argument(
    '-e', 
    '--email_list_str',
    default='',
    type=str,
    help='notif email list'
)
args = parser.parse_args()
LOG_DIR = '/var/log/jenkins_scan/python_apiscan'
RES_LOG = f'{LOG_DIR}/{args.site}_res_{args.time}.log'

def get_fail_item():
    cmd = f'grep "FAIL:\|ERROR:" {RES_LOG}'
    print(f'CMD:{cmd}')
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print(f'STDOUT:\n{p.stdout.decode()}')
    print(f'STDERR:\n{p.stderr.decode()}')
    return p.stdout.decode()


def get_total_res():
    cmd = f'cat {RES_LOG}'
    print(f'CMD:{cmd}')
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print(f'STDOUT:\n{p.stdout.decode()}')
    print(f'STDERR:\n{p.stderr.decode()}')
    return p.stdout.decode()

SUB = f'Result of [{args.time}] {args.site} apiscan test'
#LOG_LIST = [ f for f in glob.glob('/var/log/jenkins_scan/python_apiscan/*_api_response_*.log') ]
LOG_LIST = [ f'{LOG_DIR}/{args.site}_api_response_{args.time}.log' ]
ERROR_STR = get_fail_item()
TOTAL_RES = get_total_res()
SLACK_MSG = f'[{args.time}] {args.site} python apiscan 已結束\n'
MAIL_CONTENT = f'''
{args.site} python apiscan test just start at {args.time} has finished.
Attachment is the test log.
'''
if len(ERROR_STR):
    FAIL_SUMMARY_MSG = f'\nBelow are FAIL items\n{ERROR_STR}'
else:
    FAIL_SUMMARY_MSG = '\nAll test pass.'

SLACK_MSG += FAIL_SUMMARY_MSG
MAIL_CONTENT += FAIL_SUMMARY_MSG
MAIL_CONTENT += f'\n\n\n\n{TOTAL_RES}'


def send_report():
    send_msg.send_mail(SUB, MAIL_CONTENT, LOG_LIST, args.email_list_str)
    for rm_log in LOG_LIST:
        os.remove(rm_log)
        #pass

#print(f'\n\n\nTEST RESULT:\n{TOTAL_RES}')
print(f'FAIL ITEM:\n{ERROR_STR}')
send_report()
send_msg.send_slack_msg(SLACK_MSG)
send_msg.send_slack_msg(f'test result\n{TOTAL_RES}')
os.remove(RES_LOG)
