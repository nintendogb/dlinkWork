To use this ansible playbook to run relay server stress test, you need to use 'SQAD_Ubuntu1804' images in our team's AWS AMIs.

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
Ansible will show a prompt to ask your login password(decrypt and store in memory only).



Setting:
Please modify invetory, below is example.
[server:vars]
ansible_python_interpreter=/usr/bin/python3            # Using python3 on client node for ansible
ansible_ssh_common_args='-o StrictHostKeyChecking=no'  # Bypass ssh host key checking in Ansible
number_of_relay_process=24                             # Number of testing docker containers in each client node. 

[server]
13.56.78.33 ansible_user=qateam                        # Each line represent a client node, just modify the ip address.
54.183.137.31 ansible_user=qateam
54.215.211.98 ansible_user=qateam


How to use:

If your client haven't get the testing docker images or you have modify the testing tools, you need to use below playbook(Only once).
> ansible-playbook -i inventory make_env.yml


Run relay stress test.
> ansible-playbook -i inventory start_test.yml --extra-vars "relay_url={{relay server URL}}"

Check if docker containers start correctly, make sure return number of each client node is same as number_of_relay_process
> ansible all -i inventory -m command -a 'docker ps -a -f name=relay_test*'

Stop relay stress test.
> ansible-playbook -i inventory stop_test.yml 
