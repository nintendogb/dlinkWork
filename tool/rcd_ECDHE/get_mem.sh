#!/bin/bash
echo $(date +"%Y/%m/%d %H:%M") | tee -a ~/mem.log
ansible all -i /home/dlink/tool/tool/rcd_ECDHE/inventory -m shell -a 'free -h' | tee -a ~/mem.log
