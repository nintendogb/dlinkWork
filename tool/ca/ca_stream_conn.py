import asyncio
import websockets
import json
import hashlib
import agent.agent as agent
import time
from datetime import datetime
from agent.log.myLog import MyLog


# Don't show RESTAPI debug
LOGGING = MyLog()
LOGGING.removeAllLogHandler()


def get_ssl_key_password(mydlink_id):
    *************

# -------------------CONFIG----------------------------
MYDLINK_ID = '*************'
MAC = '*************'
ACCOUNT = '*************'
PASSWORD = '*************'
URI = '*************'
SOCKET_URL = "*************"

CLIENT_ID = '*************'
CLIENT_SECRET = '*************'
CA_FILE = "*************"
KEY_FILE = "*************"
CERT_FILE = "*************"
# -------------------CONFIG----------------------------


uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)
uap.get_user_token(ACCOUNT, PASSWORD)
uap.get_device_info([MYDLINK_ID])
d_token = uap.res.json()['data'][0]['device_token']
'''
import pathlib
import ssl
ssl.match_hostname = lambda cert, hostname: True
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE, password=get_ssl_key_password(MYDLINK_ID))
ssl_context.load_verify_locations(CA_FILE)
ssl_context.verify_mode = ssl.CERT_REQUIRED
'''
async def stream_conn():
  async with websockets.connect(
    SOCKET_URL,
    close_timeout=0,
    #ssl=ssl_context,
  ) as websocket:
# sign-in
    command = {
      "command": "sign_in",
      "sequence_id": 28825252,
      "role": "client_agent",
      "owner_id": ACCOUNT,
      "owner_token": uap.user_token,
      "timestamp": int(datetime.now().timestamp()),
    }
    await websocket.send(json.dumps(command))

    resData = await websocket.recv()
    resJson = json.loads(resData)
    print(resJson)
    c_id = resJson["client_id"]
# stream_conn
    command = {
        "command": "conn_init", 
        "sequence_id": 28825252, 
        "device_id": MAC,
        "client_id": c_id,
        "device_token": d_token,
        "timestamp": int(datetime.now().timestamp()),
    }
    await websocket.send(json.dumps(command))

    resData = await websocket.recv()
    resJson = json.loads(resData)
    print(resJson)
    return resJson['relay_info']['host_addr']


sa_url = asyncio.get_event_loop().run_until_complete(stream_conn()) 

print('sa_url: {}'.format(sa_url))
