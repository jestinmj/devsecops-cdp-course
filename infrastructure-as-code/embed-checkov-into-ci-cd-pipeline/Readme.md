Learn how to embed Checkov into CI/CD pipeline
================================

Use Checkov tool to perform SAST for IaC in CI/CD pipeline
----------

In this scenario, you will learn how to embed Checkov in CI/CD pipeline.

A simple CI/CD pipeline
--------------------------------

Create a new projects by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/projects/new#blank_project, give the project name terraform and click Create project button. Once done we need to push our source code into GitLab, let’s download the code using git clone in DevSecOps Box.

```
git clone https://gitlab.practical-devsecops.training/pdso/terraform.git terraform
cd terraform
```
Rename git url to the new one.
```
git remote rename origin old-origin
git remote add origin http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/terraform.git
git push -u origin --all
```

And enter the Gitlab credentials.

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

We do have four jobs in this pipeline, a build job, a test job, a integration job, and a prod job.

As a security engineer, I do not care what they are doing as part of these jobs. Why? imagine having to learn every build/testing tool used by your DevOps team, it will be a nightmare. Instead, rely on the DevOps team for help.

Let’s login into the Gitlab using the following details and execute this pipeline.

GitLab CI/CD Machine
--------------------------------

- Link : https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/terraform/-/blob/master/.gitlab-ci.yml
- Username : root
- Password : pdso-training

Next, we need to create a CI/CD pipeline by replacing the .gitlab-ci.yml file content with the above CI script. Click on the Edit button to replace the content (use Control+A and Control+V).

Save changes to the file using the Commit changes button.

Verify the pipeline run
----------

As soon as a change is made to the repository, the pipeline starts executing the jobs.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/terraform/pipelines.

Click on the appropriate job name to see the output.

Exercise
---------

Recall techniques you have learned in the previous module (Secure SDLC and CI/CD).

1. Read the [Checkov documentation](https://www.checkov.io/documentation.html)
2. Add more stage called validate and embed Checkov with job name as checkov
3. Ensure the job is running under the validate stage and save the output as JSON file
4. Follow all the best practices while embedding Checkov in the CI/CD pipeline

> Please try to do this exercise without looking at the solution on the next page.

Embed Checkov in CI/CD pipeline
--------------------------------

As discussed in the Secure IaC using Checkov exercise, we can embed Checkov in our CI/CD pipeline. However, you need to test the command manually before you embed this SAST tool in the pipeline.

```
image: docker:latest

services:
  - docker:dind

stages:
  - validate
  - build
  - test
  - release
  - preprod
  - integration
  - prod

checkov:
  stage: validate
  script:
    - docker pull bridgecrew/checkov
    - docker run --rm -w /src -v $(pwd):/src bridgecrew/checkov -d aws -o json | tee checkov-output.json
  artifacts:
    paths: [checkov-output.json]
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

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/terraform/pipelines.

Click on the appropriate job name to see the output.

You will notice that the checkov job’s output is saved in checkov-output.json file.

Allow the job failure
----------

We do not want to fail the builds/jobs/scan in DevSecOps Maturity Levels 1 and 2, as security tools spit a significant amount of false positives.

You can use the allow_failure tag to not fail the build even though the tool found issues.

```
checkov:
  stage: validate
  script:
    - docker pull bridgecrew/checkov
    - docker run --rm -w /src -v $(pwd):/src bridgecrew/checkov -d aws -o json | tee checkov-output.json
  artifacts:
    paths: [checkov-output.json]
    when: always
  allow_failure: true   #<--- allow the build to fail but don't mark it as such
```

After adding the allow_failure tag, the pipeline would look like the following.

```
image: docker:latest

services:
  - docker:dind

stages:
  - validate
  - build
  - test
  - release
  - preprod
  - integration
  - prod

checkov:
  stage: validate
  script:
    - docker pull bridgecrew/checkov
    - docker run --rm -w /src -v $(pwd):/src bridgecrew/checkov -d aws -o json | tee checkov-output.json
  artifacts:
    paths: [checkov-output.json]
    when: always
  allow_failure: true

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

You will notice that the checkov job failed however it didn’t block others from continuing further.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/terraform/pipelines.

Click on the appropriate job name to see the output.

