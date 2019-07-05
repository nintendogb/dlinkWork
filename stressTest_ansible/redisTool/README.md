To use this ansible playbook to run redis server stress test, you need to use 'SQAD_Ubuntu1804' images in our team's AWS AMIs.

Management node: Node that runs ansible
Client node: Node that controled by ansible


SQAD_Ubuntu1804's setting:
  - base on ubuntu 18.04
  - ssh connection is opend
  - python3 installed
  - docker-ce installed
  - create qateam user:
    - add qateam user to /etc/sudoers (No password for sudo)
    - add qateam user to docker group (No password to using docker)
    - add ssh id_rsa.pub of management node (No passwor forlinux ssh log-in, Optional you can also log-in with password)


If you didn't push id_rsa.pub to client node, add flag '--ask-vault-pass' to ansible command.
Ansible will show a prompt to ask your login password(decrypt and in memory only).



Setting:
Please modify invetory, below is example.
[server:vars]
ansible_python_interpreter=/usr/bin/python3            # Using python3 on client node for ansible
ansible_ssh_common_args='-o StrictHostKeyChecking=no'  # Bypass ssh host key checking in Ansible

[server]
13.56.78.33 ansible_user=qateam                        # Each line represent a client node, just modify the ip address.
54.183.137.31 ansible_user=qateam


How to use:



Run redis stress test.
> ansible-playbook -i inventory playbook_scp.yml --extra-vars "redis_url={{redis server URL}}"


Stop relay stress test, just ctrl-c after you start the test.

Important: If your management host's cpu core is less than amount of client node, ansible will be stuck.
           I will package testing tool to docker image latter to avoid it, but now 2 client node can make our tesing amount.

Command below is the maximum stress rate for 1 client node.
python ~/toolRedis/redisTool.py -t stress -c 1000000 -o 0 -m 50 -s {{redis_url}} -d 60


How to use redisTool.py seperately:
Usage: redisTool.py [OPTIONS]

Options:
  -t, --type [hset|hgetall|hdel|stress|hget|getSpeed|clearSpeed]  To send this cmd repeatedly. Except stress, getSpeed,clearSpeed。[required]
										 
  -c, --count INTEGER             How many cmd in a period  [required]
  -d, --period INTEGER            How long is a period [default: 300]
  -s, --site TEXT                 Redis' url  [default: 10.205.91.11]
  -p, --port INTEGER              Redis' port [default: 6379]
  -o, --onlyonce INTEGER          Only run once 1: True, 0: False[default: 0]
  -m, --multiple INTEGER          How many process to run[default: 1]
  --help                          Show this message and exit.

special argument:
  - stress: For stress test use, send hset to write random value and using hget to check. 
  - getSpeed: Get average test speed for latest test(store in redis).
  - clearSpeed: Clear log of test speed(store in redis).


