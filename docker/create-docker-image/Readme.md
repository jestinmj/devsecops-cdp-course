Docker Image
================================

We will learn how to create docker image
------------------------------------------------

In this scenario, you will learn how to build a container image using Docker.

Download the source code
------------------------------------------------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, We need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv
cd django.nv
```

Build the image
----------------

To build a docker image, we need a file called Dockerfile that contains instructions to build the image.

```
cat Dockerfile
---
# FROM python base image
FROM python:2-alpine

# COPY startup script
COPY . /app

WORKDIR /app

RUN apk add --no-cache gawk sed bash grep bc coreutils
RUN pip install -r requirements.txt
RUN chmod +x reset_db.sh && bash reset_db.sh

# EXPOSE port 8000 for communication to/from server
EXPOSE 8000

# CMD specifcies the command to execute container starts running.
CMD ["/app/run_app_docker.sh"]
```

Next, we can create the image using the following command.

```
docker build -t django.nv:1.0 .
```

After the build finishes, we can see the image using the following command.

```
docker images
```

As you can see above on line number 2, there is a django.nv image with TAG as 1.0.

Exercise: Create a docker image
----------------

1. Rename the docker image django.nv:1.0 to django.nv:1.1
2. Override Entrypoint to run a bash shell (/bin/bash)
    Delete the docker image django.nv:1.0


> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).


> Hint
>
> We can override entrypoint in two ways. One by overriding entrypoint. Try to run this command docker run --help then have a look at the option for entrypoint. Second, you can edit the Dockerfile and override ENTRYPOINT.