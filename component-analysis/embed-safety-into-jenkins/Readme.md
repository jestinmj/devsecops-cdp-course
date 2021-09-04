How to Embed Safety into Jenkins
================================================================================

Use Safety tool to do OAST in Jenkins CI/CD pipeline
--------------------------------------------------------------------------------

In this scenario, you will learn how to embed OAST/SCA in the Jenkins CI/CD pipeline.


Create a new job
-----------

> The Jenkins system is already configured with GitLab. If you wish to know how to configure Jenkins with GitLab, you can check out this [link](https://gitlab.practical-devsecops.training/pdso/jenkins/-/blob/master/tutorials/configure-jenkins-with-gitlab.md).

We will create a new job in Jenkins by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/newJob.

You can use the following details to log into Jenkins.

- Username : root
- Password : pdso-training

Provide a name for your new item, e.g., django.nv, select the Pipeline option, and click on the OK button.

In the next screen, click on the Build Triggers tab, check the Build when a change is pushed to GitLab..... checkbox.

At the bottom right-hand side, just below the Comment (regex) for triggering a build form field, you will find the Advanced… button. Please click on it.

Then, click on the Generate button under Secret token to generate a token. We will use this token for GitLab’s Webhook Settings. This webhook setting will allow GitLab to let Jenkins know whenever a change is made to the repository.

Please visit the following GitLab URL to set up the Jenkins webhook.

- URL : https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/hooks

Fill the form using the following details.

- URL :	https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/project/django.nv
- Secret Token : Paste the secret token we just generated above.

Click on the Add webhook button, and go back to the Jenkins tab to continue the setup process.

Click on the Pipeline tab, and select Pipeline script from SCM from Definition options. Once you do that, few more options would be made available to you.

Select Git as SCM, enter our django.nv repository http url. 

- Repository URL :	http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv.git

Since we haven’t added the GitLab credentials to the Jenkins system, you will get an error.

Let’s add the credentials by clicking on the Add button (the one with a key symbol). Select the Jenkins option and fill the pop-up form with the following details.

- Username : root
- Password : pdso-training
- ID : gitlab-auth
- Description : Leave it blank as it’s optional

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

Let’s login into Gitlab using the following details.

- Gitlab URL : https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training
- Username : root
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

1. Embed OAST scanning, Safety as test stage
2. You can make use of hysnsec/safety docker image if you wish
3. Understand the use of Docker’s -v (volume mount) flag/option
4. Ensure you follow the DevSecOps Gospel and best practices while embedding the safety tool
5. Rename test stage name to oast

> Please try to do this exercise without looking at the solution on the next page.

Embed Safety in Jenkins
-----------------

As discussed in the SCA using the Safety exercise, we can embed the Safety tool in our CI/CD pipeline. However, do remember you need to run the command manually before you embed OAST in the pipeline.

> Do you wonder which stage this job should go into?

Most of the code (up to 95%) in any software project is open-source/third-party components. It makes sense to perform SCA scans before static analysis.

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
        stage("oast-frontend") {
            agent {
                docker { 
                    image 'node:alpine3.10' 
                    args '-u root'
                }
            }
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh """
                    npm install
                    npm install -g retire
                    retire --outputformat json --outputpath retirejs-report.json --severity high
                    """
                }
            }
        }
        stage("oast") {
            steps {
                sh "docker run -v \$(pwd):/src --rm hysnsec/safety check -r requirements.txt --json | tee oast-results.json"
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

You will notice that the oast stores the output to a file oast-results.json. This is done to ensure we can process the results further either via APIs or vulnerability management systems like Defect Dojo.

Allow the stage failure
-----------

You do not want to fail the builds in DevSecOps Maturity Levels 1 and 2. If a security tool fails a build upon security findings, you would want to allow it to fail and not block the pipeline as there would be false positives in the results.

You can use the catchError function to “not fail the build” even though the tool found security issues.

> Reference: https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps.

```
        stage("oast") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {     // Allow the sast stage to fail 
                    sh "docker run -v \$(pwd):/src --rm hysnsec/safety check -r requirements.txt --json | tee oast-results.json"
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
        stage("oast-frontend") {
            agent {
                docker { 
                    image 'node:alpine3.10' 
                    args '-u root'
                }
            }
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh """
                    npm install
                    npm install -g retire
                    retire --outputformat json --outputpath retirejs-report.json --severity high
                    """
                }
            }
        }
        stage("oast") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') { 
                    sh "docker run -v \$(pwd):/src --rm hysnsec/safety check -r requirements.txt --json | tee oast-results.json"
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
            archiveArtifacts artifacts: '*.json', fingerprint: true
            deleteDir()                     // clean up workspace
        }
    }
}
```

You will notice that the oast stage has failed but didn’t block the other jobs from running.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.