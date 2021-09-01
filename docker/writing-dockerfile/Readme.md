Dockerfile
================================================================


We will learn the basics of writing a Dockerfile
--------------

In this scenario, you will learn how to write a Dockerfile.

Dockerfile Introduction
----------

> Docker CLI can build images automatically by reading the instructions from a Dockerfile. A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image. Using docker build, a user can create an automated build that executes several command-line instructions in succession.
> 
> Source: https://docs.docker.com/engine/reference/builder/

First, we need to know the syntax of Dockerfile to create our custom image from scratch. Let’s have a look at the following list:

- FROM: Creates a layer from Docker Image. Specifies the base image to use.
- COPY: Copies the files from the local directory to the docker image on a specific location.
- ADD: Similar to COPY but supports file download (HTTP), auto extracting compressed file(s), and replacing the existing file to a specific location if needed forcefully.
- RUN: Run OS command (just like you would do on a terminal) but only executes it during the image creation process.
- ENTRYPOINT: Run a command as the default command when the container starts. Its the entrypoint to the utility/command.
- CMD: Command to run when a container starts or arguments to ENTRYPOINT if specified.

These are the standard instructions used while creating a docker image.

>     Pro-tip: We are often asked what is the difference between CMD and ENTRYPOINT. This [Blog](https://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/) post explains the major differences between them.

We will try to build a Docker image with Ubuntu 18.04 as the base image. We will also install a web server in it.

Create a new file called Dockerfile under learn-dockerfile directory.

```
mkdir learn-dockerfile
cd learn-dockerfile
touch Dockerfile
```

Use any text editor of your choice like vim/nano to add the following content to the Dockerfile.

```
FROM ubuntu:18.04

RUN apt install nginx
```
As mentioned before, we run the OS command(s) available in Dockerfile to install the Nginx server. Let’s try to build the image.

```
docker build -t nginx-custom .
```

Interesting, why the image build process failed? Because we didn’t do apt update before installing the package. Hence the error E: Unable to locate package nginx.

Let’s try to update our Dockerfile.

```
FROM ubuntu:18.04

RUN apt update && apt install nginx
```
Re-build the image, and it will show another error.

When we create an image with Dockerfile, all instructions are run non-interactively; so, we can’t respond to the prompt when asked about any confirmation, including the Y/n question.

Luckily the apt command supports non-interactive package installation using the -y option.

```
apt install -y nginx
```

Great, we managed to create an image with the name nginx-custom:latest. To verify the image creation process was successful, we can use the docker images command.

```
docker images
--------------------
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE

nginx-custom        latest              6c54510dea11        44 seconds ago      159MB

ubuntu              18.04               c090eaba6b94        11 hours ago        63.3MB
```
As you can see above(line number 2), the nginx-custom image was created 44 seconds ago.

Working with Containers and Dockerfile
----------

In the previous step, we have learned the basic syntax of Dockerfile. Sometimes, it’s faster to create a container using an image as a base and add extra layers on top using the RUN commands. Once we are happy with the results, we can create a Dockerfile.

Let’s create a container using the ubuntu:18.04 image.

```
docker run -d --name ubuntu -it ubuntu:18.04
```
Use the docker exec command to start the Bash process inside the container (imagine it as though you are logging into a container).
```
docker exec -it ubuntu bash
```
Now, we are in the Ubuntu container. Let’s update the apt cache.

```
apt udpate
```
Then install the nginx package.
```
apt install -y nginx
```
OK, we installed the nginx webserver. We would want to start the nginx service, but how should we do that?

```
service nginx start
```
Great, our web server is running. We can verify it by requesting a webpage from our local container using the curl command.
```
apt insstall curl
curl localhost
```
output
```
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```
Great, this confirms that we are running an Nginx service.

Please take note of the previous commands, as we will be using them to create a Dockerfile.

```
FROM ubuntu:18.04

RUN apt update && apt install nginx -y
```
The above file is our previous Dockerfile. Do you think we can just add service nginx start into the Dockerfile?

Yes, we can do it. However, our custom image still won’t start the service. The reason being, we didn’t put the command in either CMD or ENTRYPOINT instructions.

As mentioned before, CMD/ENTRYPOINT instruction will execute the command at the end of the container start process.

```
FROM ubuntu:18.04

RUN apt update && apt install nginx -y

CMD ["/bin/bash", "-c" , "service nginx start"]
```

Let’s go ahead and build the image using the above Dockerfile.
```
docker build -t custom-nginx .
docker run -d -it custom-nginx
docker ps -a
```
output
```
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS                      PORTS               NAMES
3ab72b7d91fe        custom-nginx        "/bin/bash -c 'servi…"   4 seconds ago        Exited (0) 3 seconds ago                        blissful_hugle
```

As you can see, our container has Exited. We can see the logs to ascertain what went wrong using the docker logs command.

```
docker logs CONTAINER_ID
----------
 * Starting nginx nginx                                            [OK]
```
Looks fine. Can you fix it without looking at the solution on the next page?

> Reference: https://stackoverflow.com/questions/42218957/dockerfile-cmd-instruction-will-exit-the-container-just-after-running-it

Advanced Dockerfile
----------

An easy fix is to add sleep after the service command using CMD instruction.

If everything goes well, our container should run without issuing the Exited status.

> Read more: https://docs.docker.com/engine/reference/run/

Edit Dockerfile with your favorite text editor like vim/nano and paste the following code in your Dockerfile.

```
FROM ubuntu:18.04

RUN apt update && apt install nginx -y

CMD ["/bin/bash", "-c" , "service nginx start"]
CMD [";sleep infinity"]
```
We’re trying to add another CMD instruction to execute the command; however, we got another error now

output
```
d66fcdb905b0b449e555be59c820413e357ef23eead9ac8858b7002a5c73b3af
ddocker: Error response from daemon: OCI runtime create failed: container_linux.go:349: starting container process caused "exec: \";sleep infinity\": executable file not found in $PATH": unknown.
```
It seems only the last cmd was invoked. If more than one CMD instruction is specified, only the last CMD instruction is considered, so let’s move our sleep command on the same CMD line.

```
CMD ["/bin/bash", "-c" , "service nginx start; sleep infinity"]
```

Re-build the image, then run the image. It should work fine now.

sleep infinity tells the container to keep the process alive. It’s crude, but it gets the job done. There are several other approaches to keep our container process alive, and we have picked the easiest of them all.

Please refer to the following link to explore other approaches.

> Read more [here](https://docs.docker.com/config/containers/multi-service_container)


Now, let’s explore the difference between CMD and ENTRYPOINT.

```
FROM ubuntu:18.04

RUN apt update && apt install nginx -y

ENTRYPOINT ["/bin/bash", "-c"]

CMD ["service nginx start; sleep infinity"]
```

With ENTRYPOINT, we set the image’s default command when running a container. What does it mean?

Please have a look at the CMD instruction in the above Dockerfile. The instruction is executing a service command followed by the sleep command. What would happen if we remove sleep infinity command in CMD?

Let’s remove sleep infinity from the CMD instruction altogether, re-build the image and run the image with the following command.

```
docker run -d --name nginx -it nginx-custom
docker ps
```
>  Analyze why the container is not alive?

Run the same image using a different name (remember –name option?) with a bash towards the end.

```
docker run -d --name nginx-one -it nginx-custom bash
docker ps
```

> The second container is alive. Why?
>
> Please do not forget to share the answer with our staff via Slack Direct Message (DM).


Additional Resources
----------

For more information about Dockerfile syntax, see:

- https://docs.docker.com/engine/reference/builder
- https://docs.docker.com/develop/develop-images/dockerfile_best-practices

