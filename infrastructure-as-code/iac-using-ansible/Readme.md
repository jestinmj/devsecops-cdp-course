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

This exercise uses two machines, the DevSecOps Box with hostname as devsecops-box-p30jrhut, and a production machine, prod-p30jrhut.

We will do all the exercises locally first in DevSecOps-Box, so let’s start the activity.

First, we need to install the ansible and ansible-lint programs.

```
pip3 install ansible==8.7.0 ansible-lint==6.8.1
```

Create the inventory file
----------

Let’s create the inventory or CMDB file for Ansible using the following command.

```
cat > inventory.ini <<EOL

# DevSecOps Studio Inventory
[devsecops]
devsecops-box-p30jrhut

[prod]
prod-p30jrhut

EOL
```

> Please ignore the machine id in Command Output, it should be the same as your machine ID.

Next, we will have to ensure the SSH’s yes/no prompt is not shown while running the ansible commands, so we will be using ssh-keyscan to capture the key signatures beforehand.

```
ssh-keyscan -H prod-p30jrhut >> ~/.ssh/known_hosts
```
output
```
# prod-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
# prod-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
# prod-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
# prod-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
# prod-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
```
Let’s do this for the rest of the systems in the lab as well.
```
ssh-keyscan -H devsecops-box-p30jrhut >> ~/.ssh/known_hosts
```
output
```
# devsecops-box-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
# devsecops-box-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
# devsecops-box-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
# devsecops-box-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
# devsecops-box-p30jrhut:22 SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10
```
> Pro-tip: Instead of running the ssh-keyscan command twice, we can achieve the same using the below command.

```
ssh-keyscan -H prod-p30jrhut devsecops-box-p30jrhut >> ~/.ssh/known_hosts
```

Run the ansible commands
----------

Let’s run the ansible ad-hoc command to install the ntp service, and check the bash version of all systems.

We can use apt ansible module to install the ntp service on the production machine.

