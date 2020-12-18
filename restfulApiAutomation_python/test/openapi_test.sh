#!/bin/sh
export AUTO_TEST_SITE="$1"
export AUTO_TEST_ACCOUNT="$2"
export AUTO_TEST_PASSWORD="$3"
export AUTO_TEST_DEV="$4"
export AUTO_TEST_TIME="$5"
echo "Testing site is ${AUTO_TEST_SITE}"
echo "Testing Account is ${AUTO_TEST_ACCOUNT}"
echo "Test account's password is ${AUTO_TEST_PASSWORD}"
echo "Testing dev is ${AUTO_TEST_DEV}"
echo "START testing"
RES_LOG=/log/${AUTO_TEST_SITE}_res_${AUTO_TEST_TIME}.log
python3 /test/bind_1_dev.py
if [ -z "$6" ]
then
    nosetests /test/openapi_test.py 2>&1 | tee -a ${RES_LOG}
else
    nosetests /test/openapi_test.py:${6} 2>&1 | tee -a ${RES_LOG}
fi
echo "END testing"
