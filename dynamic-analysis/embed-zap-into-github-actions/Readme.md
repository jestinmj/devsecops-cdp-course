Learn how to embed ZAP into GitHub Actions
================================================================

Use ZAP tool to perform DAST in GitHub Actions
----------------------------------------------------------------


In this scenario, you will learn how to embed DAST in GitHub Actions.

You will learn to use ZAP Baseline Scan in CI/CD pipeline using all the best practices mentioned in the Practical DevSecOps Gospel.

A simple CI/CD pipeline
----------

You’ve learned about CI/CD systems using GitLab and Jenkins. Both are good systems, but they also have different features, and use cases. We will look into another CI/CD system named GitHub Actions that debuted on 13 November 2019. GitHub Actions is a CI/CD system that is built-in to GitHub with free and paid offerings.

Let’s get started!

1. Create a new repository
2. Create a Personal Access Token (PAT)
3. Initial git setup
4. Download the repository (django.nv)
5. Add a workflow file to the repository
```
mkdir -p .github/workflows
cat >.github/workflows/main.yaml<<EOF
name: Django                                  # workflow name

on:
  push:                                       
    branches:                                 # similar to "only" in GitLab
      - main

jobs:
  build:
    runs-on: ubuntu-latest                    # similar to "image" in GitLab
    steps:
      - uses: actions/checkout@v2

      - name: Setup python
        uses: actions/setup-python@v2
        with:
          python-version: '3.6'

      - run: |
          pip3 install --upgrade virtualenv
          virtualenv env
          source env/bin/activate
          pip install -r requirements.txt
          python manage.py check

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v2

      - name: Setup python
        uses: actions/setup-python@v2
        with:
          python-version: '3.6'

      - run: |
          pip3 install --upgrade virtualenv
          virtualenv env
          source env/bin/activate
          pip install -r requirements.txt
          python manage.py test taskManager

  integration:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - run: echo "This is an integration step"
      - run: exit 1
        continue-on-error: true

  prod:
    runs-on: ubuntu-latest
    needs: integration
    steps:
      - run: echo "This is a deploy step."
EOF
```
6. Push the changes to the repository
7. Verify the pipeline runs
Any change to the repo, will kick start the pipeline.

We can see the result of the pipeline by visiting our django.nv repository, clicking the Actions tab, and selecting the appropriate workflow name to see the output.

You will notice that the integration has exit 1 and hence failed the job, but other jobs are still running. Why?

> You can find more details at https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions#jobs.
> 
> You can check this lab on previous lab github action

Embed ZAP in GitHub Actions
--------------

As discussed in the Dynamic Analysis using ZAP exercises, we can integrate ZAP in our CI/CD pipeline. We did ensure that the ZAP command runs fine in DevSecOps-Box, now we need to embed zap into CI/CD pipeline. In GitHub Actions, there are two ways to integrate ZAP. ZAP can be integrated in GitHub actions using docker run, or using the ZAP scan actions available from the GitHub Marketplace. GitHub Marketplace offers two actions to integrate ZAP, namely the Baseline Scan and the Full Scan actions.

We will explore both the different ways of embedding ZAP in GitHub Actions, that is through a ZAP docker image, and through a ZAP action available from the GitHub marketplace.

Add secret
----------

We will set up the necessary secrets, go back to django.nv repository and click the Settings tab.

Click the Secrets option, then select New repository secret and add the following credentials into it.

> Name: PROD_URL
>
> Value: https://prod-XqiHnDZ0.lab.practical-devsecops.training

Once done, click the Add secret button.

Embed ZAP using the docker run command
----------

Go back to the DevSecOps Box machine, and replace the integration job under .github/workflows/main.yaml with the following content:

```
  zap_baseline:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - run: |
           docker pull owasp/zap2docker-stable
           docker run --user root --rm -v $(pwd):/zap/wrk:rw -w /zap owasp/zap2docker-stable zap-baseline.py -t ${{ secrets.PROD_URL }} -J zap-output.json

      - uses: actions/upload-artifact@v2
        with:
          name: ZAP Scan                    
          path: zap-output.json
        if: always()        # what is this for?
```

> To understand if: always() Please refer to conditionals.

Commit, and push the changes to GitHub.

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our django.nv repository, clicking the Actions tab, and selecting the appropriate workflow name to see the output.

Embed ZAP using an action from GitHub Marketplace
----------

Please visit the following link to see the details of ZAP Baseline Scan action [here](https://github.com/marketplace/actions/owasp-zap-baseline-scan)

You can replace the content of previous workflow file with the below content to understand the difference between embedding ZAP through docker run directly and embedding ZAP through GitHub action from the GitHub Marketplace.

> action is similar to a plugin or a template that is offered by the provider themselves.

```
  zap_baseline:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Checkout
        uses: actions/checkout@v2
        with:
          ref: master

      - name: ZAP Scan
        uses: zaproxy/action-baseline@v0.4.0
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          docker_name: 'owasp/zap2docker-stable'
          target: ${{ secrets.PROD_URL }}
```

After replacing the workflow content, commit, and push the changes to GitHub.

Any change to the repo will kick start the pipeline.

Once the pipeline is complete, you can click the Issues tab in your repository, and you will notice that there is 1 issue open. The open issue is a result of embedding ZAP through the action zaproxy/action-baseline@v0.4.0, and the issue is created automatically by github-actions bot.

