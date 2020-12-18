import agent.agent as agent
import agent.config.parameter as parameter
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '-a',
    '--account',
    type=str,
    help='test account'
)
parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='password of test account'
)
parser.add_argument(
    '-d',
    '--device',
    type=str,
    help='test device'
)
args = parser.parse_args()



CLIENT_ID = parameter.APP_ID()
CLIENT_SECRET = parameter.APP_SECRET()
URI = parameter.OPENAPI_URL()
ACCOUNT = args.account
PASSWORD = args.password
MY_DLINK_ID = args.device
uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)

# Check account and password
uap.get_user_token(ACCOUNT, PASSWORD)
if uap.user_token == '':
    sys.exit('\n\n[ALERT] Wrong user/pasword combination')
	
# Check dev binding
uap.get_device_info([MY_DLINK_ID])
res_json = uap.res.json()
if 'error' in res_json:
    sys.exit('\n\n[ALERT] Please bind dev first')

# Check dev subscribe
uap.cnvr_query_subscription()
SUBS_ID = None
try:
    subscription_list = uap.res.json()['data']
    for subscription in subscription_list:
        if MY_DLINK_ID in subscription['devices']:
            SUBS_ID = subscription['subs_uid']
except (AttributeError, IndexError):
    pass
finally:
    if SUBS_ID is None:
        sys.exit('\n\n[ALERT] Please add dev to subscribe first')
