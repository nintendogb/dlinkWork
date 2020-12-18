folder=/home/dlink/auto_res/dcd/$(date +"%Y%m%d%H%M")
mkdir -p ${folder}


python3 ./check_conn.py
python3 ./check_reconnect.py

mv ./*log* ${folder}
