#!/bin/bash

echo $(date +"%Y/%m/%d %H:%M:%S") >> /home/dlink/qa_dcd.log
echo stats | nc qa-us-dcdca-1.auto.mydlink.com 19001 -w 2 >> /home/dlink/qa_dcd.log
