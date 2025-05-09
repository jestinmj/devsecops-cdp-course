## Build Stage
The build stage is the first stage of the pipeline. This process creates a runnable instance of the software, often called a build. The stage also ensures that the codebase can be turned into a working application.

Let’s add a build stage to the existing .gitlab-ci.yml file.
```
image: docker:20.10

services:
  - docker:dind

stages:
  - build

django_build:
  stage: build
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py check
```

Please replace all the content in the .gitlab-ci.yml file with the script provided above.

Our initial step in the script is the build process. This phase tests whether the application can be built successfully and meets the expected requirements.

The final command, python manage.py check, verifies the application’s functionality. If any issues are detected during the build process, it could lead to delays or cause the build to fail.

The pipeline automatically starts executing jobs as soon as a change is made to the repository.

To view the results of this pipeline, visit https://gitlab-ce-cxlx0c4v.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the django_build job name to see the detailed output. You will see a message indicating that the build process was successful and completed without any issues.

Let’s move to the next step.


## Test Stage
In the test stage, we run automated tests against the build. These tests can include:

Unit tests (testing individual components or functions)
Integration tests (ensuring different parts of the application work together as expected)
End-to-end tests (testing the application as a whole, simulating user interactions)
The test stage ensures that new changes don’t break existing functionality and meet required quality standards.

Here is the script for the test stage job named django_test. The following script will be added to the previous script:
```
django_test:
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
Let’s add the above script to the end of the .gitlab-ci.yml file.

Here’s the complete script:

```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test

django_build:
  stage: build
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py check

django_test:
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
Based on the above script, we test the application in the test stage to verify if it’s running as expected without any issues.

When a change is made to the repository, the pipeline automatically starts executing the jobs.

To view the results of this pipeline, visit https://gitlab-ce-cxlx0c4v.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the django_test job name to see the detailed output. You’ll find information indicating that the test process completed successfully without any issues.

## Integration Stage
The integration stage combines and validates the functionality of new code with existing code or services.

After testing, the code is ready to be integrated with the existing codebase or other services. This process involves merging code branches and ensuring that the integrated system functions correctly.

In some contexts, the integration stage could also involve deploying the application to a staging environment where further integration and user acceptance tests can be performed.

Here is the script for the integration stage job named django_integration. The following script will be added to the previous script:
```
django_integration:
  stage: integration
  script:
    - echo "This is an integration step"
    - exit 1
  allow_failure: true # Even if the job fails, continue to the next stages
```
Let’s add the above script to the end of the .gitlab-ci.yml file.

Here’s the complete script after adding the integration stage:
```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test
  - integration

django_build:
  stage: build
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py check

django_test:
  stage: test
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py test taskManager

django_integration:
  stage: integration
  script:
    - echo "This is an integration step"
    - exit 1
  allow_failure: true # Even if the job fails, continue to the next stages
```

In the example provided, we use the echo command to demonstrate that we are in the integration stage. You can replace this with any other command appropriate for your integration stage.

To view the results of this pipeline:

Open the latest pipeline
Select the integration job
Check the output to see if the test process was disrupted
You can access the pipeline results by visiting https://gitlab-ce-cxlx0c4v.lab.practical-devsecops.training/root/django-nv/pipelines.

## Deploy Stage
The deploy stage is a crucial part of the Software Development Life Cycle (SDLC). It moves an application from development or testing environments to production, where end-users can access it. The deploy stage is also essential for releasing new features or fixing bugs. It employs various deployment strategies, such as blue-green, canary, or rolling deployments, to minimize disruptions.

The deploy stage often uses different job names for various environments (such as staging and production).

Here’s the script for the deploy stage job named django_deployment. We’ll add this script to the previous one:
```
django_deployment:
  stage: deploy
  script:
    - echo "This is a deploy step."
  when: manual # Continuous Delivery
```
Let’s add the above script to the end of the .gitlab-ci.yml file.

Below is the complete script:

```
image: docker:20.10

services:
  - docker:dind

stages:
  - build
  - test
  - integration
  - deploy

django_build:
  stage: build
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py check

django_test:
  stage: test
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py test taskManager

django_integration:
  stage: integration
  script:
    - echo "This is an integration step"
    - exit 1
  allow_failure: true # Even if the job fails, continue to the next stages

django_deployment:
  stage: deploy
  script:
    - echo "This is a deploy step."
  when: manual # Continuous Delivery
```
In the example provided, we use the echo command for testing. Feel free to use any other command that suits your service production deployment best practices.
In actual deployment, you’ll encounter various real-world scenarios. You’ll also experience a deployment scenario in the upcoming exercises.

Click on the latest pipeline and select the django_deployment job. The output will show that the deploy job is waiting for user input.

You can see the results of this pipeline by visiting https://gitlab-ce-cxlx0c4v.lab.practical-devsecops.training/root/django-nv/pipelines.

Sometimes, to prevent the automatic execution of the deploy job in the pipeline, it needs to be delayed. To ensure the job runs manually, you can use the when: manual attribute.

Why do we use the when: manual attribute?
> Deployments can be either automated or manual. Automated deployments, known as Continuous Deployment, occur immediately after changes are merged. Manual deployments, known as Continuous Delivery, are executed by someone who has reviewed the entire process and makes the final decision to deploy.
Developers often make frequent, sequential updates to the code, leading to continuous changes. By using when: manual, we ensure that all updates are finalized in the main branch before deploying the changes through a manual deployment in the pipeline.

The deploy stage is typically the final step in a CI/CD pipeline. It’s responsible for delivering the code to various environments such as development, staging, or production, depending on your choice.

## Conclusion
The CI/CD pipeline is a powerful system that automates software delivery. It guides the process from the first code submission to the final release in production. The pipeline is organized into key stages, each ensuring the software is created, tested, merged, and launched effectively and reliably. These stages are:

Build: The initial code compilation happens here, preparing it for further testing.
Test: The software undergoes thorough testing to find and fix any issues, ensuring quality.
Integration: The software is combined with other systems to check how well it works within the larger setup.
Deploy: In this final stage, the software is released to production and becomes available to users.
By combining these steps into a smooth, automated process, the CI/CD pipeline improves the development cycle. It increases the speed, reliability, and efficiency of software delivery. This organized approach encourages continuous improvement, allowing development teams to enhance software products quickly and deliver high-quality results faster.
