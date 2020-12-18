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
parser.add_argument(
    '-c', 
    '--test_case',
    type=str,
    help='which case to test'
)

GET_TEST_CASE = {
    "0": "Check Server Port and SignalD DNS",
    "1": "All",
    "2": "Wizard_API",
    "3": "Live_view",
    "4": "Relay_connection",
    "5": "Sigaling_update",
    "6": "Mobile_API",
    "7": "Open_API",
    "8": "Signal_DNS",
    "9": "Portal_Jmeter",
    "10": "RTSP",
    "11": "SAS_Relay",
    "12": "DCD",
    "21": "Send Event",
    "22": "FW Upgrade",
    "23": "CloudNVR",
    "31": "Create account specific site"
}


args = parser.parse_args()
TIME_DIR = '/var/log/jenkins_scan/apiscan/reponse_time'
LOG_DIR = '/var/log/jenkins_scan/apiscan'
SUM_DIR = '/var/log/jenkins_scan/apiscan/PF_check'
LOG_NAME = f'{args.site}_{args.time}.log'
TEST_CASE = GET_TEST_CASE[args.test_case]

def get_fail_item():
    cmd = f'grep FAIL {LOG_DIR}/{LOG_NAME}'
    print(f'CMD:{cmd}')
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print(f'STDOUT:\n{p.stdout.decode()}')
    print(f'STDERR:\n{p.stderr.decode()}')
    return p.stdout.decode()


SUB = f'Result of [{args.time}] {args.site} apiscan case {TEST_CASE}'
#LOG_LIST = [ f for f in glob.glob('/var/log/jenkins_scan/apiscan/*.log') ]
LOG_LIST = [ f'{LOG_DIR}/{LOG_NAME}' ]
#print(f'LOG_LIST:\n{LOG_LIST}')
ERROR_STR = get_fail_item()
print(f'ERR_STR: \n{ERROR_STR}')
SLACK_MSG = f'[{args.time}] {args.site} apiscan Case[{TEST_CASE}] 已結束\n'
MAIL_CONTENT = f'''
{args.site} apiscan test case[{TEST_CASE}] just start at {args.time} has finished.
Attachment is the test log.
'''
if len(ERROR_STR):
    END_MSG = f'\nBelow are FAIL items\n{ERROR_STR}'
else:
    END_MSG = '\nAll test pass.'

SLACK_MSG += END_MSG
MAIL_CONTENT += END_MSG


def send_report():
    send_msg.send_mail(SUB, MAIL_CONTENT, LOG_LIST, args.email_list_str)
    for rm_log in LOG_LIST:
        os.remove(rm_log)
        #pass

send_report()
send_msg.send_slack_msg(SLACK_MSG)
os.remove(f'{TIME_DIR}/{LOG_NAME}')
os.remove(f'{SUM_DIR}/{LOG_NAME}')
