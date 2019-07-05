#!/usr/bin/python3
import routineCheck.checker as checker

log_checker = checker.LogExamer()
log_checker.check_log(send_email=True)
