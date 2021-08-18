Learn how to embed Gosec into Jenkins CI/CD pipeline
================================================

Use Gosec tool to do SAST in Jenkins CI/CD pipeline
------------------------------------------------

In this scenario, you will learn how to embed GoSec in the Jenkins CI/CD pipeline.

Create a new job
-----------------
> The Jenkins system is already configured with Gitlab. If you wish to know how to configure Jenkins with Gitlab, you can check out this link.
>
> You don’t need to create a new project because the following commands will create a new project and push the code.
>
> Before executing the following commands, you need to wait until GitLab machine is up.

Add the repository for Golang
-----------------
Using git clone, let’s download the golang code that needs to be tested for security to the DevSecOps Box.

```
git clone https://gitlab.practical-devsecops.training/pdso/golang.git golang
cd golang
```

Let’s rename the git remote URL to our Gitlab instance.
```
git remote rename origin old-origin
git remote add origin http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/golang.git
git push -u origin --all
```

Create a job
-----------

We will create a new job in Jenkins by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/newJob.

You can use the following details to log into Jenkins.

Provide a name for your new item(pipeline), e.g., golang, select the Pipeline option, and click on the OK button.

In the next screen, click on the Build Triggers tab, check the Build when a change is pushed to GitLab..... checkbox.

At the bottom right-hand side, just below the Comment (regex) for triggering a build form field, you will find the Advanced… button. Please click on it.

Then, click on the Generate button under Secret token to generate a token. We will use this token for Gitlab’s Webhook Settings. This webhook setting will allow Gitlab to let Jenkins know whenever a change is made to the repository.

> Please visit the following GitLab URL to set up the Jenkins webhook.

Fill the form using the following details.
- jenkins url : https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/project/django.nv
- secret token : xxxxxxxxxxxx

Click on the Add webhook button, and go back to the Jenkins tab to continue the setup process.

Click on the Pipeline tab, and select Pipeline script from SCM from Definition options. Once you do that, few more options would be made available to you.

Select Git as SCM, enter our golang repository http url. 

Since we haven’t added the Gitlab credentials to the Jenkins system, you will get an error.

output
```
Failed to connect to repository : Command "git ls-remote -h -- http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/golang HEAD" returned status code 128:
stdout:
stderr: remote: HTTP Basic: Access denied
fatal: Authentication failed for 'http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/golang.git/'
```

Let’s add the credentials by clicking on the Add button (the one with a key symbol). Select the Jenkins option and fill the pop-up form with the following details.

Click on the Add button, and select our new credentials from the Credentials Dropdown.

The error we experienced before should be gone by now.

Finally, click the Save button.

A simple CI/CD pipeline
-----------

Considering your DevOps team created a simple Jenkinsfile with the following contents.

```
pipeline {
    agent any

    options {
        gitLabConnection('gitlab')
    }

    stages {
        stage("build") {
            steps {
                echo "This is a build step"
            }
        }
        stage("test") {
            steps {
                echo "This is a test step"
            }
        }
        stage("integration") {
            steps {
                // Allow the stage to fail
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    echo "This is an integration step"
                    sh "exit 1"
                }
            }
        }
        stage("prod") {
            steps {
                input "Deploy to production?"
                echo "This is a deploy step."
            }
        }
    }
    post {
        failure {
            updateGitlabCommitStatus(name: "${env.STAGE_NAME}", state: 'failed')
        }
        unstable {
            updateGitlabCommitStatus(name: "${env.STAGE_NAME}", state: 'failed')
        }
        success {
            updateGitlabCommitStatus(name: "${env.STAGE_NAME}", state: 'success')
        }
        aborted {
            updateGitlabCommitStatus(name: "${env.STAGE_NAME}", state: 'canceled')
        }
        always { 
            deleteDir()                     // clean up workspace
        }
    }
}
```
We do have 4 stage in this pipeline, build, test, integration and prod. We did integrate SCA/OAST beforehand, so we can carry it forward in this exercise.

As a security engineer, I do not care what they are doing as part of these stages. Why? Imagine having to learn every build/testing tool used by your DevOps team. It will be a nightmare. Instead, rely on the DevOps team for help.

Let’s log in to Gitlab account.

Add a new file to the repository by clicking on the +(plus) button and give it a name as Jenkinsfile, then add the above script into the file.

Save changes to the file using the Commit changes button.

