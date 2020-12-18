import asyncio
import websockets
import json
import hashlib
import time
from datetime import datetime

def get_ssl_key_password(mydlink_id):
    *************

def get_dev_id(mydlink_id):
    return f'AAAAAAAA{int(mydlink_id) - 44453356:04d}'

# -------------------CONFIG----------------------------
MYDLINK_ID = '*************'
# qa env
URI = '*************'
SOCKET_URL = "*************"
CA_FILE = "*************"
KEY_FILE = MYDLINK_ID + ".key"
CERT_FILE = MYDLINK_ID + ".pem"
# -------------------CONFIG----------------------------



import pathlib
import ssl
ssl.match_hostname = lambda cert, hostname: True
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE, password=get_ssl_key_password(MYDLINK_ID))
ssl_context.load_verify_locations(CA_FILE)
ssl_context.verify_mode = ssl.CERT_REQUIRED

async def send_event():
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
      "da_url": "wss://192.168.0.1:8080/SwitchCamera",
      "local_liveview": "wss://192.168.0.1:8088/m3u8",
      "sequence_id": 1569951035, 
      "mainboard_ver": "3.0.0",
      "mydlink_no": MYDLINK_ID
    }
    await websocket.send(json.dumps(command))

    resData = await websocket.recv()
    resJson = json.loads(resData)
    print(resJson)

# send event
    command = {
      "command": "event", 
      "sequence_id": int(datetime.now().timestamp()*1000),
      "timestamp": int(datetime.now().timestamp()*1000),
      "event": {
          "device_id": get_dev_id(MYDLINK_ID),
          "mydlink_no": MYDLINK_ID,
          "timestamp": int(datetime.now().timestamp()*1000000),
          "type": 56,
          "name": "battery",
          "metadata":{"conditions": [{"X": {"status": {"uid": 1,"type": 16, "idx": 0}}, "op": "le", "Y": {"value": 20}, "V": {"value": 8}}]},
          "push_event":1
        }}
    await websocket.send(json.dumps(command))

    resData = await websocket.recv()
    resJson = json.loads(resData)
    print(resJson)



asyncio.get_event_loop().run_until_complete(send_event()) 
