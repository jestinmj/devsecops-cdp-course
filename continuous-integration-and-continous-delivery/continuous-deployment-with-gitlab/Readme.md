Continuous Deployment with GitLab
========================================================

Use Gitlab CI/CD system to learn how to implement Continuous Deployment
-------

In this scenario, you will learn how to implement Continuous Deployment using Gitlab CI.

A simple CI/CD pipeline
----------
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

We have four jobs in this pipeline; a build job, a test job, a integration job, and a prod job.

Let’s login into Gitlab using the following details and execute this pipeline.

Let’s log into Gitlab using the following details and execute this pipeline once again.

- Gitlab URL :	https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml
- Username: 	root
- Password: 	pdso-training

Next, we need to create a CI/CD pipeline by replacing the .gitlab-ci.yml file content with the above CI script. Click on the Edit button to replace the content (use Control+A and Control+V).

Save changes to the file using the Commit changes button.

Verify the pipeline run
----------

As soon as a change is made to the repository, the pipeline starts executing the jobs.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Build Docker images in CI/CD pipeline
----------

Before adding a new job, we will learn some basic syntax of .gitlab-ci.yml to configure our CI/CD pipelines.

> Remember, continuous delivery involves human approval, whereas continuous deployment is automatic.

In GitLab CI, we can use when: manual to create a continuous delivery pipeline. Any job with a manual tag won’t execute until you click on the play button. Let’s create such a pipeline using the following .gitlab-ci.yml file.

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
  when: manual  # <-- this job will not be executed by GitLab automatically
```

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/jobs/4.


> We will now containerize this application to reap the benefits of container technology.

Let’s add a new job called release after the test job.

Click on the Edit button to add the following content to the .gitlab-ci.yml file

```
release:
  stage: release
  script:
   - docker build -t $CI_REGISTRY/root/django-nv .   # Build the application into Docker image
   - docker push $CI_REGISTRY/root/django-nv         # Push the image into registry
```

Save changes to the file using the Commit changes button.

You will notice that the release job failed with the error message no basic auth credentials. To fix this, we need to login into the registry with the correct credentials before pushing the image.

> Tip: Do not hardcode credentials in .gitlab-ci.yml script.


Let’s store the secrets in Gitlab CI/CD variables by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/settings/ci_cd.

Click on the Expand button under Variables section, then click the Add Variable button and add the following variables in the form of key value pairs.

- Key: CI_REGISTRY_USER
- Value: root

- Key: CI_REGISTRY_PASS
- Value: pdso-training

Next, please visit https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml.

Click on the Edit button and replace the release job with the following code.

```
release:
  stage: release
  before_script:
   - echo $CI_REGISTRY_PASS | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  script:
   - docker build -t $CI_REGISTRY/root/django-nv .   # Build the application into Docker image
   - docker push $CI_REGISTRY/root/django-nv         # Push the image into registry
```

Save changes to the file using the Commit changes button. Once the pipeline completes, you will notice that the release job is successful.

Where do we get CI_REGISTRY? Even though we don’t define it yet in Gitlab CI/CD variables, please refer to predefined environment variables [here.](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)

Deploy application from CI/CD pipeline
--------------------------------
> To run DAST exercises, we need a running application on the staging/production machine.

The following steps help you in setting up the django.nv application on the prod machine.

We have added a new job to release the container in our release job. Next, we will modify the prod job to deploy our application after the release process.

> Remember, the steps would be the same for either staging or production environment. You can imagine we are not deploying to production but staging at the moment.

We need to add the following variables (Go to → Project (django.nv) → settings → CI/CD → Variables → Expand), as we did before for the CI_REGISTRY_USER variable.

- Key: 	PROD_USERNAME
- Value: 	root
- Key: 	PROD_HOST
- Value: 	prod-XqiHnDZ0
- Key: 	PROD_SSH_PRIVKEY
- Value: 	Copy the private key from the production machine using SSH

The SSH key is available at /root/.ssh/id_rsa. You can use the following commands to accomplish that.
```
ssh root@prod-XqiHnDZ0 # Log into production machine using ssh.
```
output
```
# Ensure the lines -----BEGIN RSA PRIVATE KEY----- and -----END RSA PRIVATE KEY----- are also copied
cat /root/.ssh/id_rsa
```
> Note
> 
> Please copy the complete value from the beginning (Including BEGIN RSA and END RSA lines) to the last line. An example ~/.ssh/id_rsa is shown below for reference (Do not use this key)

Once the variables are saved on the CI system, we need to edit the .gitlab-ci.yml file content once again and replace the prod job with the following code.

```
prod:
  stage: prod
  image: kroniak/ssh-client:3.6
  environment: production
  only:
      - master
  before_script:
   - mkdir -p ~/.ssh
   - echo "$PROD_SSH_PRIVKEY" > ~/.ssh/id_rsa
   - chmod 600 ~/.ssh/id_rsa
   - eval "$(ssh-agent -s)"
   - ssh-add ~/.ssh/id_rsa
   - ssh-keyscan -t rsa $PROD_HOST >> ~/.ssh/known_hosts
  script:
   - echo
   - |
      ssh root@$PROD_HOST << EOF
        docker login -u ${CI_REGISTRY_USER} -p ${CI_REGISTRY_PASS} ${CI_REGISTRY}
        docker rm -f django.nv
        docker pull ${CI_REGISTRY}/root/django-nv
        docker run -d --name django.nv -p 8000:8000 ${CI_REGISTRY}/root/django-nv
      EOF
```

Save changes to the file using the Commit changes button.

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

release:
  stage: release
  before_script:
   - echo $CI_REGISTRY_PASS | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  script:
   - docker build -t $CI_REGISTRY/root/django-nv .   # Build the application into Docker image
   - docker push $CI_REGISTRY/root/django-nv         # Push the image into registry

integration:
  stage: integration
  script:
    - echo "This is an integration step"
    - exit 1
  allow_failure: true # Even if the job fails, continue to the next stages

prod:
  stage: prod
  image: kroniak/ssh-client:3.6
  environment: production
  only:
      - master
  before_script:
   - mkdir -p ~/.ssh
   - echo "$PROD_SSH_PRIVKEY" > ~/.ssh/id_rsa
   - chmod 600 ~/.ssh/id_rsa
   - eval "$(ssh-agent -s)"
   - ssh-add ~/.ssh/id_rsa
   - ssh-keyscan -t rsa $PROD_HOST >> ~/.ssh/known_hosts
  script:
   - echo
   - |
      ssh root@$PROD_HOST << EOF
        docker login -u ${CI_REGISTRY_USER} -p ${CI_REGISTRY_PASS} ${CI_REGISTRY}
        docker rm -f django.nv
        docker pull ${CI_REGISTRY}/root/django-nv
        docker run -d --name django.nv -p 8000:8000 ${CI_REGISTRY}/root/django-nv
      EOF
```

Notice the contents of the release and the prod jobs. We will create a docker container under the release stage, and we will deploy this container to the staging/prod machine using the prod stage.

> SSH issues? Please refer to the troubleshooting lesson on the course portal.

Let’s see the results by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

We should also see a running django.nv (Task Manager) at [this URL](https://prod-xqihndz0.lab.practical-devsecops.training/).

