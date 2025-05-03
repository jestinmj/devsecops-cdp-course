Manage Data in Docker
=========================

We will learn about managing data in docker with various options
----------

In this scenario, you will learn how to manage data in Docker containers.

Docker volumes
----------

At one time, we will need to add persistent data in Docker containers, since the containers is flexible can running as stateless also stateful workloads. So we will learn how to manage our data using Docker with various options like Volumes, Bind mounts, and tmpfs. Which option should we select when we need to run containers that require persistent data?

There is a similarity between Volumes and Bind mounts, both of them can save your data persistently but how the mechanism look like?

Let’s try it with the docker volume command that provided to doing those things.

```
docker volume --help
```
output
```
Usage:  docker volume COMMAND

Manage volumes

Commands:
  create      Create a volume
  inspect     Display detailed information on one or more volumes
  ls          List volumes
  prune       Remove all unused local volumes
  rm          Remove one or more volumes

Run 'docker volume COMMAND --help' for more information on a command.
```

List available volume on the system.

```
docker volume ls
```
It’s empty because we did not run any containers that use volumes. Let’s try to create a new volume called demo.
```
docker volume create demo
```
Execute the previous command once again to list the volumes. Now you will see our volume is created and it’s located in our system in /var/lib/docker/volumes/.
```
ls /var/lib/docker/volumes/
```
output
```
demo  metadata.db
```
So it means docker volume command has created a new directory in our system. How can we know if our container saved the data persistently even after our container is killed?

Let’s run a container with the following command to use our volumes.

```
docker run --name ubuntu -d -v demo:/opt -it ubuntu:18.04
```
Enter to the containers shell.
```
docker exec -it ubuntu bash
echo "Hello from the containers" > /opt/hello.txt
docker rm -f ubuntu
```

> Can you figure it out what’s happen on hello.txt file when we’re remove the containers?
> 
> The file is not deleted. Why? Because the file is saved on the host system.

```
ls /var/lib/docker/volumes/demo/_data/
```
output
```
hello.txt
```

If you create a file outside /opt directory it will be removed because we only mount a volumes to /opt directory.

Next, we can also use existing volumes to be attached to new containers with a different path.

```
docker run --name ubuntu1 -d -v demo:/tmp -it ubuntu:20.04
```
![image](https://github.com/user-attachments/assets/112a170a-ff32-4e7b-bd3f-ef6bc9f73a1b) need to run a command that requires user input or wants to the the output in real-time.

In summary, this command runs a detached Ubuntu 20.04 container, mounts a volume from the host machine to the container's /tmp directory, and allocates a pseudo-TTY for interactive use.


Look at /tmp directory in the containers, and you will see hello.txt file there.

> Learn more about docker volumes [here.](https://docs.docker.com/storage/volumes/)

Bind mounts
----------

The second option is bind mounts, and we don’t need to use docker volume command to create volumes as in the previous steps. Let see what the following command does.

```
docker run --name ubuntu2 -d -v /opt:/opt -it ubuntu:18.04
docker exec -it ubuntu2 bash
ls /opt
```
Why there is a directory called containerd? The previous one doesn’t showing this. Let’s exit from the containers and look at to docker volume directory if there is any directory there.

```
ls /var/lib/docker/volumes
```
The output still same, doesn’t give us information about containerd directory or volumes that created by docker. How about /opt directory on the host system?
```
ls /opt
```

Great! so that is the directory comes from. Because we use bind mounts and it will mapping our host directory to the containers with specific location that defined when to run the containers -v /opt:/opt.

Next, create a file on the host system in /opt called hello.txt.

```
echo "Hello from the host" > /opt/hello.txt
```

Remove the old containers with docker rm options, and start a new container with the same command.

```
docker rm -f ubuntu2
docker run --name ubuntu2 -d -v /opt:/opt -it ubuntu:20.04
```
Then, you can use docker exec command to get a shell into the container and validate /opt/hello.txt file inside of it.

```
docker exec -it ubuntu2 bash
ls /opt
```
output
```
root@70c10b31c605:/# ls /opt
containerd  hello.txt
```
The file success to mapped into the containers. What’s happen when we remove it from the containers?
```
rm /opt/hello.txt
```
Exit from the containers and check /opt directory on the host, the file we saved inside the container would have been removed as well. It means when we’re using the volume mount option, any files in containers are the same as those on the host. Though we’re adding, editing, or removing files inside the container, they are removed from the host as well.

> When do you use bind mounts? in development or production stage ?
https://docs.docker.com/build/building/best-practices/

> Share the answer with the staff.
>
> Learn more about bind mounts here.

tmpfs
---------

This type of mount will not save the data persistently, because it uses host’s RAM as a temporary storage.

> Learn more about tmpfs mounts [here](https://docs.docker.com/storage/tmpfs/)


Exercise
---------
1. Create a file at /opt with the name as hello.txt with any text
2. Mount the file as bind mounts inside ubuntu:18.04 container at /src
3. Create a new volume called data with docker volume command
4. Run an another ubuntu:18.04 container, then mount the data volume into the container at /src, and create a file /src/hello.txt in container with any text
5. What happens to the hello.txt file when we remove both the containers? Provide an explanation.

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).
