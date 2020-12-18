""" The description file manipulator.
"""

import asyncio
import sys
import sre_yield
import dcd_agent_device

#===================================================================================================
class TestDescription:
    """ The description file manipulator.
    this class masps to a structure of the test-description file
    """
    #===============================================================================================
    def __init__(self, in_description=None):
        # initialze member data
        if not in_description:
            self._in_description = {}
        else:
            self._in_description = in_description #original description from file.
        self._da = []        #total DAs after parse   extract , dcd_device object
        self._selected_case = {}              #selected from the description file

    #===============================================================================================
    def _find_selected_case(self):
        """
        assign the selected case to self._selected_case
        """

        #==
        if self._in_description.get("selected", None):
            if self._in_description["selected"] in self._in_description:
                #there is a "selected" field, lets save it.
                self._selected_case = self._in_description.get(
                    self._in_description["selected"], {})
            else:
                print("[error] target selcted case object is not existed.")
        else:
            if len(self._in_description) == 1:
                #only one case, run it directly.
                self._selected_case = next(iter(self._in_description.values()))
            else:
                print("[error] don't know which case to run")

        if bool(self._selected_case):
            pass
        else:
            print("[error] no selected_case")
        print("[selected_case]" + str(self._selected_case))

    #===============================================================================================
    def _gen_running_da(self):
        '''
        generate running_da from the description and store them in self._da
        '''
        conf_das = self._selected_case.get("da", {})
        default_da = conf_das.get("default", None)

        for k, v in conf_das.items():
            if k not in ('default', 'delay_connect'):
                if '_' in k:
                    start_at, total_count = [ int(i) for i in k.split('_') ]
                    da_ids = [ str(start_at + ids) for ids in range(total_count) ]
                else:
                    da_ids = list(sre_yield.AllStrings(k))
                for v2 in da_ids:
                    da = dcd_agent_device.DcdAgentDevice(
                        v2,           #mydlink_no
                        v,            #running da
                        default_da,   #default da
                        self._selected_case.get("site_prefix", "")
                        )
                    self._da.append(da)
        print("[TOTAL_DA] " + str(len(self._da)))

    #===============================================================================================
    def _run_sim(self):
        '''_run_sim
        '''
        loop = None
        if sys.platform == "win32":
            loop = asyncio.ProactorEventLoop()
        else:
            loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)

        #==
        futures = [_da.run_client() for _da in self._da]
        loop.run_until_complete(asyncio.gather(*futures))
        loop.run_forever()
        loop.close()

    #===============================================================================================
    def run(self):
        """ run
        """
        #==
        self._find_selected_case()

        #==
        self._gen_running_da()

        #===
        self._run_sim()
