Learn how to embed ZAP into CI/CD pipeline
----------------------------------------------------------------

Use ZAP tool to do DAST in CI/CD pipeline
----------------------------------------------------------------

In this scenario, you will learn how to embed DAST in CI/CD pipeline.

You will learn to use ZAP Baseline Scan in CI/CD pipeline using all the best practices mentioned in the Practical DevSecOps Gospel.

A simple CI/CD pipeline
--------------------------------

Considering your DevOps team created a simple CI pipeline with the following contents.

```
image: docker:latest  # To run all jobs in this pipeline, use the latest docker image

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
```

We have two jobs in the above pipeline, the build job and the test job. As a security engineer, I do not care what they are doing as part of these jobs. Why? Imagine having to learn every build/testing tool used by your DevOps team. It will be a nightmare! Instead, rely on the DevOps team for help.

Let’s log into GitLab using the following details and execute this pipeline.

GitLab CI/CD Machine
--------------------------------
> Link: https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml
> 
> username: root
>
> password: pdso-training

Next, we need to create a CI/CD pipeline by replacing the .gitlab-ci.yml file content with the above CI script. Click on the Edit button to replace the content.

Save changes to the file using the Commit changes button.

Verify the pipeline run
----------

As soon as a change is made to the repository, the pipeline starts executing the jobs.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Exercise
----------

We will use the Zed Attack Proxy (ZAP) to scan applications for security issues and then embed it into CI/CD using ZAP Baseline Scan docker image.

1. Explore ZAP Baseline script/tool details [here](https://www.zaproxy.org/docs/docker/baseline-scan/)
2. Use https://prod-XqiHnDZ0.lab.practical-devsecops.training as the endpoint for ZAP Scanning
3. Embed ZAP scanning in integration stage and save the output as JSON file
4. Remember to follow all best practices while adding the baseline scan to CI/CD pipeline

# Tasks:
1. Embed ZAP scanning in integration stage with job name as zap-baseline, please use softwaresecurityproject/zap-stable:2.14.0 image to perform scans
> Add the below zap-baseline job to the integration stage.
```
zap-baseline:
  stage: integration
  script:
    - docker run --user $(id -u):$(id -g) -w /zap -v $(pwd):/zap/wrk:rw --rm softwaresecurityproject/zap-stable:2.14.0 zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -J zap-output.json
```
2. Save the result as JSON file with name zap-output.json and upload it using artifacts attribute
```
zap-baseline:
  stage: integration
  before_script:
    - docker pull softwaresecurityproject/zap-stable:2.14.0
  script:
    - docker run --user $(id -u):$(id -g) -w /zap -v $(pwd):/zap/wrk:rw --rm softwaresecurityproject/zap-stable:2.14.0 zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -J zap-output.json
  after_script:
    - docker rmi softwaresecurityproject/zap-stable:2.14.0  # clean up the image to save the disk space
  artifacts:
    paths: [zap-output.json]
    when: always        # What does this do?
  allow_failure: true  # Optional
```

Embed ZAP in CI/CD pipeline
--------------------------------

As discussed in the Dynamic Analysis using ZAP exercises, we can put ZAP in our CI/CD pipeline. However, remember that it’s important to locally test a tool before integrating it into the pipeline.

Troubleshooting a tool manually in a local environment is much easier compared to troubleshooting it in a CI/CD system.

Additionally, manually exploring the tool in a local environment helps you become familiar with the tool’s options and features. We need to embed this into CI/CD pipeline now using the same command.

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

zap-baseline:
  stage: integration
  script:
    - docker pull softwaresecurityproject/zap-stable:2.14.0
    - docker run --user $(id -u):$(id -g) -w /zap -v $(pwd):/zap/wrk:rw --rm softwaresecurityproject/zap-stable:2.14.0 zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -J zap-output.json
  after_script:
    - docker rmi softwaresecurityproject/zap-stable:2.14.0  # clean up the image to save the disk space
  artifacts:
    paths: [zap-output.json]
    when: always # What does this do?
  allow_failure: true
```

> rw volume mount
> The rw in the volume mount explicitly instructs the container to volume mount in read write mode. rw is optional to be used, but ZAP documentation recommends using rw as volume mount mode.

> -w /zap
> The -w /zap instructs the container to set /zap as the working directory inside the container. The /zap working directory is required for the ZAP container to run a baseline scan.

You can try changing allow_failure: true to allow_failure: false and see what happens.


![image](https://github.com/user-attachments/assets/337400d3-b10b-42a5-9836-5f09e51604d2)

We can see the results of this pipeline by visiting https://gitlab-ce-p30jrhut.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.


