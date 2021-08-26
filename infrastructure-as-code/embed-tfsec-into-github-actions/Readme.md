Learn how to embed tfsec into GitHub Actions
================================================================

Use tfsec tool to find security issues for IaC in GitHub Actions
----------------------------------------------------------------

In this scenario, you will learn how to embed tfsec in GitHub Actions.

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

Embed tfsec in GitHub Actions
--------------

As discussed in the Secure IaC using tfsec exercise, we can embed tfsec in our CI/CD pipeline. We will
embedding tfsec in GitHub Actions through a tfsec action available from the GitHub marketplace, please visit the following link to see the details of tfsec action [here](https://github.com/marketplace/actions/terraform-security-scan).

Go back to the DevSecOps Box machine, and replace the content of the build job in .github/workflows/main.yaml file with the below content.

```
  tfsec:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Terraform security scan
        uses: triat/terraform-security-scan@v2.2.1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```


> action is similar to a plugin or a template that is offered by the provider themselves.

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our terraform repository, clicking the Actions tab, and selecting the appropriate workflow name to see the output.