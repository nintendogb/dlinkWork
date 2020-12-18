import glob
import json
from authlib.jose import JsonWebKey

def get_timestamp_from_name(key_name):
    start = key_name.rfind('/')
    end = key_name.rfind('.key.pub')
    return key_name[start+1:end]


jwt_key_res = {'keys': []}
pub_key_list = glob.glob('*.key.pub')
for pub_key in pub_key_list:
    with open(pub_key, 'r') as f:
        key = JsonWebKey.import_key(f.read(), {'kty': 'RSA'})
        update_data = {
            'kid': get_timestamp_from_name(pub_key),
            'alg': 'RS256',
            'kty': 'RSA',
            'use': 'sig,'
        }
        key.update(update_data)
        jwt_key_res['keys'].append(key)

print(json.dumps(jwt_key_res, indent=4))
