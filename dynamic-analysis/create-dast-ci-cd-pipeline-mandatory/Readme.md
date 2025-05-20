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
image: docker:latest  # To run all jobs in this pipeline, use the latest docker image

services:
  - docker:dind       # To run all jobs in this pipeline, use a docker image that contains a docker daemon running inside (dind - docker in docker). Reference: https://forum.gitlab.com/t/why-services-docker-dind-is-needed-while-already-having-image-docker/43534

stages:
  - build
  - deploy
  - test

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

# Build Docker Images in CI/CD Pipeline
--------------------------------
Before embedding the DAST scan, we will add a job to build the image whenever any changes are pushed and deploy it to the production machine.

Click on the Edit button and replace the current build job with the following content to the .gitlab-ci.yml file.
```
build:
  stage: build
  script:
   - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .  # Build the application into Docker image
   - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA        # Push the image into registry
```
Save changes to the file using the Commit changes button.

In the above code, you will notice that we use predefined variables provided by GitLab and we don’t need to manually define the image name.

Once the pipeline is finished, you will notice that the build job failed with the error message denied: access forbidden. To fix this, we need to log into the registry with the correct credentials before pushing the image.

Next, please visit https://gitlab-ce-p30jrhut.lab.practical-devsecops.training/root/django-nv/-/blob/main/.gitlab-ci.yml.

Click on the Edit button and replace the build job with the following code.
```
build:
  stage: build
  before_script:
   - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  script:
   - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .  # Build the application into Docker image
   - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA        # Push the image into registry
```
> Note
> Where do we get CI_REGISTRY_IMAGE and CI_COMMIT_SHA? Even though we haven’t defined it yet in GitLab CI/CD variables, we use predefined variables to authenticate with the registry on GitLab, so we don’t need to add any secrets to the settings. Please refer to the predefined environment variables [here](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html).

Save changes to the file using the Commit changes button. Once the pipeline is completed, you will notice that the build job is passed.

To check if the image has been pushed, you can visit Deploy → Container Registry in your project.

Let’s move to the next step to deploy this container to the production machine.

# Deploy Application from CI/CD Pipeline
--------------------------------
> Note
>To run DAST exercises, we need a running application on the staging/production machine.

The following steps help you in setting up the django.nv application on the prod machine.

We have updated a build job to build and push the container into the registry. Next, we will add the prod job to deploy our application after the build process.

> Remember
> The steps would be the same for either staging or production environment.

