import subprocess
import argparse
import json
from shutil import copyfile
import redis
parser = argparse.ArgumentParser()
parser.add_argument(
    '-n',
    '--name',
    type=str,
    help='name of aws ec2 instance'
)
parser.add_argument(
    '-a',
    '--action',
    type=str,
    help='what to do'
)
args = parser.parse_args()

if args.action == 'terminate-instances' and 'QA_US_321' in args.name:
    print("This instance can't be terminate.")
    exit() 



redis_url = '54.67.52.204'
redis_port = 6379
r = redis.Redis(
    host=redis_url,
    port=redis_port,
    decode_responses=True
)

in_testing = eval(r.get('in_testing'))
if in_testing:
    print("On testing do not do anything to server.")
    exit() 



cmd = f"aws ec2 describe-instances --region us-west-1 --filter 'Name=tag:Name,Values={args.name}'"
p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
res_data = json.loads(p.stdout.decode())
print(json.dumps(res_data, indent=4))

ins_list = []
for item in res_data['Reservations']:
    tmp = {}
    instance = item['Instances'][0]
    if instance['State']['Name'] == 'terminated':
        continue
    tmp['ip'] = instance.get('PublicIpAddress', '0.0.0.0')
    tmp['ins_id'] = instance['InstanceId']
    ins_list.append(tmp)

for ins in ins_list:
    cmd = f'aws ec2 {args.action} --region us-west-1 --instance-ids {ins["ins_id"]}'
    print(cmd)
    subprocess.call(cmd, shell=True)
