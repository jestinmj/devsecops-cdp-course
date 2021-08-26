Learn how to embed Ansible in the Jenkins CI/CD pipeline
================================

Use Ansible tool to achieve compliance automation in Jenkins CI/CD pipeline

In this scenario, you will learn how to embed Ansible in the Jenkins CI/CD pipeline.

Create a new job
-----------

> The Jenkins system is already configured with GitLab. If you wish to know how to configure Jenkins with GitLab, you can check out this [link](https://gitlab.practical-devsecops.training/pdso/jenkins/-/blob/master/tutorials/configure-jenkins-with-gitlab.md).

We will create a new job in Jenkins by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/newJob.

You can use the following details to log into Jenkins.
> Username: root
>
> Password: pdso-training

Provide a name for your new item, e.g., django.nv, select the Pipeline option, and click on the OK button.

In the next screen, click on the Build Triggers tab, check the Build when a change is pushed to GitLab..... checkbox.

At the bottom right-hand side, just below the Comment (regex) for triggering a build form field, you will find the Advanced… button. Please click on it.

Then, click on the Generate button under Secret token to generate a token. We will use this token for GitLab’s Webhook Settings. This webhook setting will allow GitLab to let Jenkins know whenever a change is made to the repository.

Please visit the following GitLab URL to set up the Jenkins webhook.

> URL : https://gitlab-ce-xqihndz0.lab.practical-devsecops.training/root/django-nv/hooks


Fill the form using the following details.

> URL           : https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/project/django.nv
> 
> Secret Tokens : Paste the secret token we just generated above.

Click on the Add webhook button, and go back to the Jenkins tab to continue the setup process.

Click on the Pipeline tab, and select Pipeline script from SCM from Definition options. Once you do that, few more options would be made available to you.

Select Git as SCM, enter our django.nv repository http url. 

Repository URL : http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv.git

Let’s add the credentials by clicking on the Add button (the one with a key symbol). Select the Jenkins option and fill the pop-up form with the following details.

> username      : root
>
> password      : pdso-training
>
> id            : gitlab-auth
>
> description   : leave it blank as its optional

Click on the Add button, and select our new credentials from the Credentials Dropdown.

The error we experienced before should be gone by now.

Finally, click the Save button.

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
We do have four stages in this pipeline, build, test, integration and prod. Assuming you do not understand python or any programming language, we can safely consider the DevOps team is building and testing the code.

Let’s login into Gitlab using the following details.

Add a new file to the repository by clicking on the +(plus) button and give it a name as Jenkinsfile, then add the above script into the file.

Save changes to the file using the Commit changes button.

Verify the pipeline run
----------

Since we want to use Jenkins to execute the CI/CD jobs, we need to remove .gitlab-ci.yml from the git repository. Doing so will prevent Gitlab from running the CI jobs on both the Gitlab Runner and the Jenkins systems.

Embed Ansible in Jenkins
-----------------

We need to add credentials into Jenkins, namely, SSH Private Key and SSH hostname of the machine we are securing, i.e., production machine. Since we don’t want the credentials to be hardcoded in the Jenkinsfile. Let’s add the creds to the Jenkins credential store by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/credentials/store/system/domain/_/.

Click on the Add Credentials link on the left sidebar, and select SSH Username with private key as Kind, then add the following credentials into it.

> id            : ssh-prod
>
> description   : Credentials to login into Production machine
>
> username      : root
>
> private key   : check Enter directly, click the Add button and copy the private key from Production machine, available at /root/.ssh/id_rsa
>
> passphrase    : leave it blank because we want this process to be automatic without any human intervention. If you desire more robust credential security mechanism, please use dedicated secret management systems like Hashicorp Vault.

Once done, click the OK button.

Add another credential to save SSH hostname, so it’s not hardcoded in the Jenkinsfile, then select Secret text as Kind, then add the following credentials into it.

> Secret  : prod-XqiHnDZ0
>
> id      : prod-server

Next, go back to the Gitlab tab and append the following code in the Jenkinsfile after the prod stage.

```
        stage("ansible-hardening"){
            agent {
                docker {
                    image 'willhallonline/ansible:2.9-ubuntu-18.04'
                    args '-u root'
                }
            }
            steps {
                sshagent(['ssh-prod']) {
                    withCredentials([string(credentialsId: 'prod-server', variable: 'DEPLOYMENT_SERVER')]) {
                        sh """
                        echo "[prod]\n$DEPLOYMENT_SERVER" >> inventory.ini
                        ansible-galaxy install dev-sec.os-hardening
                        ansible-playbook -i inventory.ini ansible-hardening.yml
                        """
                    }
                }
            }
        }
```

Save changes to the file using the Commit changes button.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build history to see the output.

Oh, it failed? Why? We also got the following helpful message in the CI output.

output

```
+ ansible-playbook -i inventory.ini ansible-hardening.yml
ERROR! the playbook: ansible-hardening.yml could not be found
script returned exit code 1
```

That makes sense. We didn’t upload the ansible-hardening.yml to the git repository.

Let’s copy the hardening script.

```
---
- name: Playbook to harden the Ubuntu OS.
  hosts: prod
  remote_user: root
  become: yes

  roles:
    - dev-sec.os-hardening
```

Visit the add new file URL https://gitlab-ce-XqiHnDZ0lab.practical-devsecops.training/root/django-nv/-/new/master/.

Paste the above ansible script into the space provided.

Ensure you name the file as `ansible-hardening.yml`

Save changes to the repo using the Commit changes button.

We can see the results by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

There you have it. We ran ansible hardening locally first and then embedded it into a CI/CD pipeline.

