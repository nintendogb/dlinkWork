folder=$(date +"%Y%m%d%H%M")
mkdir ${folder}

scp qateam@54.67.52.204:~/rcd_stats.log ./
python3 ./check_conn.py

mv ./*log* ./${folder}