```
ansible -i inventory.ini prod -m apt -a "name=ntp state=present"
```
output
```
prod-p30jrhut | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "cache_update_time": 1599221362,
    "cache_updated": false,
    "changed": true,
    "stderr": "debconf: delaying package configuration, since apt-utils is not installed\n",
    "stderr_lines": [
        "debconf: delaying package configuration, since apt-utils is not installed"
    ],
    "stdout": "Reading package lists...\nBuilding dependency tree...\nReading state information...\nThe following additional packages will be installed:\n  libopts25 netbase sntp tzdata\nSuggested packages:\n  ntp-doc\nThe following NEW packages will be installed:\n  libopts25 netbase ntp sntp tzdata\n0 upgraded, 5 newly installed, 0 to remove and 5 not upgraded.\nNeed to get 987 kB of archives.\nAfter this operation, 5547 kB of additional disk space will be used.\nGet:1 http://archive.ubuntu.com/ubuntu bionic/main amd64 netbase all 5.4 [12.7 kB]\nGet:2 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 tzdata all 2020a-0ubuntu0.18.04 [190 kB]\nGet:3 http://archive.ubuntu.com/ubuntu bionic/universe amd64 libopts25 amd64 1:5.18.12-4 [58.2 kB]\nGet:4 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 ntp amd64 1:4.2.8p10+dfsg-5ubuntu7.2 [640 kB]\nGet:5 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 sntp amd64 1:4.2.8p10+dfsg-5ubuntu7.2 [86.5 kB]\nFetched 987 kB in 1s (1735 kB/s)\nSelecting previously unselected package netbase.\r\n(Reading database ... \r(Reading database ... 5%\r(Reading database ... 10%\r(Reading database ... 15%\r(Reading database ... 20%\r(Reading database ... 25%\r(Reading database ... 30%\r(Reading database ... 35%\r(Reading database ... 40%\r(Reading database ... 45%\r(Reading database ... 50%\r(Reading database ... 55%\r(Reading database ... 60%\r(Reading database ... 65%\r(Reading database ... 70%\r(Reading database ... 75%\r(Reading database ... 80%\r(Reading database ... 85%\r(Reading database ... 90%\r(Reading database ... 95%\r(Reading database ... 100%\r(Reading database ... 10881 files and directories currently installed.)\r\nPreparing to unpack .../archives/netbase_5.4_all.deb ...\r\nUnpacking netbase (5.4) ...\r\nSelecting previously unselected package tzdata.\r\nPreparing to unpack .../tzdata_2020a-0ubuntu0.18.04_all.deb ...\r\nUnpacking tzdata (2020a-0ubuntu0.18.04) ...\r\nSelecting previously unselected package libopts25:amd64.\r\nPreparing to unpack .../libopts25_1%3a5.18.12-4_amd64.deb ...\r\nUnpacking libopts25:amd64 (1:5.18.12-4) ...\r\nSelecting previously unselected package ntp.\r\nPreparing to unpack .../ntp_1%3a4.2.8p10+dfsg-5ubuntu7.2_amd64.deb ...\r\nUnpacking ntp (1:4.2.8p10+dfsg-5ubuntu7.2) ...\r\nSelecting previously unselected package sntp.\r\nPreparing to unpack .../sntp_1%3a4.2.8p10+dfsg-5ubuntu7.2_amd64.deb ...\r\nUnpacking sntp (1:4.2.8p10+dfsg-5ubuntu7.2) ...\r\nSetting up tzdata (2020a-0ubuntu0.18.04) ...\r\n\r\nCurrent default time zone: 'Etc/UTC'\r\nLocal time is now:      Fri Sep  4 12:09:31 UTC 2020.\r\nUniversal Time is now:  Fri Sep  4 12:09:31 UTC 2020.\r\nRun 'dpkg-reconfigure tzdata' if you wish to change it.\r\n\r\nSetting up libopts25:amd64 (1:5.18.12-4) ...\r\nSetting up netbase (5.4) ...\r\nSetting up sntp (1:4.2.8p10+dfsg-5ubuntu7.2) ...\r\nSetting up ntp (1:4.2.8p10+dfsg-5ubuntu7.2) ...\r\ninvoke-rc.d: could not determine current runlevel\r\ninvoke-rc.d: policy-rc.d denied execution of start.\r\nProcessing triggers for libc-bin (2.27-3ubuntu1.2) ...\r\n",

    ...[SNIP]...

        "Setting up libopts25:amd64 (1:5.18.12-4) ...",
        "Setting up netbase (5.4) ...",
        "Setting up sntp (1:4.2.8p10+dfsg-5ubuntu7.2) ...",
        "Setting up ntp (1:4.2.8p10+dfsg-5ubuntu7.2) ...",
        "invoke-rc.d: could not determine current runlevel",
        "invoke-rc.d: policy-rc.d denied execution of start.",
        "Processing triggers for libc-bin (2.27-3ubuntu1.2) ..."
    ]
}
```

Instead of restricting the commands to the prod machine, let’s find the bash version installed on all the machines in the inventory file.
```
ansible -i inventory.ini all -m command -a "bash --version"
```
Output:
```
prod-p30jrhut | CHANGED | rc=0 >>
GNU bash, version 5.0.17(1)-release (x86_64-pc-linux-gnu)
Copyright (C) 2019 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
devsecops-box-p30jrhut | CHANGED | rc=0 >>
GNU bash, version 5.0.17(1)-release (x86_64-pc-linux-gnu)
Copyright (C) 2019 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law
```

Nice, we can see the bash version of the prod and devsecops-box represented by GNU bash, version 5.0.17(1)-release (x86_64-pc-linux-gnu) along the lines.

Exercise: Ansible Ad-hoc commands
----------------------------------

In this exercise, we will use Ansible ad-hoc command to find the uptime of our lab machines.

1. List all available Ansible modules using ansible-doc command to find shell module.
   > `ansible-doc -l | grep shell`
2. Use inventory file (-i inventory.ini) and run the uptime command on the production machine using shell module
  > `ansible -i inventory.ini prod -m shell -a "uptime"`


> How is this helpful in real-world situations? We can find uptime of all of your production machine fleet of 500 machines within 5 minutes.
> 
> Please try to do this exercise without looking at the solution on the next page.

