Learn how to embed Checkov into Jenkins CI/CD pipeline
================================================================

Use Checkov tool to perform SAST in Jenkins CI/CD pipeline
--------------------------------

In this scenario, you will learn how to embed Checkov in the Jenkins CI/CD pipeline.

Create a new job
-----------

> The Jenkins system is already configured with GitLab. If you wish to know how to configure Jenkins with GitLab, you can check out this link.

Add the repository for Terraform
--------------

Create a new project by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/projects/new#blank_project, give it a name golang and click Create project button. Once done, we need to push our source code into GitLab, let’s download the code using git clone in DevSecOps Box.

```
git clone https://gitlab.practical-devsecops.training/pdso/terraform.git terraform
cd terraform
git remote rename origin old-origin
git remote add origin http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/terraform.git
git push -u origin --all
```

And enter the Gitlab credentials.

```
git push -u origin --tags
```

Create a Job
-----------

We will create a new job in Jenkins by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/newJob.

You can use the following details to log into Jenkins.

Provide a name for your new item, e.g., terraform, select the Pipeline option, and click on the OK button.

In the next screen, click on the Build Triggers tab, check the Build when a change is pushed to GitLab..... checkbox.

At the bottom right-hand side, just below the Comment (regex) for triggering a build form field, you will find the Advanced… button. Please click on it.

Then, click on the Generate button under Secret token to generate a token. We will use this token for Gitlab’s Webhook Settings. This webhook setting will allow Gitlab to let Jenkins know whenever a change is made to the repository.

Please visit the following GitLab URL to set up the Jenkins webhook.

- url : https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/terraform/hooks

Fill the form using the following details.

- URL : https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/project/terraform
- Secret Token : paste the secret token we just generated above

Click on the Add webhook button, and go back to the Jenkins tab to continue the setup process.

Click on the Pipeline tab, and select Pipeline script from SCM from Definition options. Once you do that, few more options would be made available to you.

Select Git as SCM, enter our terraform repository http url.

- Repository URL : http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/terraform.git

Since we haven’t added the Gitlab credentials to the Jenkins system, you will get an error.

Let’s add the credentials by clicking on the Add button (the one with a key symbol). Select the Jenkins option and fill the pop-up form with the following details.

- username: root
- password: pdso-training
- id    : gitlab-auth

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
We do have four stages in this pipeline, build, test, integration and prod.

Let’s log in to Gitlab using the following details.

- gitlab url : https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training
- Username  : root
- Password : pdso-training

Add a new file to the repository by clicking on the +(plus) button and give it a name as Jenkinsfile, then add the above script into the file.

Save changes to the file using the Commit changes button.

Verify the pipeline run
-----------

Since we want to use Jenkins to execute the CI/CD jobs, we need to remove .gitlab-ci.yml from the git repository. Doing so will prevent Gitlab from running the CI jobs on both the Gitlab Runner and the Jenkins systems.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build history to see the output.

Exercise
-----------

Recall techniques you have learned in the previous module (Secure SDLC and CI/CD).

1. Read the Checkov documentation [here](https://www.checkov.io/documentation.html)
2. Run the Checkov tool in a new stage called checkov and save the output as a JSON file
3. Follow all the best practices while embedding Checkov in the CI/CD pipeline

> Please try to do this exercise without looking at the solution on the next page.

Embed Checkov in Jenkins
-----------------

As discussed in the Secure IaC using Checkov exercise, we can embed Checkov in our CI/CD pipeline. However, you need to test the command manually before you embed this SAST tool in the CI pipeline.

```
pipeline {
    agent any

    options {
        gitLabConnection('gitlab')
    }

    stages {
        stage("checkov") {
            steps {
                sh "docker run --rm -w /src -v \$(pwd):/src bridgecrew/checkov -d aws -o json | tee checkov-output.json"
            }
            post {
                always {
                    archiveArtifacts artifacts: 'checkov-output.json', fingerprint: true
                }
            }
        }
        stage("test") {
            steps {
                echo "This is a test step"
            }
        }
        stage("integration") {
            steps {
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

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/terraform.

Click on the appropriate job name to see the output.

You will notice that the checkov stage’s output is saved in the checkov-output.json file.

Allow the stage failure
-----------

We do not want to fail the builds/jobs/scan in DevSecOps Maturity Levels 1 and 2, as security tools spit a significant amount of false positives.

You can use the catchError function to “not fail the build” even though the tool found issues.

> Reference: https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps

```
        stage("checkov") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {     // Allow the sast stage to fail
                    sh "docker run --rm -w /src -v \$(pwd):/src bridgecrew/checkov -d aws -o json | tee checkov-output.json"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'checkov-output.json', fingerprint: true
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
        stage("checkov") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh "docker run --rm -w /src -v \$(pwd):/src bridgecrew/checkov -d aws -o json | tee checkov-output.json"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'checkov-output.json', fingerprint: true
                }
            }
        }
        stage("test") {
            steps {
                echo "This is a test step."
            }
        }
        stage("integration") {
            steps {
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

You will notice that the checkov job failed. However, it didn’t block other jobs from continuing further.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/terraform.

Click on the appropriate job name to see the output.

