This is a RESTful api preriodically scan project, and will output fail items of each test on webpage.
This tool runs 2 docker containers continuously
    1. redis docker for store test result
    2. tornado web server docker for get test result
And will start a automation testing container for each mp site in every testing period.
    
All test result will be store in redis for 1 month.
All RESTful api execute detail log will store on web server for 1 month.

Requirement:
    - Python: at least 3.6
    - Docker installed
    - Create user qateam and add it to docker group
    

This tool is not only for automation test use (deploy by jenkins) but also can use to send simple RESRful api (import this package after install) 
    Deploy by using jenkins for automation testing:
        Deploy parameter:
            - WORK_DIR: directory to put runtime related object.
            - LOG_DIR: directory to save routine test result.
            - TEST_INTERVAL: Interval for each test.
            - LOG_CHECK_INTERVAL: Interval for checking log in LOG_DIR.
        Webpage of result:
            - {your server}:5000/log/newest: PASS/FAIL of lastest test.
            - {your server}:5000/log/get-redis-log: History fail item of each test.
            - {your server}:5000/log/fail-count: Statistic of fail item from specific time to now.
            - {your server}:5000/log/download-list: Download link for detailed RESTful api execute log.
    For send RESTful api only:
        Install package by below command or jenkins:
            #> sudo python3 install setup.py
        How to use:
            Import this package first:
                #> import agent.agent as agent
            Initial Uap object:
                #> uap = agent.Uap({{api endpoint}}, {{client_id}}, {{client_secret}})
            Use the cmd, all cmd are in agent/aent.py:
                #> uap.list_device()
            Result of lastest RESTful api will be store in res variable in Uap object(response of python requests), you carn read result like below.
                #> uap.res
        

Test tool setting:
    Environment and test setting are in agent/config/parameter.py, please modify it before (jenkins deploy)/(install python package).
    The most important setting is SITE_CFG:
        It template is like below setting:
            [
                {
                    'account': {{mptw's testing account}},
                    'password': {{mptw's testing password}}},
                    'uri': {{mptw's endpoint}},
                    'dev1': {{mptw's testing dev1}},
                    'dev2': {{mptw's testing dev2}},
                    'site': {{Tag show in the webpage}}
                },
                {
                    'account': {{mpus's testing account}},
                    'password': {{mpus's testing password}}},
                    'uri': {{mpus's endpoint}},
                    'dev1': {{mpus's testing dev1}},
                    'dev2': {{mpus's testing dev2}},
                    'site': {{Tag show in the webpage}}
                },
            ]
        This tool only does automation test for sites in above setting.(Only do automation test for mptw and mpus site.)
        Output webpage only shows test result of sites in above setting, no matter how many sites' data are record the redis.(Only shows mptw and mpus site' result.)



directory structure:
    - agent: Python code for testing RESTful api.
    - jenkins_deploy_script: Script for jenkins deploy use.
    - routineCheck: Python code for log check, save fail item to redis and send notification email.
    - routine_script: Script for preriodical test run/result check.
    - test: Unittest for jenkins deploy
    - webpage: Flask simple webpage to show routine test result.
