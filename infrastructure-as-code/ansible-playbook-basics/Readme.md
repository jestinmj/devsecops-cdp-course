Ansible playbook basics
=======================

Learn how to create a simple playbook that sets up an application
---------

In this scenario, you will learn how to install and run Ansible on a remote machine.

You will need to install the Ansible tool and create a simple playbook.

Install Ansible
----------

```
pip3 install ansible==2.10.4
```

Create the inventory file
----------

We will learn Ansible basics by performing our experiments on these two machines. Let’s create the inventory or CMDB file for Ansible using the following command.

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
ssh-keyscan -t rsa devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
```

Let’s do this for the rest of the systems in this lab as well.

```
ssh-keyscan -t rsa sandbox-XqiHnDZ0 >> ~/.ssh/known_hosts
```

> Pro-tip: Instead of running the ssh-keyscan command twice, we can achieve the same using the below command.

```
ssh-keyscan -t rsa sandbox-XqiHnDZ0 devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
```

Create the playbook
----------

Playbooks are a collection of Ansible tasks, you can run a playbook against a local or a remote machine. They help us in configuring machine(s) according to the requirements. Ansible uses the YAML format to declare the configurations.

Playbooks follow a directory layout. A sample playbook directory structure is shown below:

```
tasks/              # task files included from playbooks
    01-install.yml  # task file to install something
    02-config.yml   # task file to copy configuration to remote machine
    main.yml        # master task playbook
roles/
    common/         # this hierarchy represents a "role"
vars/
    main.yml        # vars file to save variables
main.yml            # master playbook
```

> For more details, you can check out [Sample Directory Layout of Ansible.](https://docs.ansible.com/ansible/latest/user_guide/sample_setup.html#sample-directory-layout)

We will create a simple playbook that will execute tasks like installing, configuring Nginx, and setting up the Django application on the sandbox machine.

Let’s create a directory to store our playbook.

```
mkdir simple-playbook && cd simple-playbook
mkdir tasks

cat > tasks/main.yml <<EOL
---
- name: Install nginx
  apt:
    name: "nginx"
    state: present

- name: Copy the configuration
  template:
    src: templates/default.j2
    dest: /etc/nginx/sites-enabled/default

- name: Start nginx service
  service:
    name: nginx
    state: started
    enabled: yes

- name: Clone django repository
  git:
    repo: https://gitlab.practical-devsecops.training/pdso/django.nv.git
    dest: /opt/django

- name: Install dependencies
  command: pip3 install -r requirements.txt
  args:
    chdir: /opt/django

- name: Database migration
  command: python3 manage.py migrate
  args:
    chdir: /opt/django

