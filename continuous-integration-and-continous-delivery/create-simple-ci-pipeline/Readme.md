GitLab CI/CD Basics
============

Use Gitlab CI/CD system to learn CI/CD concepts
--------------------------------

In this scenario, you will learn how to create a simple CI/CD pipeline.

You will learn Gitlab CI/CD systems, enabling you to understand CI/CD in 9 different CI/CD systems.

Understand YAML Syntax
----------------------------------------------------------------

> YAML (a recursive acronym for “YAML Ain’t Markup Language”) is a human-readable data serialization language. It is commonly used for configuration files and in applications where data is being stored or transmitted.
>
> Source [Wikipedia](https://en.wikipedia.org/wiki/YAML).

YAML is more comfortable for humans to read and write than more common data formats like XML or JSON. This format is typically used to configure systems like CI/CD systems, Infrastructure as Code tools, Kubernetes, and much more.

YAML files start with optional three dashes (—).


e.g.,
```
---
 # A list of gadgets
- Sony
- LG
- Apple
- Samsung
```

> Pro-tip: You will see these dashes in Ansible scripts but not in the GitLab CI script because they are optional here. However, some tools do enforce these dashes.

Gitlab CI/CD uses this list concept to create stages. Notice the lack of dashes (—) below.

```
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - prod         # this is prod/production stage
```

A dictionary (key/value pair) is represented in a simple key: value form (the colon should be followed by a space).

Gitlab CI/CD uses this to configure individual settings in a job.

```
  stage: test
  image: node:alpine3.10
  script: echo "hello world"
```
A dictionary can have other dictionaries or lists in them.
```
test:
  stage: test   # Dictionary item stage with the value test
  script:       # Dictionary item with a list as the value
    - echo "This is a test step."
    - exit 1         # Non zero exit code, fails a job.
```

Combining these concepts, we can create a simple Gitlab CI/CD pipeline with four stages and four jobs.

```
# This is how a comment is added to a YAML file; please read them carefully.

stages:         # Dictionary
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - prod         # this is prod/production stage

job1:
  stage: build  # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step."  # We are running an echo command, but it can be any command.
 
job2:
  stage: test
  script:
    - echo "This is a test step."
    - exit 1          # Non zero exit code, fails a job.

job3:          # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."

job4:
  stage: prod
  script:
    - echo "This is a deploy step."
```

Now that we know the basics of the YAML format.

Run a simple CI/CD pipeline
--------------------------------

We will use the YAML code from the previous step to create a simple Gitlab CI/CD pipeline.

Let’s log into GitLab using the following details.

> Gitlab URL : https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml
>
> Username: root 
> Password: pdso-training

Next, we need to create a CI/CD pipeline by adding the following content to the .gitlab-ci.yml file.

Click on the Edit button and replace the existing content in gitlab-ci.yml file with the content below.

```
# This is how a comment is added to a YAML file; please read them carefully.
 
stages:         # Dictionary
 - build        # this is build stage
 - test         # this is test stage
 - integration  # this is an integration stage
 - prod         # this is prod/production stage
 
job1:
  stage: build  # this job belongs to the build stage. Here both job name and stage name is the same, i.e., build
  script:
    - echo "This is a build step."  # We are running an echo command, but it can be any command.
 
job2:
  stage: test
  script:
    - echo "This is a test step."
    - exit 1          # Non zero exit code, fails a job.
 
job3:          # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."
 
job4:
  stage: prod
  script:
    - echo "This is a deploy step."
```

Save changes to the file using the Commit changes button.

Verify the pipeline run
----------

As soon as a change is made to the repository, the pipeline starts executing the jobs.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Exercise 3.1 Create a simple CI/CD pipeline
----------

In this exercise, you will edit the .gitlab-ci.yml file to create a simple CI/CD pipeline.

1. Create five stages namely build, test, integration, staging and prod (deploy phase)
2. Create a job in each of these stages with job names as build, test, integration, staging and prod (You can make use of simple echo commands under the script tag)
3. If you are not comfortable with the syntax, explore the GitLab CI syntax at https://docs.gitlab.com/ee/ci/yaml/README.html#stages


> Please do not forget to share the answer (a screenshot and the YML file) with our staff via Slack Direct Message (DM).
