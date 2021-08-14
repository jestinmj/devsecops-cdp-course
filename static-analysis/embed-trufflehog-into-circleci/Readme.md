Learn how to embed TruffleHog into CircleCI
================================================

Use TruffleHog tool to perform SAST in CircleCI
------------------------------------------

In this scenario, you will learn how to embed SAST in CircleCI.

You will learn to use TruffleHog in CircleCI and how to allow job failure when the tool found several issues.

Initial Setup
----------

You’ve learned about CI/CD systems such as GitLab, Jenkins, GitHub Actions and so on. Remember every CI/CD system has its own advantages, and limitations, we just need to find what is suitable for our needs.

Now, we will look into another CI/CD system called **CircleCI**, this system doesn’t have a built-in Git repository like GitLab or GitHub. But it can be integrated with GitHub or Bitbucket as the repository, so let’s get started!

### 1. Create a new repository

> If you haven’t registered for a GitHub account, please sign up for an account [here](https://github.com/join?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home)

First, we need to create a repository in our GitHub account by visiting https://github.com/new.

Create a repository named *django.nv*, you can also check the box with **Public or Private** options, and please ignore **Initialize this repository** with section for now.

Click the **Create repository** button.

### 2. Create a Personal Access Token (PAT)

Next, we will create and use PAT for git authentication in DevSecOps Box because GitHub will not support account passwords starting August 2021.

Let’s create PAT by visiting https://github.com/settings/tokens, then click Generate new token button and give your token a name e.g. django.

Select repo option to access repositories from the command line and scroll down to generate a new token.

> The token will have a format like ghp_xxxxxxxxx.

Once you have the token, please copy and save it as a file in DevSecOps Box, so we can use it whenever we needed.

### 3. Initial git setup

To work with git repositories via Command Line Interface (CLI), aka terminal/command prompt, we need to set up a user and an email. We can use git config command to configure git user and email.

```
git config --global user.email "your_email@gmail.com"
git config --global user.name "your_username"
```

> You need to use your email and username, which are registered in GitHub.
> 
> **Please don’t use your company’s GitHub credentials or token to practice these exercises.**

### 4. Download the repository
Let’s start by cloning django.nv in DevSecOps Box.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv.git
```

By cloning the above repository, we created a local copy of the remote repository.

Let’s cd into this repository to explore its content. 
```
cd django.nv
```

Since this repository was cloned from Gitlab, the remote URL of this Git repository is going to point to the Gitlab URL. Let’s rename the repository’s Git URL to point to GitHub, enabling us to push our code to GitHub.

```
git remote rename origin old-origin
```

> In the command below, please change “username” with your GitHub username.

```
git remote add origin https://github.com/username/django.nv.git
```

Let’s check the status of our git repository.

```
git status
```

We are in the master branch and we need to create one more branch called main as a default branch.

```
git checkout -b main
```

> Why we need to do this? Because in this exercise we will use the main branch as a control to run the pipeline in every commit. If you don’t do this, you will not be able to see any pipeline in your repository.
> 
> Read more about [Renaming the default branch from master](https://github.com/github/renaming).

Then, let’s push the code to the GitHub repository.

```
git push -u origin main
```

And enter your GitHub credentials when prompted (please use Personal Access Token as a password), then the code will be pushed to the GitHub repository.

### 5. Create an account in CircleCI

> If you’ve already created the CircleCI account, you can ignore this step.

To use CircleCI, we need to create an account by signing up at https://circleci.com/signup, click the Signup with GitHub button and you will be redirected to the page which tells you to allow CircleCI to access your GitHub account, accept it by clicking the Authorize circleci button.

Next, you will see the repository lists which has a button called Set Up Project. Select django.nv repository then click on that button to start using CircleCI as our CI/CD pipeline and you will get a pop-up with Select a config.yml file for django.nv message, please ignore it for now because we will create the CircleCI YML file in our GitHub repository.

A simple CI/CD pipeline
----------

You need to create .circleci directory and create a new YAML file named config.yml and add the following CI script.

```
mkdir -p .circleci
```

```
cat >.circleci/config.yml<<EOF
jobs:
  build:
    docker:
      - image: python:3.6                   # similar to "image" in GitLab
    steps:
      - checkout
      - run: |                              # similar to "script" in GitLab
          pip install -r requirements.txt
          python manage.py check

  test:
    docker:
      - image: python:3.6
    steps:
      - checkout
      - run: |
          pip install -r requirements.txt
          python manage.py test taskManager

  integration:
    docker:
      - image: python:3.6
    steps:
      - checkout
      - run:
          command: |
            echo "This is an integration step"
            exit 1

  prod:
    docker:
      - image: python:3.6
    steps:
      - checkout
      - run: echo "This is a deploy step."

workflows:
  version: 2
  django:
    jobs:
      - build
      - test:
          requires:
            - build 
      - integration:
          requires:
            - test
      - prod:
          type: approval
          requires:
            - integration
EOF
```

> If you are not comfortable with the syntax, explore the CircleCI syntax at https://circleci.com/docs/2.0/configuration-reference/


Let’s add this file to the repository and commit the changes. 

```
git add .circleci/config.yml
git commit -m "Add CircleCI config"
```

Since git is a decentralized source code management system, all changes are made in your local git repository. You have to push these changes to the remote server for the committed changes to reflect on the remote git repository.

Let’s push the changes to the remote git repository using the git push command.

```
git push origin main
```

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our [CircleCI account](https://app.circleci.com/). Click Projects, select django.nv repository and select the appropriate pipeline to see the output.

Embed TruffleHog in CircleCI
----------

As discussed in the Static Analysis using TruffleHog exercise, we can embed TruffleHog in our CI/CD pipeline. However, do remember you need to run the command manually before you embed this SAST tool in the pipeline.

Go back to the DevSecOps Box machine, and copy the below content to the .circleci/config.yml file under test job.

```
  secret_scanning:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -v $(pwd):/src hysnsec/trufflehog file:///src --json > trufflehog-output.json

      - store_artifacts:
          path: trufflehog-output.json
          destination: trufflehog-artifact
```

Please remember to add the above job name to the workflows section as shown below:

```
workflows:
  version: 2
  django:
    jobs:
      - build
      - test:
          requires:
            - build
      - secret_scanning:
          requires:
            - test
      - integration:
          requires:
            - secret_scanning
      - prod:
          type: approval
          requires:
            - integration
```
Commit, and push the changes to GitHub.
Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our [CircleCI account](https://app.circleci.com/). Click Projects, select django.nv repository and select the appropriate pipeline to see the output.

Allow the job failure
----------

We do not want to fail the builds/jobs/scan in DevSecOps Maturity Levels 1 and 2, as security tools spit a significant amount of false positives.

You can use the when: always syntax to not fail the build even though the tool found security issues.

```
  secret_scanning:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -v $(pwd):/src hysnsec/trufflehog file:///src --json > trufflehog-output.json

      - store_artifacts:
          path: trufflehog-output.json
          destination: trufflehog-artifact
          when: always              # Even if the job fails, continue to the next stages
```
The final pipeline would look like the following:

```
jobs:
  build:
    docker:
      - image: python:3.6                   # similar to "image" in GitLab
    steps:
      - checkout
      - run: |                              # similar to "script" in GitLab
          pip install -r requirements.txt
          python manage.py check

  test:
    docker:
      - image: python:3.6
    steps:
      - checkout
      - run: |
          pip install -r requirements.txt
          python manage.py test taskManager

  secret_scanning:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -v $(pwd):/src hysnsec/trufflehog file:///src --json > trufflehog-output.json

      - store_artifacts:
          path: trufflehog-output.json
          destination: trufflehog-artifact
          when: always              # Even if the job fails, continue to the next stages

  integration:
    docker:
      - image: python:3.6
    steps:
      - checkout
      - run:
          command: |
            echo "This is an integration step"
            exit 1
          when: always                    # Even if the job fails, continue to the next stages

  prod:
    docker:
      - image: python:3.6
    steps:
      - checkout
      - run: echo "This is a deploy step."

workflows:
  version: 2
  django:
    jobs:
      - build
      - test:
          requires:
            - build
      - secret_scanning:
          requires:
            - test
      - integration:
          requires:
            - secret_scanning
      - prod:
          type: approval
          requires:
            - integration
```

Go ahead and add the above content to the .circleci/config.yml file to run the pipeline.

You will notice that the secret_scanning job has failed but didn’t block the other jobs from running.

As discussed, any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our [CircleCI account](https://app.circleci.com/). Click Projects, select django.nv repository and select the appropriate pipeline to see the output.