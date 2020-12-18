import redis
import argparse
import json
from datetime import datetime
import subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    '-u', 
    '--url', 
    type=str,
    help='url address of redis'
)
parser.add_argument(
    '-p', 
    '--port', 
    type=int,
    help='port of redis'
)

args = parser.parse_args()
redis_url = args.url
redis_port = args.port
#print(f'redis url: {redis_url}')
#print(f'redis port: {redis_port}')



r = redis.Redis(
    host=redis_url,
    port=redis_port,
    decode_responses=True
)


tool_dir = '/home/dlink/tool/tool/jenkins2aws/'
server_status_cfg = r.hgetall('server_status_cfg')
#print(f'res: {server_status_cfg}')
rm_cron_cmd = f'sudo crontab -u dlink -l | grep -v ctl_aws_instance.py | sudo crontab -u dlink -'
p = subprocess.run(rm_cron_cmd, stdout=subprocess.PIPE, shell=True)
for server, server_cfg in server_status_cfg.items():
    server_cfg_list = json.loads(server_cfg)
    
    for server_cfg in server_cfg_list:
        server_action = server_cfg['action']
        cmd = f'python3 {tool_dir}ctl_aws_instance.py -n \'"{server}"\' -a {server_action}'
        #print(cmd)
        if 'cron' in server_cfg:
            cron = server_cfg['cron']
            cron_cmd = f'(sudo crontab -u dlink -l ; echo "{cron} {cmd}") | sudo crontab -u dlink -'
            print(f'write into cron: {cron_cmd}')
            p = subprocess.run(cron_cmd, stdout=subprocess.PIPE, shell=True)
        else:
            print(f'just send cmd: {cmd}')
            p = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

