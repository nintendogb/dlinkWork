import redis
import argparse
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
    '-n', 
    '--num', 
    type=int,
    help='dev number to insert to redis'
)
args = parser.parse_args()
print(f'redis url: {args.url}')
print(f'redis port: {args.port}')
print(f'how many dev to insert: {args.num}')


r = redis.Redis(
    host=args.url,
    port=args.port,
    decode_responses=True
)
for insert_dev in range(args.num):
    hex_id = f'{insert_dev:X}'
    key = f'DS:FFFFFFFF{hex_id:0>4}'
    r.hset(key, 'cnvr_state', 1)
    print(f'{key}: cnvr')
    r.hset(key, 'stream_type', 2)
    print(f'{key}: stream')
