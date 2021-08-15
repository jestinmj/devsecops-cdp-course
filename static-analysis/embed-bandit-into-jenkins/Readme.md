Learn how to embed Bandit in the Jenkins CI/CD pipeline
================================================================
****

Use Bandit tool to do SAST in Jenkins CI/CD pipeline
----------------------------------------------------------------
In this scenario, you will learn how to embed Bandit in the Jenkins CI/CD pipeline.

Create a new job
-----------------

> The Jenkins system is already configured with GitLab. If you wish to know how to configure Jenkins with GitLab, you can check out this [link](https://gitlab.practical-devsecops.training/pdso/jenkins/-/blob/master/tutorials/configure-jenkins-with-gitlab.md).

Login to you jenkins server 

Provide a name for your new item, e.g., django.nv, select the Pipeline option, and click on the OK button.

In the next screen, click on the Build Triggers tab, check the Build when a change is pushed to GitLab..... checkbox.

At the bottom right-hand side, just below the Comment (regex) for triggering a build form field, you will find the Advanced… button. Please click on it.

Then, click on the Generate button under Secret token to generate a token. We will use this token for GitLab’s Webhook Settings. This webhook setting will allow GitLab to let Jenkins know whenever a change is made to the repository.

Please visit the following GitLab URL to set up the Jenkins webhook.

Click on the Add webhook button, and go back to the Jenkins tab to continue the setup process.

Click on the Pipeline tab, and select Pipeline script from SCM from Definition options. Once you do that, few more options would be made available to you. 

Select Git as SCM, enter our django.nv repository http url. 

Let’s add the credentials by clicking on the Add button (the one with a key symbol). Select the Jenkins option and fill the pop-up form with the following details.

Click on the Add button, and select our new credentials from the Credentials Dropdown.

A simple CI/CD pipeline
-----------------

Considering your DevOps team created a simple Jenkinsfile with the following contents.

```
pipeline {
    agent any

    options {
        gitLabConnection('gitlab')
    }

    stages {
        stage("build") {
            agent {
                docker {
                    image 'python:3.6'
                    args '-u root'
                }
            }
            steps {
                sh """
                pip3 install --user virtualenv
                python3 -m virtualenv env
                . env/bin/activate
                pip3 install -r requirements.txt
                python3 manage.py check
                """
            }
        }
        stage("test") {
            agent {
                docker {
                    image 'python:3.6'
                    args '-u root'
                }
            }
            steps {
                sh """
                pip3 install --user virtualenv
                python3 -m virtualenv env
                . env/bin/activate
                pip3 install -r requirements.txt
                python3 manage.py test taskManager
                """
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

We do have four stages in this pipeline, build, test, integration and prod. We did integrate SCA/OAST beforehand, so let’s carry it forward in this exercise as well.

As a security engineer, I do not care what they are doing as part of these stages. Why? Imagine having to learn every build/testing tool used by your DevOps team. It will be a nightmare. Instead, rely on the DevOps team for help.

**Login to your gitlab account**

Add a new file to the repository by clicking on the +(plus) button and give it a name as Jenkinsfile, then add the above script into the file.

Save changes to the file using the Commit changes button.

Verify the pipeline run
-----------------

Since we want to use Jenkins to execute the CI/CD jobs, we need to remove .gitlab-ci.yml from the git repository. Doing so will prevent Gitlab from running the CI jobs on both the Gitlab Runner and the Jenkins systems.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build history to see the output.

Exercise
-----------------

Recall techniques you have learned in the previous module (Secure SDLC and CI/CD).

1. Read the [bandit documentation](https://github.com/PyCQA/bandit/tree/master/bandit)
2. Embed SAST backend tool, Bandit in sast stage
3. You can either install Bandit manually or use hysnsec/bandit docker container
4. Follow all the best practices while embedding Bandit in the CI/CD pipeline, and don’t forget the tool evaluation criteria

> Please try to do this exercise without looking at the solution on the next page.

Embed Bandit in Jenkins
-----------------

As discussed in the Static Analysis using Bandit exercise, we can embed bandit in our CI/CD pipeline. However, you need to test the command manually before you embed this SAST tool in the pipeline.

```
pipeline {
    agent any

    options {
        gitLabConnection('gitlab')
    }

    stages {
        stage("build") {
            agent { 
                docker { 
                    image 'python:3.6'
                    args '-u root'
                }
            }
            steps {
                sh """
                pip3 install --user virtualenv
                python3 -m virtualenv env
                . env/bin/activate
                pip3 install -r requirements.txt
                python3 manage.py check
                """
            }
        }
        stage("test") {
            agent { 
                docker { 
                    image 'python:3.6'
                    args '-u root'
                }
            }
            steps {
                sh """
                pip3 install --user virtualenv
                python3 -m virtualenv env
                . env/bin/activate
                pip3 install -r requirements.txt
                python3 manage.py test taskManager
                """
            }
        }
        stage("sast") {
            steps {
                sh "docker run -v \$(pwd):/src --rm hysnsec/bandit -r /src -f json -o /src/bandit-output.json"
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-output.json', fingerprint: true
                }
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



As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build history to see the output.

Allow the stage failure
-----------------

We do not want to fail the builds/jobs/scan in DevSecOps Maturity Levels 1 and 2, as security tools spit a significant amount of false positives.

You can use the catchError function to “not fail the build” even though the tool found security issues.

> Reference: https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps.

```
        stage("sast") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {     // Allow the sast stage to fail
                    sh "docker run -v \$(pwd):/src --rm hysnsec/bandit -r /src -f json -o /src/bandit-output.json"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-output.json', fingerprint: true
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
            agent {
                docker {
                    image 'python:3.6'
                    args '-u root'
                }
            }
            steps {
                sh """
                pip3 install --user virtualenv
                python3 -m virtualenv env
                . env/bin/activate
                pip3 install -r requirements.txt
                python3 manage.py check
                """
            }
        }
        stage("test") {
            agent {
                docker {
                    image 'python:3.6'
                    args '-u root'
                }
            }
            steps {
                sh """
                pip3 install --user virtualenv
                python3 -m virtualenv env
                . env/bin/activate
                pip3 install -r requirements.txt
                python3 manage.py test taskManager
                """
            }
        }
        stage("sast") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh "docker run -v \$(pwd):/src --rm hysnsec/bandit -r /src -f json -o /src/bandit-output.json"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-output.json', fingerprint: true
                }
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

You will notice that the sast stage failed. However, it didn’t block other jobs from continuing further.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build history to see the output.

Notes
---------

The above option mounts the current directory in the host (runner) to /src inside the container. This could also be -v /home/ubuntu/code:/src or c:\Users\username\code:/src if you were using windows.

Instead of manually removing the container after the scan, we can use the –rm option so the docker can clean up after itself.