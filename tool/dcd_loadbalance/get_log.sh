source ./host_config.sh
counter=1

for host in "${AWS_HOST[@]}"; do
    echo "$host"
    scp qateam@${host}:/home/qateam/dcd_tester/tester/LB_*.log ./
done
