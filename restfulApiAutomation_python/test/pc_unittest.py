#!/usr/bin/python3
import agent.agent as agent
import unittest
import time
import os
import re
import wget
import agent.config.parameter as parameter
from datetime import datetime, timedelta
from agent.log.myLog import MyLog

# Test variable
RES_THRESHOLD = timedelta(seconds=parameter.REQ_THRESHOLD_SECS())

ACCOUNT = 'usmp@test.com'
PASSWORD = '******'
URI = 'mpus.com.us'
MY_DLINK_ID = '111114'
MY_DLINK_ID_2ND = '111115'
SITE = 'usmp'

# Log handle
LOGGING = MyLog()
LOGGING.removeAllLogHandler()

CLIENT_ID = parameter.APP_ID()
CLIENT_SECRET = parameter.APP_SECRET()
DEV_LIST = [MY_DLINK_ID, MY_DLINK_ID_2ND]


class BaseApiTest(unittest.TestCase):
    def setUp(self):
        LOGGING.info('Current testing: {}'.format(self.id().split('.')[-1]))

    def tearDown(self):
        LOGGING.info('End testing: {}'.format(self.id().split('.')[-1]))
        LOGGING.info('')
        LOGGING.info('')

    def assertRes(self, res, res_key, expect_data):
        res_json = res.json()[res_key]
        for data in expect_data:
            if data == 'stat_code':
                self.assertEqual(expect_data[data], res.status_code)
            else:
                self.assertEqual(expect_data[data],  res_json[data])
        self.assertGreater(RES_THRESHOLD, res.elapsed)

class CnvrRelatedTest(BaseApiTest):
    uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)
    uap.get_user_token(ACCOUNT, PASSWORD)
    uap.cnvr_query_subscription()
    try:
        return_data = uap.res.json()['data']
        SUBS_ID = return_data[0]['subs_uid']
        DEV_ID = return_data[0]['devices'][0]
    except (AttributeError, IndexError):
        SUBS_ID = 'Query subcription fail'
        DEV_ID = 'Query subcription fail'

    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=30)
    START_TS = int(start_time.timestamp())
    END_TS = int(end_time.timestamp())
    NO_EVENT = 'No record found for the given information.'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_favorite_behavior(self):
        # Get event to add to favorite
        fav_id_list = []
        event_ts = None
        self.uap.cnvr_list_event(self.START_TS, self.END_TS)
        res_json = self.uap.res.json()['data'][0]['data']
        for event in res_json:
            try:
                if event['act'][0]['mydlink_id'] == self.DEV_ID and \
                   event['act'][0]['subs_uid'] == self.SUBS_ID:
                    event_ts = event['act'][0]['timestamp']
            except (KeyError, IndexError):
                continue

        if event_ts is None:
            return

        # Add event to favorite
        self.uap.cnvr_add_favorite(self.SUBS_ID, self.DEV_ID, event_ts)
        self.assertRes(
            self.uap.res,
            'data',
            {
                'stat_code': 200,
                'result': True,
            },
        )

        # Check favorite event
        self.uap.cnvr_query_favorite_list(start_ts=self.START_TS, end_ts=self.END_TS)
        self.assertRes(
            self.uap.res,
            'data',
            {
                'stat_code': 200,
                'result': True,
            },
        )
        res_json = self.uap.res.json()['data']['list']
        self.assertIsInstance(res_json, (list))
        ts_has_find = False
        for favorite in res_json:
            if int(favorite['timestamp']) == int(event_ts):
                fav_id_list.append(favorite['act'][0]['fav_id'])
                ts_has_find = True
        self.assertTrue(ts_has_find)

        # Remove favorite event
        self.assertRes(
            self.uap.res,
            'data',
            {
                'stat_code': 200,
                'result': True,
            },
        )

        # Check favorite event remove
        self.uap.cnvr_query_favorite_list(start_ts=self.START_TS, end_ts=self.END_TS)
        res_json = self.uap.res.json()['data']['list']
        ts_has_find = False
        for favorite in res_json:
            if int(favorite['timestamp']) == int(event_ts):
                ts_has_find = True
        self.assertFalse(res_json)


class UserRelatedTest(BaseApiTest):
    uap = agent.Uap(URI, CLIENT_ID, CLIENT_SECRET)

    def setUp(self):
        super().setUp()
        self.uap.get_user_token(ACCOUNT, PASSWORD)

    def tearDown(self):
        super().tearDown()

    def test_get_user_info(self):
        self.uap.get_user_info()
        self.assertRes(
            self.uap.res,
            'data',
            {
                'stat_code': 200,
                'email': ACCOUNT,
            },
        )
        res_json = self.uap.res.json()['data']
        self.assertIn('first_name', res_json)

    @unittest.skip("Just skip")
    def test_update_account(self):
        f_name = 'Bruce' + str(int(time.time()))
        l_name = 'Wayne' + str(int(time.time()))
        # Set new name
        self.uap.update_account(ACCOUNT, PASSWORD, f_name, l_name)
        self.assertRes(
            self.uap.res,
            'data',
            {
                'stat_code': 200,
                'first_name': f_name,
                'last_name': l_name,
            },
        )

        # Check if setting successful
        self.uap.get_user_info()
        self.assertRes(
            self.uap.res,
            'data',
            {
                'stat_code': 200,
                'first_name': f_name,
                'last_name': l_name,
            },
        )


if __name__ == '__main__':
    unittest.main()
