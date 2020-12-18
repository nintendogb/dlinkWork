import requests
import re
from datetime import datetime
hermes_num = {
'qa': 2,
'mq': 3
}
log_file = '/home/dlink/hermes_conn.log'
site = 'qa'
curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
for i in range(hermes_num[site]):
    print(f'hermes{i+1}')
    print(curr_time)
    # print(f'http://{site}-us-hermes-{i+1}.auto.mydlink.com:9997/nginx_status')
    response = requests.get(f'****************************')
    
    print(response.text)
    with open(log_file, 'a') as myfile:
        myfile.write(f'hermes{i+1}\n')
        myfile.write(curr_time+'\n')
        myfile.write(response.text)
