Harden machines in CI/CD pipelines
=======================

Learn how to embed hardening in CI/CD pipelines
---------

In this scenario, you will learn how to install, run and embed Ansible on a remote machine.

You will need to install the Ansible tool and then finally run the Ansible playbook against the remote machine using CI/CD pipeline.

Install Ansible
----------

```
pip3 install ansible==2.10.4
```

Create the inventory file
----------

Let’s create the inventory or CMDB file for Ansible using the following command.

```
cat > inventory.ini <<EOL

# DevSecOps Studio Inventory
[devsecops]
devsecops-box-XqiHnDZ0

[gitservers]
gitlab-ce-XqiHnDZ0

[prod]
prod-XqiHnDZ0
EOL
```

Next, we will have to ensure the SSH’s yes/no prompt is not shown while running the ansible commands, so we will be using ssh-keyscan to capture the key signatures beforehand.

```
ssh-keyscan -t rsa prod-XqiHnDZ0 >> ~/.ssh/known_hosts
ssh-keyscan -t rsa gitlab-ce-XqiHnDZ0 >> ~/.ssh/known_hosts
ssh-keyscan -t rsa devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
```

> Pro-tip: Instead of running the ssh-keyscan command thrice, we can achieve the same result using the below command.

```
ssh-keyscan -t rsa prod-XqiHnDZ0 gitlab-ce-XqiHnDZ0 devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
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
ansible-playbook -i inventory.ini ansible-hardening.yml

PLAY [Playbook to harden ubuntu OS.] *******************************************

TASK [Gathering Facts] *********************************************************
ok: [prod-sxfnfgse]

TASK [dev-sec.os-hardening : Set OS family dependent variables] ****************
ok: [prod-sxfnfgse]

TASK [dev-sec.os-hardening : Set OS dependent variables] ***********************

TASK [dev-sec.os-hardening : install auditd package | package-08] **************
changed: [prod-sxfnfgse]

TASK [dev-sec.os-hardening : configure auditd | package-08] ********************
changed: [prod-sxfnfgse]

TASK [dev-sec.os-hardening : find files with write-permissions for group] ******
ok: [prod-sxfnfgse] => (item=/usr/local/sbin)
ok: [prod-sxfnfgse] => (item=/usr/local/bin)
ok: [prod-sxfnfgse] => (item=/usr/sbin)
ok: [prod-sxfnfgse] => (item=/usr/bin)
ok: [prod-sxfnfgse] => (item=/sbin)
ok: [prod-sxfnfgse] => (item=/bin)

...[SNIP]...

PLAY RECAP *********************************************************************
prod-sxfnfgse              : ok=40   changed=19   unreachable=0    failed=0    skipped=27   rescued=0    ignored=0
```

As we can see, there were 19 changes (changed=19) made to the production machine while hardening.

> As we can see, there were 19 changes (changed=19) made to the production machine while hardening.
>
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