Run the Ansible playbook
----------
Let’s create a playbook to run against the production environment.

```
cat > playbook.yml <<EOL
---
- name: Example playbook to install firewalld
  hosts: prod
  remote_user: root
  become: yes
  gather_facts: no
  vars:
    state: present

  tasks:
  - name: ensure firewalld is at the latest version
    apt:
      name: firewalld
      update_cache: yes
EOL
```
- update_cache: yes will ensure package handler updates its repository cache prior to attempting the package installation.

Let’s run this playbook against the prod machine.

```
ansible-playbook -i inventory.ini playbook.yml
```
output
```
PLAY [Example playbook to install firewalld] ******************************************

TASK [ensure firewalld is installed] ***********************************************************************************
ok: [prod-p30jrhut]

PLAY RECAP ************************************************************************
prod-p30jrhut             : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
Try running the above ansible command once again.

```
ansible-playbook -i inventory.ini playbook.yml
```
output
```
PLAY [Example playbook to install firewalld] ******************************************

TASK [ensure firewalld is installed] ***********************************************************************************
ok: [prod-p30jrhut]

PLAY RECAP ************************************************************************
prod-p30jrhut             : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
> Did you notice the changed=0? What is its importance from a security perspective?
> To check if there's any deviation from the baseline standards.

Exercise: Create playbook with roles from ansible-galaxy
---------

In this task, we are going to develop a playbook employing roles present on Ansible Galaxy, and it will be executed on the inventory group designated for the Production host.

1. Create a new directory /challenge and create a playbook.yml file inside the /challenge directory. 
   You can use the above playbook.yml syntax as a starter for this task, but the /challenge/playbook.yml needs to use the secfigo.terraform role to install the Terraform utility.

Create the /challenge directory and copy an existing inventory.ini file.
```
mkdir /challenge && cd /challenge
cp ../inventory.ini .
```
Create the playbook.yml file with secfigo.terraform role.
```
cat > /challenge/playbook.yml <<EOL
---
- name: Example playbook to install Terraform using ansible role.
  hosts: prod
  remote_user: root
  become: yes

  roles:
    - secfigo.terraform
EOL
```

2. Install secfigo.terraform role using ansible-galaxy.<br>
`ansible-galaxy install secfigo.terraform`

3. Execute the /challenge/playbook.yml against the prod machine to install the Terraform utility. Optionally put this hardening job in the CI pipeline.<br>
`ansible-playbook -i /challenge/inventory.ini /challenge/playbook.yml`

> Please try to do this exercise without looking at the solution on the next page.

Download roles from Ansible Galaxy
--------------
Ansible galaxy helps you in storing open source Ansible roles.

Let’s explore the options it provides us.

```
ansible-galaxy role --help

usage: ansible-galaxy role [-h] ROLE_ACTION ...

positional arguments:
  ROLE_ACTION
    init       Initialize new role with the base structure of a role.
    remove     Delete roles from roles_path.
    delete     Removes the role from Galaxy. It does not remove or alter the actual GitHub repository.
    list       Show the name and version of each role installed in the roles_path.
    search     Search the Galaxy database by tags, platforms, author and multiple keywords.
    import     Import a role into a galaxy server
    setup      Manage the integration between Galaxy and the given source.
    info       View more details about a specific role.
    install    Install role(s) from file(s), URL(s) or Ansible Galaxy

options:
  -h, --help   show this help message and exit
```
We can search for desired roles using the search option.
```
ansible-galaxy install secfigo.terraform

- [WARNING]: - 'secfigo.terraform' (1.0.1) is already installed - use --force to change version to unspecified
```
> Notice, the role was installed under /root/.ansible/roles/secfigo.terraform directory?

Let’s create a directory and playbook to install the terraform on the production machine.

