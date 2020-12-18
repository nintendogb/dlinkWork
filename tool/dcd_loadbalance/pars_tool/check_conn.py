import re
import csv
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.ticker import MaxNLocator
from matplotlib.pyplot import MultipleLocator
import matplotlib.dates as mdates
from datetime import datetime


DCD_NUM = 4
CSV_TMP = defaultdict(dict)
PIC_VAL_TMP = defaultdict(list)



DCD_PATT = re.compile(
    r'(?P<timestamp>\d{4}/\d{2}/\d{2} \d*:\d{2})\n'
    r'(?P<dcd_num>DCD-\d)\n' +
    r'STAT uptime\s*(?P<uptime>.*)\n' +
    r'STAT system\s*\(CPU/MEM\)\s*(?P<cpu>\d*\.\d*)\s*(?P<mem>\d*\.\d*)\n' +
    r'STAT device-conn-online\s*(?P<conn>\d*)\n' +
    r'STAT Device_KEEP_ALIVE.*\n'
)




with open('./keep.log', 'r') as f:
    log = f.read()
	


dcd_list = [ m.groupdict() for m in DCD_PATT.finditer(log) ]
#print(dcd_list)
for dcd_log in dcd_list:
    CSV_TMP[dcd_log['timestamp']][dcd_log['dcd_num']] = {
        'cpu': dcd_log['cpu'],
        'mem': dcd_log['mem'],
        'conn': dcd_log['conn'],
    }
#print(CSV_TMP)

    


with open('log.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    row_name = ['time']
    for i in range(DCD_NUM):
        row_name += [f'DCD{i+1}_CPU', f'DCD{i+1}_MEM', f'DCD{i+1}_conn']
    row_name += ['total_conn']
    writer.writerow(row_name)
    for time, row in CSV_TMP.items():
        PIC_VAL_TMP['count'] += [datetime.strptime(str(time), '%Y/%m/%d %H:%M')]
        #PIC_VAL_TMP['count'] += [time]
        tmp_list = [time]
        total = 0
        for i in range(DCD_NUM):
            if f'DCD-{i+1}' in row:
                tmp_list += [
                    row[f'DCD-{i+1}']['cpu'],
                    row[f'DCD-{i+1}']['mem'],
                    row[f'DCD-{i+1}']['conn']
                ]
                total += int(row[f'DCD-{i+1}']['conn'])
                PIC_VAL_TMP[f'DCD-{i+1}-CPU'] += [float(row[f'DCD-{i+1}']['cpu'])]
                PIC_VAL_TMP[f'DCD-{i+1}-MEM'] += [float(row[f'DCD-{i+1}']['mem'])]
                PIC_VAL_TMP[f'DCD-{i+1}-CONN'] += [int(row[f'DCD-{i+1}']['conn'])]
            else:
                tmp_list += ['Not Exist'] * 3
                PIC_VAL_TMP[f'DCD-{i+1}-CPU'] += [0.0]
                PIC_VAL_TMP[f'DCD-{i+1}-MEM'] += [0.0]
                PIC_VAL_TMP[f'DCD-{i+1}-CONN'] += [0.0]
        tmp_list += [total]
        PIC_VAL_TMP[f'total_conn'] += [total]
        writer.writerow(tmp_list)

#PIC_VAL_TMP['count'] = [i for i in range(len(CSV_TMP))]
#PIC_VAL_TMP['count'] = ['2020/02/10 11:46', '2020/02/10 11:47', '2020/02/10 11:48']

def print_conn_pic():
    plt.title('CONN Analysis')
    plt.figure(figsize=(20,10))
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-1-CONN'], color='green', label='dcd1')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-2-CONN'], color='red', label='dcd2')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-3-CONN'], color='yellow', label='dcd3')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-4-CONN'], color='blue', label='dcd4')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP['total_conn'], color='black', label='total')
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('count')
    plt.savefig('conn_log.png', dpi=600, format='png')
    plt.clf()


def print_cpu_pic():
    plt.title('CPU Analysis')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-1-CPU'], color='green', label='dcd1')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-2-CPU'], color='red', label='dcd2')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-3-CPU'], color='yellow', label='dcd3')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-4-CPU'], color='blue', label='dcd4')
    
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('percent')
    plt.savefig('cpu_log.png', dpi=600, format='png')
    plt.clf()


def print_mem_pic():
    plt.title('MEM Analysis')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-1-MEM'], color='green', label='dcd1')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-2-MEM'], color='red', label='dcd2')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-3-MEM'], color='yellow', label='dcd3')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'DCD-4-MEM'], color='blue', label='dcd4')

    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('percent')
    plt.savefig('mem_log.png', dpi=600, format='png')
    plt.clf()


#fig, ax = plt.subplots()

#hoursLoc = mdates.HourLocator(interval=1)
#minlocator = mdates.MinuteLocator(interval=20)
'''
fig = plt.figure(figsize=(15,5))
ax = fig.add_subplot(1,1,1)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d, %H'))
'''
'''
hoursLoc = mdates.HourLocator()
minlocator = mdates.MinuteLocator()

ax.xaxis.set_major_locator(hoursLoc)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d, %H'))
ax.xaxis.set_minor_locator(minlocator)
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%M'))
'''
'''
myFmt = mdates.DateFormatter('%m/%d, %H:%M')
ax.xaxis.set_major_formatter(myFmt)
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)
'''
#fig.autofmt_xdate()



#plt.gcf().autofmt_xdate()
#ax = plt.figure().gca()
#ax.yaxis.set_major_locator(MaxNLocator(integer=True))
#plt.figure(figsize=(10,20))
print_conn_pic()
print_cpu_pic()
print_mem_pic()
