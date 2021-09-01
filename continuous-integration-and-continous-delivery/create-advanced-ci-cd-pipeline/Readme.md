GitLab CI/CD Advanced
================================

Use Gitlab CI/CD system to learn Advanced CI/CD concepts
----------------------------------------------------------------

In this scenario, you will learn how to create an advanced CI/CD pipeline.

You will learn Gitlab CI/CD systems, enabling you to understand CI/CD in 9 different CI/CD systems.

A simple CI/CD pipeline
----------

> Gitlab CI/CD is an implementation of the CI/CD pipeline, which you can use to create a deployment pipeline for your project.
>
> Learning Gitlab CI/CD pipeline helps you automatically learn many CI/CD systems like Travis CI, Circle CI, and Bitbucket CI with minor changes.
>
> Other Gitlab CI/CD alternatives are Jenkins, Travis, Circle CI, Bitbucket Pipelines, and Drone CI.

We saw the following simple CI/CD pipeline in Create Simple CI Pipeline exercise.

```
# This is how a comment is added to a YAML file; please read them carefully.

stages:   # Dictionary
 - build   # this is build stage
 - test    # this is test stage
 - integration # this is an integration stage
 - prod       # this is prod/production stage

build:       # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same, i.e., build
  script:
    - echo "This is a build step."  # We are running an echo command, but it can be any command.

test:
  stage: test
  script:
    - echo "This is a test step."
    - exit 1         # Non zero exit code, fails a job.

integration:        # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
```

Let’s log into GitLab using the following details and execute this pipeline once again.

- Gitlab URL : https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml
- Username: root
- Password: pdso-training

Next, we need to create a CI/CD pipeline by adding the above content to the .gitlab-ci.yml file.

Let’s click on the Edit button to start adding the content.

Save changes to the file using the Commit changes button.

Verify the pipeline run
----------

As soon as a change is made to the repository, the pipeline starts executing the jobs.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Fail a build using exit code
-----------

As discussed in the Linux basics exercises, a process shares its pass/fail status via exit codes. The CI/CD systems also behave similarly and use exit codes to either pass or fail a job/stage.

```
stages:   # Dictionary
 - build   # this is build stage
 - test    # this is test stage
 - integration # this is an integration stage
 - prod       # this is prod/production stage

job1:       # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step"  # We are running an echo command, but it can be any command.

job2:
  stage: test
  script:
    - echo "This is a test step"
    # ************ Non zero exit code, fails a job. ************ #
    - exit 1

job3:        # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."

job4:
  stage: prod
  script:
    - echo "This is a deploy step."
```

You will notice that job2 has exit 1. When you add/edit this job in Gitlab, it will fail the build because of exit 1. CI/CD systems look for exit codes to determine if a job passed or failed.

For example, you ran a security tool on your codebase, and it found some security issues, then the security tool might give a non zero exit code. Non zero exit code fails a job (red color), but if the tool gives you a zero exit code (green color) CI/CD system will mark it as passed.

> Note
>
> By default, most CI/CD systems take the last command’s exit code. If you have multiple commands and some failed, but the last one passed, then the CI system will mark the job as passed.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

Allow the job failure
----------

You do not want to fail the builds in DevSecOps Maturity Levels 1 and 2. If a security tool fails a build upon security findings, you would not want this job to block the other jobs and stages as there could be false positives in the results.

You can use the allow_failure tag to “not fail the build” even though the tool found issues.

```
job2:
  stage: test
  script:
     - execute_script_that_will_fail
  allow_failure: true   #<--- allow the build to fail but don't mark it as such
```

The pipeline would look like the following.

```
stages:   # Dictionary
 - build   # this is build stage
 - test    # this is test stage
 - integration # this is an integration stage
 - prod       # this is prod/production stage

job1:       # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step"  # We are running an echo command, but it can be any command.

job2:
  stage: test
  script:
    - echo "This is a test step."
    - exit 1         # Non zero exit code, fails a job.
  allow_failure: true   #<--- allow the build to fail, but don't mark it as such


job3:        # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step"

job4:
  stage: prod
  script:
    - echo "This is a deploy step."
```

You will notice that job2 has exit 1. If you add the above script to the GitLab, it will fail the build because of the exit 1 command. The CI/CD systems look for exit codes to determine if a job passed or failed.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

