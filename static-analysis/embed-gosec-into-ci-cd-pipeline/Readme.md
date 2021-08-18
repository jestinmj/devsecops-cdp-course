Learn how to embed Gosec into CI/CD pipeline
================================================================

Use Gosec tool to perform SAST in CI/CD pipeline
----------

In this scenario, you will learn how to embed GoSec in the CI/CD pipeline.

You will learn to use gosec in CI/CD pipeline and how to allow job failure when the tool found several issues.

A simple CI/CD pipeline
----------
Create a new project by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/projects/new#blank_project, give the project name golang and click Create project button. Once done we need to push our source code into GitLab, let’s download the code using git clone in DevSecOps Box.

```
git clone https://gitlab.practical-devsecops.training/pdso/golang.git golang
cd golang
```
Next, considering your DevOps team created a simple CI pipeline with the following contents.

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
  script:
    - echo "This is a build step"

test:
  stage: test
  script:
    - echo "This is a test step"

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
We have four jobs in this pipeline, a build job, a test job, a integration job and a prod job.

As a security engineer, I do not care much about what the DevOps team is doing as part of these jobs. Why? Imagine having to learn every build/testing tool used by your DevOps team, it will be a nightmare. Instead, rely on the DevOps team for help.

Let’s login into the GitLab using the following details and execute this pipeline.

GitLab CI/CD Machine
---------

login to your gitlab account 

Next, we need to create a CI/CD pipeline by replacing the .gitlab-ci.yml file content with the above CI script. Click on the Edit button to replace the content (use Control+A and Control+V).

Save changes to the file using the Commit changes button.

Verify the pipeline run
----------

As soon as a change is made to the repository, the pipeline starts executing the jobs.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/golang/pipelines.

Click on the appropriate job name to see the output.

Exercise
---------
Recall techniques you have learned in the previous module (Secure SDLC and CI/CD).

1. Read the [Gosec documentation](https://github.com/securego/gosec)
2. Embed SAST backend tool, Gosec in test stage with job name as sast
3. Ensure the job is running under the test stage
4. After the above steps, move it to the build stage now
5. You can either install Gosec manually or use the Docker image
6. Follow all the best practices while embedding Gosec in the CI/CD pipeline. Don’t forget the tool evaluation criteria

> Please try to do this exercise without looking at the solution on the next page.

Embed Gosec in CI/CD pipeline
--------------------------------

As discussed in the Static Analysis using Gosec exercise, we can embed Gosec in our CI/CD pipeline. However, do remember you need to run the command manually before you embed this SAST tool in the pipeline.

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
  script:
    - echo "This is a build step"

sast:
  stage: build
  image: golang:1.15-alpine
  before_script:
    - go get github.com/securego/gosec/v2/cmd/gosec
  script:
    - gosec -fmt json -out gosec-output.json ./... 
  artifacts:
    paths: [gosec-output.json]
    when: always

test:
  stage: test
  script:
    - echo "This is a test step"

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
As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/golang/pipelines.

Click on the appropriate job name to see the output.

You will notice that the sast job’s output is saved in gosec-output.json file

Allow the job failure
----------

We do not want to fail the builds/jobs/scan in DevSecOps Maturity Levels 1 and 2, as security tools spit a significant amount of false positives.

You can use the allow_failure tag to “not fail the build” even though the tool found issues

```
sast:
  stage: build
  image: golang:1.15-alpine
  before_script:
    - go get github.com/securego/gosec/v2/cmd/gosec
  script:
    - gosec -fmt json -out gosec-output.json ./...
  artifacts:
    paths: [gosec-output.json]
    when: always
  allow_failure: true
```
After adding the allow_failure tag, the pipeline would look like the following.
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

sast:
  stage: build
  image: golang:1.15-alpine
  before_script:
    - go get github.com/securego/gosec/v2/cmd/gosec
  script:
    - gosec -fmt json -out gosec-output.json ./...
  artifacts:
    paths: [gosec-output.json]
    when: always
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

You will notice that the sast job failed. However, it didn’t block other jobs from continuing further.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/golang/pipelines.

Click on the appropriate job name to see the output.

