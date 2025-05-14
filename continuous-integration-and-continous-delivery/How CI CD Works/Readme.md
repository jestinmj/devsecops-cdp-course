## How CI/CD Works

# Introduction to CI/CD System
A CI/CD system, which stands for Continuous Integration/Continuous Deployment, is a way to automate software development. It helps make building, testing, and deploying apps easier. This allows developers to work more efficiently and release updates faster while keeping the code reliable and high-quality.

In a CI/CD workflow, developers often add their code changes to a shared repository. This starts an automatic process that builds the code, runs tests, and finds any problems. By catching issues early, teams can fix bugs quickly and avoid conflicts between different parts of the code.

When the code passes all tests, the CI/CD system automatically sends the changes to different environments like development, testing, and production. This ensures the app is deployed consistently and reliably, while reducing manual work and human errors in the process.

To set up a CI/CD system, developers use various tools and technologies. These include version control systems like Git, build servers such as Jenkins, automated testing tools, and deployment automation software. All these tools work together to automate different stages of the development and deployment process.

Let’s move to the next step.

# Understanding GitLab CI/CD
In this exercise, we will use GitLab as our CI/CD system because it is popular and easy to use. By learning the basics of YAML files, you can also apply this knowledge to different CI/CD systems.

>> YAML (a recursive acronym for “YAML Ain’t Markup Language”) is a human-readable data serialization language. It is commonly used for configuration files and in applications where data is being stored or transmitted.

# How it Works
The first step in running the pipeline is to create the environment inside the GitLab CI/CD pipeline before the jobs start. As soon as the pipeline begins, the job pulls the Docker image to build the environment for the first time while the job is running.

The first step when running the pipeline is to create the environment inside the GitLab CI/CD pipeline before the jobs start running. As soon as the pipeline starts, the job will pull the docker image to build the environment for the first time while the job is running.

```
Running with gitlab-runner 16.4.0 (4e724e03)
  on gitlab-runner-77k0huze BxQ1DEzn, system ID: s_93fa9ab39c75
Preparing the "docker" executor 00:43
Using Docker executor with image docker:20.10 ...
Using helper image:  gitlab/gitlab-runner-helper:x86_64-latest  (overridden, default would be  registry.gitlab.com/gitlab-org/gitlab-runner/gitlab-runner-helper:x86_64-4e724e03 )
Pulling docker image gitlab/gitlab-runner-helper:x86_64-latest ...

...[SNIP]...
```
> The executor in GitLab CI/CD refers to the environment where the CI/CD pipelines run and execute jobs. It determines where and how the jobs defined in your GitLab CI/CD configuration file are executed.
> GitLab provides different executor options to choose from based on your needs. Each executor has its own capabilities, requirements, and usage scenarios.

Next, you will see that the next process is getting the sources from Git repository.
```
...[SNIP]...

$ rm -f .git/index.lock
Fetching changes with git depth set to 20...
Initialized empty Git repository in /builds/BxQ1DEzn/0/root/django-nv/.git/
Created fresh repository.
Checking out 8ee7dc23 as detached HEAD (ref is main)...
Skipping Git submodules setup

...[SNIP]...
```

While reading the sources, the next step is to execute the scripts that we have defined in .gitlab-ci.yml file.
```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

job:
  stage: build
  script:
    - echo "I'm a job"

```

Afterwards, the process will be displayed as it appears at the end of the job, as shown below:
```
...[SNIP]...

Executing "step_script" stage of the job script 00:01
Using docker image sha256:ed9a10a5bc310dfdad94ab737c61698d5a5bc8074a039804531452fe19200896 for docker:20.10 with digest docker@sha256:2967f0819c84dd589ed0a023b9d25dcfe7a3c123d5bf784ffbb77edf55335f0c ...
$ echo "I'm a job"
I'm a job
Job succeeded
```

You can see that the instruction echo “I’m a job” is reflected in the pipeline. This means that anything inside the script attribute will be executed by GitLab Runner.

Let’s attempt to customize the script to execute any command of our choosing.

Edit .gitlab-ci.yml file content inside the project and copy the below code by clicking on the Edit button or visiting this link

