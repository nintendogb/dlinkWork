import base64
import requests
import json
import jwt
from datetime import datetime
start_ts = int(datetime.now().timestamp())
end_ts = start_ts + 300

def get_kid_from_jwt(token):
    base64_message = token[:token.find('.')]
    missing_padding = 4 - len(base64_message) % 4
    if missing_padding:
        missing_equal = '=' * missing_padding
        base64_message = f'{base64_message}{missing_equal}'
    data = eval(base64.b64decode(base64_message))
    return data['kid']



headers = {
    'typ': 'JWT',
    'alg': 'RS256',
    'kid': '1606462396'
}

payload = {
    "iss": "https://appleid.apple.com", # The assertion's issuer
    "sub": "dfjhdjklj", # The unique ID of the partner’s user
    "aud": "90c34f1145f63ab65b328ac2e556946d", # Partner’s client id, assigned by D-Link
    "iat": start_ts,
    "exp": end_ts,
    "name": "Jason_Mraz", # Alias/nickname of the user.
    "email": "jm@mymail.com", # User's email address (keep empty for none)
    "language": "en" # Language of the user (refer to Appendix V)
}


with open('./1606462396.key', 'r') as f:
     private_key = f.read()

print(private_key)

json_web_token = jwt.encode(
    payload,
    private_key,
    algorithm='RS256',
    headers=headers,
)

print(f'JWT = [{json_web_token}]')


res = requests.get('http://54.67.52.204:5000/tool/jwk')
print(json.dumps(res.json(), indent=4))
public_keys = {}
for jwk in res.json()['keys']:
    kid = jwk['kid']
    print(kid)
    public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

'''
with open('./1606462396.key.pub', 'r') as f:
    public_key = f.read()
'''
key = jwt.get_unverified_header(json_web_token)['kid']
# key = get_kid_from_jwt(json_web_token)
public_key = public_keys[key]
payload = jwt.decode(json_web_token, public_key, algorithms=['RS256'], options={'verify_aud': False})
print(payload)
