import requests
import re
from datetime import datetime
from collections import defaultdict

log_file = './hermes_conn.log'
site = 'qa'
curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
param = {
    'range': 'all'
}
response = requests.get(
    f'******************************',
    params=param,
    verify=False
)

tmp = defaultdict(dict)

tmp['curr_time'] = curr_time
for host in response.json():
    tmp[host['host']]['avg_load'] = host['avg_loading']
    tmp[host['host']]['cpu'] = host['cpu_load'][:host['cpu_load'].index('*')]
    tmp[host['host']]['mem'] = host['mem_load'][:host['mem_load'].index('*')]
print(tmp)
