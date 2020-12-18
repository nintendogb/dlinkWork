import os

DEV_NUM = 300
EXEC_BIN = 'rcd_test.v20200310'
SCRIPT_LOC = './rcd_ecdhe_test.sh'

def get_mac(id):
    #hex_id = f'{id:X}'
    return f'FFFF{88000000+id}'


with open(SCRIPT_LOC, 'w') as f:
    print('#!/bin/bash', file=f)
    for id in range(DEV_NUM):
        dev_mac = get_mac(id)
        print(f'./{EXEC_BIN} {dev_mac} 15 0 1 0 &', file=f)
        if id % 4:
            print('sleep 1', file=f)

os.chmod(SCRIPT_LOC, 0o777)
