Ansible Ad-hoc commands
========================

Learn how to use Ansible Ad-hoc commands to perform tasks on remote machine
------------------------------------------------


In this scenario, you will learn how to install Ansible and run Ad-hoc commands on a remote machine.

Install Ansible
----------

```
pip3 install ansible==2.10.4
```

Inventory file
----------

Inventory is a file to define a list of hosts that can can be sorted as groups, it provides ability to store and manage some variables. The inventory can be created as INI or YAML, but the most common format is INI and might look like this:

```
[devsecops]
devsecops-box-XqiHnDZ0

[sandbox]
sandbox-XqiHnDZ0

[prod]
prod-XqiHnDZ0
```

The headings in the bracket are a group name that used to defines our hosts. So let’s create the inventory file for Ansible using the following command.

```
cat > inventory.ini <<EOL

[devsecops]
devsecops-box-XqiHnDZ0

[sandbox]
sandbox-XqiHnDZ0

[prod]
prod-XqiHnDZ0

EOL
```

To see which hosts in our inventory matches a supplied group name, let’s try the following command.

```
ansible -i inventory.ini prod --list-hosts
```

You can change the prod value to another group name like sandbox or devsecops to see if there is a host match. In case there is no host match, the output looks like below for a group named gitlab that does not exist in our inventory file.

```
ansible -i inventory.ini gitlab --list-hosts

[WARNING]: Could not match supplied host pattern, ignoring: gitlab
[WARNING]: No hosts matched, nothing to do
  hosts (0):
```

Ansible Configuration file
----------

Ansible also can be customized by modifying the ansible configuration called ansible.cfg. You can see if there is any default configuration through the following command:

```
ansible --version
```

config file is None, if you’re using CentOS, you will find out there is a config file at /etc/ansible/ansible.cfg by default.

Because we don’t have an ansible.cfg in our machine, we can create it manually by doing:

```
mkdir /etc/ansible/
cat > /etc/ansible/ansible.cfg <<EOF
[defaults]
stdout_callback = yaml
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /inventory.ini
EOF
```

If you type ansible –version command once again, you will see config file value now reflects the config file we created above. 

With the config file, you can define any settings like inventory default location or output formats when Ansible finishes a certain command or a playbook. If you want to see further details about the config, you can check out this link and the ansible.cfg default config at [here.](https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg)

> Pro-tip: Instead of using /etc/ansible/ansible.cfg file, you can create an ansible.cfg file in the directory which you create a playbook or run Ansible commands.

Ad-hoc commands
------------------------------------------------

Ansible uses ad-hoc command to execute a single task on one or more remote hosts, and this way of executing a command is easy and fast, but it’s not reusable like the playbook.

For example, we want to use ping module through ad-hoc command. But before we do that, we will have to ensure the SSH’s yes/no prompt is not shown while running the ansible commands, so let’s use the ssh-keyscan to capture the key signatures beforehand.

```
ssh-keyscan -t rsa devsecops-box-XqiHnDZ0 sandbox-XqiHnDZ0 prod-XqiHnDZ0 >> ~/.ssh/known_hosts
```

> Please ignore the machine id in Command Output above, it your case it would be the same as your machine id.

Then execute the ansible command.

```
ansible -i inventory.ini all -m ping
```
As you can see the command output above, all our hosts(line number 1, 9 and 15) are connected to Ansible. Next, use the shell module of Ansible to run the hostname command on all machines.

```
ansible -i inventory.ini all -m shell -a "hostname"
```

We can use another module to install a package inside the remote host.

```
ansible -i inventory.ini all -m apt -a "name=ntp"
```

To find the available modules, you can check out this link or use the local help command-line tool.

```
ansible-doc -l
```

Exercise
----------

1. Find a module that can send a file from DevSecOps-Box to remote machines
2. Use the ansible-doc command to see help examples
3. Create a file called notes and add any string into it, then copy this file into all remote machines (sandbox and production) using ad-hoc command

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).
