How to Embed RetireJS into CircleCI
================================

Use RetireJS tool to perform OAST in CircleCI
----------------------------------------------------------------

In this scenario, you will learn how to embed an SCA tool in CircleCI.

You will learn to use RetireJS in CircleCI and allow the job to fail even when the tool found several issues.

Initial Setup
----------

You’ve learned about CI/CD systems such as GitLab, Jenkins, GitHub Actions and so on. Remember every CI/CD system has its own advantages, and limitations, we just need to find what is suitable for our needs.

Now, we will look into another CI/CD system called CircleCI, this system doesn’t have a built-in Git repository like GitLab or GitHub. But it can be integrated with GitHub or Bitbucket as the repository, so let’s get started!


1. Create a new repository
2. Create a Personal Access Token (PAT)
3. Initial git setup
4. Download the repository
5. Create an account in CircleCI

Next, you will see the repository lists which has a button called Set Up Project. Select django.nv repository then click on that button to start using CircleCI as our CI/CD pipeline and you will get a pop-up with Select a config.yml file for django.nv message, please ignore it for now because we will create the CircleCI YML file in our GitHub repository.

A simple CI/CD pipeline
----------

You need to create .circleci directory and create a new YAML file named config.yml and add the following CI script.

```
mkdir -p .circleci
----------
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

Embed RetireJS in CircleCI
----------

As discussed in the SCA using the RetireJS exercise, we can embed the RetireJS tool in our CI/CD pipeline. However, do remember you need to run the command manually before you embed OAST in the pipeline.

Since, most of the code (sometimes up to 95%) in any software project is open-source/third-party components, it makes sense to perform SCA scans before static analysis.

Go back to the DevSecOps Box machine, and copy the below content to the .circleci/config.yml file under test job.

```
  oast-frontend:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -v $(pwd):/src -w /src hysnsec/retire --outputformat json --outputpath retirejs-output.json --severity high

      - store_artifacts:
          path: retirejs-output.json
          destination: retirejs-artifact
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
      - oast-frontend:
          requires:
            - test
      - integration:
          requires:
            - oast-frontend
      - prod:
          type: approval
          requires:
            - integration
```

Commit, and push the changes to GitHub.

Any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our CircleCI account. Click Projects, select django.nv repository and select the appropriate pipeline to see the output.

Allow the job failure
----------

You don’t want to fail the builds in DevSecOps Maturity Levels 1 and 2. If a security tool fails a build upon security findings, you would want to allow it to fail and not block the pipeline as there would be false positives in the results.

You can use the when: always syntax to not fail the build even though the tool found security issues.

```
  oast-frontend:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -v $(pwd):/src -w /src hysnsec/retire --outputformat json --outputpath retirejs-output.json --severity high

      - store_artifacts:
          path: retirejs-output.json
          destination: retirejs-artifact
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

  oast-frontend:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -v $(pwd):/src -w /src hysnsec/retire --outputformat json --outputpath retirejs-output.json --severity high

      - store_artifacts:
          path: retirejs-output.json
          destination: retirejs-artifact
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
      - oast-frontend:
          requires:
            - test
      - integration:
          requires:
            - oast-frontend
      - prod:
          type: approval
          requires:
            - integration
```

Go ahead and add the above content to the .circleci/config.yml file to run the pipeline.

You will notice that the oast-frontend job has failed but didn’t block the other jobs from running.

As discussed, any change to the repo will kick start the pipeline.

We can see the result of the pipeline by visiting our CircleCI account. Click Projects, select django.nv repository and select the appropriate pipeline to see the output.