We need to add the following variables (Go to Project (django.nv) → Settings → CI/CD → Variables → Expand).
![image](https://github.com/user-attachments/assets/a66551c9-8d47-4ef4-9add-a33e4b3f6215)

The SSH key is available at /root/.ssh/id_rsa. You can use the following command to accomplish that.

Log into the production machine using SSH.
<br>`ssh root@prod-p30jrhut`

<br>

Then view the value of id_rsa. You can use the following command:<br>
`more /root/.ssh/id_rsa`

> Please copy the complete value from the beginning (-----BEGIN RSA PRIVATE KEY-----) to the last line (-----END RSA PRIVATE KEY-----) are also copied.

> # Security Best Practices
> Storing SSH keys in GitLab variables poses significant security risks due to plain text storage and limited access controls. For production environments, it’s recommended to use dedicated key management solutions like HashiCorp Vault for secure key storage, rotation, and access control. Learn more about managing SSH access at scale here.

Once the variables are saved on the CI system, we need to edit the .gitlab-ci.yml file content once again and replace the prod job with the following code.
```
prod:
  stage: deploy
  image: kroniak/ssh-client:3.6
  environment: production
  only:
      - main
  before_script:
   - mkdir -p ~/.ssh
   - echo "$PROD_SSH_PRIVKEY" > ~/.ssh/id_rsa
   - chmod 600 ~/.ssh/id_rsa
   - eval "$(ssh-agent -s)"
   - ssh-add ~/.ssh/id_rsa
   - ssh-keyscan -H $PROD_HOSTNAME >> ~/.ssh/known_hosts
  script:
   - echo
   - |
      ssh $PROD_USERNAME@$PROD_HOSTNAME << EOF
        docker login -u ${CI_REGISTRY_USER} -p ${CI_REGISTRY_PASS} ${CI_REGISTRY}
        docker rm -f django.nv
        docker run -d --name django.nv -p 8000:8000 $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      EOF
```
Save changes to the file using the Commit changes button.
```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - deploy
  - test

build:
  stage: build
  before_script:
   - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  script:
   - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .  # Build the application into Docker image
   - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA        # Push the image into registry

prod:
  stage: deploy
  image: kroniak/ssh-client:3.6
  environment: production
  needs:
    - build
  only:
    - main
  before_script:
   - mkdir -p ~/.ssh
   - echo "$PROD_SSH_PRIVKEY" > ~/.ssh/id_rsa
   - chmod 600 ~/.ssh/id_rsa
   - eval "$(ssh-agent -s)"
   - ssh-add ~/.ssh/id_rsa
   - ssh-keyscan -H $PROD_HOSTNAME >> ~/.ssh/known_hosts
  script:
   - echo
   - |
      ssh $PROD_USERNAME@$PROD_HOSTNAME << EOF
        docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
        docker rm -f django.nv
        docker run -d --name django.nv -p 8000:8000 $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      EOF
```

Notice the contents of the build and prod jobs. We create a docker image under the build stage, and we will deploy this container to the prod machine using the prod stage.

> SSH issues? Please refer to the troubleshooting lesson on the course portal.

Let’s see the results by visiting https://gitlab-ce-p30jrhut.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Now, we should see the Task Manager application running by accessing this [URL](https://prod-p30jrhut.lab.practical-devsecops.training/).

> If you can access above URL, It means the deployment process is successful

There you go, we have implemented a Continuous Deployment (CD).

# Challenge
Recall the techniques you have learned in the previous module (CI/CD, OAST, and SAST).

- Visit the respective tool’s documentation page to see if you can create an appropriate command to run and test the tool locally first, before integrating the tools into the CI/CD pipeline.
- Please follow the DevSecOps Gospel and other best practices while trying to embed the above scanners.

# 1
Create a job named nikto, nmap, and sslyze using hysnsec docker images in the CI/CD pipeline to run scans against the production machine https://prod-p30jrhut.lab.practical-devsecops.training
```
nikto:
  stage: test
  script:
    - docker pull hysnsec/nikto
    - docker run --rm -v $(pwd):/tmp hysnsec/nikto -h http://prod-p30jrhut.lab.practical-devsecops.training -o /tmp/nikto-output.xml
  artifacts:
    paths: [nikto-output.xml]
    when: always

sslyze:
  stage: test
  script:
    - docker pull hysnsec/sslyze
    - docker run --rm -v $(pwd):/tmp hysnsec/sslyze prod-p30jrhut.lab.practical-devsecops.training:443 --json_out /tmp/sslyze-output.json
  artifacts:
    paths: [sslyze-output.json]
    when: always

nmap:
  stage: test
  script:
    - docker pull hysnsec/nmap
    - docker run --rm -v $(pwd):/tmp hysnsec/nmap prod-p30jrhut -oX /tmp/nmap-output.xml
  artifacts:
    paths: [nmap-output.xml]
    when: always
```


Embed DAST in CI/CD pipeline
--------------------------------

As discussed in the Dynamic Analysis exercises, we can integrate DAST tools like Nikto, SSLyze and Nmap in our CI/CD pipelines.

There is no specific standard for when to run DAST. It’s recommended to scan your live application post-deployment in all your environments: development, staging, and production. You can choose to do this for all environments or selectively, depending on your organization’s needs.

> What would you do if the tools are not installed? You can either install it yourself, provided you have permission to do so, or ask your operations team to help you out.

```
image: docker:20.10  # To run all jobs in this pipeline, use the latest docker image

services:
  - docker:dind       # To run all jobs in this pipeline, use a docker image that contains a docker daemon running inside (dind - docker in docker). Reference: https://forum.gitlab.com/t/why-services-docker-dind-is-needed-while-already-having-image-docker/43534

stages:
  - build
  - deploy
  - test

build:
  stage: build
  before_script:
   - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  script:
   - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .  # Build the application into Docker image
   - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA        # Push the image into registry

prod:
  stage: deploy
  image: kroniak/ssh-client:3.6
  environment: production
  needs:
    - build
  only:
    - main
  before_script:
   - mkdir -p ~/.ssh
   - echo "$PROD_SSH_PRIVKEY" > ~/.ssh/id_rsa
   - chmod 600 ~/.ssh/id_rsa
   - eval "$(ssh-agent -s)"
   - ssh-add ~/.ssh/id_rsa
   - ssh-keyscan -H $PROD_HOSTNAME >> ~/.ssh/known_hosts
  script:
   - echo
   - |
      ssh $PROD_USERNAME@$PROD_HOSTNAME << EOF
        docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
        docker rm -f django.nv
        docker run -d --name django.nv -p 8000:8000 $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      EOF

nikto:
  stage: test
  script:
    - docker pull hysnsec/nikto
    - docker run --rm -v $(pwd):/tmp hysnsec/nikto -h prod-p30jrhut -o /tmp/nikto-output.xml
  artifacts:
    paths: [nikto-output.xml]
    when: always

sslyze:
  stage: test
  script:
    - docker pull hysnsec/sslyze
    - docker run --rm -v $(pwd):/tmp hysnsec/sslyze prod-p30jrhut.lab.practical-devsecops.training:443 --json_out /tmp/sslyze-output.json
  artifacts:
    paths: [sslyze-output.json]
    when: always

nmap:
  stage: test
  script:
    - docker pull hysnsec/nmap
    - docker run --rm -v $(pwd):/tmp hysnsec/nmap prod-p30jrhut -oX /tmp/nmap-output.xml
  artifacts:
    paths: [nmap-output.xml]
    when: always
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
  stage: test
  script:
    - docker pull hysnsec/sslyze
    - docker run --rm -v $(pwd):/tmp hysnsec/sslyze prod-p30jrhut.lab.practical-devsecops.training:443 --json_out /tmp/sslyze-output.json
  artifacts:
    paths: [sslyze-output.json]
    when: always
  allow_failure: true   #<--- allow the build to fail but don't mark it as such
```
Similarly, let’s append Nikto and nmap jobs as well.

After appending the above jobs to the pipeline, our pipeline would look like the following.

```
image: docker:20.10  # To run all jobs in this pipeline, use the latest docker image

services:
  - docker:dind       # To run all jobs in this pipeline, use a docker image that contains a docker daemon running inside (dind - docker in docker). Reference: https://forum.gitlab.com/t/why-services-docker-dind-is-needed-while-already-having-image-docker/43534

stages:
  - build
  - deploy
  - test

build:
  stage: build
  before_script:
   - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  script:
   - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .  # Build the application into Docker image
   - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA        # Push the image into registry

prod:
  stage: deploy
  image: kroniak/ssh-client:3.6
  environment: production
  needs:
    - build
  only:
    - main
  before_script:
   - mkdir -p ~/.ssh
   - echo "$PROD_SSH_PRIVKEY" > ~/.ssh/id_rsa
   - chmod 600 ~/.ssh/id_rsa
   - eval "$(ssh-agent -s)"
   - ssh-add ~/.ssh/id_rsa
   - ssh-keyscan -H $PROD_HOSTNAME >> ~/.ssh/known_hosts
  script:
   - echo
   - |
      ssh $PROD_USERNAME@$PROD_HOSTNAME << EOF
        docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
        docker rm -f django.nv
        docker run -d --name django.nv -p 8000:8000 $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      EOF

nikto:
  stage: test
  script:
    - docker pull hysnsec/nikto
    - docker run --rm -v $(pwd):/tmp hysnsec/nikto -h prod-p30jrhut -o /tmp/nikto-output.xml
  artifacts:
    paths: [nikto-output.xml]
    when: always
  allow_failure: true

sslscan:
  stage: test
  script:
    - docker pull hysnsec/sslyze
    - docker run --rm -v $(pwd):/tmp hysnsec/sslyze prod-p30jrhut.lab.practical-devsecops.training:443 --json_out /tmp/sslyze-output.json
  artifacts:
    paths: [sslyze-output.json]
    when: always
  allow_failure: true

nmap:
  stage: test
  script:
    - docker pull hysnsec/nmap
    - docker run --rm -v $(pwd):/tmp hysnsec/nmap prod-p30jrhut -oX /tmp/nmap-output.xml
  artifacts:
    paths: [nmap-output.xml]
    when: always
  allow_failure: true
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