```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

job:
  stage: build
  script:
    - echo "I'm a job"
    - whoami
    - hostname
```

Check the last pipeline and click on the appropriate job name.

You will see that the output is the same as what we have in the repository. Why? By default, GitLab Runner will clone the repository itself as the working directory, so you no longer need to add the git clone command inside the configuration file (.gitlab-ci.yml).

```
...[SNIP]...

$ echo "I'm a job"
I'm a job
$ whoami
root
$ hostname
runner-bxq1dezn-project-2-concurrent-0
Job succeeded
```

If we see the output of the two commands we added, it appears that the instructions are being executed within containers. How did we come to know that it runs on top of a container?

You can add `cat /proc/self/mountinfo` command after hostname.

Once done, please click on the appropriate job name, and you will see the following output.
```
...[SNIP]...

$ cat /proc/self/mountinfo
7975 7553 0:510 / / rw,relatime master:3409 - overlay overlay rw,lowerdir=/var/lib/docker/overlay2/l/N2DAW4RT2JYC6D3QXQZMPQOI5D:/var/lib/docker/overlay2/l/WVUBAR2L2RBICUEXPFEGR2UNGJ:/var/lib/docker/overlay2/l/CYJQ4CSL5AYWCLUIFWJAM752SW:/var/lib/docker/overlay2/l/KTSMLJMG6YGPS74FO5U4GHVB4A:/var/lib/docker/overlay2/l/77EE4NHWL47MD5DBY4YVD3MHMD:/var/lib/docker/overlay2/l/65SV6UCPHFRP22XOF5VHIILF2H:/var/lib/docker/overlay2/l/E7TJ4ZFTNEIQVL23VPJO5TCQBE:/var/lib/docker/overlay2/l/KOVW7V7D4F4QKYDO4OS6GPQPPI:/var/lib/docker/overlay2/l/HNANG2WE43S7HAUSJPAXWJEH3M:/var/lib/docker/overlay2/l/U4GHHJ5XGOF6PJQGWKFUM35WXF,upperdir=/var/lib/docker/overlay2/3ce7ad96882801b5d4bbecddf615e55c25563bf2eaac356be71c38f5c5865a6d/diff,workdir=/var/lib/docker/overlay2/3ce7ad96882801b5d4bbecddf615e55c25563bf2eaac356be71c38f5c5865a6d/work,userxattr
7977 7975 0:513 / /proc rw,nosuid,nodev,noexec,relatime - proc proc rw
7978 7977 0:419 /proc/swaps /proc/swaps rw,nosuid,nodev,relatime - fuse sysboxfs rw,user_id=0,group_id=0,default_permissions,allow_other
7979 7977 0:419 /proc/sys /proc/sys ro,nosuid,nodev,relatime - fuse sysboxfs rw,user_id=0,group_id=0,default_permissions,allow_other
7980 7977 0:419 /proc/uptime /proc/uptime rw,nosuid,nodev,relatime - fuse sysboxfs rw,user_id=0,group_id=0,default_permissions,allow_other
7981 7977 0:425 /bus /proc/bus ro,nosuid,nodev,noexec,relatime - proc proc rw

...[SNIP]...
Job succeeded
```

You don’t need to explore this further, but it will provide you with some information on how we identify the commands in the configuration file that are running on the container behind the scenes.

Let’s move to the next step.

# Running Jobs in Docker Containers
In the Docker exercise, we learned how to use Docker through the command line and its various options. Now, we’ll apply this knowledge to CI/CD. But first, we need to understand how the image attribute is used in different scenarios.

Let’s replace the existing CI/CD pipeline by copying the following content:
```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

job:
  stage: build
  image: python:3.6
  script:
    - pip install -r requirements.txt
```

Click the Commit changes button and go back to the pipeline page. The change will display the output below in the pipeline.

