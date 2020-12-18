source ./host_config.sh
counter=1

for host in "${AWS_HOST[@]}"; do
    echo "$host"
    scp qateam@${host}:/home/qateam/dcd_tester/dcd_tester_docker_20200408/LB_*.log ./
done

cp ~/keep.log ./
