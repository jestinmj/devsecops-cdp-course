Harden machines in CI/CD pipelines
=======================

Learn how to embed hardening in CI/CD pipelines
---------

In this scenario, you will learn how to install, run and embed Ansible on a remote machine.

You will need to install the Ansible tool and then finally run the Ansible playbook against the remote machine using CI/CD pipeline.

Install Ansible
----------

```
pip3 install ansible==8.7.0
```

Create the inventory file
----------

Let’s create the inventory or CMDB file for Ansible using the following command.

```
cat > inventory.ini <<EOL

# DevSecOps Studio Inventory
[devsecops]
devsecops-box-p30jrhut

[gitservers]
gitlab-ce-p30jrhut

[prod]
prod-p30jrhut
EOL
```

Next, we will have to ensure the SSH’s yes/no prompt is not shown while running the ansible commands, so we will be using ssh-keyscan to capture the key signatures beforehand.

```
ssh-keyscan -t rsa prod-XqiHnDZ0 >> ~/.ssh/known_hosts
ssh-keyscan -t rsa gitlab-ce-XqiHnDZ0 >> ~/.ssh/known_hosts
ssh-keyscan -t rsa devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts

ssh-keyscan -H prod-p30jrhut >> ~/.ssh/known_hosts
ssh-keyscan -H gitlab-ce-p30jrhut >> ~/.ssh/known_hosts
ssh-keyscan -H devsecops-box-p30jrhut >> ~/.ssh/known_hosts


```

> Pro-tip: Instead of running the ssh-keyscan command thrice, we can achieve the same result using the below command.

```
ssh-keyscan -t rsa prod-XqiHnDZ0 gitlab-ce-XqiHnDZ0 devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts

NEW:
ssh-keyscan -H prod-p30jrhut gitlab-ce-p30jrhut devsecops-box-p30jrhut >> ~/.ssh/known_hosts
```

Harden the production environment
----------
    
> Dev-Sec Project has lots of good examples on how to create Ansible roles and uses lots of best practices which we can use as a baseline in our roles.
>
> For example, https://github.com/dev-sec/ansible-os-hardening.

We will choose the dev-sec.os-hardening role from the dev-sec project to harden our production environment.

```
ansible-galaxy install dev-sec.os-hardening
```

Let’s create a playbook to use this role against a remote machine.

```
cat > ansible-hardening.yml <<EOL
---
- name: Playbook to harden Ubuntu OS.
  hosts: prod
  remote_user: root
  become: yes

  roles:
    - dev-sec.os-hardening

EOL
```

Let’s run this playbook against the prod machine to harden it.

```
ansible-playbook -i inventory.ini ansible-hardening.yml
```
Once the playbook runs, we should see the output as shown below.

```
PLAY [Playbook to harden ubuntu OS.] *******************************************

TASK [Gathering Facts] *********************************************************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : Set OS family dependent variables] ****************
ok: [prod-p30jrhut]

TASK [dev-sec.os-hardening : Set OS dependent variables] ***********************

TASK [dev-sec.os-hardening : install auditd package | package-08] **************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : configure auditd | package-08] ********************
changed: [prod-p30jrhut]

TASK [dev-sec.os-hardening : find files with write-permissions for group] ******
ok: [prod-p30jrhut] => (item=/usr/local/sbin)
ok: [prod-p30jrhut] => (item=/usr/local/bin)
ok: [prod-p30jrhut] => (item=/usr/sbin)
ok: [prod-p30jrhut] => (item=/usr/bin)
ok: [prod-p30jrhut] => (item=/sbin)
ok: [prod-p30jrhut] => (item=/bin)

...[SNIP]...

PLAY RECAP *********************************************************************
prod-p30jrhut              : ok=42   changed=20   unreachable=0    failed=0    skipped=28   rescued=0    ignored=0
```

As we can see, there were 20 changes (changed=20) made to the production machine while hardening.

> Can we put it into CI? Yes, why not?

