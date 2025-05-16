How to Embed Safety into GitLab
================================================

Use Safety tool to do OAST in CI/CD pipeline
----------------------------------------------------------------

In this scenario, you will learn how to embed the OAST tool in CI/CD pipeline.

You will learn to use Safety in CI/CD pipeline and allow the job to fail even when the tool found several issues.

Once you click the Start the Exercise button, you will need to wait 2 minutes for the GitLab machine to start.

A simple CI/CD pipeline
----------

Considering your DevOps team created a simple CI pipeline with the following contents. Please add the Safety scan to the below Gitlab CI Script.

```
image: docker:latest

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

build:
  stage: build
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py check

test:
  stage: test
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py test taskManager
```

There are some jobs in the pipeline, and we need to embed the OAST tool in this pipeline.

Let’s login into GitLab using the following details and execute this pipeline once again.


Notes
---------

We need to share the project’s source code inside the container for it to access these files. We can do that using the -v option of the docker command.

```
-v $(pwd):/src
```

The above option mounts the current directory in the host (runner) to /src inside the container. This could also be -v /home/ubuntu/code:/src or c:\Users\student\code:/src if you were using windows.

Exercise
---------

Recall techniques you have learned in the previous module (Secure SDLC and CI/CD).

1. Create a job named oast in the test stage using the safety tool. Make sure you are using hysnsec/safety docker image for this task. Understand the use of Docker’s -v (volume mount) flag/option. Ensure you follow the DevSecOps Gospel and best practices while embedding the safety tool.
```
oast:
  stage: test
  script:
    # We are going to pull the hysnsec/safety image to run the safety scanner
    - docker pull hysnsec/safety
    # third party components are stored in requirements.txt for python, so we will scan this particular file with safety.
    - docker run --rm -v $(pwd):/src hysnsec/safety check -r requirements.txt --json > oast-results.json
  artifacts:
    paths: [oast-results.json]
    when: always # What does this do?
  allow_failure: true
```
2. You can make use of hysnsec/safety docker image if you wish
3. Understand the use of Docker’s -v (volume mount) flag/option
4. Ensure you follow the DevSecOps Gospel and best practices while embedding the safety tool.
5. Rename test job name to oast.

Embed Safety in CI/CD pipeline
--------------------------------

As discussed in the SCA using the Safety exercise, we can embed the Safety tool in our CI/CD pipeline. However, do remember you need to run the command manually before you embed OAST in the pipeline.

> Do you wonder which stage this job should go into?

Most of the code (up to 95%) in any software project is open-source/third-party components. It makes sense to perform SCA scans before static analysis.


```
image: latest  # To run all jobs in this pipeline, use the latest docker image

services:
  - docker:dind       # To run all jobs in this pipeline, use a docker image that contains a docker daemon running inside (dind - docker in docker). Reference: https://forum.gitlab.com/t/why-services-docker-dind-is-needed-while-already-having-image-docker/43534

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

build:
  stage: build
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env                       # Create a virtual environment for the python application
   - source env/bin/activate              # Activate the virtual environment
   - pip install -r requirements.txt      # Install the required third party packages as defined in requirements.txt
   - python manage.py check               # Run checks to ensure the application is working fine

test:
  stage: test
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py test taskManager

oast:
  stage: test
  script:
    - docker pull hysnsec/safety  # We are going to pull the hysnsec/safety image to run the safety scanner
    # third party components are stored in requirements.txt for python, so we will scan this particular file with safety.
    - docker run --rm -v $(pwd):/src hysnsec/safety check -r requirements.txt --json > oast-results.json
  artifacts:
    paths: [oast-results.json]
    when: always # What does this do?

integration:
  stage: integration
  script:
    - echo "This is an integration step."
    - exit 1
  allow_failure: true # Even if the job fails, continue to the next stages

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
  when: manual # Continuous Delivery
```

> Instead of manually removing the container after the scan, we can use the –rm option so the container can clean up after itself.

Copy the above CI script and add it to the .gitlab.ci.yml file on Gitlab repo at https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

> Did you notice the job failed because of non zero exit code(here, exit code 64)? Why did the job fail? Because the tool found security issues. This is the expected behavior of any DevSecOps friendly tool. You need to either fix the security issues or add allow_failure: true to let the job finish without blocking other jobs. If you have troubles understanding exit code, please go through the exercise titled Working with Exit Code.

You will notice that the oast job stores the output to a file oast-results.json. We need the output file to process the results further either via APIs or vulnerability management systems like Defect Dojo.

Allow the job failure
----------

You do not want to fail the builds in DevSecOps Maturity Levels 1 and 2. If a security tool fails a build upon security findings, you would want to allow it to fail and not block the pipeline as there would be false positives in the results.

You can use the allow_failure tag to “not fail the build” even though the tool found issues.

```
oast:
  stage: test
  script:
    - docker pull hysnsec/safety
    - docker run --rm -v $(pwd):/src hysnsec/safety check -r requirements.txt --json > oast-results.json
  artifacts:
    paths: [oast-results.json]
    when: always        # What does this do?
  allow_failure: true   # <--- allow the build to fail but don't mark it as such
```
The pipeline would look like the following.

```
image: docker:20.10  # To run all jobs in this pipeline, use the latest docker image

services:
  - docker:dind       # To run all jobs in this pipeline, use a docker image that contains a docker daemon running inside (dind - docker in docker). Reference: https://forum.gitlab.com/t/why-services-docker-dind-is-needed-while-already-having-image-docker/43534

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

build:
  stage: build
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env                       # Create a virtual environment for the python application
   - source env/bin/activate              # Activate the virtual environment
   - pip install -r requirements.txt      # Install the required third party packages as defined in requirements.txt
   - python manage.py check               # Run checks to ensure the application is working fine

test:
  stage: test
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py test taskManager

oast:
  stage: test
  script:
    # We are going to pull the hysnsec/safety image to run the safety scanner
    - docker pull hysnsec/safety
    # third party components are stored in requirements.txt for python, so we will scan this particular file with safety.
    - docker run --rm -v $(pwd):/src hysnsec/safety check -r requirements.txt --json > oast-results.json
  artifacts:
    paths: [oast-results.json]
    when: always # What does this do?
  allow_failure: true

integration:
  stage: integration
  script:
    - echo "This is an integration step"
    - exit 1
  allow_failure: true # Even if the job fails, continue to the next stages

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
  when: manual # Continuous Delivery
```

Go ahead and add it to the .gitlab-ci.yml file to run the pipeline.

You will notice that the oast job has failed but didn’t block the other jobs from running.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

![image](https://github.com/user-attachments/assets/ec395082-d7e4-454e-b3ae-d9393d86f3e5)
