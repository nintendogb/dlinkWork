import redis
import json
prefix = 'HERMES.STORYBOARD:'
r = redis.Redis(
    host='**********',
    port=6379,
    db=1,
    decode_responses=True
)
index, redis_key = r.scan(
    cursor=0,
    match=f'{prefix}*',
)
print(f'total: {len(redis_key)}')
count = 0
for key in redis_key:
    count += 1
    data = r.hgetall(key)
    for k, v in data.items():
        print(f'{k}: {v}')

print(f'count: {count}')
