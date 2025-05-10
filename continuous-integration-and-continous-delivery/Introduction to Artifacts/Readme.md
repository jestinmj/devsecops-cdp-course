## Working With Artifacts In GitLab CI/CD Pipeline

# Introduction to Artifacts

What Is An Artifact?
An artifact is an output generated during the pipeline process. It could be a result file from the application or any other item necessary for building an application.

Why Are Artifacts Important In CI/CD?
Artifacts play a significant role in the CI/CD pipeline for several reasons:

- Artifacts represent the state of a project at a specific point in time.
- Artifacts can be preserved and shared across different stages of the pipeline.
- Artifacts can be used to roll back a release to a previous version if something goes wrong.
Each step of the CI/CD pipeline produces an artifact that can be used by the next step in the process.

How Do Artifacts Work In A Pipeline?
The following flowchart illustrates how the pipeline works with artifacts.
![image](https://github.com/user-attachments/assets/85a37db7-9ec3-414d-a5bb-04355ebbf6fd)



Let’s understand the process based on the above image:

1. First, the user triggers the pipeline in a CI/CD application using the pipeline file (.gitlab-ci.yml, Jenkinsfile, etc.). After defining some jobs, the pipeline runs each job in sequence based on the established rules. In this case, the user also includes a rule to generate artifacts once the job is completed.
2. Next, the job runs in the pipeline process. When the pipeline file includes a rule for storing the output as artifacts, the job generates an artifact once it completes successfully.
3. Finally, after all the pipeline processes have finished, the deployment process is triggered.
In conclusion, artifacts are an essential part of the CI/CD pipeline. How they are managed can significantly impact the speed, safety, and reliability of software delivery.

# Saving Job Result As Artifact In GitLab
To manage the output as a file during the pipeline process, we aim to store the scan results in a file and save it on the CI system for further processing.

You can store the tool result(s) in a file using the artifacts tag as shown below.
```
someScan:
  script: 
    - ./security-tool.sh    # <-- this example script may generate a file as an output
  artifacts:                    # <--- To save results, we use artifacts tag
    paths:                      # <--- We then give the path/paths of the scan result files we want to store for further processing
    - vulnerabilities.json                  #<--- The filename
    when: always
    expire_in: 1 week       # <--- To save disk space, we want to store only for 1 week
```

As you can see above, we need to specify the output file’s path on line numbers 4 and 5 then the expiration(line number 6) under the artifacts tag.
To keep our pipeline simple for everyone, we will try to echo the JSON string into a file for now instead of running a security tool.

```
stages:   # Dictionary
 - build   # this is build stage
 - test    # this is test stage
 - integration # this is an integration stage
 - prod       # this is prod/production stage

build:       # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step"  # We are running an echo command, but it can be any command.
    - echo "{\"vulnerability\":\"SQL Injection\"}" > vulnerabilities.json
  artifacts:      # notice a new tag artifacts
    paths: [vulnerabilities.json]   # this is the path to the vulnerabilities.json file
    when: always
    expire_in: 1 week       # <--- To save disk space, we want to store only for 1 week

test:
  stage: test
  script:
    - echo "This is a test step."
    - exit 1         # Non zero exit code, fails a job.
  allow_failure: true   #<--- allow the build to fail but don't mark it as such

integration:        # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
```

Run the pipeline by clicking commit changes button.

Based on the above script you may see the following script in build job.
```
build:       # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step"  # We are running an echo command, but it can be any command.
    - echo "{\"vulnerability\":\"SQL Injection\"}" > vulnerabilities.json
  artifacts:      # notice a new tag artifacts
    paths: [vulnerabilities.json]   # this is the path to the vulnerabilities.json file
```
Based on above script, we define an artifacts tag to generate an artifact.

While the artifacts tag is defined in a build job, you can click the build job to see until the process is successful.
![image](https://github.com/user-attachments/assets/46c95700-2066-4ce8-82c1-371810a4eb41)

Once the job succeeds, you can see the artifact displayed at the end of the job report.
![image](https://github.com/user-attachments/assets/685ce2a6-54d3-4db9-a826-0a74241a41dd)

You will find and download the vulnerabilities.json file under the artifacts section on your right-hand side.
![image](https://github.com/user-attachments/assets/33e21790-e3a1-47c6-ae3c-5b16c65ef47c)

# Producing Artifact From Docker Output
Next, we will try to understand how we can produce the artifact from the docker output.

Now, let’s run the below script.
```
stages:   # Dictionary
 - build   # this is build stage
 - test    # this is test stage
 - integration # this is an integration stage
 - prod       # this is prod/production stage

build:       # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step"  # We are running an echo command, but it can be any command.

test:
  stage: test
  script:
    - echo "This is a test step."
    - docker run -i alpine sh -c "echo '{\"vulnerability\":\"XSS Injection\"}' > vulnerabilities.json"
  artifacts:      # notice a new tag artifacts
    paths: [vulnerabilities.json]   # this is the path to the vulnerabilities.json file
  allow_failure: true   #<--- allow the build to fail but don't mark it as such

integration:        # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
```

Run the pipeline by clicking commit changes button.

Based on the above script you can see the following script in test job.
```
test:
  stage: test
  script:
    - echo "This is a test step."
    - docker run -i alpine sh -c "echo '{\"vulnerability\":\"XSS Injection\"}' > vulnerabilities.json" # docker command produces an output file
  artifacts:      # notice a new tag artifacts
    paths: [vulnerabilities.json]   # this is the path to the vulnerabilities.json file
  allow_failure: true   #<--- allow the build to fail but don't mark it as such
  ```

Based on the above script, you may see that we define an artifact tag to generate an artifact from the script running inside docker.

We can see the results of this pipeline by visiting https://gitlab-ce-cxlx0c4v.lab.practical-devsecops.training/root/django-nv/pipelines.

While the artifacts tag is defined in a test job, you can click the test job to check whether the process succeeded.
![image](https://github.com/user-attachments/assets/d85571d7-2399-4ddc-a2de-3d20754c5dd2)

Oooops! We find an error here.
The error message informs that the pipeline is unable to locate the output file, so the artifact will not be generated.
> Docker has a -v command to bind the local machine path to the Docker container machine path. Please refer to the Manage data in Docker exercise for a detailed explanation.

Let’s modify the command to bind the local CI/CD machine with the docker container machine using -v option in the /app path inside the container.
`docker run -i -v $(pwd):/app alpine sh -c "echo '{\"vulnerability\":\"XSS Injection\"}' > /app/vulnerabilities.json"`

Here is the implementation of above command in the pipeline script:
```
stages:   # Dictionary
 - build   # this is build stage
 - test    # this is test stage
 - integration # this is an integration stage
 - prod       # this is prod/production stage

build:       # this is job named build, it can be anything, job1, job2, etc.,
  stage: build    # this job belongs to the build stage. Here both job name and stage name is the same i.e., build
  script:
    - echo "This is a build step"  # We are running an echo command, but it can be any command.

test:
  stage: test
  script:
    - echo "This is a test step."
    - docker run -i -v $(pwd):/app alpine sh -c "echo '{\"vulnerability\":\"XSS Injection\"}' > /app/vulnerabilities.json" # make an output file created in /app path
  artifacts:      # notice a new tag artifacts
    paths: [vulnerabilities.json]   # this is the path to the vulnerabilities.json file in the local CI/CD machine
  allow_failure: true   #<--- allow the build to fail but don't mark it as such

integration:        # integration job under stage integration.
  stage: integration
  script:
    - echo "This is an integration step."

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
```

Perfect! Now, the results are successful. You can see the generated file after the pipeline script works as expected in generating an artifact.

# Conclusion
In GitLab, we use an artifact tag to store job results. This tag saves script outputs, like files from security scans, for later use. These outputs, or artifacts, are stored in specific paths so we can easily find them later.

We showed an example job called build. In this job, we used an echo command to create a file named “vulnerabilities.json”.
> Artifacts are created for each job when we define the ‘artifacts’ tag. These artifacts give us important information about each stage of our process. We can download them to look at them more closely. This helps us fix problems and keep our CI/CD pipeline working well.

 Additional Resources
- GitLab CI/CD Artifact: https://docs.gitlab.com/ee/ci/jobs/job_artifacts.html
- Jenkins Artifact: https://www.jenkins.io/doc/pipeline/tour/tests-and-artifacts/
- GitHub Action Artifact: https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts
- Artifact DevOps: https://medium.com/@balaug3/artifact-devops-69335d054e20
