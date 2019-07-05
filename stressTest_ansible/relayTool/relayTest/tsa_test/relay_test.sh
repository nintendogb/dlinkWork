#!/bin/sh

if [ ${#} -ne 2 ];then
	echo 'Please input parameter: <device start number> <Relay server IP>'
	exit
fi
MAIN_PREFIX=$PWD

DEV_NUM=$1
RELAY_URL=$2
RELAY_IP=$(nslookup $RELAY_URL | grep Address | awk -F' ' '{print $2}' | grep -v '#')
DID="${DEV_NUM}0"
BID="${DEV_NUM}1"
SERVER_LOG="$MAIN_PREFIX/log/${DID}"
CLIENT_LOG="$MAIN_PREFIX/log/${BID}"


EXE_TIME=''
WGET_LONG_PID=''
WGET_SHORT_PID=''
TSA_DEV_PID=''
TSA_BRO_PID=''
BID_PORT=''
DID_PORT=''



function get_port() {
	BEGAIN_PORT=''
	while [ -z $BEGAIN_PORT ];
	do
		PORT=$(( 1025 + $RANDOM % 65535 ))
		RESULT=$(netstat -lnpt | awk -F' ' '{print $4}'| awk -F':' '{print $2}' | grep $PORT)
		if [ -z "$RESULT" ];then
			BEGAIN_PORT=$PORT
		else
			continue
		fi
	done
	echo $BEGAIN_PORT
}

function NEW_TUNNEL() {
	DID_PORT=$(get_port)
	BID_PORT=$(get_port)

	$MAIN_PREFIX/tsa_dev -l $DID_PORT -d 4 >& $SERVER_LOG &
	TSA_DEV_PID=$!
	sleep 1

	$MAIN_PREFIX/tsa_bro -l $BID_PORT -d 4 >& $CLIENT_LOG &
	TSA_BRO_PID=$!
	sleep 1

	TSA_PORT=''
	while [ -z "$TSA_PORT" ];
	do
		echo "$MAIN_PREFIX/sendcmd $DID_PORT create server $DID $BID 127.0.0.1 127.0.0.1 $RELAY_IP 2047 2048 2175 >& /dev/null "
		$MAIN_PREFIX/sendcmd $DID_PORT create server $DID $BID 127.0.0.1 127.0.0.1 $RELAY_IP 2047 2048 2175 >& /dev/null 
		sleep 5
		echo "$MAIN_PREFIX/sendcmd $BID_PORT create client $BID $DID 127.0.0.1 127.0.0.1 $RELAY_IP 2047 2048 2175 >& /dev/null "
		$MAIN_PREFIX/sendcmd $BID_PORT create client $BID $DID 127.0.0.1 127.0.0.1 $RELAY_IP 2047 2048 2175 >& /dev/null 
		sleep 5
		if [ -e "$CLIENT_LOG" ];then
                        echo "find tsa port"
			TSA_PORT=$(cat $CLIENT_LOG | grep 'Add dest port' | grep '127.0.0.1' | awk -F':' '{print $5}')
                        echo $TSA_PORT
		fi
		#echo "sendcmd : $TSA_PORT"
	done

        PORT=$(echo $TSA_PORT | awk -F' ' '{print $1}')
	#$MAIN_PREFIX/tsa_short.sh $PORT &
	#WGET_SHORT_PID=$!
        echo "before wget"
        date
	wget --continue --timeout=20 --tries=30 -q -O /dev/null http://127.0.0.1:${PORT}/test.dat 
	WGET_LONG_PID=$!
        echo "after get"
        date
        echo $WGET_LONG_PID
}

function TSA_KILL() {
	rm -rf $SERVER_LOG $CLIENT_LOG
	kill -9 $TSA_DEV_PID $TSA_BRO_PID $WGET_SHORT_PID $WGET_LONG_PID >& /dev/null
	EXE_TIME=''
	WGET_LONG_PID=''
	WGET_SHORT_PID=''
}

while [ 1 ];
do
 	FIND_PID=$(ps aux | grep wget |grep -v grep | grep "$WGET_LONG_PID" | awk -F' ' '{print $2}')
#	echo -e "CheckTime : $CHECK_TIME \t WGetPID: $FIND_PID"
	if [ -z "$FIND_PID" ] ;then
		echo "kill tunnel and init"
		TSA_KILL
		NEW_TUNNEL
	fi
	sleep 5
done
