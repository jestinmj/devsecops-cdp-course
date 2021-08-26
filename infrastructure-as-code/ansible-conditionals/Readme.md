Ansible conditionals
=======================


Learn how to use Ansible conditionals to make decisions in the playbook
---------

In this scenario, you will learn how to install Ansible and use conditionals statements in the playbook.

Install Ansible
----------

```
pip3 install ansible==2.10.4
```

Create the inventory file
----------

As we’ve learned in the Ansible Ad-hoc Commands exercise, we need to create an inventory file to save our remote hosts to be used by Ansible. Let’s create the file using the following command.

```
cat > inventory.ini <<EOL

# DevSecOps Studio Inventory
[devsecops]
devsecops-box-XqiHnDZ0

[sandbox]
sandbox-XqiHnDZ0

EOL
```

As Ansible uses SSH as its RPC mechanism, we will have to ensure the SSH’s yes/no prompt doesn’t wait for our input indefinitely while running the Ansible commands. To overcome this, we will be using the ssh-keyscan command to capture the key signatures beforehand.

```
ssh-keyscan -t rsa sandbox-XqiHnDZ0 >> ~/.ssh/known_hosts
```

Let’s do this for the rest of the systems in this lab as well.

```
ssh-keyscan -t rsa devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
```

> Pro-tip: Instead of running the ssh-keyscan command twice, we can achieve the same using the below command.

```
ssh-keyscan -t rsa sandbox-XqiHnDZ0 devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
```
when
---------

In Ansible, we can use conditionals to run a single task or multiple tasks in a playbook. Before doing this exercise, you should be familiar with Ad-hoc commands and Ansible Playbook to easily understand conditionals.

Let’s start by creating a simple task to use when statement in the playbook.

```
cat > main.yml <<EOL
---
- name: Simple playbook
  hosts: all
  remote_user: root
  gather_facts: yes     # what does it means?

  tasks:
  - debug:
      msg: "This system uses Ubuntu-based distro"
    when: ansible_distribution == "Ubuntu"
EOL
```

In the above content, we just created one task to print the message in the terminal if the remote hosts are using Ubuntu-based distribution.

> How did you get ansible_distribution as conditions?
>
> We can use the setup module in ansible to discover variables about a system.
>
> execute this command to use setup module as ad-hoc commands:
> 
> ``` ansible -i inventory.ini all -m setup ```

Let’s run our playbook using the following command.

```
ansible-playbook -i inventory.ini main.yml
```
output
```
PLAY [Simple playbook] ****************************************************************************************************************************

TASK [Gathering Facts] ****************************************************************************************************************************
[DEPRECATION WARNING]: Distribution Ubuntu 18.04 on host devsecops-box-JnOHfNpe should use /usr/bin/python3, but is using /usr/bin/python for backward compatibility with prior Ansible releases. A future Ansible release will default to using the discovered platform python for this
host. See https://docs.ansible.com/ansible/2.10/reference_appendices/interpreter_discovery.html for more information. This feature will be removed in version 2.12. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [devsecops-box-JnOHfNpe]
[DEPRECATION WARNING]: Distribution Ubuntu 18.04 on host sandbox-JnOHfNpe should use /usr/bin/python3, but is using /usr/bin/python for backward compatibility with prior Ansible releases. A future Ansible release will default to using the discovered platform python for this host.
See https://docs.ansible.com/ansible/2.10/reference_appendices/interpreter_discovery.html for more information. This feature will be removed in version 2.12. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [sandbox-JnOHfNpe]

TASK [debug] ****************************************************************************************************************************
ok: [devsecops-box-JnOHfNpe] => {
    "msg": "This system uses Ubuntu-based distro"
}
ok: [sandbox-JnOHfNpe] => {
    "msg": "This system uses Ubuntu-based distro"
}

PLAY RECAP ****************************************************************************************************************************
devsecops-box-JnOHfNpe     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
sandbox-JnOHfNpe           : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
As expected, we’ve got the output because the remote hosts are Ubuntu-based, and if the condition is incorrect, it will skip the task, which in our case will result in simply not printing the message output.

Let’s try to change the value of our when condition from Ubuntu to CentOS.

```
cat > main.yml <<EOL
---
- name: Simple playbook
  hosts: all
  remote_user: root
  gather_facts: yes     # what does it mean?

  tasks:
  - debug:
      msg: "This system is used CentOS-based distro"
    when: ansible_distribution == "CentOS"
EOL
```

```
ansible-playbook -i inventory.ini main.yml
```
output
```
PLAY [Simple playbook] ****************************************************************************************************************************
 
