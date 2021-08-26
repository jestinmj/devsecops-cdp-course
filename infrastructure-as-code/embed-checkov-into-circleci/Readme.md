Learn how to embed Checkov into CircleCI
================================================

Use Checkov tool to perform SAST for IaC in CircleCI
--------------------------------

In this scenario, you will learn how to embed Checkov in CircleCI.

Initial Setup
----------
1. Create a new repository
2. Create a Personal Access Token (PAT)
3. Initial git setup
4. Download the repository
5. Create an account in CircleCI

A simple CI/CD pipeline
----------

You need to create .circleci directory and create a new YAML file named config.yml and add the following CI script.

```
mkdir -p .circleci

cat >.circleci/config.yml<<EOF
jobs:
  build:
    machine: true
    steps:
      - checkout
      - run: echo "This is a build step"

  test:
    machine: true
    steps:
      - checkout
      - run: echo "This is a test step"

  integration:
    machine: true
    steps:
      - checkout
      - run:
          command: |
            echo "This is an integration step"
            exit 1

  prod:
    machine: true
    steps:
      - checkout
      - run: echo "This is a deploy step"

workflows:
  version: 2
  terraform:
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

Let’s add this file to the repository, commit the changes push to repository. 

Embed Checkov in CircleCI
----------

As discussed in the Secure IaC using Checkov exercise, we can embed Checkov in our GitHub Actions. However, you need to test the command manually before you embed this SAST tool in the pipeline.

Go back to the DevSecOps Box machine, and replace the content of the build job in .circleci/config.yml file.

```
  checkov:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -w /src -v $(pwd):/src bridgecrew/checkov -d aws -o json | tee checkov-output.json

      - store_artifacts:
          path: checkov-output.json
          destination: checkov-artifact
```

Please remember to replace the above job name to the checkov in workflows section as shown below:

```
workflows:
  version: 2
  terraform:
    jobs:
      - checkov
      - test:
          requires:
            - checkov
      - integration:
          requires:
            - test
      - prod:
          type: approval
          requires:
            - integration
```

Commit, and push the changes to GitHub.

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our CircleCI account. Click Projects, select terraform repository and select the appropriate pipeline to see the output

Allow the job failure
----------

We do not want to fail the builds/jobs/scan in DevSecOps Maturity Levels 1 and 2, as security tools spit a significant amount of false positives.

You can use the when: always syntax to not fail the build even though the tool found security issues.

```
  checkov:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -w /src -v $(pwd):/src bridgecrew/checkov -d aws -o json | tee checkov-output.json

      - store_artifacts:
          path: checkov-output.json
          destination: checkov-artifact
          when: always              # Even if the job fails, continue to the next stages
```
The final pipeline would look like the following:

```
jobs:
  build:
    machine: true
    steps:
      - checkout
      - run: echo "This is a build step"

  test:
    machine: true
    steps:
      - checkout
      - run: echo "This is a test step"

  checkov:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -w /src -v $(pwd):/src bridgecrew/checkov -d aws -o json | tee checkov-output.json

      - store_artifacts:
          path: checkov-output.json
          destination: checkov-artifact
          when: always              # Even if the job fails, continue to the next stages

  integration:
    machine: true
    steps:
      - checkout
      - run:
          command: |
            echo "This is an integration step"
            exit 1

  prod:
    machine: true
    steps:
      - checkout
      - run: echo "This is a deploy step"

workflows:
  version: 2
  terraform:
    jobs:
      - checkov
      - test:
          requires:
            - checkov
      - integration:
          requires:
            - test
      - prod:
          type: approval
          requires:
            - integration
```

Go ahead and add the above content to the .circleci/config.yml file to run the pipeline.

You will notice that the checkov job failed however it didn’t block others from continuing further.

As discussed, any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our CircleCI account. Click Projects, select terraform repository and select the appropriate pipeline to see the output.
