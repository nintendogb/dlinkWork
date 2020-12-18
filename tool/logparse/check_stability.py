import re
import csv
from collections import defaultdict
CONN_THRES = 80000
DCD_NUM = 2
CSV_TMP = defaultdict(dict)
PRE_UPTIME = defaultdict(str)
MIN_SECS = 60
HOUR_SECS = 60 * MIN_SECS
DAY_SECS = 24 * HOUR_SECS
DCD_PATT = re.compile(
    r'(?P<timestamp>\d{4}/\d{2}/\d{2} \d*:\d{2})\n'
    r'(?P<dcd_num>DCD-\d)\n' +
    r'STAT uptime\s*(?P<uptime>.*)\n' +
    r'STAT system\s*\(CPU/MEM\)\s*(?P<cpu>\d*\.\d*)\s*(?P<mem>\d*\.\d*)\n' +
    r'STAT device-conn-online\s*(?P<conn>\d*)\n' +
    r'STAT Device_KEEP_ALIVE.*\n'
)

TIME_PATT = re.compile(r'(?P<days>\d*) days, (?P<hrs>\d*) hours, (?P<mins>\d*) minutes, (?P<secs>\d*) seconds')


def get_cur_uptime(time_str):
    try:
        uptime = TIME_PATT.match(time_str).groupdict()
    except AttributeError:
        return 0

    return int(uptime['days']) * DAY_SECS + int(uptime['hrs']) * HOUR_SECS + int(uptime['mins']) * MIN_SECS + int(uptime['secs'])


with open('./keep.log', 'r') as f:
    log = f.read()
	


dcd_list = [ m.groupdict() for m in DCD_PATT.finditer(log) ]
for dcd_log in dcd_list:
    CSV_TMP[dcd_log['timestamp']][dcd_log['dcd_num']] = {
        'cpu': dcd_log['cpu'],
        'mem': dcd_log['mem'],
        'conn': dcd_log['conn'],
        'uptime': dcd_log['uptime'],
    }

    


with open('log.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    row_name = ['time']
    for i in range(DCD_NUM):
        row_name += [f'DCD{i+1}_CPU', f'DCD{i+1}_MEM', f'DCD{i+1}_conn', f'DCD{i+1}_uptime']
    row_name += ['total_conn']
    writer.writerow(row_name)

    for time, row in CSV_TMP.items():
        tmp_list = [time]
        total = 0
        for i in range(DCD_NUM):
            if f'DCD-{i+1}' in row:
                tmp_list += [
                    row[f'DCD-{i+1}']['cpu'],
                    row[f'DCD-{i+1}']['mem'],
                    row[f'DCD-{i+1}']['conn'],
                    row[f'DCD-{i+1}']['uptime'],
                ]
                total += int(row[f'DCD-{i+1}']['conn'])
                cur_uptime = get_cur_uptime(row[f'DCD-{i+1}']['uptime'])
                pre_uptime = get_cur_uptime(PRE_UPTIME[f'DCD-{i+1}'])
                if pre_uptime >= cur_uptime:
                    print(f'[{time}] DCD-{i+1} has restart. pre_uptime: ({PRE_UPTIME[f"DCD-{i+1}"]}) -> cur_uptime: ({row[f"DCD-{i+1}"]["uptime"]})')
                PRE_UPTIME[f'DCD-{i+1}'] = row[f'DCD-{i+1}']['uptime']
                
            else:
                tmp_list += ['Not Exist'] * 4
        if total < CONN_THRES:
            print(f'[{time}] Conn less than thres({CONN_THRES}). Curr conn is ({total})')
        tmp_list += [total]
        writer.writerow(tmp_list)