TASK [Gathering Facts] ****************************************************************************************************************************
[DEPRECATION WARNING]: Distribution Ubuntu 18.04 on host devsecops-box-JnOHfNpe should use /usr/bin/python3, but is using /usr/bin/python for backward compatibility with prior Ansible releases. A future Ansible release will default to using the discovered platform python for this
host. See https://docs.ansible.com/ansible/2.10/reference_appendices/interpreter_discovery.html for more information. This feature will be removed in version 2.12. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [devsecops-box-JnOHfNpe]
[DEPRECATION WARNING]: Distribution Ubuntu 18.04 on host sandbox-JnOHfNpe should use /usr/bin/python3, but is using /usr/bin/python for backward compatibility with prior Ansible releases. A future Ansible release will default to using the discovered platform python for this host.
See https://docs.ansible.com/ansible/2.10/reference_appendices/interpreter_discovery.html for more information. This feature will be removed in version 2.12. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [sandbox-JnOHfNpe]
 
TASK [debug] ****************************************************************************************************************************
skipping: [devsecops-box-JnOHfNpe]
skipping: [sandbox-JnOHfNpe]
 
PLAY RECAP ****************************************************************************************************************************
devsecops-box-JnOHfNpe     : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
sandbox-JnOHfNpe           : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

As you can see above, a task is skipped because we changed the value in the when condition from Ubuntu to CentOS. Apart from this, you can use the when statement on each Ansible module and re-use it as a variable for desired tasks.

register
---------

register statement is used to save a task as a new variable that can be used for the desired tasks. To understand how it works, let’s replace the previous main.yml file by executing the following command.

```
cat > main.yml <<EOL
---
- name: Simple playbook
  hosts: all
  remote_user: root
  gather_facts: no     # what does it mean?

  tasks:
  - name: Show the content of /etc/os-release
    command: cat /etc/os-release
    register: os_release

  - debug:
      msg: "This system uses Ubuntu-based distro"
    when: os_release.stdout.find('Ubuntu') != -1
EOL
```

> If you curious why we use -1, check out this [link.](https://docs.python.org/2/library/string.html#string.find)

The first task uses the command module to execute cat /etc/os-release command and if you execute cat /etc/os-release on the DevSecOps box, the output is as below.

```
NAME="Ubuntu"
VERSION="18.04.5 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.5 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic
```
We will use the above output in the next task to find Ubuntu string.

> when: os_release.stdout.find('Ubuntu') != -1

You can see two properties in the syntax above, there is stdout (output of the command) and find (search for particular strings). We use it in a conditional statement to print a message in the terminal when the string Ubuntu is found.

Then, run the playbook once again to review the expected output.

output
```
PLAY [Simple playbook] **************************************************************************************************************************************

TASK [Gathering Facts] ****************************************************************************************************************************
[DEPRECATION WARNING]: Distribution Ubuntu 18.04 on host devsecops-box-JnOHfNpe should use /usr/bin/python3, but is using /usr/bin/python for backward compat
ibility with prior Ansible releases. A future Ansible release will default to using the discovered platform python for this 
host. See https://docs.ansible.com/ansible/2.10/reference_appendices/interpreter_discovery.html for more information. This feature will be removed in version
 2.12. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.ok: [devsecops-box-JnOHfNpe]
[DEPRECATION WARNING]: Distribution Ubuntu 18.04 on host sandbox-JnOHfNpe should use /usr/bin/python3, but is using /usr/bin/python for backward compatibility w
ith prior Ansible releases. A future Ansible release will default to using the discovered platform python for this host. See 
https://docs.ansible.com/ansible/2.10/reference_appendices/interpreter_discovery.html for more information. This feature will be removed in version 2.12. Dep
recation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [sandbox-JnOHfNpe]

TASK [Show the content of /etc/os-release] ******************************************************************************************************************

changed: [devsecops-box-JnOHfNpe]
changed: [sandbox-JnOHfNpe]

TASK [debug] ************************************************************************************************************************************************

ok: [devsecops-box-JnOHfNpe] => {
    "msg": "This system uses Ubuntu-based distro"
}
ok: [sandbox-JnOHfNpe] => {
    "msg": "This system uses Ubuntu-based distro"
}

PLAY RECAP **************************************************************************************************************************************************

devsecops-box-JnOHfNpe     : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
sandbox-JnOHfNpe              : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```

Exercise
---------

1. Create a new playbook that contains tasks to check nginx package is installed or not
2. If nginx is installed, print nginx version to the terminal by using the msg module
3. Otherwise, let your playbook install the missing nginx using the apt module

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

