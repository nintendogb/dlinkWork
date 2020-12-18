source ./host_config.sh
counter=1

for host in "${AWS_HOST[@]}"; do
    echo "$host"

    for i in {1..2}; do
        ssh qateam@${host} "cd ~/dcd_tester/tester;nohup python3 dcd_test.py --file_path lb${counter}.json > ~/lb${counter}.log 2>&1 &"
        echo "ssh qateam@${host} nohup python3 dcd_test.py --file_path lb${counter}.json > ~/lb${counter}.log 2>&1 &"
        counter=$((++counter))
        sleep 5
    done
    sleep 20
done
