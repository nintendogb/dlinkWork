#!/usr/bin/python3
# Parameter for routine log checker
def TEST_DURATION_MINUTES(): return 3
def NOTIF_MAIL_SUB(): return 'Routine Fail Report of Python Client' 
# Parameter for environment
def WORK_DIR(): return '{{WORK_DIR}}'
def LOG_DIR(): return '{{LOG_DIR}}'
def LOGGING_PERIOD(): return '{{LOGGING_PERIOD}}'
def LOG_TIMEOUT_DAYS(): return 31
def LOCAL_TIMEZONE(): return 'Asia/Taipei'
# Parameter for redis setting
def REDIS_PORT(): return 6379
def REDIS_SERVER(): return '127.0.0.1' 
def REDIS_SCAN_AMOUNT(): return 100000
# Parameter for testing environment.
def REQ_THRESHOLD_SECS(): return 40
def APP_ID(): return '****'
def APP_SECRET(): return '****'
def SITE_CFG(): return [
    {
        'account': 'twmp@test.com',
        'password': '******',
        'uri': 'mptw.com.tw',
        'dev1': '111112',
        'dev2': '111113',
        'site': 'twmp'
    },
    {
        'account': 'usmp@test.com',
        'password': '******',
        'uri': 'mpus.com.us',
        'dev1': '111114',
        'dev2': '111115',
        'site': 'usmp'
    },
    {
        'account': 'eump@test.com',
        'password': '******',
        'uri': 'mpeu.com.eu',
        'dev1': '111116',
        'dev2': '111117',
        'site': 'eump'
    },
    {
        'account': 'sgmp@test.com',
        'password': '******',
        'uri': 'mpsg.com.sg',
        'dev1': '111118',
        'dev2': '111119',
        'site': 'sgmp'
    },
    {
        'account': 'cnmp@test.com',
        'password': '******',
        'uri': 'mpcn.net.cn',
        'dev1': '111120',
        'dev2': '111121',
        'site': 'cnmp'
    },
]
# Parameter to send email notif
def NOTIF_LIST(): return [
    'nintendogb@gmail.com',
    'Ted.Kao@dlinkcorp.com',
]
def NOTIF_SENDER_ACCOUNT(): return 'dlinkqateam@gmail.com'
def NOTIF_SENDER_PW(): return '***********'

