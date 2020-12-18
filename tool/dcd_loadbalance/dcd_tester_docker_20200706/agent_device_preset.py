''' constant values for some commands.
  If some values are always constant, you'll wanna add these values to the
  description file. Then you can add these values here.
'''

REQUEST_PARAMETER = {
    "sign_in":{
        "role":"device_agent",
        "da_url":"wss://192.168.0.106:8080/SwitchCamera",
        "local_liveview":"http://192.168.0.106:8088/live.m3u8",
        "camera_func":1,
        "policy_version":"",
        "schedule_version":"",
        "regular_version":"",
        "mainboard_ver":"3.3.4-b04",
        "time_zone":"CST-8",
        "gmt_offset":28800,
        "api_version":1,
        "capability":0,
        "firmware_ver":"v1.06.00",
        "hardware_ver":"A1"
    },
    "get_policy":{
        "version":""
    },
    "get_regular":{
        "version":""
    },
    "get_schedule":{
        "version":""
    }
}
