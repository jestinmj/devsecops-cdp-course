Docker Compose
===============

We will learn the basic of Docker Compose
--------------------------------------------------------

In this scenario, you will learn how to operate the containers using Docker.

Introduction
---------

In the previous exercise, we’ve learned the basic usage of Docker containers such as: how to manage data, networking, registry, and so on.

Now, we will discuss about Docker Compose. This tool allows us to handle multiple containers using a single file called docker-compose.yml.

Before moving forward, we need to know what are the differences between Docker and Docker Compose.

Let’s take an example to understand the differences.

First, we will try to run a container using docker run command.

```
docker run -d --name ubuntu -i ubuntu:18.04
```
Next, lets accomplish the above task using Docker Compose. Can we just change the docker command to docker-compose command to make it work? No, because Docker Compose expects a docker-compose.yml YAML file containing the above instructions in a pre-defined format.

```
cat >docker-compose.yml<<EOF
version: "3"
 
services:
  ubuntu:
    image: ubuntu:18.04
    stdin_open: true        # the same way like docker run -i
EOF
```

As you can see in the above docker-compose.yml file, we are creating a container called ubuntu using ubuntu:18.04(line number 6) image while keeping the stdin open(line number 7).

Let’s try running it using the following command.

```
docker-compose up -d
```
> You don’t need to define a file because by default docker-compose command will check if there is a docker-compose.yml file in the current working directory.

As you can notice in the above command output, the docker compose created a network during the provisioning.

We’ve run both containers using docker and docker-compose command, lets verify their behaviour using the docker ps command.

```
docker ps
```

output
```
CONTAINER ID   IMAGE          COMMAND       CREATED              STATUS              PORTS     NAMES
0fccd1d3f697   ubuntu:18.04   "/bin/bash"   About a minute ago   Up About a minute             default_ubuntu_1
f1074decc746   ubuntu:18.04   "/bin/bash"   About a minute ago   Up About a minute             ubuntu
```

did you notice the similarities? we created them using different approaches but we are seeing similar container behaviour.

Now, imagine you have to run 3 or more containers for an application/task in the same network. How you can achieve this task manually running the docker run command multiple times? Definitely not!

In this scenario, we should define your desired container behavior in the docker-compose.yml file and use docker compose to provision them.

In the next step, you will learn more things from Docker Compose

Compose file
---------

When you want to run/handle multiple containers, you would need to use docker-compose command and its YAML file instead of the docker command. As we have learned in the previous step, we just have to convert docker run command into a YAML file. This YAML file will will then be used by Docker Compose to manage the containers as per the instruction in the file.

Let’s explore the basic syntax used in the docker-compose.yml file

```
version: "3"

services:
  web:
    image: nginx
    container_name: webserver       # name of container
    ports:
     - "80:80"                      # similar to docker run -p 80:80
    environment:
     - NGINX_HOST=example.com       # similar to docker run -e VAR=value
    volumes:
     - ./:/var/www/html/app             # ./ means a bind mounts
     - image_data:/var/www/html/images  # image_data means use docker volume

volumes:
  image_data:                       # similar to docker volume create
```

The above docker-compose.yml has these instructions in it.

- version : Version of compose file format to use, check out this link
- image : Specify the image to run
- container_name 	Specify a custom container name, rather than a default name
- ports : Expose port(s), similar to docker run -p argument
- environment : Add environment variables into the container by defining a key-value pair
- volumes : Volumes to save our data persistently using various options type like bind or volumes

We have definitely used the above features(instructions) in our previous docker exercises via docker run arguments. However, using a docker-compose file is more efficient as we are declaring the desired behaviour using a file(IaC).

The container behaviour is definied inside the services: dictionary, without it you won’t be able to operate docker containers using docker-compose command such as run, stop, exec etc.

>  Learn more about compose command [here](https://docs.docker.com/compose/reference)

Now, lets create a compose file and paste the following code in it:

```
version: "3"

services:
  ubuntu:
    image: ubuntu:18.04
    volumes:
     - data:/opt

  alpine:
    image: alpine:3.13
    container_name: alpine
    volumes:
     - data:/tmp

volumes:
  data:
```

And execute the following command.

```
docker-compose up -d
```


Exercise
---------
1. Explain why these two containers have stopped (Exit 0)
2. Figure out how can you make the containers run indefinitely. Recall the techniqeus you have learned in Learn Docker Commands exercise
3. What does container_name line accomplish under the second container’s description (alpine) and why are we not using it in the first one (ubuntu)?
4. Create a random file inside the ubuntu container using docker-compose exec command and save it in /opt/hello.txt
5. Explain behind the scenes behavior of the above step

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

