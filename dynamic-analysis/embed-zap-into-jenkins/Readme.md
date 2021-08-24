Learn how to embed ZAP into Jenkins CI/CD pipeline
================================================================

Use ZAP tool to do DAST in Jenkins CI/CD pipeline
--------------------------------------------------------------------------------

In this scenario, you will learn how to embed DAST in the Jenkins CI/CD pipeline.

You will learn to use ZAP Baseline Scan in CI/CD pipeline using all the best practices mentioned in the Practical DevSecOps Gospel.

Create a new job
-----------

> The Jenkins system is already configured with GitLab. If you wish to know how to configure Jenkins with GitLab, you can check out this [link](https://gitlab.practical-devsecops.training/pdso/jenkins/-/blob/master/tutorials/configure-jenkins-with-gitlab.md)

We will create a new job in Jenkins by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/newJob.

You can use the following details to log into Jenkins.
> username: root
>
> password: pdso-training

Provide a name for your new item, e.g., django.nv, select the Pipeline option, and click on the OK button.

In the next screen, click on the Build Triggers tab, check the Build when a change is pushed to GitLab..... checkbox.

At the bottom right-hand side, just below the Comment (regex) for triggering a build form field, you will find the Advanced… button. Please click on it.

Then, click on the Generate button under Secret token to generate a token. We will use this token for GitLab’s Webhook Settings. This webhook setting will allow GitLab to let Jenkins know whenever a change is made to the repository.

Please visit the following GitLab URL to set up the Jenkins webhook.

> url: https://gitlab-ce-xqihndz0.lab.practical-devsecops.training/root/django-nv/hooks

Fill the form using the following details.
> URL: https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/project/django.nv
> 
> Secret Token: Paste the secret token we just generated above.

Click on the Add webhook button, and go back to the Jenkins tab to continue the setup process.

Click on the Pipeline tab, and select Pipeline script from SCM from Definition options. Once you do that, few more options would be made available to you.

Select Git as SCM, enter our django.nv repository http url. 

> Repository URL: http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv.git

Let’s add the credentials by clicking on the Add button (the one with a key symbol). Select the Jenkins option and fill the pop-up form with the following details.

> Username  : root
>
> Password  : root
>
> ID        : gitlab-auth

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

As we can see in the above CI Script, we have has two stages, namely build and test. Assuming you do not understand python or any programming language, we can safely consider the DevOps team is building and testing the code.

Let’s log in to Gitlab using the following details.
> Gitlab URL: https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training
> 
> Username: root
>
> Password: pdso-training

Add a new file to the repository by clicking on the +(plus) button and give it a name as Jenkinsfile, then add the above script into the file.

Save changes to the file using the Commit changes button.

Verify the pipeline run
-----------

Since we want to use Jenkins to execute the CI/CD jobs, we need to remove .gitlab-ci.yml from the git repository. Doing so will prevent Gitlab from running the CI jobs on both the Gitlab Runner and the Jenkins systems.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build history to see the output.

Exercise
-----------

We will use the Zed Attack Proxy (ZAP) to scan applications for security issues and then embed it into CI/CD using ZAP Baseline Scan docker image.

1. Explore ZAP Baseline script/tool details [here](https://www.zaproxy.org/docs/docker/baseline-scan/)
2. Use https://prod-XqiHnDZ0.lab.practical-devsecops.training as the endpoint for ZAP Scanning
3. Embed ZAP scanning as zap-baseline stage and save the output as JSON file
4. Remember to follow all best practices while adding the baseline scan to CI/CD pipeline

Once done, please do not forget to share the pipeline script with our staff.

Embed ZAP in Jenkins
-----------------

As discussed in the Dynamic Analysis using ZAP exercises, we can put ZAP in our CI/CD pipeline. We did ensure that the ZAP command runs fine in DevSecOps-Box, now we need to embed zap into CI/CD pipeline.

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
                    sh "docker run -u root -v \$(pwd):/zap/wrk:rw --rm -t owasp/zap2docker-stable zap-baseline.py -t https://prod-XqiHnDZ0.lab.practical-devsecops.training -J zap-output.json"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'zap-output.json', fingerprint: true
                }
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

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build history to see the output.

