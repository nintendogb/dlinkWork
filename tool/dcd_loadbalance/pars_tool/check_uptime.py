import re
import csv
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.ticker import MaxNLocator
from matplotlib.pyplot import MultipleLocator
import matplotlib.dates as mdates
from datetime import datetime
import json


DCD_NUM = 4
CSV_TMP = defaultdict(dict)
PIC_VAL_TMP = defaultdict(list)
CSV_TS = None


DCD_PATT = re.compile(
    r'(?P<timestamp>\d{4}/\d{2}/\d{2} \d*:\d{2})\n'
    r'(?P<dcd_num>DCD-\d)\n' +
    r'STAT uptime\s*(?P<uptime>.*)\n' +
    r'STAT system\s*\(CPU/MEM\)\s*(?P<cpu>\d*\.\d*)\s*(?P<mem>\d*\.\d*)\n' +
    r'STAT device-conn-online\s*(?P<conn>\d*)\n' +
    r'STAT Device_KEEP_ALIVE.*\n'
)




with open('/home/dlink/keep.log', 'r') as f:
    log = f.read()
	


dcd_list = [ m.groupdict() for m in DCD_PATT.finditer(log) ]
#print(dcd_list)
for dcd_log in dcd_list:
    if CSV_TS is None:
        CSV_TS = dcd_log['timestamp'].replace(' ', '').replace('/', '').replace(':', '')
    CSV_TMP[dcd_log['timestamp']][f'{dcd_log["dcd_num"]}'] = dcd_log['uptime'],
print(json.dumps(CSV_TMP, indent=4))

#with open(f'uptime{datetime.now().strftime("%Y%m%d%H%M")}.csv', 'w', newline='') as csvfile:
with open(f'uptime{CSV_TS}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    row_name = ['time']
    for i in range(DCD_NUM):
        row_name += [f'DCD{i+1}_uptime']
    writer.writerow(row_name)
    for time, data in CSV_TMP.items():
        tmp_list = [time]
        for i in range(DCD_NUM):
            tmp_list += [
                data.get(f'DCD-{i+1}', 'Not Exist')
            ]
        writer.writerow(tmp_list)
