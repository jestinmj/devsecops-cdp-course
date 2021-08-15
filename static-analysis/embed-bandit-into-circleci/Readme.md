Learn how to embed Bandit into CircleCI
================================================
****

Use Bandit tool to perform SAST in CircleCI
------------------------------------------------

In this scenario, you will learn how to embed SAST in CircleCI.

You will learn to use Bandit in CircleCI and how to allow job failure when the tool found several issues.

Initial Setup
----------

You’ve learned about CI/CD systems such as GitLab, Jenkins, GitHub Actions and so on. Remember every CI/CD system has its own advantages, and limitations, we just need to find what is suitable for our needs.

Now, we will look into another CI/CD system called CircleCI, this system doesn’t have a built-in Git repository like GitLab or GitHub. But it can be integrated with GitHub or Bitbucket as the repository, so let’s get started!

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

> if you are not comfortable with the syntax, explore the CircleCI syntax at https://circleci.com/docs/2.0/configuration-reference/

Let’s add this file to the repository and commit the changes. 
```
git add .circleci/config.yml
git commit -m "Add CircleCI config"
git push origin main
```

We can see the result of the pipeline by visiting our [CircleCI account](https://app.circleci.com/). Click Projects, select django.nv repository and select the appropriate pipeline to see the output.

Let’s move to the next step.

Embed Bandit in CircleCI
----------

As discussed in the Static Analysis using Bandit exercise, we can embed Bandit in our CI/CD pipeline. However, do remember you need to run the command manually before you embed this SAST tool in the pipeline.

Go back to the DevSecOps Box machine, and copy the below content to the .circleci/config.yml file under test job.

```
  sast:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -v $(pwd):/src hysnsec/bandit -r /src -f json -o /src/bandit-output.json

      - store_artifacts:
          path: bandit-output.json
          destination: bandit-artifact
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
      - sast:
          requires:
            - test
      - integration:
          requires:
            - sast
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

We do not want to fail the builds in DevSecOps Maturity Levels 1 and 2, as security tools spit a significant amount of false positives in their default configuration.

You can use the when: always syntax to not fail the build even though the tool found security issues.

```
  sast:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -v $(pwd):/src hysnsec/bandit -r /src -f json -o /src/bandit-output.json

      - store_artifacts:
          path: bandit-output.json
          destination: bandit-artifact
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

  sast:
    machine: true
    steps:
      - checkout

      - run: docker run --rm -v $(pwd):/src hysnsec/bandit -r /src -f json -o /src/bandit-output.json

      - store_artifacts:
          path: bandit-output.json
          destination: bandit-artifact
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
      - sast:
          requires:
            - oast-frontend
      - integration:
          requires:
            - sast
      - prod:
          type: approval
          requires:
            - integration
```

> Did you see we sneaked oast-frontend at the end?

Go ahead and add the above content to the .circleci/config.yml file to run the pipeline.

You will notice that the sast job has failed but didn’t block the other jobs from running.

As discussed, any change to the repo will kick start the pipeline.