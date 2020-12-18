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
    help='dir of rcd tool'
)
parser.add_argument(
    '-c', 
    '--connect_num', 
    type=str,
    help='number of rcd connection'
)

args = parser.parse_args()
cmd = f"aws ec2 describe-instances --region us-west-1 --filter 'Name=tag:Name,Values={args.name}'"
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()

res_data = json.loads(output)
print(json.dumps(res_data, indent=4))

for item in res_data['Reservations']:
    tmp = {}
    instance = item['Instances'][0]
    if instance['State']['Name'] == 'terminated':
        continue
    ip = instance['PublicIpAddress']
    break
print(f'PUBLIC ip: [{ip}]')
'''
copyfile(f'{args.dir}/inventory_template', f'{args.dir}/rcd_cfg')
print('COPY template CFG successful.')
subprocess.call(f'echo {ip} >> {args.dir}/rcd_cfg', shell=True)
print('write ip to cfg.')
'''
with open(f'{args.dir}/rcd_cfg', 'w') as f:
    f.write(f'''[server:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
dev_num={args.connect_num}
ansible_user=qateam

[server]
{ip}
    ''')
