source ./host_config.sh
counter=1

for host in "${AWS_HOST[@]}"; do
    echo "$host"
    ssh qateam@${host} 'rm /home/qateam/dcd_tester/dcd_tester_docker_20200325/LB_*.log'
done

rm ~/keep.log
