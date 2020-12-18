source ./host_config.sh


for host in "${AWS_HOST[@]}"; do
    echo "$host"
    ssh qateam@${host} 'mkdir -p ~/dcd_tester'
    rsync -avzh ./tester qateam@${host}:~/dcd_tester
done