Verify the pipeline run
-----------

Since we want to use Jenkins to execute the CI/CD jobs, we need to remove .gitlab-ci.yml from the git repository. Doing so will prevent Gitlab from running the CI jobs on both the Gitlab Runner and the Jenkins systems.

> Don’t forget to disable Auto DevOps in Gitlab as it will execute the job when any changes are pushed to the repository even though the .gitlab-ci.yaml file is missing.
>
> Visit http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/settings/ci_cd to disable it.

Exercise
-----------

Recall techniques you have learned in the previous module (Secure SDLC and CI/CD).

1. Read the gosec documentation
2. Embed SAST backend tool, Gosec in the test stage
3. Ensure the job is running under the test stage
4. Follow all the best practices while embedding Gosec in
5. the CI/CD pipeline. Don’t forget the tool evaluation criteria

> Please try to do this exercise without looking at the solution on the next page.

Embed Gosec in Jenkins
-----------------

As discussed in the Static Analysis using Gosec exercise, we can embed the GoSec in our CI/CD pipeline. However, you need to test the command manually before you embed this SAST tool in the pipeline.

```
pipeline {
    agent any

    options {
        gitLabConnection('gitlab')
    }

    stages {
        stage("build") {
            steps {
                echo "This is a build step"
            }
        }
        stage("sast") {
            steps {
                sh "docker run --rm -w /src -v \$(pwd):/src securego/gosec -fmt json -out /src/gosec-output.json /src/..."
            }
            post {
                always {
                    archiveArtifacts artifacts: 'gosec-output.json', fingerprint: true
                }
            }
        }
        stage("integration") {
            steps {
                // Allow the stage to fail
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    echo "This is an integration step."
                    sh "exit 1"
                }
            }
        }
        stage("prod") {
            steps {
                input "Deploy to production?"
                echo "This is a deploy step."
            }
        }
    }
    post {
        failure {
            updateGitlabCommitStatus(name: STAGE_NAME, state: 'failed')
        }
        unstable {
            updateGitlabCommitStatus(name: STAGE_NAME, state: 'failed')
        }
        success {
            updateGitlabCommitStatus(name: STAGE_NAME, state: 'success')
        }
        aborted {
            updateGitlabCommitStatus(name: STAGE_NAME, state: 'skipped')
        }
        always { 
            deleteDir()                     // clean up workspace
        }
    }
}
```

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/golang.

Click on the appropriate build history to see the output.

Allow the stage failure
-----------

We do not want to fail the builds/jobs/scan in DevSecOps Maturity Levels 1 and 2, as security tools spit a significant amount of false positives.

You can use the catchError function to “not fail the build” even though the tool found issues.

> Reference: https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps.

```
        stage("sast") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {     // Allow the sast stage to fail
                    sh "docker run --rm -w /src -v \$(pwd):/src securego/gosec -fmt json -out /src/gosec-output.json /src/..."
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'gosec-output.json', fingerprint: true
                }
            }
        }
```

After adding the catchError function, the pipeline would look like the following.

```
pipeline {
    agent any

    options {
        gitLabConnection('gitlab')
    }

    stages {
        stage("build") {
            steps {
                echo "This is a build step."
            }
        }
        stage("sast") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh "docker run --rm -w /src -v \$(pwd):/src securego/gosec -fmt json -out /src/gosec-output.json /src/..."
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'gosec-output.json', fingerprint: true
                }
            }
        }
        stage("integration") {
            steps {
                // Allow the stage to fail
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    echo "This is an integration step."
                    sh "exit 1"
                }
            }
        }
        stage("prod") {
            steps {
                input "Deploy to production?"
                echo "This is a deploy step."
            }
        }
    }
    post {
        failure {
            updateGitlabCommitStatus(name: STAGE_NAME, state: 'failed')
        }
        unstable {
            updateGitlabCommitStatus(name: STAGE_NAME, state: 'failed')
        }
        success {
            updateGitlabCommitStatus(name: STAGE_NAME, state: 'success')
        }
        aborted {
            updateGitlabCommitStatus(name: STAGE_NAME, state: 'skipped')
        }
        always {
            deleteDir()                     // clean up workspace
        }
    }
}
```

You will notice that the sast stage failed. However, it didn’t block other jobs from continuing further.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/golang.

Click on the appropriate build history to see the output.