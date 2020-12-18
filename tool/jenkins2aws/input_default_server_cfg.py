import redis
import argparse
import json
from datetime import datetime

redis_url = '54.67.52.204'
redis_port = 6379

with open('./server_status.cfg') as cfg_file:
    #server_cfg = json.load(json_file)
    server_cfg = eval(cfg_file.read())


r = redis.Redis(
    host=redis_url,
    port=redis_port,
    decode_responses=True
)

for server, condition_cfg in server_cfg.items():
    r.hset('server_status_cfg', server, json.dumps(condition_cfg))



curr_res = r.hgetall('server_status_cfg')
print(f'res: {curr_res}')
