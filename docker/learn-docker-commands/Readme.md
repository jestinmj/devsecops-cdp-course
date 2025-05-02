Docker Command Basics
================================================================

We will learn the basic commands of docker
----------------------------------------------------------------

In this scenario, you will learn how to operate the containers using Docker.

Pull the image
----------

pull is an argument to download the docker image from the docker registry, its similar to git repository but designed to store the docker images than the code.

By default, the docker command will pull the image from DockerHub. When you do a pull, if the tag/version is not given for an image, the docker daemon assumes the latest tag by default.

```
docker pull ubuntu
```

You will see the following output for the docker pull command. If you wish, you can hide the output with an extra argument called –quiet or -q.

```
docker pull -q alpine
```

Run the image
----------------------------------------------------------------

run is an argument to start a container from the docker image. There are a lot of options that we can use, such as a name for the container, bind port, and so on.

For example, we can run a container in the background using -d option and give it a name using –name option.

```
docker run -d --name myubuntu ubuntu
```

The container will start/run in the background, but if you list the containers with docker ps, you won’t find the container with myubuntu name.

Why? Because there is no process attached to the container so it will exit as soon as it starts with the status exited. To keep the container running, we can add the -interactive or -i argument.

```
docker run -d --name myubuntu -i ubuntu
```

If you run the above command, it will raise an error as we are using the same container name as before.

How do we fix this? We can run the docker rm command to remove the previous container. 

```
docker rm myubuntu
```

Let’s re-run the myubuntu interactive command. 

```
docker run -d --name myubuntu -i ubuntu
```

Lets run docker ps command to see if myubuntu container is still running or not. 
As you can see, the container is still running.

Run a command in a running container
----------

exec is an argument to execute a command inside a container or to get the shell in the container.

```
docker exec myubuntu whoami
docker exec myubuntu cat /etc/lsb-release
```

Or you can also spawn a shell in the container.

```
docker exec -it myubuntu bash
```
![image](https://github.com/user-attachments/assets/eff5ff04-170e-4e37-811e-6512833f60f7)

As you can see, we are dropped into a bash shell. Let’s exit out of it using exit command. 

```
exit
```

List containers
----------

ps is an argument to list containers (running form of images). It provides various options to filter the output according to the status of the container like created, running, exited, or stopped etc.

Let’s run a container that exits and see if -a options shows us the container’s status.

```
docker run -d --name yourubuntu ubuntu
docker ps -a
```

As you can see, the above output shows all containers of status included, exited, or stopped.

What happens if you use th above command without -a?

Show the running processes of a container
----------

top is an argument to display the running processes inside a container.

```
docker top myubuntu
```

Exercise
----------

1. How can you run the nginx container in the background?
2. Give the container a name such as webserver and add any environment variables into it
3. Don’t forget to bind container port to the host as port 80 so you can access it through this url

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

> Hint
>
> To add environment variables refer to - [set environment variables](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file)
>
> For examples related to port binding refer to - [publish or expose port](https://docs.docker.com/engine/reference/commandline/run/#publish-or-expose-port--p---expose)


Additional Resources
----------

For more information about Docker commands, see the following references:

- https://docs.docker.com/engine/reference/commandline/pull
- https://docs.docker.com/engine/reference/commandline/run
- https://docs.docker.com/engine/reference/commandline/exec
- https://docs.docker.com/engine/reference/commandline/ps

