#!/bin/bash

echo $(date +"%Y/%m/%d %H:%M:%S") >> /home/dlink/mp_dcd.log
echo stats | nc mp-us-dcdca-2.auto.mydlink.com 19001 -w 2 >> /home/dlink/mp_dcd.log
