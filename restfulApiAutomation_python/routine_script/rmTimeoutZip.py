#!/usr/bin/python3
from datetime import datetime
from datetime import timedelta
import glob
import os
import agent.config.parameter as parameter
zip_list = [
    f for f in glob.glob(
        '/webpage/static/testLog/*.zip'
    )
]
for zip_loc in zip_list:
    zipName = zip_loc.split('/')[-1]
    zip_ts = int(zipName.split('.')[0])
    zip_time = datetime.fromtimestamp(zip_ts)
    if datetime.now() > (zip_time + timedelta(days=parameter.LOG_TIMEOUT_DAYS())):
        os.remove(zip_loc)
