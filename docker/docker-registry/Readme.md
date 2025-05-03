Docker Registry
================================

We will learn how to store the image on a private registry
---------

In this scenario, you will learn how to build, push and run the container image using Docker.

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, We need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv
cd django.nv
```

Build the image
----------

To build a docker image, we need a file called Dockerfile. This Dockerfile contains the instructions(blueprint) to create the image.

```
cat Dockerfile
---------
# FROM python base image
FROM python:3-alpine

# COPY startup script
COPY . /app

WORKDIR /app

RUN apk add --no-cache gawk sed bash grep bc coreutils
RUN pip install -r requirements.txt
RUN chmod +x reset_db.sh run_app_docker.sh && bash reset_db.sh

# EXPOSE port 8000 for communication to/from server
EXPOSE 8000

# CMD specifcies the command to execute container starts running.
CMD ["/app/run_app_docker.sh"]
```

The above Dockerfile has these instructions in it.

- From : Initialize an operating system as a base (image).
- COPY : Copy the files or directories from the host to the container
- WORKDIR : Sets the working directory in the container. Similar to the cd command on Linux
- RUN : Executes the commands in the current image

Next, we can create the image using the following command.

```
docker build -t django.nv:1.0 .
```

After the build finishes, we can see the newly created image using the following command

```
docker images
```

Store the docker image in the registry
---------

To store the image, we need the docker repository called registry. We can deploy a registry server locally using the following command.

```
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```
The purpose of this command is to run a Docker container from the official registry image, version 2, in detached mode, and configure it to:

1. Map port 5000 on the host machine to port 5000 in the container.
2. Restart the container automatically if it exits or crashes.
3. Assign a name to the container, registry, so it can be easily managed and stopped/restarted later.
   
In essence, this command sets up a Docker container that runs a Docker registry, which is a service that stores and manages Docker images. The --restart=always flag ensures that the registry will always be available, even in the event of a system restart or other unexpected shutdown.

> Deploy a registry server: https://docs.docker.com/registry/deploying.


After the registry is up, we can push the image(s), but we need to add the image name with the registry url as a prefix. e.g., REGISTRY_URL/IMAGE_NAME:IMAGE_TAG

```
docker tag django.nv:1.0 localhost:5000/django.nv:1.0

docker push localhost:5000/django.nv:1.0

curl localhost:5000/v2/_catalog
```
output
```
{"repositories":["django.nv"]}
```

As you can see above, the registry has the django.nv image. You can consume this image by pulling it from this registry.


Exercise: Store the docker image in registry
---------

For this exercise, use the Docker image we created in the previous task to store on Docker Hub.

1. Sign up for the Free Docker Hub Account here
2. Login using the above account details and use the docker login command on the DevSecOps-Box machine to login into the Docker Hub registry
3. Push/Upload django.nv:1.0 image you created in the above exercise to Docker Hub
4. Stop the registry container and remove the images to save the disk space

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

