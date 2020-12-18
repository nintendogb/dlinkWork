import re
import csv
import json
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
    r'> (?P<timestamp>\d{4}/\d{2}/\d{2} \d*:\d{2}:\d{2})\n'
    r'(.|\n)*?'
    r'STAT uptime\s*(?P<uptime>.*)\n'
    r'(.|\n)*?'
    r'STAT system\s*\(CPU/MEM\)\s*(?P<cpu>\d*\.\d*)\s*(?P<mem>\d*\.\d*)\n' +
    r'(.|\n)*?'
    r'STAT device-conn-online\s*(?P<conn>\d*)\n' +
    r'(.|\n)*?'
    r'STAT Device_SIGN_IN\s*\(Avg/Acc\)\s*\d*\s*(?P<sign_in>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_EVENT\s*\(Avg/Acc\)\s*\d*\s*(?P<event>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_START_VIEWING\s*\(Avg/Acc\)\s*\d*\s*(?P<start_viewing>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_STOP_VIEWING\s*\(Avg/Acc\)\s*\d*\s*(?P<stop_viewing>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_REGISTER\s*\(Avg/Acc\)\s*\d*\s*(?P<register>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_RECYCLE_CHANNEL\s*\(Avg/Acc\)\s*\d*\s*(?P<recycle_channel>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_GET_POLICY\s*\(Avg/Acc\)\s*\d*\s*(?P<get_policy>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_GET_SCHEDULE\s*\(Avg/Acc\)\s*\d*\s*(?P<get_schedule>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_CHANGE_POLICY\s*\(Avg/Acc\)\s*\d*\s*(?P<change_policy>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_CHANGE_SCHEDULE\s*\(Avg/Acc\)\s*\d*\s*(?P<change_schedule>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_CHANGE_SCENE\s*\(Avg/Acc\)\s*\d*\s*(?P<change_scene>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_GET_SERVER_INFO\s*\(Avg/Acc\)\s*\d*\s*(?P<get_server_info>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_KEEP_ALIVE\s*\(Avg/Acc\)\s*\d*\s*(?P<keep_alive>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_GET_REGULAR\s*\(Avg/Acc\)\s*\d*\s*(?P<get_regular>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_M2M_EVENT\s*\(Avg/Acc\)\s*\d*\s*(?P<m2m_event>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_RTSP_ACK_CHANNEL\s*\(Avg/Acc\)\s*\d*\s*(?P<rtsp_ack_channel>\d*)\n'
    r'(.|\n)*?'
    r'STAT Device_CHECK_ALIVE\s*\(Avg/Acc\)\s*\d*\s*(?P<check_alive>\d*)\n'
    r'(.|\n)*?'
)




with open('./qa_dcd.log', 'r') as f:
    log = f.read()
	


dcd_list = [ m.groupdict() for m in DCD_PATT.finditer(log) ]
print(json.dumps(dcd_list, indent=4))

    


with open('log.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    row_name = [
        'timestamp',
        'uptime',
        'cpu',
        'mem',
        'conn',
        'sign_in',
        'event',
        'start_viewing',
        'stop_viewing',
        'register',
        'recycle_channel',
        'get_policy',
        'get_schedule',
        'change_policy',
        'change_schedule',
        'change_scene',
        'get_server_info',
        'keep_alive',
        'get_regular',
        'm2m_event',
        'rtsp_ack_channel',
        'check_alive'
    ]
    writer.writerow(row_name)
    pre_val = None
    for dcd_log in dcd_list:
        tmp_list = []
        if pre_val is not None:
            PIC_VAL_TMP['count'] += [datetime.strptime(str(dcd_log['timestamp']), '%Y/%m/%d %H:%M:%S')]
            for item in row_name:
                if item in ['timestamp', 'uptime', 'cpu', 'mem', 'conn']:
                    tmp_list.append(dcd_log[item])
                    if item in ['cpu', 'mem', 'conn']:
                        PIC_VAL_TMP[item].append(float(dcd_log[item]))
                else:
                    tmp_list.append(int(dcd_log[item]) - int(pre_val[item]))
            writer.writerow(tmp_list)
        pre_val = dcd_log
            

def print_conn_pic():
    plt.title('CONN Analysis')
    plt.figure(figsize=(20,10))
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'conn'], color='green', label='dcdCONN')
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('count')
    plt.savefig('conn_log.png', dpi=600, format='png')
    plt.clf()


def print_cpu_pic():
    plt.title('CPU Analysis')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'cpu'], color='red', label='dcdCPU')
    
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('percent')
    plt.savefig('cpu_log.png', dpi=600, format='png')
    plt.clf()


def print_mem_pic():
    plt.title('MEM Analysis')
    plt.plot(PIC_VAL_TMP['count'], PIC_VAL_TMP[f'mem'], color='yellow', label='dcdMEM')

    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('percent')
    plt.savefig('mem_log.png', dpi=600, format='png')
    plt.clf()

print_conn_pic()
print_cpu_pic()
print_mem_pic()
