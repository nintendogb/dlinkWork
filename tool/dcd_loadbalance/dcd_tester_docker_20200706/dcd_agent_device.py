""" dcd_agent_device.py
"""
import uuid
import hashlib
import os
import json
import time
import copy
import asyncio
import agent_device_preset
from dcd_base_client import DcdBaseClient


#===================================================================================================
def get_ssl_key_password(mydlink_id):
    """get_ssl_key_password()
    """
    rev_mydlink_num = mydlink_id[::-1]
    key = rev_mydlink_num + 'Kb2g7X9u'
    mid = hashlib.md5(key.encode()).hexdigest()
    return hashlib.md5(mid.encode()).hexdigest()

#===================================================================================================
class DcdAgentDevice(DcdBaseClient):
    """DcdAgentDevice
    this class is to simulate a device, like camera, plug..etc
    """

    #===============================================================================================
    def __init__(self, mydlink_no, running_da, default_da, site_prefix):
        super().__init__()
        self._running_da = running_da
        self._default_da = default_da
        self._mydlink_no = mydlink_no
        self._site_prefix = site_prefix
        self._init_device_essense_from_default_da()
        self._init_device_essense()
        self._init_device_step()
        del self._running_da
        del self._default_da

    #===============================================================================================
    def _fill_device_step(self):
        '''
        copy stpes data form agent_device_preset.py to self._step
        '''
        for v in self._step.values():
            #iterate all steps from the config file.

            #--
            #fill defaulit parameter from agent_device_preset.py
            command_name = v["request_parameter"].get("command", None)
            if command_name:
                command_preset = agent_device_preset.REQUEST_PARAMETER.get(
                    command_name, None)
                if command_preset:
                    for k2, v2 in command_preset.items():
                        if k2 not in v["request_parameter"]:
                            v["request_parameter"][k2] = copy.deepcopy(v2)

            #fill common parameters
            v["request_parameter"]["device_id"] = self._device_id
            v["request_parameter"]["role"] = "device_agent"

            #parameters of specific commands
            if command_name == "sign_in":
                v["request_parameter"]["mydlink_no"] = self._mydlink_no



    #==============================================================================================
    def _init_device_essense_from_default_da(self):
        """
        """
        for k, v in self._default_da.items():
            if k == "step":
                # this will be handled by DcdBaseClient::_gen_device_step()
                continue
            if k not in self._running_da:
                self._running_da[k] = copy.deepcopy(v)

    #===============================================================================================
    def _init_device_essense(self):
        #--
        _device_id = self._running_da.get("device_id", None)
        _mac_prefix = self._running_da.get("mac_prefix", None)

        if _device_id:
            self._device_id = _device_id
        else:
            if _mac_prefix:
                self._device_id = f"{_mac_prefix}{self._mydlink_no}"
            else:
                self._device_id = f"FFFF{self._mydlink_no}"

        #--
        self._ssl_password = get_ssl_key_password(self._mydlink_no)

        #--
        _key_path = self._running_da.get("key_path", None)
        if _key_path:
            if os.path.exists(_key_path):
                self._key_path = _key_path
            else:
                self._key_path = os.path.join(os.getcwd(), _key_path)
        else:
            self._key_path = os.path.join(os.getcwd(), self._mydlink_no + ".key")

        #--
        _cert_path = self._running_da.get("cert_path", None)

        if _cert_path:
            if os.path.exists(_cert_path):
                self._cert_path = _cert_path
            else:
                self._cert_path = os.path.join(os.getcwd(), _cert_path)
        else:
            self._cert_path = os.path.join(os.getcwd(), self._mydlink_no + ".pem")

        #--
        self._cipher_list = self._running_da.get("cipher_list", "")

        #--
        self._delay_connect = self._running_da.get("delay_connect", None)

        #--
        self._ws_url = "wss://" + self._site_prefix
            #"-dcdda-1.auto.mydlink.com:443/SwitchCamera"

    #===============================================================================================
    # pylint: disable=no-self-use
    def _add_runtime_field(self, request_parameter):

        # all commands need these field
        request_parameter["sequence_id"] = int(time.time())

        # specific commands treatment
        command = request_parameter.get("command", {})

        #Commands need timestamp
        if command in ("sync_info", "start_viewing", "get_server_info", "event"):
            request_parameter["timestamp"] = int(time.time())

        #--
        if command == "sign_in":
            request_parameter["mydlink_no"] = self._mydlink_no
        elif command == "event":
            request_parameter["timestamp"] = int(time.time())
            #--
            if (not "event" in request_parameter) or \
               (not isinstance(request_parameter["event"], dict)):
                request_parameter["event"] = {}
            request_parameter["event"]["timestamp"] = int(time.time() * 1000000)
            request_parameter["event"]["device_id"] = self._device_id
            request_parameter["event"]["mydlink_no"] = self._mydlink_no

            # metadata might be a dict(policy condition hit) or an array(unit data change).
            # If it's a dict, we add seesion_id
            if (not "metadata" in request_parameter["event"]):
                request_parameter["event"]["metadata"] = {}
            if isinstance(request_parameter["event"]["metadata"], dict):
                request_parameter["event"]["metadata"]["session_id"] = uuid.uuid4().hex

    #===============================================================================================
    async def _on_keep_alive(self):
        '''
        send the keep_alive command to the DCD server
        '''
        command = copy.deepcopy(agent_device_preset.REQUEST_PARAMETER.get(
            "keep_alive", {}))
        command["command"] = "keep_alive"
        command["device_id"] = self._device_id
        command["sequence_id"] = int(time.time())
        command["opt_redirect"] = 1

        await asyncio.sleep(55)
        task = asyncio.get_event_loop().create_task(self._on_keep_alive())

        # Save this task in advanced to prevent from that if hanging of below codes,
        # we can cancel this task immediately later.
        self._ws_keep_alive_tasks.append(task)

        # send this message
        await self._ws_send_str(json.dumps(command))

        if len(self._ws_keep_alive_tasks) > 0:
            #pylint:disable=bare-except,broad-except
            try:
                # This task is going to be finished, we pop out the task we put earlier.
                self._ws_keep_alive_tasks.remove(asyncio.Task.current_task())
            except Exception:
                pass
