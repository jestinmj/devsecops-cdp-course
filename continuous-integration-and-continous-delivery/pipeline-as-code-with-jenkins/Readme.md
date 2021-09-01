Pipeline as Code (PaC) with Jenkins
===================

Use Jenkins CI/CD system to learn Pipeline concepts
------------------------------------------------

In this scenario, you will learn how to configure Jenkins with GitLab as CI/CD pipeline and create a simple Jenkinsfile for your projects.

Create a new job
-----------

> The Jenkins system is already configured with Gitlab. If you wish to know how to configure Jenkins with Gitlab, you can check out this link.

We will create a new job in Jenkins by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/newJob.

You can use the following details to log into Jenkins.

- Username : root
- Password : pdso-training

Provide a name for your new item, e.g., django.nv, select the Pipeline option, and click on the OK button.

In the next screen, click on the Build Triggers tab, check the Build when a change is pushed to GitLab..... checkbox.

At the bottom right-hand side, just below the Comment (regex) for triggering a build form field, you will find the Advanced… button. Please click on it.

Then, click on the Generate button under Secret token to generate a token. We will use this token for Gitlab’s Webhook Settings. This webhook setting will allow Gitlab to let Jenkins know whenever a change is made to the repository.

Please visit the following GitLab URL to set up the Jenkins webhook.

URL: https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/hooks

Fill the form using the following details.

- URL: 	https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/project/django.nv
- Secret Token: 	Paste the secret token we just generated above.

Click on the Add webhook button, and go back to the Jenkins tab to continue the setup process.

Click on the Pipeline tab, and select Pipeline script from SCM from Definition options. Once you do that, few more options would be made available to you. Select Git as SCM, enter our django.nv repository http url i.e, http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv.git.

Since we haven’t added the GitLab credentials to the Jenkins system, you will get an error.

output
```
Failed to connect to repository : Command "git ls-remote -h -- http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv HEAD" returned status code 128:
stdout:
stderr: remote: HTTP Basic: Access denied
fatal: Authentication failed for 'http://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv.git/'
```

Let’s add the credentials by clicking on the Add button (the one with a key symbol). Select the Jenkins option and fill the pop-up form with the following details.

- Username: 	root
- Password: 	pdso-training
- ID: 	gitlab-auth
- Description: 	Leave it blank as it’s optional.

Click on the Add button, and select our new credentials from the Credentials Dropdown.

The error we experienced before should be gone by now.

Pipeline as Code with Jenkinsfile
-----------

> Pipeline as Code describes a set of features that allow Jenkins users to define pipelined job processes with code, stored and versioned in a source repository.
> 
> Source: https://www.jenkins.io/doc/book/pipeline-as-code

Unlike Gitlab, Jenkins provides us the ability to create a function to define a set of instructions/commands in each stage.

We can then call this function in any job of our choice, instead of writing long lines riddled with &&.

There are two ways to write Pipeline as Code in Jenkins:

1. Declatarive Pipeline
2. Scripted Pipeline

To know about these differences, please visit this [link](https://www.jenkins.io/doc/book/pipeline/#declarative-versus-scripted-pipeline-syntax).

For your reference, a simple Declarative pipeline is shown below.

```
pipeline {
    agent any
    stages {
        stage('build'){         // similar to __stage__ in .gitlab-ci.yml
            steps{              // similar to __script__ in .gitlab-ci.yml
                echo "hello"
            }
        }
    }
}
```
In Jenkinsfile, we don’t need to define stages at the beginning of the file, like we used to do in Gitlab.

```
 - build   # this is build stage
 - test    # this is test stage
 - integration # this is an integration stage
 - prod       # this is prod/production stage
```

We define a stage inside the stages as shown below.

```
...
    ...
    stages {
        stage('build'){
            ...
        }
...
```

Getting started with Jenkinsfile
-----------

We just learned some basic syntax of the Declarative pipeline, and let’s learn more about it now.

Since we want to use Jenkins to execute the CI/CD jobs, we will remove .gitlab-ci.yml file from the git repository. Doing so will prevent Gitlab from running the CI jobs on both the Gitlab Runner, and the Jenkins systems.

Visit https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml and click on the Delete button.

Add a new file to the repository by clicking on the +(plus) button and give it the name Jenkinsfile.

Please copy the following content into it.

```
pipeline {
    agent any

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
}
```

Save changes to the file using the Commit changes button.

The above pipeline script is an elementary example similar to what we did in Gitlab.

We used echo commands under steps as well. We can even call other commands using the sh instruction.

Verify the pipeline run
-----------

We know that the pipeline starts executing the jobs as soon as any change is made to the repository.

We can see the results of this pipeline by visiting https://jenkins-XqiHnDZ0.lab.practical-devsecops.training/job/django.nv.

Click on the appropriate build job/console output to see the job output. At the end of the pipeline run, you will notice that the integration stage failed but continued to the prod stage.

Exercise
-----------

In this exercise, you will edit the Jenkinsfile file to create a simple CI/CD pipeline.

1. Create four stages, namely build, test, integration, prod and each of these stages doing a simple echo command with their stage names
2. In the integration stage, create a file named output.txt and save it as an artifact
3. If you are not comfortable with the syntax, explore the Jenkins Pipeline syntax at https://www.jenkins.io/doc/pipeline/tour/getting-started

> Please do not forget to share the answer (a screenshot and the Jenkinsfile) with our staff via Slack Direct Message (DM).