You will notice that we now have an exclamation (!) mark instead of a green or red mark.

Save scan results
----------

To manage found vulnerabilities during the scan, we would like to store the scan results in a file and save it on the CI system for further processing.

You can store the tool result(s) in a file using the artifacts tag as shown below.

```
someScan:
  script: ./security-tool.sh    # <-- this tool generates vulnerabilities.json as output
  artifacts:                    # <--- To save results, we use artifacts tag
    paths:                      # <--- We then give the path/paths of the scan result files we want to store for further processing
    - vulnerabilities.json                  #<--- The filename
    expire_in: 1 week       # <--- To save disk space, we want to store only for 1 week
```

As you can see above, we need to specify the output file’s path on line numbers 4 and 5 and the expiration(line number 6) under the artifacts tag.

To keep our pipeline simple for everyone, we will echo the JSON string into a file for now instead of running a security tool.

```
stages:   # Dictionary
 - build   # this is build stage
 - test    # this is test stage
 - integration # this is an integration stage
 - prod       # this is prod/production stage

job1:       # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step"  # We are running an echo command, but it can be any command.
    - echo "{\"vulnerability\":\"SQL Injection\"}" > output.json
  artifacts:      # notice a new tag artifacts
    paths: [output.json]   # this is the path to the output.json file

job2:
  stage: test
  script:
    - echo "This is a test step."
    - exit 1         # Non zero exit code, fails a job.
  allow_failure: true   #<--- allow the build to fail but don't mark it as such

job3:        # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."

job4:
  stage: prod
  script:
    - echo "This is a deploy step."
```

You will notice that job1 generates the output.json, and if we do not specify expire_in tag, the output file will live on the CI System indefinitely.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the pipeline output.

> You will find the output.json file under the artifacts section on your right-hand side.

Implement Continuous Delivery
----------

If you wish to have a human approval process before deployment, you can use the continuous delivery feature of Gitlab using the when tag.

As you can see below, using a when: manual tag, we can enforce a human intervention (click the play button in Gitlab) to run a job (deployment).

```
deploy_prod:
  stage: deploy
  script:
    - echo "Deploy to prod server."
  when: manual   #<-- A human has to click a button (play button in Gitlab) for this task to execute.
```

To keep our pipeline simple for everyone, instead of deploying an app, we will add when tag to the pipeline.

```
stages:   # Dictionary
 - build   # this is build stage
 - test    # this is test stage
 - integration # this is an integration stage
 - prod       # this is prod/production stage

job1:       # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step"  # We are running an echo command, but it can be any command.
    - echo "{\"vulnerability\":\"SQL Injection\"}" > output.json
  artifacts:      # notice a new tag artifacts
    paths: [output.json]   # this is the path to the output.json file

job2:
  stage: test
  script:
    - echo "This is a test step."
    - exit 1         # Non zero exit code, fails a job.
  allow_failure: true   #<--- allow the build to fail but don't mark it as such

job3:        # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."

job4:
  stage: prod
  script:
    - echo "This is a deploy step."
  when: manual   #<-- A human has to click a button (play button in Gitlab) for this task to
```

You will notice that job4 has when: manual and it will enforce a human intervention, and a person has to approve the job before it runs.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the pipeline output.

Exercise: Fail a job and allow it to fail
----------

In this exercise, you will edit the .gitlab-ci.yml file to use advanced CI/CD options.

1. Create four stages, namely build, test, integration, and deploy
2. Create a file using the echo "this is an output" > output.txt command in the integration stage and upload it using the artifacts tag
3. Fail the integration job using exit code
4. Allow the integration job to fail yet move on to the next stage
5. Create a job requiring a person’s approval (a button, play button) before running this job

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

> Hint - CI Lint
>
> Please use the CI Lint feature available in GitLab to validate the .gitlab-ci.yml file.
> To access the CI Lint tool, navigate to CI/CD > Pipelines or CI/CD > Jobs in your project and click CI Lint.

> Hint - Upload Artifacts
> 
> Artifacts won’t upload under integration stage?
> Research the when:always tag in artifacts for GitLab. You can either google the tag or explore the GitLab documentation.