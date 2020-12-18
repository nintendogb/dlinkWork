#1/bin/bash
wait_start=1
ip=$(aws ec2 describe-instances --region us-west-1 --filter "Name=tag:Name,Values=${1}" | grep PublicIpAddress | awk 'BEGIN {FS="\""}; {print $4}')
until [ $wait_start -gt 15 ]
do
    echo Waiting for instance start, ${wait_start} times
    ssh qateam@${ip} exit
    [ $? -eq 0 ] || break
    (( wait_start++ ))
    sleep 1
done

[ $wait_start -gt 15 ] && exit 1
echo "${1} is runnning" && exit 0
