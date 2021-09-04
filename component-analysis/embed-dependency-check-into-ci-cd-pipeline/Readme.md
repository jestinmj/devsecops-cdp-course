How to Embed Dependency-Check into GitLab
================================

Use Dependency Check tool to do OAST in CI/CD pipeline
----------

In this scenario, you will learn how to embed OAST in CI/CD pipeline.

You will learn to use OWASP Dependency Check in CI/CD pipeline and allow the job to fail even when the tool found several issues.

A simple CI/CD pipeline
----------
Create a new project by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/projects/new#blank_project. Give the project a name webgoat and click on the Create project button.

Once done, we need to push our source code into GitLab. Let’s download the code using git clone in DevSecOps Box.

```
git clone https://github.com/WebGoat/WebGoat.git webgoat
cd webgoat
```

Embed Dependency Check in CI/CD pipeline
----------------------------------------------------------------

As discussed in the SCA using Dependency Check exercise, we can put Dependency Check in our CI/CD pipeline. However, do remember you need to run the command manually before you embed OAST in the pipeline.

Visit https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/webgoat/-/new/master/ to create a new file called run-depcheck.sh with the following contents.

```
#!/bin/sh

DATA_DIRECTORY="$PWD/data"
REPORT_DIRECTORY="$PWD/reports"

if [ ! -d "$DATA_DIRECTORY" ]; then
  echo "Initially creating persistent directories"
  mkdir -p "$DATA_DIRECTORY"
  chmod -R 777 "$DATA_DIRECTORY"

  mkdir -p "$REPORT_DIRECTORY"
  chmod -R 777 "$REPORT_DIRECTORY"
fi

cd webgoat-container

# Make sure we are using the latest version
docker pull owasp/dependency-check

# mvn install -Dmaven.test.skip=true
docker run --rm \
  --volume $(pwd):/src \
  --volume "$DATA_DIRECTORY":/usr/share/dependency-check/data \
  --volume "$REPORT_DIRECTORY":/report \
  owasp/dependency-check \
  --scan /src \
  --format "CSV" \
  --project "Webgoat" \
  --failOnCVSS 8 \
  --out /report
```

>  Do not forget to use File Name as run-depcheck.sh

Then update the content of the .gitlab-ci.yml with the following.

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

odc-backend:
  stage: test
  image: gitlab/dind:latest
  script:
    - chmod +x ./run-depcheck.sh
    - ./run-depcheck.sh
  artifacts:
    paths:
      - reports/dependency-check-report.csv
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

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/webgoat/pipelines.

Click on the appropriate job name to see the output.

Allow the job failure
----------

You do not want to fail the builds in DevSecOps Maturity Levels 1 and 2. If a security tool fails a job, it won’t allow other DevOps jobs like release/deploy to run hence causing great distress to DevOps Team. Moreover, the security tools suffer from false positives. Failing a build on inaccurate data is a sure recipe for disaster.

You can use the allow_failure tag to not fail the build even though the tool found security issues.

output
```
odc-backend:
  stage: test
  image: gitlab/dind:latest
  script:
    - chmod +x ./run-depcheck.sh
    - ./run-depcheck.sh
  artifacts:
    paths:
      - reports/dependency-check-report.csv
    when: always
    expire_in: one week
  allow_failure: true #<--- allow the build to fail but don't mark it as such
```

The pipeline would look like the following.

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

odc-backend:
  stage: test
  image: gitlab/dind:latest
  script:
    - chmod +x ./run-depcheck.sh
    - ./run-depcheck.sh
  artifacts:
    paths:
      - reports/dependency-check-report.csv
    when: always
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

You will notice that the odc-backend job has failed, but other jobs and stages ran fine.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/webgoat/pipelines.

Click on the appropriate job name to see the output/results.