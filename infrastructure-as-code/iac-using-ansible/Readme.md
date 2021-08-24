Hardening using Ansible
========================

Learn how to use Ansible to harden a production environment
------------------------------------------------

In this scenario, you will learn how to install and run Ansible on a remote machine.

You will need to install the Ansible and then finally run the Ansible ad-hoc and playbook commands on the remote machine.

Install Ansible and Ansible Lint
--------------------------------

> Ansible uses simple English like language to automate configurations, settings, and deployments in traditional and cloud environments. It’s easy to learn and can be understood by even non-technical folks.
> 
> Source: [Ansible official website.](https://www.ansible.com/)

This exercise uses two machines, the DevSecOps Box with hostname as devsecops-box-XqiHnDZ0, and a production machine, prod-XqiHnDZ0.

We will do all the exercises locally first in DevSecOps-Box, so let’s start the activity.

First, we need to install the ansible and ansible-lint programs.

```
pip3 install ansible==2.10.4 ansible-lint==4.3.7
```

Create the inventory file
----------

Let’s create the inventory or CMDB file for Ansible using the following command.

```
cat > inventory.ini <<EOL

# DevSecOps Studio Inventory
[devsecops]
devsecops-box-XqiHnDZ0

[prod]
prod-XqiHnDZ0

EOL
```

> Please ignore the machine id in Command Output, it should be the same as your machine ID.

Next, we will have to ensure the SSH’s yes/no prompt is not shown while running the ansible commands, so we will be using ssh-keyscan to capture the key signatures beforehand.

```
ssh-keyscan -t rsa prod-XqiHnDZ0 >> ~/.ssh/known_hosts
```
output
```
# prod-XqiHnDZ0:22 SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
```
Let’s do this for the rest of the systems in the lab as well.
```
ssh-keyscan -t rsa devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
```
output
```
# devsecops-box-XqiHnDZ0:22 SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
```
> Pro-tip: Instead of running the ssh-keyscan command twice, we can achieve the same using the below command.

```
ssh-keyscan -t rsa prod-XqiHnDZ0 devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
```

Run the ansible commands
----------

Let’s run the ansible ad-hoc command to check the production machine’s uptime, install the ntp service, and check the bash version of all systems.

Let’s use the shell module of ansible to run the uptime command on the production machine.

```
ansible -i inventory.ini prod -m shell -a "uptime"
```
output
```
prod-XqiHnDZ0 | CHANGED | rc=0 >>
 04:11:19 up 26 min,  1 user,  load average: 0.75, 0.94, 0.88
```

Similarly, we can use apt ansible module to install the ntp service on the production machine.

```
ansible -i inventory.ini prod -m apt -a "name=ntp state=present"
```

Instead of restricting the commands to the prod machine, let’s find the bash version installed on all the machines in the inventory file.
```
ansible -i inventory.ini all -m command -a "bash --version"
```

Nice, we can see the bash version of the prod and devsecops-box GNU bash, version 4.4.20(1)-release (x86_64-pc-linux-gnu).

Exercise: Ansible Ad-hoc commands
----------------------------------

In this exercise, we will use Ansible ad-hoc command to find the uptime of our lab machines.

1. Use inventory file (-i inventory.ini) and the following command to find the uptime
2. Use the Ansible command module to find uptime

> How is this helpful in real-world situations? We can find uptime of all of your production machine fleet of 500 machines within 5 minutes.
> 
> Please try to do this exercise without looking at the solution on the next page.

Run the Ansible playbook
----------
Let’s create a playbook to run against the production environment.

```
cat > playbook.yml <<EOL
---
- name: Example playbook to install nginx
  hosts: prod
  remote_user: root
  become: yes
  gather_facts: no
  vars:
    state: present

  tasks:
  - name: ensure Nginx is at the latest version
    apt:
      name: nginx

EOL
```

Let’s run this playbook against the prod machine.

```
ansible-playbook -i inventory.ini playbook.yml
```
output
```
PLAY [Example playbook to install nginx] ******************************************

TASK [ensure Nginx is at the latest version] ***********************************************************************************
ok: [prod-qopqfmfu]

PLAY RECAP ************************************************************************
prod-qopqfmfu             : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
Try running the above ansible command once again.

```
ansible-playbook -i inventory.ini playbook.yml
```
output
```
PLAY [Example playbook to install nginx] ******************************************

TASK [ensure Nginx is at the latest version] ***********************************************************************************
ok: [prod-qopqfmfu]

PLAY RECAP ************************************************************************
prod-qopqfmfu             : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
> Did you notice the changed=0? What is its importance from a security perspective?

Exercise: Create playbook with roles from ansible-galaxy
---------

In this exercise, we will create a playbook using roles available on Ansible Galaxy and run it on the inventory group, devsecops

1. Create a new directory exercise-7.1 and create a file in it called playbook.yml
2. Download secfigo.terraform role using ansible-galaxy
3. Execute the playbook to install the Terraform utility using ansible-playbook command

> Please try to do this exercise without looking at the solution on the next page.

Download roles from Ansible Galaxy
--------------
Ansible galaxy helps you in storing open source Ansible roles.

Let’s explore the options it provides us.

```
ansible-galaxy role --help
```
We can search for desired roles using the search option.
```
ansible-galaxy install secfigo.terraform
```
> Notice, the role was installed under /root/.ansible/roles/secfigo.terraform directory?

Let’s create a directory and playbook to install the terraform on the production machine.

```
mkdir exercise-7.1 && cd exercise-7.1
mv ../inventory.ini .

cat > playbook.yml <<EOL
---
- name: Example playbook to install Terraform using ansible role.
  hosts: prod
  remote_user: root
  become: yes

  roles:
    - secfigo.terraform
EOL
```
Let’s run this playbook against the prod machine to install the Terraform utility.

```
ansible-playbook -i inventory.ini playbook.yml
```

Harden the production environment
----------

> Dev-Sec Project has lots of good examples on how to create Ansible roles and uses lots of best practices which we can use as a baseline in our roles.
>
> For example, https://github.com/dev-sec/ansible-os-hardening.

Exercise: Using Ansible to Harden prod server
---------
In this exercise, we will create a new playbook that uses dev-sec.os-hardening role available from Ansible galaxy to harden the prod environment.

1. Create a new directory hardening and create a file in it called ansible-hardening.yml
2. Download dev-sec.os-hardening role from ansible-galaxy
3. Execute the playbook to harden the Ubuntu production machine
4. Optionally put this hardening job in the CI pipeline (please refer to Exercise 6.0 for some inspiration)


> Trivia: Which stage should this job run in? and against which machines?
>
> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

