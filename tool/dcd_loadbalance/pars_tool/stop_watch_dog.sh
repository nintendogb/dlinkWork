source ./host_config.sh

stop_dcd_watch_dog () {
    ssh tedkao@qa-us-dcdda-${1}.auto.mydlink.com 'sudo systemctl stop dcd_watchdog'
}
stop_dcd_watch_dog 1
stop_dcd_watch_dog 2
stop_dcd_watch_dog 3
stop_dcd_watch_dog 4
