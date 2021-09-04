How to Embed Safety into GitHub Actions
================================================

Use Safety tool to perform OAST in GitHub Actions
----------------------------------------------------------------

In this scenario, you will learn how to embed an SCA tool in GitHub Actions.

You will learn to use Safety in GitHub Actions and allow the job to fail even when the tool found several issues.

A simple CI/CD pipeline
----------

You’ve learned about CI/CD systems using GitLab and Jenkins. Both are good systems, but they also have different features, and use cases. We will look into another CI/CD system named GitHub Actions that debuted on 13 November 2019. GitHub Actions is a CI/CD system that is built-in to GitHub with free and paid offerings.

Let’s get started!

1. Create a new repository
2. Create a Personal Access Token (PAT)
3. Initial git setup
4. Download the repository
5. Add a workflow file to the repository
6. Push the changes to the repository
7. Verify the pipeline runs

Embed Safety in GitHub Actions
--------------

As discussed in the SCA using the Safety exercise, we can embed the Safety tool in our CI/CD pipeline. However, do remember you need to run the command manually before you embed OAST in the pipeline.

Do you wonder which stage this job should go into?

Since, most of the code (sometimes up to 95%) in any software project is open-source/third-party components, it makes sense to perform SCA scans before static analysis.

Go back to the DevSecOps Box machine, and copy the below content to the .github/workflows/main.yaml file under test job.

```
  oast:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v2

      - run: docker run --rm -v $(pwd):/src hysnsec/safety check -r requirements.txt --json | tee oast-results.json

      - uses: actions/upload-artifact@v2
        with:
          name: Safety
          path: oast-results.json
        if: always()                        # what is this for?
```

Commit, and push the changes to GitHub.

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our django.nv repository, clicking the Actions tab, and selecting the appropriate workflow name to see the output

Allow the job failure
----------

You don’t want to fail the builds in DevSecOps Maturity Levels 1 and 2. If a security tool fails a build upon security findings, you would want to allow it to fail and not block the pipeline as there would be false positives in the results.

You can use the continue-on-error syntax to not fail the build even though the tool found security issues.

```
  oast:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v2

      - run: docker run --rm -v $(pwd):/src hysnsec/safety check -r requirements.txt --json | tee oast-results.json
        continue-on-error: true             # allow the build to fail, similar to "allow_failure: true" in GitLab

      - uses: actions/upload-artifact@v2
        with:
          name: Safety
          path: oast-results.json
        if: always()                        # what is this for?
```

The final pipeline would look like the following:


```
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

  oast:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v2

      - run: docker run --rm -v $(pwd):/src hysnsec/safety check -r requirements.txt --json | tee oast-results.json
        continue-on-error: true             # allow the build to fail, similar to "allow_failure: true" in GitLab

      - uses: actions/upload-artifact@v2
        with:
          name: Safety
          path: oast-results.json
        if: always()                        # what is this for?

  integration:
    runs-on: ubuntu-latest
    needs: oast-frontend
    steps:
      - run: echo "This is an integration step"
      - run: exit 1
        continue-on-error: true

  prod:
    runs-on: ubuntu-latest
    needs: integration
    steps:
      - run: echo "This is a deploy step."
```

Go ahead and add the above content to the .github/workflows/main.yaml file to run the pipeline.

You will notice that the oast job has failed but didn’t block the other jobs from running.

As discussed, any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our django.nv repository, clicking the Actions tab, and selecting the appropriate workflow name to see the output.

