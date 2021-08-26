How to Embed Inspec into Jenkins
-----------

Use Inspec tool to achieve compliance automation in Jenkins CI/CD pipeline
----------

In this scenario, you will learn how to embed Inspec in the Jenkins CI/CD pipeline.

Create a new job
-----------

> The Jenkins system is already configured with GitLab. If you wish to know how to configure Jenkins with GitLab, you can check out this link.

We will create a new job in Jenkins by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/newJob.

You can use the following details to log into Jenkins.

- username: root
- password: pdso-training

Provide a name for your new item, e.g., django.nv, select the Pipeline option, and click on the OK button.

In the next screen, click on the Build Triggers tab, check the Build when a change is pushed to GitLab..... checkbox.

At the bottom right-hand side, just below the Comment (regex) for triggering a build form field, you will find the Advanced… button. Please click on it.

Then, click on the Generate button under Secret token to generate a token. We will use this token for GitLab’s Webhook Settings. This webhook setting will allow GitLab to let Jenkins know whenever a change is made to the repository.

Please visit the following GitLab URL to set up the Jenkins webhook.

- URL : https://gitlab-ce-xqihndz0.lab.practical-devsecops.training/root/django-nv/hooks

Fill the form using the following details.

- URL : https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/project/django.nv
- Secret Token : Paste the secret token we just generated above.

Click on the Add webhook button, and go back to the Jenkins tab to continue the setup process.

Click on the Pipeline tab, and select Pipeline script from SCM from Definition options. Once you do that, few more options would be made available to you.

Select Git as SCM, enter our django.nv repository http url. 

- Repository URL : http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv.git

Since we haven’t added the GitLab credentials to the Jenkins system, you will get an error.

Let’s add the credentials by clicking on the Add button (the one with a key symbol). Select the Jenkins option and fill the pop-up form with the following details.

- Username: root
- Password: pdso-training
- ID : gitlab-auth
- Description: Optional

Click on the Add button, and select our new credentials from the Credentials Dropdown.

The error we experienced before should be gone by now.

A simple CI/CD pipeline
----------

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

We do have four stages in this pipeline, build, test, integration and prod. Assuming you don’t understand Python or any programming language, we can safely consider the DevOps team is building and testing the code.

Let’s login into Gitlab using the following details.

- Gitlab URL : https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training
- Username : root
- Password : pdso-training

Add a new file to the repository by clicking on the +(plus) button and give it a name as Jenkinsfile, then add the above script into the file.

Save changes to the file using the Commit changes button.

Verify the pipeline run
----------

Since we want to use Jenkins to execute the CI/CD jobs, we need to remove .gitlab-ci.yml from the git repository. Doing so will prevent Gitlab from running the CI jobs on both the Gitlab Runner and the Jenkins systems.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build history to see the output

Embed Inspec in Jenkins
-----------------

As discussed in the automate compliance exercise, we can embed the Inspec tool in our CI/CD pipeline. However, you need to test the command manually before you embed this CaC tool in the pipeline.

We need to add credentials into Jenkins, namely, SSH Private Key and SSH hostname of the machine we are securing, i.e., production machine. Since we don’t want the credentials to be hardcoded in the Jenkinsfile. Let’s add the creds to the Jenkins credential store by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/credentials/store/system/domain/_/.

Click on the Add Credentials link on the left sidebar, and select SSH Username with private key as Kind, then add the following credentials into it.

- ID : ssh-prod
- Description : Credentials to login into Production machine
- Username: root
- private-key: Check Enter directly, click the Add button and copy the private key from Production machine, available at /root/.ssh/id_rsa
- Passphrase: Leave it blank because we want this process to be automatic without any human intervention. If you desire more robust credential security mechanism, please use dedicated secret management systems like Hashicorp Vault.

Once done, click the OK button.

Add another credential to save SSH hostname, so it’s not hardcoded in the Jenkinsfile, then select Secret text as Kind, then add the following credentials into it.

- Secret: prod-XqiHnDZ0
- ID : prod-server

Next, go back to the GitLab tab and add inspec stage in the Jenkinsfile. Now our Jenkinsfile will look like the following.

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
        stage("Inspec"){
            agent {
                docker {
                    image 'hysnsec/inspec'
                    args '-u root'
                }
            }
            steps {
                sshagent(['ssh-prod']) {
                    sh "inspec exec https://github.com/dev-sec/linux-baseline -t ssh://root@prod-XqiHnDZ0 --chef-license accept --reporter json:inspec-output.json"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'inspec-output.json', fingerprint: true
                }
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
------------------------------------------------

We do not want to fail the builds/jobs/scan in DevSecOps Maturity Levels 1 and 2, as security tools spit a significant amount of false positives.

You can use the catchError function to “not fail the build” even though the tool found security issues.

> Reference: https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps.

```
        stage("Inspec"){
            agent {
                docker {
                    image 'hysnsec/inspec'
                    args '-u root'
                }
            }
            steps {
                sshagent(['ssh-prod']) {
                    catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {     // Allow the sast stage to fail
                        sh "inspec exec https://github.com/dev-sec/linux-baseline -t ssh://root@prod-XqiHnDZ0 --chef-license accept --reporter json:inspec-output.json"
                    }
                }
            }
            ...
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
        stage("Inspec"){
            agent {
                docker {
                    image 'hysnsec/inspec'
                    args '-u root'
                }
            }
            steps {
                sshagent(['ssh-prod']) {
                    sh "inspec exec https://github.com/dev-sec/linux-baseline -t ssh://root@prod-XqiHnDZ0 --chef-license accept --reporter json:inspec-output.json"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'inspec-output.json', fingerprint: true
                }
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

You will notice that the inspec stage failed. However, it didn’t block other jobs from continuing further.

As discussed, any change to the repo kick starts the pipeline.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build history to see the output.