```
mkdir /challenge && cd /challenge
cp ../inventory.ini .

cat > /challenge/playbook.yml <<EOL
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
ansible-playbook -i /challenge/inventory.ini /challenge/playbook.yml

PLAY [Example playbook to install Terraform using ansible role.] *************

TASK [Gathering Facts] *******************************************************
ok: [prod-p30jrhut]

TASK [secfigo.terraform : Make sure unzip is installed] **********************
ok: [prod-p30jrhut]

TASK [secfigo.terraform : Download and Install Terraform] ********************
skipping: [prod-p30jrhut]

PLAY RECAP *******************************************************************
prod-p30jrhut              : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

Harden the production environment
----------

> Dev-Sec Project has lots of good examples on how to create Ansible roles and uses lots of best practices which we can use as a baseline in our roles.
>
> For example, https://github.com/dev-sec/ansible-os-hardening.

Exercise: Using Ansible to Harden prod server
---------
In this exercise, we will create a new playbook that uses dev-sec.os-hardening role available from Ansible galaxy to harden the prod environment.

> Trivia: Which stage should this job run in? and against which machines?
> If you are struggling with the exercises, please refer the hints in the lab portal, and the learning resources in the course portal.

1. Create a new directory hardening and create a file in it called ansible-hardening.yml
Create the /hardening directory and copy an existing inventory.ini file.
```
mkdir /hardening && cd /hardening
cp ../inventory.ini .
```
Create the ansible-hardening.yml file with dev-sec.os-hardening role.
```
cat > /hardening/ansible-hardening.yml <<EOL
---
- name: Playbook to harden Ubuntu OS.
  hosts: prod
  remote_user: root
  become: yes

  roles:
    - dev-sec.os-hardening

EOL
```

2. Install dev-sec.os-hardening role from ansible-galaxy<br>
`ansible-galaxy install dev-sec.os-hardening`

3. Execute the /hardening/ansible-hardening.yml to harden the Ubuntu production machine. Optionally put this hardening job in the CI pipeline.
```
ansible-playbook -i /hardening/inventory.ini /hardening/ansible-hardening.yml


Starting galaxy role install process
- downloading role 'os-hardening', owned by dev-sec
- downloading role from https://github.com/dev-sec/ansible-os-hardening/archive/6.2.0.tar.gz
- extracting dev-sec.os-hardening to /root/.ansible/roles/dev-sec.os-hardening
- dev-sec.os-hardening (6.2.0) was installed successfully
/hardening# ansible-playbook -i /hardening/inventory.ini /hardening/ansible-hardening.yml

PLAY [Playbook to harden Ubuntu OS.] ********************************************************************************

TASK [Gathering Facts] **********************************************************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : Set OS family dependent variables] *****************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : Set OS dependent variables] ************************************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : install auditd package | package-08] ***************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : configure auditd | package-08] *********************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : create limits.d-directory if it does not exist | sysctl-31a, sysctl-31b] ***************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : create additional limits config file -> 10.hardcore.conf | sysctl-31a, sysctl-31b] *****
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : set 10.hardcore.conf perms to 0400 and root ownership] *********************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove 10.hardcore.conf config file] ***************************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : create login.defs | os-05, os-05b] *****************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : find files with write-permissions for group] *******************************************
ok: [prod-p30jrhut] => (item=/usr/local/sbin)
ok: [prod-p30jrhut] => (item=/usr/local/bin)
ok: [prod-p30jrhut] => (item=/usr/sbin)
ok: [prod-p30jrhut] => (item=/usr/bin)
ok: [prod-p30jrhut] => (item=/sbin)
ok: [prod-p30jrhut] => (item=/bin)

TASK [dev-sec.os-hardening : minimize access on found files] ********************************************************
changed: [prod-p30jrhut] => (item=[{'changed': False, 'stdout': '/usr/local/bin/terraform', 'stderr': '', 'rc': 0, 'cmd': 'find -L /usr/local/bin -perm /go+w -type f', 'start': '2025-05-21 06:22:58.501605', 'end': '2025-05-21 06:22:58.507506', 'delta': '0:00:00.005901', 'msg': '', 'invocation': {'module_args': {'_raw_params': 'find -L /usr/local/bin -perm /go+w -type f', '_uses_shell': True, 'stdin_add_newline': True, 'strip_empty_ends': True, 'argv': None, 'chdir': None, 'executable': None, 'creates': None, 'removes': None, 'stdin': None}}, 'stderr_lines': [], 'failed': False, 'item': '/usr/local/bin', 'ansible_loop_var': 'item'}, '/usr/local/bin/terraform'])

