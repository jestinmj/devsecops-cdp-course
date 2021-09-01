GitLab rules for Conditional Pipelines
================================================================

Learn how to include or exclude jobs in Gitlab CI/CD system
-------

In this scenario, you will learn how to include or exclude jobs in GitLab CI/CD pipeline.

You will learn Gitlab CI/CD system, enabling you to understand and work with 9 different CI/CD systems.

A simple CI/CD pipeline
----------

> Gitlab CI/CD is an implementation of the CI/CD pipeline, which you can use to create a deployment pipeline for your project.
>
> Learning Gitlab CI/CD pipeline helps you automatically learn many CI/CD systems like Jenkins, Travis CI, Circle CI, Bitbucket Pipelines, GitHub Actions, Drone CI, and others with minor changes.

We saw the following simple CI/CD pipeline in Create Simple CI Pipeline exercise.

```
# This is how a comment is added to a YAML file; please read them carefully.

stages:         # Dictionary
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - prod         # this is prod/production stage

build:            # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same, i.e., build
  script:
    - echo "This is a build step."  # We are running an echo command, but it can be any command.

test:
  stage: test
  script:
    - echo "This is a test step."
    - exit 1     # Non zero exit code, fails a job.

integration:            # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
```

Let’s log into Gitlab using the following details and execute this pipeline once again.

- Gitlab URL :	https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml
- Username: 	root
- Password: 	pdso-training

Next, we need to create a CI/CD pipeline by adding the above content to the .gitlab-ci.yml file.

Let’s click on the Edit button to start adding the content,

Once done, you can save the file’s changes using the Commit changes button.

Verify the pipeline run
----------

As soon as a change is made to the repository, the pipeline starts executing the jobs.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Rules attributes
-------

rules is YAML syntax for GitLab CI to include or exclude your jobs in pipelines. rules replaces the only and except clauses. Using this syntax, you can control when a job will be triggered in a pipeline based on the rules you defined in .gitlab-ci.yml file.

> Check out the changelog from GitLab that introduced rules clause https://about.gitlab.com/blog/2020/05/06/gitlab-com-13-0-breaking-changes/.

Let’s see some examples of the rules clause.

rules:if
-------

```
stages:         # Dictionary
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - prod         # this is prod/production stage

build:              # this is job named build, it can be anything, job1, job2, etc.,
  stage: build      # this job belongs to the build stage. Here both job name and stage name is the same, i.e., build
  script:
    - echo "This is a build step."          # We are running an echo command, but it can be any command.
  rules:
    - if: '$CI_COMMIT_BRANCH == "master"'   # this job will get triggered when the branch name is __master__
```

You will notice that build job has if statement that uses branch name under rules as a condition. So, any changes in master branch will kick start the pipelines because the value ​​being compared is master. Other than that, you can also use any expressions like (==, !=, =~, ~=) and conjunction/disjunction like (&&, ||) then combine them with the help of predefined variables from GitLab to make your CI/CD workflow.

> If no attributes are defined in rules clause, the defaults are when: on_success and allow_failure: false. That is by default execute this job when the previous jobs in earlier stages succeeded (when: on_success), and fail the entire build if this job fails to run (allow_failure: false).

```
stages:         # Dictionary
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - staging      # this is staging stage
 - prod         # this is prod/production stage

job1:               # this is job named build, it can be anything, job1, job2, etc.,
  stage: build      # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step"          # We are running an echo command, but it can be any command.

job4:
  stage: test
  script:
    - echo "This is a test step."
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

The above content has job4, which will get triggered with Merge Request event.

rules:changes
-------

```
stages:         # Dictionary
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - prod         # this is prod/production stage

build:              # this is job named build, it can be anything, job1, job2, etc.,
  stage: build      # this job belongs to the build stage. Here both job name and stage name is the same, i.e., build
  script:
    - echo "This is a build step."          # We are running an echo command, but it can be any command.
  rules:
    - changes:
      - Dockerfile
```

In this sample, we define the rule clause to specify under what rules the job should be executed. The above sample specifies that the job named build should only run when a file named Dockerfile is changed. So, if you edit the .gitlab-ci.yml file, then copy the above content and save the changes, it won’t execute the pipeline because the was no change was no change to the Dockerfile.

The changes clause can be combined with if statement as shown below:

```
stages:         # Dictionary
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - prod         # this is prod/production stage

build:              # this is job named build, it can be anything, job1, job2, etc.,
  stage: build      # this job belongs to the build stage. Here both job name and stage name is the same, i.e., build
  script:
    - echo "This is a build step."          # We are running an echo command, but it can be any command.
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      changes:
        - Dockerfile
```

rules:exists
-------

```
stages:         # Dictionary
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - prod         # this is prod/production stage

build:              # this is job named build, it can be anything, job1, job2, etc.,
  stage: build      # this job belongs to the build stage. Here both job name and stage name is the same, i.e., build
  script:
    - docker build -t $CI_REGISTRY/root/django-nv .
  rules:
    - exists:
      - Dockerfile
```
In the above example, a job will run when certain file exists. In this case, our rule specifies to the run when a file named Dockerfile exists, or you can use [glob patterns](https://en.wikipedia.org/wiki/Glob_(programming)) to match multiple files in a specific directory. 

rules:allow_failure
-------

```
stages:         # Dictionary
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - staging      # this is staging stage
 - prod         # this is prod/production stage

job4:
  stage: staging
  script:
    - echo "This is a deploy step to staging environment."
    - exit 1    # Non zero exit code, fails a job.
  rules:
    - if: '$CI_COMMIT_BRANCH == "master"'   # this job will get triggered when the branch name is __master__
      allow_failure: true

job5:
  stage: prod
  script:
    - echo "This is a deploy step to production environment."
  rules:
    - if: '$CI_COMMIT_TAG !~ "/^$/"'   # this job will trigger when you create a new tag
      when: manual
```

In this file:

1. job4: if the changes are pushed to master branch, job4 will run, and the pipeline will continue to run the next job because there is allow_failure: true even though there is an exit 1 indicting a job failure
2. job5: if the changes are pushed for a new tag with any name, and need a human approval before the job can run

As discussed, any change to the repo kick starts the pipeline in accordance with the rules specified in the job.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

