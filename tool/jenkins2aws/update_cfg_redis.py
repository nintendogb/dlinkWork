import redis
import argparse
import json
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument(
    '-u', 
    '--url', 
    type=str,
    help='url address of redis'
)
parser.add_argument(
    '-p', 
    '--port', 
    type=int,
    help='port of redis'
)
parser.add_argument(
    '-j', 
    '--json', 
    type=str,
    help='cfg of json'
)

args = parser.parse_args()
redis_url = args.url
redis_port = args.port
print(f'redis url: {redis_url}')
print(f'redis port: {redis_port}')
#print(f'json:\n{args.json}')
server_cfg = eval(args.json)


r = redis.Redis(
    host=redis_url,
    port=redis_port,
    decode_responses=True
)

key = 'server_status_cfg'
r.delete(key)
for server, condition_cfg in server_cfg.items():
    r.hset(key, server, json.dumps(condition_cfg))



curr_res = r.hgetall(key)
print(f'res: {curr_res}')