TASK [dev-sec.os-hardening : change shadow ownership to root and mode to 0600 | os-02] ******************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : change passwd ownership to root and mode to 0644 | os-03] ******************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : change su-binary to only be accessible to user and group root] *************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : set option hidepid for proc filesystem] ************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : update pam on Debian systems] **********************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove pam ccreds to disable password caching] *****************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove pam_cracklib, because it does not play nice with passwdqc] **********************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : install the package for strong password checking] **************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : configure passwdqc] ********************************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove passwdqc] ***********************************************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : install tally2] ************************************************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : configure tally2] **********************************************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : delete tally2 when retries is 0] *******************************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove pam_cracklib, because it does not play nice with passwdqc] **********************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : install the package for strong password checking] **************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove passwdqc] ***********************************************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : configure passwdqc and tally via central system-auth confic] ***************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : Gather package facts] ******************************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : NSA 2.3.3.5 Upgrade Password Hashing Algorithm to SHA-512] *****************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : install modprobe to disable filesystems | os-10] ***************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : check if efi is installed] *************************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove vfat from fs-list if efi is used] ***********************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove used filesystems from fs-list] **************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : disable unused filesystems | os-10] ****************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : add pinerolo_profile.sh to profile.d] **************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove pinerolo_profile.sh from profile.d] *********************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : create securetty] **********************************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove suid/sgid bit from binaries in blacklist | os-06] *******************************
ok: [prod-p30jrhut] => (item=/usr/bin/rcp)
ok: [prod-p30jrhut] => (item=/usr/bin/rlogin)
ok: [prod-p30jrhut] => (item=/usr/bin/rsh)
ok: [prod-p30jrhut] => (item=/usr/libexec/openssh/ssh-keysign)
changed: [prod-p30jrhut] => (item=/usr/lib/openssh/ssh-keysign)
ok: [prod-p30jrhut] => (item=/sbin/netreport)
ok: [prod-p30jrhut] => (item=/usr/sbin/usernetctl)
ok: [prod-p30jrhut] => (item=/usr/sbin/userisdnctl)
ok: [prod-p30jrhut] => (item=/usr/sbin/pppd)
ok: [prod-p30jrhut] => (item=/usr/bin/lockfile)
ok: [prod-p30jrhut] => (item=/usr/bin/mail-lock)
ok: [prod-p30jrhut] => (item=/usr/bin/mail-unlock)
ok: [prod-p30jrhut] => (item=/usr/bin/mail-touchlock)
ok: [prod-p30jrhut] => (item=/usr/bin/dotlockfile)
ok: [prod-p30jrhut] => (item=/usr/bin/arping)
ok: [prod-p30jrhut] => (item=/usr/sbin/uuidd)
ok: [prod-p30jrhut] => (item=/usr/bin/mtr)
ok: [prod-p30jrhut] => (item=/usr/lib/evolution/camel-lock-helper-1.2)
ok: [prod-p30jrhut] => (item=/usr/lib/pt_chown)
ok: [prod-p30jrhut] => (item=/usr/lib/eject/dmcrypt-get-device)
ok: [prod-p30jrhut] => (item=/usr/lib/mc/cons.saver)

