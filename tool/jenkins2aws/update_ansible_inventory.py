import subprocess
import argparse
import json
from shutil import copyfile
parser = argparse.ArgumentParser()
parser.add_argument(
    '-n',
    '--name',
    type=str,
    help='name of aws ec2 instance'
)
parser.add_argument(
    '-d',
    '--dir',
    type=str,
    help='dir of config'
)
args = parser.parse_args()

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

copyfile(f'{args.dir}/inventory_template', f'{args.dir}/rcd_lb_test')
with open(f'{args.dir}/rcd_lb_test', 'a') as myfile:
    for instance in ins_list:
        myfile.write(f"{instance['ip']}\n")
