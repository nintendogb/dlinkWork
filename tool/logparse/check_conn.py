import re
import csv
from collections import defaultdict
DCD_NUM = 3
CSV_TMP = defaultdict(dict)

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
            else:
                tmp_list += ['Not Exist'] * 3
        tmp_list += [total]
        writer.writerow(tmp_list)

