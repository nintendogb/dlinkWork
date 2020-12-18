import re
import sre_yield

expect_list = list(sre_yield.AllStrings('FFFF8800000[0-9]'))

with open('./dcd.log', 'r') as f:
    log = f.read()
	
sign_in_pattern = re.compile(r'\[dcd_da.c/1023/dcd_recv_da_sign_in\(\)\] - Notice: Device\[([F]{4}[\d]{8})\]')
real_sign_in_list = sign_in_pattern.findall(log)
print(f'Expected sign-in dev:\n{expect_list}')
print(f'Actual sign-in dev:\n{real_sign_in_list}')



for dev in expect_list:
    if dev not in real_sign_in_list:
        print(f'dev [{dev}] sign-in failed')