Running ansible role as part of the CI pipeline.
--------------------------------

Let’s login into the Gitlab and configure production machine https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/settings/ci_cd.

We can use the Gitlab credentials provided below to login i.e.,

- username: root 
- password: pdso-training

Click on the Expand button under the Variables section, then click the Add Variable button.

Add the following key/value pair in the form.

- key: DEPLOYMENT_SERVER
- value: prod-XqiHnDZ0
- key: DEPLOYMENT_SERVER_SSH_PRIVKEY
- value: Copy the private key from the production machine using SSH. The SSH key is available at /root/.ssh/id_rsa. Please refer to Advanced Linux Exercises for a refresher on SSH Keys

Finally, Click on the button Add Variable.

Next, please visit https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml.

Click on the Edit button and append the following code to the .gitlab-ci.yml file.

```
ansible-hardening:
  stage: prod
  image: willhallonline/ansible:2.9-ubuntu-18.04
  before_script:
    - mkdir -p ~/.ssh
    - echo "$DEPLOYMENT_SERVER_SSH_PRIVKEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -t rsa $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
  script:
    - echo -e "[prod]\n$DEPLOYMENT_SERVER" >> inventory.ini
    - ansible-galaxy install dev-sec.os-hardening
    - ansible-playbook -i inventory.ini ansible-hardening.yml
```
The purpose of this Ansible code is to automate the hardening of a production server by installing and running a playbook that applies security settings.

Here's a breakdown of the code:
- stage: prod: This specifies that the deployment is for a production environment.
- image: willhallonline/ansible:2.16-ubuntu-22.04: This specifies the Docker image to use for the deployment, which is a specific version of Ansible (2.16) on an Ubuntu 22.04 base image.
- before_script: This section runs a series of commands before the Ansible playbook is executed. These commands:
    - Create a .ssh directory and add a private SSH key to it.
    - Set the permissions of the private key to 600 (read and write for the owner only).
    - Start the SSH agent and add the private key to it.
    - Add the SSH server's fingerprint to the known_hosts file.
- script: This section runs the Ansible playbook. The playbook is executed with the following steps:
    - Adds a host to the inventory.ini file, specifying the production server as the host.
    - Installs the dev-sec.os-hardening Ansible role, which is a collection of playbooks and tasks for hardening an operating system.
    - Runs the ansible-hardening.yml playbook, which applies the security settings defined in the role.

In summary, this code is used to automate the hardening of a production by installing and running an Ansible playbook that applies security settings to the server.

> With the echo command, we are simply copying the contents of the private key variable stored in Gitlab CI into the id_rsa file under ~/.ssh inside the container.
eval runs the command ssh-agent in the background and sends the key whenever SSH asks for a key in an automated fashion.

Save changes to the file using the Commit changes button.

We can see the results by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Oh, it failed? Why? We also got the following helpful message in the CI output.

```
ansible-playbook -i inventory.ini ansible-hardening.yml
 ERROR! the playbook: ansible-hardening.yml could not be found
 ERROR: Job failed: exit status 1
```

That makes sense. We didn’t upload the ansible-hardening.yml to the git repository yet.

Let’s copy the hardening script.

```
---
- name: Playbook to harden ubuntu OS.
  hosts: prod
  remote_user: root
  become: yes

  roles:
    - dev-sec.os-hardening
```

Visit the add new file URL https://gitlab-ce-XqiHnDZ0lab.practical-devsecops.training/root/django-nv/-/new/master/

Paste the above ansible script into the space provided. Ensure you name the file as `ansible-hardening.yml.`

Save changes to the repo using the Commit changes button.

We can see the results by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

There you have it. We ran ansible hardening locally first and then embedded it into a CI/CD pipeline.

> If you see Permisison Denied, Enter passphrase for /root/.ssh/id_rsa or any other SSH related issue, then you have to ensure a proper key is copied in the CI/CD variable DEPLOYMENT_SERVER_SSH_PRIVKEY.

