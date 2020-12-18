#!/bin/bash
ulimit -n 65536
echo "config dir perf_conf_${1}"
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_keep.json &
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_event.json &
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_get_regular.json &
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_get_policy.json &
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_get_schedule.json &
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_get_server_info.json &
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_recycle_channel.json &
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_sync_info.json &
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_unit_change.json &
nohup python3 run_test.py --file_path ./perf_conf_${1}/perf_start_viewing.json &
