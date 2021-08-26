Learn how to embed TFLint into GitHub Actions
================================

Use TFLint tool to find security issues for IaC in GitHub Actions
--------------

In this scenario, you will learn how to embed TFLint in GitHub Actions.

A simple CI/CD pipeline
----------
1. Create a new repository
2. Create a Personal Access Token (PAT)
3. Initial git setup
4. Download the repository
```
git clone https://gitlab.practical-devsecops.training/pdso/terraform.git
```
5. Add a workflow file to the repository
```
mkdir -p .github/workflows
cat >.github/workflows/main.yaml<<EOF
name: Terraform                               # workflow name

on:
  push:                                       
    branches:                                 # similar to "only" in GitLab
      - main

jobs:
  build:
    runs-on: ubuntu-latest                    # similar to "image" in GitLab
    steps:
      - run: echo "This is a build step"

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - run: echo "This is a test step"

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
      - run: echo "This is a deploy step"
EOF
```
6. Push the changes to the repository
7. Verify the pipeline runs

Embed TFLint in GitHub Actions
--------------

As discussed in the Terraform Linter using TFLint exercise, we can embed TFLint in our CI/CD pipeline. We will
embedding TFLint in GitHub Actions through a TFLint action available from the GitHub marketplace, please visit the following link to see the details of TFLint action [here.](https://github.com/marketplace/actions/setup-tflint)

Go back to the DevSecOps Box machine, and replace the content of the build job in .github/workflows/main.yaml file with the below content.

```
  tflint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - uses: terraform-linters/setup-tflint@v1
        name: Setup TFLint
        with:
          tflint_version: latest

      - name: Run TFLint
        run: tflint -f json aws > tflint-output.json

      - uses: actions/upload-artifact@v2
        with:
          name: TFLint
          path: tflint-output.json
        if: always()                        # what is this for?
```

Commit, and push the changes to GitHub.

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our terraform repository, clicking the Actions tab, and selecting the appropriate workflow name to see the output.

