import re
import csv
import json
from collections import defaultdict
DCD_NUM = 4
LB_NUM = 12
ans = defaultdict(dict)


CHANGE_PATT = {}
FAIL_PATT = {}
for i in range(1, DCD_NUM+1):
    str_patt = r'\[change_url\]\[F{4}\d{8}\] to wss://' + f'qa-us-dcdda-{i}.auto.mydlink.com:443/SwitchCamera'
    CHANGE_PATT[f'dcd-{i}'] = re.compile(
        str_patt
    )

    str_patt = f'Cannot connect to host qa-us-dcdda-{i}.local.mydlink.com:443 ssl:False'
    FAIL_PATT[f'dcd-{i}'] = re.compile(
        str_patt
    )

FAIL_PATT[f'dcd'] = re.compile(
    r'Cannot connect to host qa-us-dcdda.local.mydlink.com:443 ssl:False'
)

ans['total'] = defaultdict(int)
for i in range(1, LB_NUM+1):
    ans[f'LB_{i}'] = defaultdict(int)
    with open(f'./LB_{i}.log', 'r') as f:
        log = f.read()
	


    for key in CHANGE_PATT:
        change_list = CHANGE_PATT[key].findall(log)
        ans[f'LB_{i}'][key + 'change'] = len(change_list)
        ans['total'][key + 'change'] += len(change_list)

    for key in FAIL_PATT:
        fail_list = FAIL_PATT[key].findall(log)
        ans[f'LB_{i}'][key + 'fail'] = len(fail_list)
        ans['total'][key + 'fail'] += len(fail_list)

with open('cal.log', 'w') as outfile:
    json.dump(ans, outfile, indent=4)
