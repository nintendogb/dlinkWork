import re
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.ticker import MaxNLocator
from matplotlib.pyplot import MultipleLocator
import matplotlib.dates as mdates
from datetime import datetime
'''
hermes2
04/24/2020, 09:59:25
Active connections: 1
server accepts handled requests
 33619 33619 59300
Reading: 0 Writing: 1 Waiting: 0
'''
hermes_patt = re.compile(
    r'(?P<hermes_num>hermes\d)\n'
    r'(?P<timestamp>\d{2}/\d{2}/\d{4}, \d*:\d{2}:\d{2})\n'
    r'Active connections:\s*(?P<conn>\d*)\s*\n'
    r'server accepts handled requests\n\s*(?P<accept>\d*)\s*(?P<handle>\d*)\s*(?P<requset>\d*)\s*\n'
    r'Reading: (?P<reading>\d*) Writing: (?P<writing>\d*) Waiting: (?P<waiting>\d*)\s*\n'
)
'''
hermes1_patt = re.compile(
    r'(?P<hermes_num>hermes1)\n'
    r'(?P<timestamp>\d{2}/\d{2}/\d{4}, \d*:\d{2}:\d{2})\n'
    r'Active connections:\s*(?P<conn>\d*)\s*\n'
    r'server accepts handled requests\n\s*(?P<accept>\d*)\s*(?P<handle>\d*)\s*(?P<requset>\d*)\s*\n'
    r'Reading: (?P<reading>\d*) Writing: (?P<writing>\d*) Waiting: (?P<waiting>\d*)\s*\n'
)

hermes2_patt = re.compile(
    r'(?P<hermes_num>hermes2)\n'
    r'(?P<timestamp>\d{2}/\d{2}/\d{4}, \d*:\d{2}:\d{2})\n'
    r'Active connections:\s*(?P<conn>\d*)\s*\n'
    r'server accepts handled requests\n\s*(?P<accept>\d*)\s*(?P<handle>\d*)\s*(?P<requset>\d*)\s*\n'
    r'Reading: (?P<reading>\d*) Writing: (?P<writing>\d*) Waiting: (?P<waiting>\d*)\s*\n'
)
'''
with open('/home/dlink/hermes_conn_bk.log', 'r') as f:
    log = f.read()

hermes_list = [ m.groupdict() for m in hermes_patt.finditer(log) ]
#hermes1_list = [ m.groupdict() for m in hermes1_patt.finditer(log) ]
#hermes2_list = [ m.groupdict() for m in hermes2_patt.finditer(log) ]
#print(hermes1_list)
hermes1_counter = 0
hermes2_counter = 0
cal_dict = defaultdict(dict)
hermes1_conn = []
hermes2_conn = []
total_conn = []
ts_list = []
for item in hermes_list:
    cal_dict[item['timestamp']][item['hermes_num']] = item['conn']

    
#print(cal_dict)
for ts, res in cal_dict.items():
    ts_list.append(datetime.strptime(ts, '%m/%d/%Y, %H:%M:%S'))
    hermes1 = 0
    hermes2 = 0
    if 'hermes1' in res:
        hermes1 = int(res['hermes1'])

    if 'hermes2' in res:
        hermes2 = int(res['hermes2'])

    hermes1_conn.append(hermes1)
    hermes1_counter += (hermes1)
    hermes2_conn.append(hermes2)
    hermes2_counter += (hermes2)
    total_conn.append(hermes1 - hermes2)

print(f'hermes1 counter: {hermes1_counter}, hermes2 counter: {hermes2_counter}')

def print_conn_pic():
    plt.title('CONN analysis')
    plt.figure(figsize=(20,10))
    plt.plot(ts_list, hermes1_conn, color='green', label='hermes1')
    plt.plot(ts_list, hermes2_conn, color='red', label='hermes2')
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('count')
    plt.savefig('./conn_log.png', dpi=600, format='png')
    plt.clf()

def print_total_pic():
    plt.title('CONN analysis')
    plt.figure(figsize=(20,10))
    plt.plot(ts_list, total_conn, color='black', label='hermes_conn')
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('count')
    plt.savefig('./total_log.png', dpi=600, format='png')
    plt.clf()

#print_conn_pic()
print_total_pic()
