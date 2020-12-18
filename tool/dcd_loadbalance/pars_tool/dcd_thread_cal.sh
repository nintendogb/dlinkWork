folder=/home/dlink/auto_res/dcd_thread/dcd_thread$(date +"%Y%m%d%H%M")
mkdir -p ${folder}

cp /home/dlink/qa_dcd.log ./
cp /home/dlink/tool/tool/dcd_loadbalance/dcd_tester_docker_20200706/gen_thread_test.py ./log_cfg.py
python3 ./check_stat.py

mv ./*log* ${folder}
