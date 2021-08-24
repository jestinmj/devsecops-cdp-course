Run static analysis on Dockerfile
================================================================================

Learn how to run find common issues in Dockerfile
--------------------------------------------------------------------------------

In this scenario, you will learn how to install and run Docker best practices scans on a Dockerfile.

You will need to download the code, install the Hadolint tool and then finally run the static analysis scan on the Dockerfile.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp
cd webapp
```

Installing Hadolint
----------
> Hadolint checks a Dockerfile for Docker image best practices. The linter is parsing the Dockerfile into an AST and performs rules on top of the AST.
>
> You can find more details about the project at https://github.com/hadolint/hadolint.

Let’s install the Hadolint tool on the system to perform static analysis of Dockerfiles.

```
wget https://github.com/hadolint/hadolint/releases/download/v1.18.0/hadolint-Linux-x86_64
```
Let’s rename this file to make it easy for us to type it.

```
mv hadolint-Linux-x86_64 hadolint
chmod +x hadolint
./hadolint --help
```

Run the Hadolint on Dockerfile
--------------
As we have learned in DevSecOps best practices, always run and test a tool locally first, before putting it into a CI/CD pipeline.

```
./hadolint Dockerfile
```
output
```
Dockerfile:9 DL3018 Pin versions in apk add. Instead of `apk add <package>` use `apk add <package>=<version>
```
Hadolint ran successfully, and it found one issue i.e., we are not following the best practices for Dockerfile.

To fix this, you need to edit Dockerfile and add a specific version of the package.

Let’s check the contents of the Dockerfile using the cat command.
```
cat -n Dockerfile
```
> Pro-tip, -n options allows you to show line numbers.


```
     1  # FROM python base image
     2  FROM python:2-alpine
     3
     4  # COPY startup script
     5  COPY . /app
     6
     7  WORKDIR /app
     8
     9  RUN apk add --no-cache gawk sed bash grep bc coreutils
    10  RUN pip install -r requirements.txt
    11  RUN chmod +x reset_db.sh && bash reset_db.sh
    12
    13  # EXPOSE port 8000 for communication to/from server
    14  EXPOSE 8000
    15
    16  # CMD specifcies the command to execute container starts running.
    17  CMD ["/app/run_app_docker.sh"]
```

As per the Hadolint finding Dockerfile:9 DL3018 Pin versions in apk add., the Dockerfile line number 9 has a problem.

So let’s fix it.

> From
```
9  RUN apk add --no-cache gawk sed bash grep bc coreutils
```
> To
```
9  RUN apk add --no-cache gawk=5.0.1-r0 sed=4.7-r0 bash=5.0.11-r1 grep=3.3-r0 bc=1.07.1-r1 coreutils=8.31-r0
```

let's edit the dockerfile add these changes 
```
cat > Dockerfile <<EOL
# FROM python base image
FROM python:2-alpine

# COPY startup script
COPY . /app

WORKDIR /app

RUN apk add --no-cache gawk=5.0.1-r0 sed=4.7-r0 bash=5.0.11-r1 grep=3.3-r0 bc=1.07.1-r1 coreutils=8.31-r0
RUN pip install -r requirements.txt
RUN chmod +x reset_db.sh && bash reset_db.sh

# EXPOSE port 8000 for communication to/from server
EXPOSE 8000

# CMD specifcies the command to execute container starts running.
CMD ["/app/run_app_docker.sh"]
EOL
```
It’s time to run the Hadolint scan once again.

```
./hadolint Dockerfile
```
output
```
/webapp# ./hadolint Dockerfile
/webapp#
```

Hurray! no issues found.