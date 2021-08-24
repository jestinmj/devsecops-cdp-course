Learn how to embed ZAP into CircleCI
================================

Use ZAP tool to perform DAST in CircleCI
------------------------------------------------

In this scenario, you will learn how to embed DAST in CircleCI.

You will learn to use ZAP Baseline Scan in CI/CD pipeline using all the best practices mentioned in the Practical DevSecOps Gospel.

Initial Setup
----------

You’ve learned about CI/CD systems such as GitLab, Jenkins, GitHub Actions and so on. Remember every CI/CD system has its own advantages, and limitations, we just need to find what is suitable for our needs.

Now, we will look into another CI/CD system called CircleCI, this system doesn’t have a built-in Git repository like GitLab or GitHub. But it can be integrated with GitHub or Bitbucket as the repository, so let’s get started!

1. Create a new repository (django.nv)
2. Create a Personal Access Token (PAT)
3. Initial git setup
4. Download the repository (`git clone https://gitlab.practical-devsecops.training/pdso/django.nv.git`)
5. Create an account in CircleCI

> you can check full documentation at previous lab circleci

A simple CI/CD pipeline
----------

You need to create .circleci directory and create a new YAML file named config.yml and add the following CI script.

```
mkdir -p .circleci
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

commit and push new file .circleci to github

Embed ZAP in CircleCI
----------

As discussed in the Dynamic Analysis using ZAP exercises, we can integrate ZAP in our CI/CD pipeline. In the previous exercises, we did ensure that the ZAP command runs fine in DevSecOps-Box, now we need to embed zap into CI/CD pipeline.

Add secret
----------

We will set up the necessary secrets by visiting https://app.circleci.com/pipelines/github/username/django.nv, then click Project Settings on the top right and select Environment Variables to add the following variables in the form of key value pairs.

> Key: PROD_URL
>
> Value: https://prod-XqiHnDZ0.lab.practical-devsecops.training

Go back to the DevSecOps Box machine, and replace the integration job under .circleci/config.yml with the following content:

```
  zap_baseline:
    machine: true
    steps:
      - checkout

      - run: |
          docker pull owasp/zap2docker-stable
          docker run --user root --rm -v $(pwd):/zap/wrk:rw -w /zap owasp/zap2docker-stable zap-baseline.py -t ${PROD_URL} -J zap-output.json

      - store_artifacts:
          path: zap-output.json
          destination: zap-artifact
```

Commit, and push the changes to GitHub.

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our CircleCI account. Click Projects, select django.nv repository and select the appropriate pipeline to see the output.

