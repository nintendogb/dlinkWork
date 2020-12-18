#! /bin/bash

MYDLINK_ID=${1}
MAC=${2}
POST_LOG=${3}
SAVE_LOC=./$(date +"%Y%m%d%H%M")/

DCD_MESSAGE_LOG='/var/log/mydlink/dcd/message.log'
DCD_ONGKANON_LOG='/var/log/mydlink/dcd/dcd_to_ongkanon.log'
MORPHEUS_LOG='/var/log/mydlink/morpheus/morpheus.log'
MORPHEUS_SUCCESS_LOG='/var/log/mydlink/morpheus/service_success.log'
MORPHEUS_FAIL_LOG='/var/log/mydlink/morpheus/service_fail.log'


mkdir -p ${SAVE_LOC}

echo 'Grep dcd message log'
echo zgrep "\"event\":{\"device_id\":\"${2}\"" ${DCD_MESSAGE_LOG}${POST_LOG}
zgrep "\"event\":{\"device_id\":\"${2}\"" ${DCD_MESSAGE_LOG}${POST_LOG} > ${SAVE_LOC}/dcd_messgae.log

echo 'Grep dcd to ongkanon log'
echo zgrep "{\"device_id\":\"${2}\"," ${DCD_ONGKANON_LOG}${POST_LOG}
zgrep "{\"device_id\":\"${2}\"," ${DCD_ONGKANON_LOG}${POST_LOG} > ${SAVE_LOC}/dcd_ongkanon.log

echo 'Grep morpheus log'
echo zgrep "mydlink_no:${1}" ${MORPHEUS_LOG}${POST_LOG}
zgrep "mydlink_no:${1}" ${MORPHEUS_LOG}${POST_LOG} > ${SAVE_LOC}/morpheus.log

echo 'Grep morpheus service success log'
echo zgrep ",${2}," ${MORPHEUS_SUCCESS_LOG}${POST_LOG}
zgrep ",${2}," ${MORPHEUS_SUCCESS_LOG}${POST_LOG} > ${SAVE_LOC}/morpheus_success.log

echo 'Grep morpheus service fail log'
echo zgrep ",mac:${2}," ${MORPHEUS_FAIL_LOG}${POST_LOG}
zgrep ",mac:${2}," ${MORPHEUS_FAIL_LOG}${POST_LOG} > ${SAVE_LOC}/morpheus_fail.log
