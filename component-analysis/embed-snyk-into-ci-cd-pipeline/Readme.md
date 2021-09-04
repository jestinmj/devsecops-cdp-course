How to Embed Snyk into GitLab
================================

Use Snyk tool to perform OAST in CI/CD pipeline
----------

In this scenario, you will learn how to embed OAST in CI/CD pipeline.

You will learn to use Snyk in CI/CD pipeline and allow the job to fail even when the tool found several issues.

Exercise
---------

We will use a commercial offering Snyk to scan for vulnerable third-party components.

1. Add another job name oast-snyk under the build stage with the Snyk tool
2. Sign up for the Snyk’s Free service and generate/copy the token
3. Store Snyk token in Variables via Project –> Settings –> CI/CD –> Variables https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/settings/ci_cd
4. Create a new variable SNYK_TOKEN and put the token you got from the service, and ensure the protected flag is turned on
5. Use Snyk’s Linux binary to scan the dependencies in the project

Embed Snyk in CI/CD pipeline
--------------------------------

As discussed in the SCA using the Snyk exercise, we can put Snyk in our CI/CD pipeline. However, do remember you need to run the command manually before you embed OAST in the pipeline.

Since Snyk is a paid tool, you would also need to add the SNYK_TOKEN to the CI/CD variables on Gitlab CI.

Let’s login into the GitLab and configure this token https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/settings/ci_cd

Click on the Expand button under the Variables section, then click on the Add Variable button.

Add the following key/value pair in the form.

Finally, Click on the button Add Variable

Next, please visit https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml

Click on the edit button and append the following code to the .gitlab-ci.yml file.

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

oast-snyk:
  stage: test
  image: node:latest
  before_script:
    - wget -O snyk https://github.com/snyk/snyk/releases/download/v1.388.0/snyk-linux
    - chmod +x snyk
    - mv snyk /usr/local/bin/
  script:
    - npm install
    - snyk test --json > snyk-results.json
  artifacts:
    paths:
      - snyk-results.json
    when: always
    expire_in: one week

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

As discussed, any change to the repo kickstarts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Allow the job failure
----------

You do not want to fail the builds in DevSecOps Maturity Levels 1 and 2. If a security tool fails a job upon finding security issues, you would want to allow it to fail and not block the builds as there would be false positives in the results.

You can use the allow_failure tag to “not fail the build” even though the tool found security issues.

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

oast-snyk:
  stage: test
  image: node:latest
  before_script:
    - wget -O snyk https://github.com/snyk/snyk/releases/download/v1.566.0/snyk-linux
    - chmod +x snyk
    - mv snyk /usr/local/bin/
  script:
    - npm install
    - snyk test --json > snyk-results.json
  artifacts:
    paths:
    - snyk-results.json
    expire_in: one week
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

Extra Mile Exercise: Analyze the results from Snyk and remove any false positives
Who should do this exercise?
------
1. This exercise is beyond the CDP course’s scope. It’s added to help folks who already know these concepts in and out.
2. You can write small scripts in Python or Ruby or Golang.
3. You consider yourself an expert or advanced user in SAST.

Challenge
---------
Recall techniques you have learned in the previous exercises.

1. Login into the Snyk portal and explore the findings
2. Mark false positives as false positives
3. Ensure each result is at the right severity level (HIGH, MEDIUM, LOW)
4. Export the final report and suggest remediation steps to developers
5. Ensure false positives are not shown again in CI scans