```
...[SNIP]...
$ pip install -r requirements.txt
Collecting Django==3.0
  Downloading Django-3.0-py3-none-any.whl (7.4 MB)
Collecting pytz
  Downloading pytz-2023.3.post1-py2.py3-none-any.whl (502 kB)
Collecting sqlparse>=0.2.2
  Downloading sqlparse-0.4.4-py3-none-any.whl (41 kB)
Collecting asgiref~=3.2
  Downloading asgiref-3.4.1-py3-none-any.whl (25 kB)
Collecting typing-extensions
  Downloading typing_extensions-4.1.1-py3-none-any.whl (26 kB)
Installing collected packages: typing-extensions, sqlparse, pytz, asgiref, Django
Successfully installed Django-3.0 asgiref-3.4.1 pytz-2023.3.post1 sqlparse-0.4.4 typing-extensions-4.1.1
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
WARNING: You are using pip version 21.2.4; however, version 21.3.1 is available.
You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.
Job succeeded
```

Now, let’s compare the previous YAML file with the new one:

```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

job1:
  stage: build
  image: python:3.6
  script:
    - pip install -r requirements.txt

job2:
  stage: build
  script:
    - apk add python3 py3-pip
    - pip install -r requirements.txt
```
Can you identify the differences between job1 and job2?

The command appears similar, but if you observe closely, job1 uses the image attribute, whereas job2 does not define it. Instead, it uses the - apk add python3 py3-pip command to install pip.

> Reference: https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#what-is-an-image.

You might be wondering why we need to install the python3-pip package in job2. This is because if no image attribute is defined, it will use the default image that is defined at the top of the configuration file, which is image: docker:20.10. The image is based on Alpine Linux, and the package manager used is apk.

# Docker-in-Docker in GitLab

Docker-in-Docker (DinD) is a feature in GitLab that allows you to run Docker containers inside a Docker container. DinD enables you to use the full capabilities of Docker in your GitLab CI/CD pipelines.

When using DinD, GitLab creates a virtual Docker environment within your pipeline job. This allows you to build, test, and deploy applications using Docker commands. It provides an isolated Docker runtime environment where you can run containers, build images, and execute tasks that require Docker functionality.

DinD is useful when you need to perform tasks like building and pushing Docker images, running Dockerized tests, or deploying applications using Docker. It allows you to replicate the same Docker environment within your pipeline as you would have on your local machine or a dedicated Docker host.

To use DinD in GitLab CI/CD pipelines, you simply need to configure your pipeline job to use the Docker image available at https://hub.docker.com/_/docker. You can choose the specific version you need.

We have already learned about DinD in the previous step. Now, we will explore it further within the CI/CD system.

These are the last changes we made in the pipeline:
```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

job1:
  stage: build
  image: python:3.6
  script:
    - pip install -r requirements.txt

job2:
  stage: build
  script:
    - apk add python3 py3-pip
    - pip install -r requirements.txt
```

Let us try to see how the docker:20.10 image can be used to operate Docker inside the pipeline.

Please copy the following content and replace it in your .gitlab-ci.yml file.
```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

job1:
  stage: build
  script:
    - docker version
```

Check the last pipeline and click on the appropriate job name.
![image](https://github.com/user-attachments/assets/4b7bc581-879b-44c9-8329-529467118f07)

That is interesting! The docker command is available in the pipeline, and we can use it to minimize the installation of any tools we need to run in the CI/CD system. Let’s take an example of using the safety tool, which we will cover in a separate exercise.

Use the following content in your .gitlab-ci.yml file.

```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

job1:
  stage: build
  script:
    - docker run --rm -v $(pwd):/src hysnsec/safety check -r /src/requirements.txt --json
```
![image](https://github.com/user-attachments/assets/33bcc39d-4a80-4bb8-8d02-16dc59376dfb)

The purpose is the same as the code snippet below.
![image](https://github.com/user-attachments/assets/5b613176-bb2c-48ac-ab6d-5cf6a2715c1a)

# Shared Runner
> A Shared Runner in GitLab is a resource that multiple projects can use to run their CI/CD pipelines. It provides a centralized execution environment, eliminating the need for each project to have dedicated resources. Shared Runners are configured at the GitLab instance level and can be shared across different projects within that instance. They allow projects to use the same CI/CD infrastructure, taking advantage of shared computing power and resources.

 ![image](https://github.com/user-attachments/assets/368f6a5e-4698-47bf-b54a-bd63c6a32f66)
 
![image](https://github.com/user-attachments/assets/7a3291e4-1610-4ad0-bb3b-f2e041aa7abd)

 
