#!/bin/bash
ulimit -n 65536
echo "config dir dcd_thread_${1}"
#nohup python3 run_test.py --file_path ./dcd_thread_${1}/keep_alive.json &
#nohup python3 run_test.py --file_path ./dcd_thread_${1}/event.json &
nohup python3 run_test.py --file_path ./dcd_thread_${1}/sign_in.json &
