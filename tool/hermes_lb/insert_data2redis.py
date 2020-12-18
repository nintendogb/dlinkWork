import redis


r = redis.Redis(
    host='********************',
    port=6379,
    decode_responses=True
)
for insert_dev in range(88000000, 88003000):
    hex_id = f'{insert_dev:X}'
    key = f'DS:FFFF{insert_dev}'
    r.hset(key, 'cnvr_state', 1)
    print(f'{key}: cnvr')
    r.hset(key, 'stream_type', 2)
    print(f'{key}: stream')
