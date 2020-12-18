import re
import csv
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import matplotlib.dates as mdates
from datetime import datetime
RCD_NUM = 3
CSV_TMP = defaultdict(dict)
PIC_VAL_TMP = defaultdict(list)
MAX_DIFF = []
RCD_PATT = re.compile(
    r'(?P<timestamp>\d{4}/\d{2}/\d{2} \d*:\d{2}:\d{2})\n'
    r'(?P<rcd_num>RCD-\d)\n'
    r'STAT uptime\s*(?P<uptime>.*)\n'
    r'STAT system\s*\(CPU\%\)\s*(?P<cpu>\d*\.\d*)\n'
    r'STAT system\s*\(MEM\%\)\s*(?P<mem>\d*\.\d*)\n'
    r'STAT device-conn-online\s*(?P<conn>\d*)\n'
    r'STAT device-conn \(Avg/Acc\)\s*(?P<avg_conn>\d*)\s*(?P<acc_conn>\d*)\n'
)

PIC_COLOR = [
    'green',
    'red',
    'yellow',
    'blue',
]


with open('./rcd_stats.log', 'r') as f:
    log = f.read()
	


rcd_list = [ m.groupdict() for m in RCD_PATT.finditer(log) ]
#print(rcd_list)
for rcd_log in rcd_list:
    CSV_TMP[rcd_log['timestamp']][rcd_log['rcd_num']] = {
        'cpu': rcd_log['cpu'],
        'mem': rcd_log['mem'],
        'conn': rcd_log['conn'],
    }
#print(CSV_TMP)

with open('log.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    row_name = ['time']
    for i in range(RCD_NUM):
        row_name += [f'RCD{i+1}_CPU', f'RCD{i+1}_MEM', f'RCD{i+1}_conn']
    row_name += ['total_conn', 'max_diff']
    writer.writerow(row_name)

    for time, row in CSV_TMP.items():
        PIC_VAL_TMP['count'] += [datetime.strptime(str(time), '%Y/%m/%d %H:%M:%S')]
        tmp_list = [time]
        tmp_dev_conn = []
        total = 0
        for i in range(RCD_NUM):
            if f'RCD-{i+1}' in row:
                tmp_list += [
                    row[f'RCD-{i+1}']['cpu'],
                    row[f'RCD-{i+1}']['mem'],
                    row[f'RCD-{i+1}']['conn']
                ]
                tmp_dev_conn.append(int(row[f'RCD-{i+1}']['conn']))
                total += int(row[f'RCD-{i+1}']['conn'])
                PIC_VAL_TMP[f'RCD-{i+1}-CPU'] += [float(row[f'RCD-{i+1}']['cpu'])]
                PIC_VAL_TMP[f'RCD-{i+1}-MEM'] += [float(row[f'RCD-{i+1}']['mem'])]
                PIC_VAL_TMP[f'RCD-{i+1}-CONN'] += [int(row[f'RCD-{i+1}']['conn'])]
            else:
                tmp_list += ['Not Exist'] * 3
                PIC_VAL_TMP[f'RCD-{i+1}-CPU'] += [0.0]
                PIC_VAL_TMP[f'RCD-{i+1}-MEM'] += [0.0]
                PIC_VAL_TMP[f'RCD-{i+1}-CONN'] += [0.0]
        max_diff = max(tmp_dev_conn) - min(tmp_dev_conn)
        max_diff_percent = max_diff / ( total / RCD_NUM ) * 100
        MAX_DIFF.append(max_diff_percent)
        tmp_list += [total, max_diff_percent]
        PIC_VAL_TMP[f'total_conn'] += [total]
        writer.writerow(tmp_list)

def print_conn_pic():
    plt.title('CONN Analysis')
    plt.figure(figsize=(20,10))
    for i in range(RCD_NUM):
        plt.plot(
            PIC_VAL_TMP['count'],
            PIC_VAL_TMP[f'RCD-{i+1}-CONN'],
            color=PIC_COLOR[i],
            label=f'rcd{i+1}'
        )
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP['total_conn'], color='black', label='total')
    '''
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-1-CONN'], color='green', label='rcd1')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-2-CONN'], color='red', label='rcd2')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-3-CONN'], color='yellow', label='rcd3')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-4-CONN'], color='blue', label='rcd4')
    '''
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('count')
    plt.savefig('conn_log.png', dpi=600, format='png')
    plt.clf()


def print_cpu_pic():
    plt.title('CPU Analysis')
    for i in range(RCD_NUM):
        plt.plot(
            PIC_VAL_TMP['count'],
            PIC_VAL_TMP[f'RCD-{i+1}-CPU'],
            color=PIC_COLOR[i],
            label=f'rcd{i+1}')
    '''
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-2-CPU'], color='red', label='rcd2')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-3-CPU'], color='yellow', label='rcd3')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-4-CPU'], color='blue', label='rcd4')
    '''
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('percent')
    plt.savefig('cpu_log.png', dpi=600, format='png')
    plt.clf()


def print_mem_pic():
    plt.title('MEM Analysis')
    for i in range(RCD_NUM):
        plt.plot(
            PIC_VAL_TMP['count'],
            PIC_VAL_TMP[f'RCD-{i+1}-MEM'],
            color=PIC_COLOR[i],
            label=f'rcd{i+1}'
        )
    '''
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-2-MEM'], color='red', label='rcd2')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-3-MEM'], color='yellow', label='rcd3')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'RCD-4-MEM'], color='blue', label='rcd4')
    '''
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('percent')
    plt.savefig('mem_log.png', dpi=600, format='png')
    plt.clf()


def print_diff_pic():
    plt.title('Max diffrence Analysis')
    plt.plot(PIC_VAL_TMP['count'], MAX_DIFF, color='black', label='diff percent')

    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('percentage')
    plt.savefig('diff_log.png', dpi=600, format='png')
    plt.clf()


print_conn_pic()
print_cpu_pic()
print_mem_pic()
print_diff_pic()