- name: Load data from the fixtures
  command: python3 manage.py loaddata fixtures/*
  args:
    chdir: /opt/django

- name: Run an application in the background
  shell: nohup python3 manage.py runserver 0.0.0.0:8000 &
  args:
    chdir: /opt/django
EOL
```
Then, we will create a templates directory to save our configuration file.

```
mkdir templates
```

We will create a default.j2 template file. This file gets copied to the remote machine to adjust the template variables according to the requirements.

```
cat > templates/default.j2 <<EOL
{% raw %}
server {
    listen      80;
    server_name localhost;

    access_log  /var/log/nginx/django_access.log;
    error_log   /var/log/nginx/django_error.log;

    proxy_buffers 16 64k;
    proxy_buffer_size 128k;

    location / {
        proxy_pass  http://localhost:8000;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_redirect off;

        proxy_set_header    Host \$host;
        proxy_set_header    X-Real-IP \$remote_addr;
        proxy_set_header    X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header    X-Forwarded-Proto http;
    }
}
{% endraw %}
EOL
```

Let’s create a main.yml playbook file that uses the main.yml under the tasks folder.

```
cat > main.yml <<EOL
---
- name: Simple playbook
  hosts: sandbox
  remote_user: root
  gather_facts: no

  tasks:
  - include: tasks/main.yml
EOL
```
So far, we have created two directories and three files. We can check out our current directory layout using the tree command.

```
tree
....
simple-playbook# tree
.
├── main.yml
├── tasks
│   └── main.yml
└── templates
    └── default.j2

2 directories, 3 files
```

Run the Ansible playbook
----------

Let’s run our playbook using the following command.

```
ansible-playbook -i inventory.ini main.yml
```

> Oops, why our playbook didn’t execute? Can you look at the output and figure out why?

It’s simple! Ansible couldn’t find the inventory.ini file. This file is needed to marry the host groups and individual machines in it. Let’s move the inventory.ini file we created before to our current directory.

```
mv ../inventory.ini .
ansible-playbook -i inventory.ini main.yml
```
output
```
PLAY [Simple playbook] *********************************************************************************************

TASK [Install nginx] ***********************************************************************************************
[WARNING]: Updating cache and auto-installing missing dependency: python-apt
[DEPRECATION WARNING]: Distribution Ubuntu 18.04 on host sandbox-XqiHnDZ0 should use /usr/bin/python3, but is using
 /usr/bin/python for backward compatibility with prior Ansible releases. A future Ansible release will default to 
using the discovered platform python for this host. See 
https://docs.ansible.com/ansible/2.10/reference_appendices/interpreter_discovery.html for more information. This 
feature will be removed in version 2.12. Deprecation warnings can be disabled by setting deprecation_warnings=False
 in ansible.cfg.
changed: [sandbox-XqiHnDZ0]

TASK [Copy the configuration] **************************************************************************************
changed: [sandbox-XqiHnDZ0]

TASK [Start nginx service] *****************************************************************************************
changed: [sandbox-XqiHnDZ0]

TASK [Clone django repository] *************************************************************************************
changed: [sandbox-XqiHnDZ0]

TASK [Install dependencies] ****************************************************************************************
changed: [sandbox-XqiHnDZ0]

TASK [Database migration] ******************************************************************************************
changed: [sandbox-XqiHnDZ0]

TASK [Load data from the fixtures] *********************************************************************************
changed: [sandbox-XqiHnDZ0]

TASK [Run an application in the background] ************************************************************************
changed: [sandbox-XqiHnDZ0]

PLAY RECAP *********************************************************************************************************
sandbox-XqiHnDZ0           : ok=8    changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Once the Ansible playbook finishes, you will notice that the output has changed=8.

> What does it mean? Why is it important? What can we do with it?

The changed=8 specifics that ansible made 8 changes to the system. What would it mean if changed=0? It would mean there were no changes. Since we ran about 8 tasks, we can assume each task made a change to the system, and we got our changed=8 as the output.

Let’s verify if nginx was installed, started, and properly deployed. We will use SSH to log into the sandbox machine.

```
ssh root@sandbox-XqiHnDZ0
```
Check if nginx is installed or not.
```
which nginx
```
Looks good. Next, let’s list all listening ports to check nginx (port 80) and django (port 8000) are being used.

```
# netstat -tlpn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      9488/python3        
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      5603/nginx: master  
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      559/systemd-resolve 
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      719/sshd            
tcp        0      0 127.0.0.11:45215        0.0.0.0:*               LISTEN      -               
```

Perfect, we see port 80 is being used by nginx and 8000 by Django application.

Lets exit from the sandbox machine and head over to the DevSecOps-Box.

```
exit
```
Now, let’s verify our Django application is indeed serving the requests using the curl command.
```
curl sandbox-XqiHnDZ0
```
output
```
<!DOCTYPE html>
<html>
    <head>
    <title>Task Manager</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Styles
    ================================================== -->

    <link rel="stylesheet" href="/static/taskManager/css/bootstrap.css"/>
    <link rel="stylesheet" href="/static/taskManager/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="/static/taskManager/css/font-awesome.css"/>
    <link rel="stylesheet" href="/static/taskManager/css/style.css"/>

...[SNIP]...

                    <p>e: <a href="javascript:;">info@tm.com</a></p>
                </address>
            </div>

            <div class="col-lg-2 col-sm-2 col-lg-offset-1">
                <h1>Our Mission</h1>
                <p>Making life easier, one task at a time.</p>
            </div>

        </div>
    </div>
</footer>
<!--footer end-->

<!-- End Footer -->

<!-- Javascript
================================================== -->
    <!--<script src="/static/taskManager/js/bootstrap.min.js" ></script>
    <script src="http://code.jquery.com/jquery-latest.js"></script>-->

</body>
```
Good, it seems our automation did work.

Exercise
---------
1. Do you think it made sense for us to use Jinja 2 extension file as our templating file? Please look at the file templates/default.j2 and make a call
2. Can we still execute the playbook without gather_facts syntax in main.yml?
3. Try to execute the playbook once again, and explain why the output is different than before, especially changed= field?

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

