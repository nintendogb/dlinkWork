#!/bin/sh
export AUTO_TEST_SITE="$1"
export AUTO_TEST_TIME="$2"
echo "Testing site is ${AUTO_TEST_SITE}"
echo "START testing"
export PREFIX_2FA_LOG=/log/2fa_${AUTO_TEST_SITE}_${AUTO_TEST_TIME}
if [ -z "$3" ]
then
    echo "nosetests /test/testing_2fa.py 2>&1 | tee -a ${PREFIX_2FA_LOG}_res.log"
    nosetests /test/testing_2fa.py 2>&1 | tee -a ${PREFIX_2FA_LOG}_res.log
else
    echo "nosetests /test/testing_2fa.py 2>&1 | tee -a ${PREFIX_2FA_LOG}_res.log"
    nosetests /test/testing_2fa.py:${3} 2>&1 | tee -a ${PREFIX_2FA_LOG}_res.log
fi
echo "END testing"
