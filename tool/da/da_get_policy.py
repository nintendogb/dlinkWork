import asyncio
import websockets
import json
import hashlib
import agent.agent as agent
import time
from datetime import datetime

def get_ssl_key_password(mydlink_id):
    *************

def get_dev_id(mydlink_id):
    return f'AAAAAAAA{int(mydlink_id) - 44453356:04d}'

# -------------------CONFIG----------------------------
MYDLINK_ID = '*************'
ACCOUNT = '*************'
PASSWORD = '*************'
URI = '*************'
SOCKET_URL = "*************"
CLIENT_ID = '*************'
CLIENT_SECRET = '*************'
CA_FILE = "*************"
KEY_FILE = MYDLINK_ID + ".key"
CERT_FILE = MYDLINK_ID + ".pem"
# -------------------CONFIG----------------------------


uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)
uap.get_user_token(ACCOUNT, PASSWORD)

import pathlib
import ssl
ssl.match_hostname = lambda cert, hostname: True
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE, password=get_ssl_key_password(MYDLINK_ID))
ssl_context.load_verify_locations(CA_FILE)
ssl_context.verify_mode = ssl.CERT_REQUIRED

async def get_policy():
  async with websockets.connect(
    SOCKET_URL,
    close_timeout=0,
    ssl=ssl_context,
  ) as websocket:
# sign-in
    command = {
      "command": "sign_in",
      "role": "device_agent",
      "device_id": get_dev_id(MYDLINK_ID),
      "owner_id": ACCOUNT,
      "owner_token": uap.user_token,
      "da_url": "wss://192.168.0.1:8080",
      "local_liveview": "wss://192.168.0.1:8088/m3u8",
      "sequence_id": 28825252, 
      "mainboard_ver": "3.0.0",
      "mydlink_no": MYDLINK_ID,
    }
    await websocket.send(json.dumps(command))

    resData = await websocket.recv()
    print(resData)
    resJson = json.loads(resData)
    print(resJson)

# get policy
    command = {
      "command": "get_policy", 
      "role": "device_agent",
      "sequence_id": 28825252, 
      "version": "",
    }
    await websocket.send(json.dumps(command))

    resData = await websocket.recv()
    print(resData)
    resJson = json.loads(resData)
    print(resJson)



asyncio.get_event_loop().run_until_complete(get_policy()) 
