""" dcd_base_client.py
"""
import os
import ssl
import json
import copy
import random
import asyncio
from sortedcontainers import  SortedDict
import aiohttp


#===================================================================================================
# pylint: disable=no-member
class DcdBaseClient:
    """ DcdBaseClient
    """
    # one application should have only 1 session.
    _ws_session = None
    _ws_connection_no = 0
    _ssl_context = None
    _conn_semaphore = asyncio.Semaphore(value=1024)

    #===============================================================================================
    def __init__(self):
        self._key_path = ""
        self._cert_path = ""
        self._cipher_list = ""
        self._ssl_password = ""
        self._ws_url = ""
        self._ws_redirect_url = ""
        self._websocket = None
        self._step = SortedDict()     #all steps of this client
        self._ws_recv_redirect = False
        self._delay_connect = None
        self._step_event = asyncio.Event()
        self._round_counter = 1
        self._sign_in_success = False

        #async tasks
        self._ws_keep_alive_tasks = []
        self._ws_execute_step_task = None
        self._ws_recv_message_task = None

    #===============================================================================================
    def _init_device_step(self):
        self._gen_device_step()
        self._fill_device_step()

    #===============================================================================================
    def _fill_device_step(self):
        '''
        it will be override from the derived class
        '''

    #===============================================================================================
    # pylint: disable=fixme
    def _gen_device_step(self):
        '''
        copy steps from self._default_da and self._running_da to self._step
        '''
        #copy default steps from default da into self._step.
        #now self._step has steps copied from default da.
        for k, v in self._default_da.get("step", {}).items():
            default_da_step = copy.deepcopy(v)
            self._step[k] = default_da_step

        # extract steps from running_da and merge them into self._step
        for k, v in self._running_da.get("step", {}).items():
            # k,v is running_da_step
            # k is step_id
            # v is step_content
            #   {
            #      "requst_parameter":{"command":"sign_in"}
            #   }

            running_da_step = copy.deepcopy(v)

            # todo.. parallel step,
            # now only deal with sequencial steps.
            same_command = False
            if k in self._step:
                # running_da.step_id is the same as default_da_step
                if running_da_step.get("request_parameter", {}).get("command", "") ==  \
                     self._step[k].get("request_parameter", {}).get("command", ""):
                    same_command = True
                    #same_command, we should copy running_da_step to self._step
                    for k2, v2 in v.items():
                        #iterate running_step
                        if k2 == "request_parameter":
                            for k3, v3 in v2.items():
                                self._step[k][k2][k3] = v3
                        else:
                            self._step[k][k2] = v2

            if not same_command:
                self._step[k] = running_da_step

    #===============================================================================================
    async def _ws_on_reconnect(self):

        # important. _step_event.wait() to be signaled, so _execute_step() can go on
        # next line.
        self._step_event.set()

        #==
        if self._ws_execute_step_task:
            self._ws_execute_step_task.cancel()

        #==
        if not self._websocket:
            if not self._websocket.closed:
                await self._websocket.close()
            self._websocket = None

        # There is no necessary to send keep_alive tasks,
        # because the connection is clsed.
        # Let's cancel the pending keep_alive tasks.
        if len(self._ws_keep_alive_tasks) > 0:
            #pylint: disable=broad-except,bare-except
            for task in self._ws_keep_alive_tasks:
                try:
                    task.cancel()
                except:
                    pass

        if self._sign_in_success:
            DcdBaseClient._ws_connection_no -= 1
        if self._ws_recv_redirect:
            print(f"[change_url][{self._device_id}] to {self._ws_redirect_url}- \
                {DcdBaseClient._ws_connection_no}")
        else:
            print(f"[disconnect][{self._device_id}] :\
                {DcdBaseClient._ws_connection_no}")

    #===============================================================================================
    # pylint: disable=broad-except
    # pylint: disable=no-else-break
    async def _ws_recv_message(self):

        try:
            if self._websocket:
                async for message in self._websocket:
                    recv = json.loads(message.data)
                    print(f"[recv] {message.data}")
                    try:
                        command = recv.get("command", "")
                        if command == "keep_alive":
                            if recv.get("code", -1) == 0:
                                ws_url = recv.get("dcd_url", None)
                                if ws_url:
                                    # use  redirect url
                                    self._ws_recv_redirect = True
                                    self._ws_redirect_url = ws_url
                                    break
                            else:
                                # This is DA's behavior. DA will reconnect to the DCD server if DA
                                # receives an error code not 0 from the DCD server.
                                break;
                        else:
                            #other command.
                            if command == "sign_in":
                                if recv.get("code", -1) == 0:
                                    self._sign_in_success = True
                                    DcdBaseClient._ws_connection_no += 1
                                    task = asyncio.get_event_loop().create_task(
                                        self._on_keep_alive()
                                    )
                                    self._ws_keep_alive_tasks.append(task)
                                    print(f"[_ws_recv_message][{self._device_id}]\
                                      sign_in succeed:{DcdBaseClient._ws_connection_no}")
                                else:
                                    print(f"[_ws_recv_message][{self._device_id}]\
                                    sign_in failed.")
                                    break

                            self._round_counter -= 1
                            if self._round_counter == 0:
                                self._step_event.set()
                    except Exception as e1:
                        print(f"[excp][_ws_recv_message]{e1}")
                        break

        except Exception as e:
            print(f"[excp][_ws_recv_message]{e}")

        #something wrong in websocket connection or recevice dcd_url from the
        #keep_alive command.
        #do some closing tasks to make sure it can be reconnected again.
        await self._ws_on_reconnect()

    #===============================================================================================
    #pylint:disable=bare-except
    async def _ws_send_str(self, message):
        try:
            if self._websocket and (not self._websocket.closed):
                await self._websocket.send_str(message)
                #print("[send]" + str(message))
        except Exception as e:
            print(f"[excp][_ws_send_str]{e}")

    #===============================================================================================
    #pylint:disable=bare-except
    async def _execute_step(self):
        try:
            #iterate each step
            for v in self._step.values():
                await self._step_event.wait()
                if self._ws_recv_redirect:
                    break
                self._step_event.clear()

                if isinstance(v, list):
                    #parallel command
                    # todo
                    pass
                else:
                    request_parameter = v.get("request_parameter", {})
                    self._add_runtime_field(v.get("request_parameter", {}))

                    #round_no
                    round_no = v.get("round", 1)
                    if round_no < 1:
                        round_no = 1

                    self._round_counter = round_no
                    #pylint: disable=unused-variable
                    for i in range(round_no):
                        if self._ws_recv_redirect:
                            break

                        #--  pre_pause
                        pre_pause = v.get("pre_pause", None)
                        if pre_pause and (isinstance(pre_pause, list)):
                            sleep_time = 0
                            if len(pre_pause) == 1:
                                sleep_time = random.randint(0, pre_pause[0])
                            elif len(pre_pause) == 2:
                                sleep_time = random.randint(pre_pause[0], pre_pause[1])
                            await asyncio.sleep(sleep_time)
                        await  self._ws_send_str(json.dumps(request_parameter))
                if self._ws_recv_redirect:
                    break
        except:
            pass
            #print(f"[excp][_execute_step]{e}")

    #===============================================================================================
    async def _on_keep_alive(self):
        '''
        it will be overriden by the derived class
        '''

    #===============================================================================================
    async def run_client(self):
        '''run_client()
        '''
        acquired = False
        try:
            conn_exception = False
            self._sign_in_success = False

            # according to https://aiohttp.readthedocs.io/
            # one session instance per process.
            if not DcdBaseClient._ws_session:
                conn = aiohttp.TCPConnector(limit=0, limit_per_host=0)
                DcdBaseClient._ws_session = aiohttp.ClientSession(
                    connector=conn
                )

            #--
            if self._ws_recv_redirect:
                ws_url = self._ws_redirect_url
            else:
                ws_url = self._ws_url
            self._ws_recv_redirect = False

            # _delay_connect is initialzed in
            # dcd_agent_device._init_device_essense()
            # pylint: disable=unsubscriptable-object
            if self._delay_connect and isinstance(self._delay_connect, list):
                if len(self._delay_connect) == 1:
                    await asyncio.sleep(
                        random.randint(0, self._delay_connect[0])
                    )
                elif len(self._delay_connect) == 2:
                    await asyncio.sleep(
                        random.randint(
                            self._delay_connect[0],
                            self._delay_connect[1]
                        )
                    )
            #--
            ssl_used = False
            if os.path.exists(self._cert_path) and os.path.exists(self._key_path):
                ssl_used = True

            if ssl_used:
                if not DcdBaseClient._ssl_context:
                    DcdBaseClient._ssl_context = ssl.create_default_context()
                    DcdBaseClient._ssl_context.load_cert_chain(
                        self._cert_path,
                        self._key_path,
                        password=self._ssl_password
                    )

                    if self._cipher_list != "":
                        DcdBaseClient._ssl_context.set_ciphers(self._cipher_list)

            #limit the connection count because it costs too many CPU.
            await DcdBaseClient._conn_semaphore.acquire()
            acquired = True

            self._websocket = await DcdBaseClient._ws_session.ws_connect(
                ws_url,
                heartbeat=None,
                autoping=False,
                ssl=DcdBaseClient._ssl_context,
                timeout=600
            )
        except Exception as excp:
            conn_exception = True
            print(f"[excp][run_client]{excp}, reconnect it later")
        finally:
            if acquired:
                DcdBaseClient._conn_semaphore.release()

        #==
        if not conn_exception:
            #the connection has been established we should do our steps
            self._step_event.set()

            self._ws_execute_step_task = asyncio.get_event_loop().create_task(
                self._execute_step())
            self._ws_recv_message_task = asyncio.get_event_loop().create_task(
                self._ws_recv_message())

            # wait until the connection closed and the step proceedure is exited.
            # copy from
            # https://docs.python.org/3.6/library/asyncio-task.html#asyncio.shield
            if self._ws_execute_step_task:
                try:
                    await self._ws_execute_step_task
                except asyncio.CancelledError:
                    pass
                self._ws_execute_step_task = None

            if len(self._ws_keep_alive_tasks) > 0:
                #pylint: disable=broad-except
                for task in self._ws_keep_alive_tasks:
                    try:
                        await task
                    except:
                        pass
                self._ws_keep_alive_tasks.clear()

            #==
            if self._ws_recv_message_task:
                await self._ws_recv_message_task
                self._ws_recv_message_task = None

            #if the program reaches this line, it means the weboscket  connection is
            # broken. because asyncio functions had been exited.

        # reconnect via async
        asyncio.get_event_loop().create_task(self.run_client())
