Learn how to embed Terrascan into GitHub Actions
================================

Use Terrascan tool to perform SAST for IaC in GitHub Actions
--------------

In this scenario, you will learn how to embed Terrascan in GitHub Actions.

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

Embed Terrascan in GitHub Actions
--------------

As discussed in the Secure IaC using Terrascan exercise, we can embed Terrascan in our CI/CD pipeline. We will
embedding Terrascan in GitHub Actions through a Terrascan action available from the GitHub marketplace, please visit the following link to see the details of Terrascan action here.

Go back to the DevSecOps Box machine, and replace the content of the build job in .github/workflows/main.yaml file with the below content.

```
  terrascan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Run Terrascan
        id: terrascan
        uses: accurics/terrascan-action@v1
        with:
          iac_type: 'terraform'
          iac_version: 'v14'
          policy_type: 'aws'
          only_warn: true
          iac_dir: 'aws'
```

> action is similar to a plugin or a template that is offered by the provider themselves.

Commit, and push the changes to GitHub.

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our terraform repository, clicking the Actions tab, and selecting the appropriate workflow name to see the output.
