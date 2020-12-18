import asyncio
import websockets
import json
import hashlib
import time
import agent.agent as agent
from datetime import datetime
import agent.agent as agent

MYDLINK_ID = '*************'
def get_ssl_key_password(mydlink_id):
    ***************************

# -------------------CONFIG----------------------------
MYDLINK_ID = '*************'
# qa env
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


async def sign_in():
  async with websockets.connect(
    SOCKET_URL,
    close_timeout=0,
  ) as websocket:

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



asyncio.get_event_loop().run_until_complete(sign_in()) 