TASK [dev-sec.os-hardening : find binaries with suid/sgid set | os-06] **********************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : gather files from which to remove suids/sgids and remove system white-listed files | os-06] ***
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove suid/sgid bit from all binaries except in system and user whitelist | os-06] ****
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : protect sysctl.conf] *******************************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : set Daemon umask, do config for rhel-family | NSA 2.2.4.1] *****************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : install initramfs-tools] ***************************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : rebuild initramfs with starting pack of modules, if module loading at runtime is disabled] ***
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : create a combined sysctl-dict if overwrites are defined] *******************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : Change various sysctl-settings, look at the sysctl-vars file for documentation] ********
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.ip_forward', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.all.forwarding', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.all.accept_ra', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.default.accept_ra', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.all.rp_filter', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.default.rp_filter', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.icmp_echo_ignore_broadcasts', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.icmp_ignore_bogus_error_responses', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.icmp_ratelimit', 'value': 100})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.icmp_ratemask', 'value': 88089})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.all.disable_ipv6', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.tcp_timestamps', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.all.arp_ignore', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.all.arp_announce', 'value': 2})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.tcp_rfc1337', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.all.shared_media', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.default.shared_media', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.all.accept_source_route', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.default.accept_source_route', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.default.accept_redirects', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.all.accept_redirects', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.all.secure_redirects', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.default.secure_redirects', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.default.accept_redirects', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.all.accept_redirects', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.all.send_redirects', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.default.send_redirects', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.all.log_martians', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv4.conf.default.log_martians', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.default.router_solicitations', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.default.accept_ra_rtr_pref', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.default.accept_ra_pinfo', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.default.accept_ra_defrtr', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.default.autoconf', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.default.dad_transmits', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'net.ipv6.conf.default.max_addresses', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'kernel.sysrq', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'fs.suid_dumpable', 'value': 0})
changed: [prod-p30jrhut] => (item={'key': 'kernel.randomize_va_space', 'value': 2})
changed: [prod-p30jrhut] => (item={'key': 'kernel.core_uses_pid', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'kernel.yama.ptrace_scope', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'vm.mmap_min_addr', 'value': 65536})
changed: [prod-p30jrhut] => (item={'key': 'fs.protected_hardlinks', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'fs.protected_symlinks', 'value': 1})
changed: [prod-p30jrhut] => (item={'key': 'vm.mmap_rnd_bits', 'value': 32})
changed: [prod-p30jrhut] => (item={'key': 'vm.mmap_rnd_compat_bits', 'value': 16})
changed: [prod-p30jrhut] => (item={'key': 'kernel.kptr_restrict', 'value': 2})
changed: [prod-p30jrhut] => (item={'key': 'kernel.kexec_load_disabled', 'value': 1})

TASK [dev-sec.os-hardening : Change various sysctl-settings on rhel6-hosts or older, look at the sysctl-vars file for documentation] ***
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : Apply ufw defaults] ********************************************************************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : get UID_MIN from login.defs] ***********************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : calculate UID_MAX from UID_MIN by substracting 1] **************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : set UID_MAX on Debian-systems if no login.defs exist] **********************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : set UID_MAX on other systems if no login.defs exist] ***********************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : get all system accounts] ***************************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove always ignored system accounts from list] ***************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : change system accounts not on the user provided ignore-list] ***************************
ok: [prod-p30jrhut] => (item=daemon)
ok: [prod-p30jrhut] => (item=bin)
ok: [prod-p30jrhut] => (item=sys)
ok: [prod-p30jrhut] => (item=games)
ok: [prod-p30jrhut] => (item=man)
ok: [prod-p30jrhut] => (item=lp)
ok: [prod-p30jrhut] => (item=mail)
ok: [prod-p30jrhut] => (item=news)
ok: [prod-p30jrhut] => (item=uucp)
ok: [prod-p30jrhut] => (item=proxy)
ok: [prod-p30jrhut] => (item=www-data)
ok: [prod-p30jrhut] => (item=backup)
ok: [prod-p30jrhut] => (item=list)
ok: [prod-p30jrhut] => (item=irc)
ok: [prod-p30jrhut] => (item=gnats)
ok: [prod-p30jrhut] => (item=_apt)
ok: [prod-p30jrhut] => (item=systemd-network)
ok: [prod-p30jrhut] => (item=systemd-resolve)
ok: [prod-p30jrhut] => (item=messagebus)
ok: [prod-p30jrhut] => (item=sshd)
ok: [prod-p30jrhut] => (item=ntp)

