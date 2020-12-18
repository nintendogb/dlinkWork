#!/bin/bash
KEY_NAME=$(date +%s)
ssh-keygen -t rsa -b 4096 -m PEM -f ${KEY_NAME}.key
# Don't add passphrase
openssl rsa -in ${KEY_NAME}.key -pubout -outform PEM -out ${KEY_NAME}.key.pub
cat ${KEY_NAME}.key
cat ${KEY_NAME}.key.pub
