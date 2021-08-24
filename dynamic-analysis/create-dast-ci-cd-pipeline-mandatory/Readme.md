Learn how to embed Nikto, SSLyze, and Nmap into CI/CD pipeline
================================

Use Nikto, SSLyze, and Nmap to do DAST in CI/CD pipeline
------------------------------------------------

In this scenario, you will learn how to embed DAST scan in a CI/CD pipeline.

You will learn to incorporate DAST tools in CI/CD pipeline and handle job failures in Maturity Levels 1 and 2.

A simple CI/CD pipeline
----------

Imagine your boss asked you to embed DAST tools in a project’s CI pipeline. You have access to the source code, and you saw they were using the following .gitlab-ci.yml script.

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

You saw that the CI Script has two jobs, the build job and the test job. Assuming you do not understand python or any programming language, we can safely consider the DevOps team is building and testing the code.

Let’s log into GitLab using the following details and execute this pipeline once again.

GitLab CI/CD Machine
-----
> Link : https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml
> 
> Username : root
> 
> Password : pdso-training

Next, we need to create a CI/CD pipeline by replacing the .gitlab-ci.yml file content with the above CI script. Click on the Edit button to replace the content (use Control+A and Control+V).

Save changes to the file using the Commit changes button.

Verify the pipeline run
----------
As soon as a change is made to the repository, the pipeline starts executing the jobs.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Exercise
---------

Recall the techniques you have learned in the previous module (CI/CD, OAST, and SAST).

1. In this exercise, we will explore how to add DAST tools, nikto, nmap, and sslyze in the CI/CD pipeline against the production machine https://prod-XqiHnDZ0.lab.practical-devsecops.training
2. Visit the respective tool’s documentation page to see if you can create an appropriate command to run and test the tool locally first, before integrating in to the CI/CD pipeline
3. Please follow the DevSecOps Gospel and other best practices while trying to embed the above scanners

> Please try to do this exercise without looking at the solution on the next page.

Embed DAST in CI/CD pipeline
--------------------------------

As discussed in the Dynamic Analysis exercises, we can integrate DAST tools like Nikto, SSLyze and Nmap in our CI/CD pipelines.

> What would you do if the tools are not installed? You can either install it yourself, provided you have permission to do so, or ask your operations team to help you out.

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

nikto:
  stage: integration
  script:
    - docker pull hysnsec/nikto
    - docker run --rm -v $(pwd):/tmp hysnsec/nikto -h http://prod-XqiHnDZ0.lab.practical-devsecops.training -o /tmp/nikto-output.xml
  artifacts:
    paths: [nikto-output.xml]
    when: always

sslscan:
  stage: integration
  script:
    - docker pull hysnsec/sslyze
    - docker run --rm -v $(pwd):/tmp hysnsec/sslyze --regular prod-XqiHnDZ0.lab.practical-devsecops.training:443 --json_out /tmp/sslyze-output.json
  artifacts:
    paths: [sslyze-output.json]
    when: always

nmap:
  stage: integration
  script:
    - docker pull hysnsec/nmap
    - docker run --rm -v $(pwd):/tmp hysnsec/nmap prod-XqiHnDZ0 -oX /tmp/nmap-output.xml
  artifacts:
    paths: [nmap-output.xml]
    when: always

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
  when: manual # Continuous Delivery
```

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Allow the job failure
----------

You do not want to fail the builds in DevSecOps Maturity Levels 1 and 2. If a security tool fails a job, it won’t allow other DevOps jobs like release/deploy to run hence causing great distress to DevOps Team. Moreover, the security tools suffer from false positives. Failing a build on inaccurate data is a sure recipe for disaster.

> Pro-tip: Don’t block builds unless you are sure about the result’s quality.

You can use the allow_failure tag to not fail the build even though the tool found issues.

```
sslscan:
  stage: integration
  script:
    - docker pull hysnsec/sslyze
    - docker run --rm -v $(pwd):/tmp hysnsec/sslyze --regular prod-XqiHnDZ0.lab.practical-devsecops.training:443 --json_out /tmp/sslyze-output.json
  artifacts:
    paths: [sslyze-output.json]
    when: always
  allow_failure: true   #<--- allow the build to fail but don't mark it as such
```
Similarly, let’s append Nikto and nmap jobs as well.

After appending the above jobs to the pipeline, our pipeline would look like the following.

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

nikto:
  stage: integration
  script:
    - docker pull hysnsec/nikto
    - docker run --rm -v $(pwd):/tmp hysnsec/nikto -h http://prod-XqiHnDZ0.lab.practical-devsecops.training -o /tmp/nikto-output.xml
  artifacts:
    paths: [nikto-output.xml]
    when: always
  allow_failure: true

sslscan:
  stage: integration
  script:
    - docker pull hysnsec/sslyze
    - docker run --rm -v $(pwd):/tmp hysnsec/sslyze --regular prod-XqiHnDZ0.lab.practical-devsecops.training:443 --json_out /tmp/sslyze-output.json
  artifacts:
    paths: [sslyze-output.json]
    when: always
  allow_failure: true

nmap:
  stage: integration
  script:
    - docker pull hysnsec/nmap
    - docker run --rm -v $(pwd):/tmp hysnsec/nmap prod-XqiHnDZ0 -oX /tmp/nmap-output.xml
  artifacts:
    paths: [nmap-output.xml]
    when: always
  allow_failure: true

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
  when: manual # Continuous Delivery
```

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Extra Mile Exercise: Create a docker image for SSLyze and run it in the pipeline
------------------------------------------------

Who should do this exercise?
------------------------------------------------

1. This exercise is beyond the scope of the CDP course and is added to help folks who already know these concepts in and out
2. You know how to write small scripts in Python/Ruby/Golang
3. You are comfortable writing Dockerfiles
4. You consider yourself an expert or advanced user in DAST

Challenge
----------

Recall techniques you have learned in the docker security course.

1. Read the [SSLyze documentation](https://github.com/nabla-c0d3/sslyze)
2. Create the docker image with the help of a Dockerfile and use alpine as the base image
3. Run the docker image in CI/CD pipeline against django.nv web application

> Please do note, we will not provide solutions for this extra mile exercise.
