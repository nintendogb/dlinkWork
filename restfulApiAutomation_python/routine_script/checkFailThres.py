#!/usr/bin/python3
import routineCheck.checker as checker

log_checker = checker.LogExamer()
log_checker.fail_alert(send_email=True)
