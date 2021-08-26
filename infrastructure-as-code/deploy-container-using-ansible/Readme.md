Container deployment using Ansible
================================================================


Learn how to use Ansible to deploy the container
---------

In this scenario, you will learn how to deploy an app on a production machine using Ansible.

You will install the Ansible tool, run the Ansible ad-hoc command, and playbook against the remote machine.

Install Ansible
----------

```
pip3 install ansible==2.10.4
```

Create the inventory file
----------

Let’s create the inventory or CMDB file for ansible using the following command

```
cat > inventory.ini <<EOL

# DevSecOps Studio Inventory
[devsecops]
devsecops-box-XqiHnDZ0

[prod]
prod-XqiHnDZ0 ansible_python_interpreter=/usr/bin/python3

EOL
```

> Did you see ansible_python_interpreter=/usr/bin/python3? figure out why its used


Next, we will have to ensure the SSH’s yes/no prompt is not shown while running the ansible commands, so we will be using ssh-keyscan to capture the key signatures beforehand.

```
ssh-keyscan -t rsa prod-XqiHnDZ0 devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
```

Run the ansible commands
----------

Let’s run the ansible ad-hoc command to check if the production machine has docker installed.

Let’s use the shell module of ansible to run the docker version command on the production machine.

```
ansible -i inventory.ini prod -m shell -a "docker version"
```
output
```
prod-XqiHnDZ0 | CHANGED | rc=0 >>
Client: Docker Engine - Community
 Version:           20.10.6
 API version:       1.41
 Go version:        go1.13.15
 Git commit:        370c289
 Built:             Fri Apr  9 22:46:01 2021
 OS/Arch:           linux/amd64
 Context:           default
 Experimental:      true

Server: Docker Engine - Community
 Engine:
  Version:          20.10.6
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.13.15
  Git commit:       8728dd2
  Built:            Fri Apr  9 22:44:13 2021
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.4.4
  GitCommit:        05f951a3781f4f2c1911b05e61c160e9c30eaa8e
 runc:
  Version:          1.0.0-rc93
  GitCommit:        12644e614e25b05da6fd08a38ffa0cfe1903fdec
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

As you can see, we got the output of docker version from the production machine.

Build the image
----------

Before we deploy the container, we need to build the docker image first and store it in the docker registry.

Let’s SSH into the production machine.

```
ssh root@prod-XqiHnDZ0
```
Next, clone django.nv from git repository.
```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv.git
```
Let’s cd into the django.nv directory so we can run the application.
```
cd django.nv
```
Next, let’s create the django.nv application’s docker image.
```
docker build -t registry-XqiHnDZ0.lab.practical-devsecops.training/django.nv:1.1 .
```

> Please refer to Docker Registry exercise if you are not comfortable working with Docker registry.

We’re tagging the image with the registry location and the version(1.1). In the above command, we are using the shorthand instead of running two different commands, i.e., docker build and docker tag.

After the build finishes, we can push the image into the registry using the following command.

```
docker push registry-XqiHnDZ0.lab.practical-devsecops.training/django.nv:1.1
```
If you try to push this image, you will get an error no basic auth credentials as we are not authenticated to the registry. Let’s use the docker login command to login.

```
docker login --username root registry-XqiHnDZ0.lab.practical-devsecops.training
```
And type pdso-training as the password to login

If you try to rerun the previous command, you will see that the image push did complete.

```
docker push registry-XqiHnDZ0.lab.practical-devsecops.training/django.nv:1.1
```

Exit from the production machine.

```
exit
```
Run the Ansible playbook
----------------------------------------------------------------

Let’s create a playbook to deploy our newly created django.nv docker image to the production environment.

```
cat > playbook.yml <<EOL
---
- name: Deploy container using Ansible
  hosts: prod
  remote_user: root
  gather_facts: no

  vars:
    state: present

  tasks:
  - name: Ensure docker is installed
    stat:
      path: "/usr/bin/docker"
    register: docker_result

  - debug:
      msg: "Please install the docker"
    when: not docker_result.stat.exists

  - name: Pull new image
    docker_image:
      name: "registry-XqiHnDZ0.lab.practical-devsecops.training/django.nv:1.1"
      source: pull

  - name: Stopped container
    docker_container:
      name: "django.nv"
      state: absent

  - name: Run a new container
    docker_container:
      name: "django.nv"
      image: "registry-XqiHnDZ0.lab.practical-devsecops.training/django.nv:1.1"
      detach: yes
      ports:
        - 8000:8000
