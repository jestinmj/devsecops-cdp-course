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

Once you’re done, please do not forget to share the answer with our staff via Slack Direct Message(DM).

Embed ZAP in CI/CD pipeline
--------------------------------

As discussed in the Dynamic Analysis using ZAP exercises, we can put ZAP in our CI/CD pipeline. We did ensure the zap command runs fine in DevSecOps-Box, we need to embed this into CI/CD pipeline now using the same command.

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

zap-baseline:
  stage: integration
  script:
    - docker pull owasp/zap2docker-stable
    - docker run --user $(id -u):$(id -g) -w /zap -v $(pwd):/zap/wrk:rw --rm owasp/zap2docker-stable zap-baseline.py -t https://prod-XqiHnDZ0.lab.practical-devsecops.training -J zap-output.json
  after_script:
    - docker rmi owasp/zap2docker-stable  # clean up the image to save the disk space
  artifacts:
    paths: [zap-output.json]
    when: always # What does this do?
  allow_failure: false
```

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.