TASK [dev-sec.os-hardening : Get user accounts | os-09] *************************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : delete rhosts-files from system | os-09] ***********************************************
ok: [prod-p30jrhut] => (item=root)
ok: [prod-p30jrhut] => (item=daemon)
ok: [prod-p30jrhut] => (item=bin)
ok: [prod-p30jrhut] => (item=sys)
ok: [prod-p30jrhut] => (item=sync)
ok: [prod-p30jrhut] => (item=games)
ok: [prod-p30jrhut] => (item=man)
ok: [prod-p30jrhut] => (item=lp)
ok: [prod-p30jrhut] => (item=mail)
ok: [prod-p30jrhut] => (item=news)
ok: [prod-p30jrhut] => (item=uucp)
ok: [prod-p30jrhut] => (item=proxy)
ok: [prod-p30jrhut] => (item=www-data)
ok: [prod-p30jrhut] => (item=backup)
ok: [prod-p30jrhut] => (item=list)
ok: [prod-p30jrhut] => (item=irc)
ok: [prod-p30jrhut] => (item=gnats)
ok: [prod-p30jrhut] => (item=nobody)
ok: [prod-p30jrhut] => (item=_apt)
ok: [prod-p30jrhut] => (item=systemd-network)
ok: [prod-p30jrhut] => (item=systemd-resolve)
ok: [prod-p30jrhut] => (item=messagebus)
ok: [prod-p30jrhut] => (item=sshd)
ok: [prod-p30jrhut] => (item=ntp)

TASK [dev-sec.os-hardening : delete hosts.equiv from system | os-01] ************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : delete .netrc-files from system | os-09] ***********************************************
ok: [prod-p30jrhut] => (item=root)
ok: [prod-p30jrhut] => (item=daemon)
ok: [prod-p30jrhut] => (item=bin)
ok: [prod-p30jrhut] => (item=sys)
ok: [prod-p30jrhut] => (item=sync)
ok: [prod-p30jrhut] => (item=games)
ok: [prod-p30jrhut] => (item=man)
ok: [prod-p30jrhut] => (item=lp)
ok: [prod-p30jrhut] => (item=mail)
ok: [prod-p30jrhut] => (item=news)
ok: [prod-p30jrhut] => (item=uucp)
ok: [prod-p30jrhut] => (item=proxy)
ok: [prod-p30jrhut] => (item=www-data)
ok: [prod-p30jrhut] => (item=backup)
ok: [prod-p30jrhut] => (item=list)
ok: [prod-p30jrhut] => (item=irc)
ok: [prod-p30jrhut] => (item=gnats)
ok: [prod-p30jrhut] => (item=nobody)
ok: [prod-p30jrhut] => (item=_apt)
ok: [prod-p30jrhut] => (item=systemd-network)
ok: [prod-p30jrhut] => (item=systemd-resolve)
ok: [prod-p30jrhut] => (item=messagebus)
ok: [prod-p30jrhut] => (item=sshd)
ok: [prod-p30jrhut] => (item=ntp)

TASK [dev-sec.os-hardening : remove unused repositories] ************************************************************
skipping: [prod-p30jrhut] => (item=CentOS-Debuginfo) 
skipping: [prod-p30jrhut] => (item=CentOS-Media) 
skipping: [prod-p30jrhut] => (item=CentOS-Vault) 
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : get yum-repository-files] **************************************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : activate gpg-check for yum-repository-files] *******************************************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : activate gpg-check for config files] ***************************************************
skipping: [prod-p30jrhut] => (item=/etc/yum.conf) 
skipping: [prod-p30jrhut] => (item=/etc/dnf/dnf.conf) 
skipping: [prod-p30jrhut] => (item=/etc/yum/pluginconf.d/rhnplugin.conf) 
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove deprecated or insecure packages | package-01 - package-09] **********************
skipping: [prod-p30jrhut]

TASK [dev-sec.os-hardening : remove deprecated or insecure packages | package-01 - package-09] **********************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : configure selinux | selinux-01] ********************************************************
skipping: [prod-p30jrhut]

RUNNING HANDLER [dev-sec.os-hardening : update-initramfs] ***********************************************************
changed: [prod-p30jrhut]

PLAY RECAP **********************************************************************************************************
prod-p30jrhut              : ok=43   changed=20   unreachable=0    failed=0    skipped=27   rescued=0    ignored=0   

```




Optionally put this hardening job in the CI pipeline (please refer to Exercise 6.0 for some inspiration)


> Trivia: Which stage should this job run in? and against which machines?

