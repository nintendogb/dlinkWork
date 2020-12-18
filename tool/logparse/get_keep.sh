patterns="uptime|system|device-conn-online|Device_KEEP" 

function log_dcd_node () {
    echo ${curr_time} >> /home/dlink/keep.log
    echo "DCD-$1" | tee -a /home/dlink/keep.log
    echo stats | nc qa-us-dcdca-$1.auto.mydlink.com 19001 -w 2 | grep -aE ${patterns} | tee -a /home/dlink/keep.log
}


curr_time=$(date +"%Y/%m/%d %H:%M")
log_dcd_node 1
log_dcd_node 2