EOL
```

> Reference: https://docs.ansible.com/ansible/latest/scenario_guides/guide_docker.html.

Lets run this playbook against the prod machine.

```
ansible-playbook -i inventory.ini playbook.yml
```
output
```
PLAY [Deploy container using Ansible] ******************************************************************************

TASK [Ensure docker is installed] **********************************************************************************
The authenticity of host 'prod-xqihndz0 (10.192.38.66)' can't be established.
ECDSA key fingerprint is SHA256:1W7eyPFe8dx0BOFVbQvOUDsEAzqJLQw+YiZhITXIKSI.
Are you sure you want to continue connecting (yes/no)? yes
ok: [prod-XqiHnDZ0]

TASK [debug] *******************************************************************************************************
skipping: [prod-XqiHnDZ0]

TASK [Pull new image] **********************************************************************************************
fatal: [prod-XqiHnDZ0]: FAILED! => {"changed": false, "msg": "Failed to import the required Python library (Docker SDK for Python: docker (Python >= 2.7) or docker-py (Python 2.6)) on prod-XqiHnDZ0's Python /usr/bin/python3. Please read the module documentation and install it in the appropriate location. If the required library is installed, but Ansible is using the wrong Python interpreter, please consult the documentation on ansible_python_interpreter, for example via `pip install docker` or `pip install docker-py` (Python 2.6). The error was: No module named 'requests'"}

PLAY RECAP *********************************************************************************************************
prod-XqiHnDZ0              : ok=1    changed=0    unreachable=0    failed=1    skipped=1    rescued=0    ignored=0
```
The output shows us an error about Python module called docker-py, we need to install it in our production machine. SSH again into the production machine.

```
ssh root@prod-XqiHnDZ0
```
Then install the python library.
```
pip3 install docker-py
exit
```
If we execute the previous ansible command, we will see the following output.

```
ansible-playbook -i inventory.ini playbook.yml
```
output
```
PLAY [Deploy container using Ansible] ******************************************

TASK [Ensure docker is installed] **********************************************
ok: [prod-STUDENT_ID]

TASK [debug] *******************************************************************
skipping: [prod-STUDENT_ID]

TASK [Pull new image] **********************************************************
ok: [prod-STUDENT_ID]

TASK [Stopped container] *******************************************************
[DEPRECATION WARNING]: The container_default_behavior option will change its
default value from "compatibility" to "no_defaults" in community.general 3.0.0.
 To remove this warning, please specify an explicit value for it now. This
feature will be removed from community.general in version 3.0.0. Deprecation
warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [prod-STUDENT_ID]

TASK [Run a new container] *****************************************************
changed: [prod-STUDENT_ID]

PLAY RECAP *********************************************************************
prod-STUDENT_ID              : ok=4    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

You can verify the new image is deployed on the production using the ansible ad-hoc command.

```
ansible -i inventory.ini prod -m shell -a "docker ps"
```
output

```
prod-XqiHnDZ0 | CHANGED | rc=0 >>
CONTAINER ID        IMAGE                                                                  COMMAND                  CREATED             STATUS
    PORTS                    NAMES
c40eb809a416        registry-XqiHnDZ0.lab.practical-devsecops.training/django.nv:1.1   "/app/run_app_docker…"   36 seconds ago      Up 35 seconds       0.0.0.0:8000->8000/tcp   django.nv
```
Awesome! we managed to deploy an app to another machine.

> Think, how this would look like in a CI/CD setup.



