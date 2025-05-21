Ansible Ad-hoc commands
========================

Learn how to use Ansible Ad-hoc commands to perform tasks on remote machine
------------------------------------------------


In this scenario, you will learn how to install Ansible and run Ad-hoc commands on a remote machine.

Install Ansible
----------

```
pip3 install ansible==8.7.0
```

Inventory file
----------

Inventory is a file to define a list of hosts that can can be sorted as groups, it provides ability to store and manage some variables. The inventory can be created as INI or YAML, but the most common format is INI and might look like this:

```
[devsecops]
devsecops-box-p30jrhut

[sandbox]
sandbox-p30jrhut

[prod]
prod-p30jrhut
```

The headings in the bracket are a group name that used to defines our hosts. So let’s create the inventory file for Ansible using the following command.

```
cat > inventory.ini <<EOL

[devsecops]
devsecops-box-p30jrhut

[sandbox]
sandbox-p30jrhut

[prod]
prod-p30jrhut

EOL
```

To see which hosts in our inventory matches a supplied group name, let’s try the following command.

```
ansible -i inventory.ini prod --list-hosts

 hosts (1):
    prod-p30jrhut
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

ansible [core 2.13.5]
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.8/dist-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.8.10 (default, Jun 22 2022, 20:18:18) [GCC 9.4.0]
  jinja version = 3.1.2
  libyaml = True
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
```
ansible [core 2.13.5]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.8/dist-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.8.10 (default, Jun 22 2022, 20:18:18) [GCC 9.4.0]
  jinja version = 3.1.2
  libyaml = True
```

With the config file, you can define any settings like inventory default location or output formats when Ansible finishes a certain command or a playbook. If you want to see further details about the config, you can check out this link and the ansible.cfg default config at [here.](https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg)

> Pro-tip: Instead of using /etc/ansible/ansible.cfg file, you can create an ansible.cfg file in the directory which you create a playbook or run Ansible commands.

Ad-hoc commands
------------------------------------------------

Ansible uses ad-hoc command to execute a single task on one or more remote hosts, and this way of executing a command is easy and fast, but it’s not reusable like the playbook.

For example, we want to use ping module through ad-hoc command. But before we do that, we will have to ensure the SSH’s yes/no prompt is not shown while running the ansible commands, so let’s use the ssh-keyscan to capture the key signatures beforehand.

```
ssh-keyscan -H devsecops-box-p30jrhut sandbox-p30jrhut prod-p30jrhut >> ~/.ssh/known_hosts

# prod-p30jrhut:22 SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
# devsecops-box-p30jrhut:22 SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
# sandbox-p30jrhut:22 SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.5
```

> Please ignore the machine id in Command Output above, it your case it would be the same as your machine id.

Then execute the ansible command.

```
ansible -i inventory.ini all -m ping

## OUTPUT
devsecops-box-p30jrhut | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
sandbox-p30jrhut | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
prod-p30jrhut | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```
As you can see the command output above, all our hosts(line number 1, 9 and 15) are connected to Ansible. Next, use the shell module of Ansible to run the hostname command on all machines.

```
ansible -i inventory.ini all -m shell -a "hostname"

devsecops-box-p30jrhut | CHANGED | rc=0 >>
devsecops-box-p30jrhut
sandbox-p30jrhut | CHANGED | rc=0 >>
sandbox-p30jrhut
prod-p30jrhut | CHANGED | rc=0 >>
prod-p30jrhut
```

We can use another module to install a package inside the remote host.

```
ansible -i inventory.ini all -m apt -a "name=ntp"

sandbox-p30jrhut | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "cache_update_time": 1644912480,
    "cache_updated": false,
    "changed": true,
    "stderr": "debconf: delaying package configuration, since apt-utils is not installed\n",
    "stderr_lines": [
        "debconf: delaying package configuration, since apt-utils is not installed"
    ],

...[SNIP]...

        "Setting up libopts25:amd64 (1:5.18.12-4) ...",
        "Setting up sntp (1:4.2.8p10+dfsg-5ubuntu7.3) ...",
        "Setting up ntp (1:4.2.8p10+dfsg-5ubuntu7.3) ...",
        "Created symlink /etc/systemd/system/network-pre.target.wants/ntp-systemd-netif.path → /lib/systemd/system/ntp-systemd-netif.path.",
        "Created symlink /etc/systemd/system/multi-user.target.wants/ntp.service → /lib/systemd/system/ntp.service.",
        "/usr/sbin/policy-rc.d returned 101, not running 'start ntp-systemd-netif.path'",
        "/usr/sbin/policy-rc.d returned 101, not running 'start ntp-systemd-netif.path ntp-systemd-netif.service'",
        "invoke-rc.d: policy-rc.d denied execution of start.",
        "Processing triggers for systemd (237-3ubuntu10.53) ...",
        "Processing triggers for libc-bin (2.27-3ubuntu1.4) ..."
    ]
}

```
> Did you get the following error?
```
   [WARNING]: Updating cache and auto-installing missing dependency: python3-apt
devsecops-box-p30jrhut | FAILED! => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "msg": "python3-apt must be installed and visible from /usr/bin/python3."
}
```
It means there’s incompability with our python packages. Let’s use python 3.8 instead:
<br>`export ANSIBLE_PYTHON_INTERPRETER=/usr/bin/python3.8`

 
To find the available modules, you can check out this link or use the local help command-line tool.

```
ansible-doc -l
```
Example:<br>
`ansible-doc -l | egrep "add_host|amazon.aws.aws"`
```
[WARNING]: dellemc.openmanage.ome_active_directory has a documentation
formatting error
add_host                                                                                 Add a host (and alternatively a group) to the ansible-playbook in-me...
amazon.aws.aws_az_facts                                                                  Gather information about availabilit...
amazon.aws.aws_az_info                                                                   Gather information about availabilit...
amazon.aws.aws_caller_info                                                               Get information about the user and account being used to ...
amazon.aws.aws_s3
```

Exercise
----------
1. Use the ansible-doc command to see help examples and find a module that can send a file from DevSecOps-Box to remote machines
> `ansible-doc -h`

2. Create a file with some content, let the file name be notes at the location /root
> echo "test" > /root/notes

3. Using an ansible ad-hoc command, copy the file /root/notes into all remote machines (sandbox and production) to the destination directory /root
> ansible -i inventory.ini all -m copy -a "src=/root/notes dest=/root"


> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).
