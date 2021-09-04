A Full Enterprise Grade DevSecOps Pipelines
===============================

A full enterprise-grade DevSecOps Pipeline
------------------------------------------------

In this scenario, you will learn to tie SCA, SAST, DAST, IaC, CaC scans and Vulnerability Management aspects of the DevSecOps Together.

Of course, you will be embedding the above practices in the CI/CD pipeline to create a full fledged DevSecOps Pipeline.

Explore SCA, SAST, DAST, IaC, CaC and VM exercises
----------------------------------------------------------------
Considering your DevOps team created a simple CI pipeline with the following contents.

```
image: docker:latest

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

build:
  stage: build
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py check

test:
  stage: test
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py test taskManager

integration:
  stage: integration
  script:
    - echo "This is an integration step"
    - exit 1
  allow_failure: true # Even if the job fails, continue to the next stages

prod:
  stage: prod
  script:
    - echo "This is a deploy step."
  when: manual # Continuous Delivery
```

We will explore each chapter in the lab and gather their respective Gitlab CI/CD scripts and embed them in their respective pipeline stages.

Software Component Analysis (SCA)
--------------------------------

```
# Software Component Analysis
sca-frontend:
  stage: build
  image: node:alpine3.10
  script:
    - npm install
    - npm install -g retire # Install retirejs npm package.
    - retire --outputformat json --outputpath retirejs-report.json --severity high --exitwith 0
  artifacts:
    paths: [retirejs-report.json]
    when: always # What is this for?
    expire_in: one week

sca-backend:
  stage: build
  script:
    - docker pull hysnsec/safety
    - docker run --rm -v $(pwd):/src hysnsec/safety check -r requirements.txt --json > oast-results.json
  artifacts:
    paths: [oast-results.json]
    when: always # What does this do?
  allow_failure: true #<--- allow the build to fail but don't mark it as such
```

Static Application Security Testing (SAST)
--------------------------------

```

# Git Secrets Scanning
secrets-scanning:
  stage: build
  script:
    - apk add git
    - git checkout master
    - docker run --rm -v $(pwd):/src hysnsec/trufflehog file:///src --json | tee trufflehog-output.json
  artifacts:
    paths: [trufflehog-output.json]
    when: always # What is this for?
    expire_in: one week
  allow_failure: true   #<--- allow the build to fail but don't mark it as such

# Static Application Security Testing
sast:
  stage: build
  script:
    - docker pull hysnsec/bandit  # Download bandit docker container
    # Run docker container, please refer docker security course, if this doesn't make sense to you.
    - docker run --user $(id -u):$(id -g) --rm -v $(pwd):/src hysnsec/bandit -r /src -f json -o /src/bandit-output.json
  artifacts:
    paths: [bandit-output.json]
    when: always
  allow_failure: true   #<--- allow the build to fail but don't mark it as such
```

Dynamic Application Security Testing (DAST)
--------------------------------

```

# Dynamic Application Security Testing
nikto:
  stage: integration
  script:
    - docker pull hysnsec/nikto
    - docker run --rm -v $(pwd):/tmp hysnsec/nikto -h prod-XqiHnDZ0 -o /tmp/nikto-output.xml
  artifacts:
    paths: [nikto-output.xml]
    when: always

sslscan:
  stage: integration
  script:
    - docker pull hysnsec/sslyze
    - docker run --rm -v $(pwd):/tmp hysnsec/sslyze --regular prod-XqiHnDZ0.lab.practical-devsecops.training:443 --json_out /tmp/sslyze-output.json
  artifacts:
    paths: [sslyze-output.json]
    when: always

nmap:
  stage: integration
  script:
    - docker pull hysnsec/nmap
    - docker run --rm -v $(pwd):/tmp hysnsec/nmap prod-XqiHnDZ0 -oX /tmp/nmap-output.xml
  artifacts:
    paths: [nmap-output.xml]
    when: always

zap-baseline:
  stage: integration
  script:
    - docker pull owasp/zap2docker-stable
    - docker run --user $(id -u):$(id -g) -w /zap -v $(pwd):/zap/wrk:rw --rm owasp/zap2docker-stable zap-baseline.py -t https://prod-XqiHnDZ0.lab.practical-devsecops.training -J zap-output.json
  after_script:
    - docker rmi owasp/zap2docker-stable  # clean up the image to save the disk space
  artifacts:
    paths: [zap-output.json]
    when: always # What does this do?
  allow_failure: false
```

Infrastructure as Code (IaC)
--------------------------------

```
# Infrastructure as Code
# PLEASE ENSURE YOU HAVE SETUP THE ENVIRONMENT VARIABLES APPROPRIATELY
ansible-hardening:
  stage: prod
  image: willhallonline/ansible:2.9-ubuntu-18.04
  before_script:
    - mkdir -p ~/.ssh
    - echo "$DEPLOYMENT_SERVER_SSH_PRIVKEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -t rsa $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
  script:
    - echo -e "[prod]\n$DEPLOYMENT_SERVER" >> inventory.ini
    - ansible-galaxy install dev-sec.os-hardening
    - ansible-playbook -i inventory.ini ansible-hardening.yml
```

Compliance as Code (CaC)
--------------------------------

```

# Compliance as Code
# PLEASE ENSURE YOU HAVE SETUP THE ENVIRONMENT VARIABLES APPROPRIATELY
inspec:
  stage: prod
  only:
    - "master"
  environment: production
  before_script:
    - mkdir -p ~/.ssh
    - echo "$DEPLOYMENT_SERVER_SSH_PRIVKEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -t rsa $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
  script:
    - docker run --rm -v ~/.ssh:/root/.ssh -v $(pwd):/share hysnsec/inspec exec https://github.com/dev-sec/linux-baseline -t ssh://root@$DEPLOYMENT_SERVER -i ~/.ssh/id_rsa --chef-license accept --reporter json:inspec-output.json
  artifacts:
    paths: [inspec-output.json]
    when: always
```

Vulnerability Management
----------

```
# Vulnerability Management(VM)
sast-with-vm:
  stage: build
  before_script:
    - apk add py-pip curl
    - curl https://gitlab.practical-devsecops.training/-/snippets/3/raw -o upload-results.py
  script:
    - docker pull hysnsec/bandit  # Download bandit docker container
    - docker run --user $(id -u):$(id -g) -v $(pwd):/src --rm hysnsec/bandit -r /src -f json -o /src/bandit-output.json
  after_script:
    - python3 upload-results.py --host $DOJO_HOST --api_key $DOJO_API_TOKEN --engagement_id 1 --product_id 1 --lead_id 1 --environment "Production" --result_file bandit-output.json --scanner "Bandit Scan"
  artifacts:
    paths: [bandit-output.json]
    when: always
```

Combining various scans together
----------

Let’s combine the SCA, SAST, DAST, IaC, CaC scans and Vulnerability Management steps into a Gitlab CI script.

We will login into the GitLab using the following details and execute this pipeline.

Next, we need to create a CI/CD pipeline by replacing the .gitlab-ci.yml file content with the below Gitlab CI script. Click on the Edit button to start replacing the content (use Control+A and Control+V).

```
image: docker:latest

services:
  - docker:dind

stages:
  - build
  - test
  - release
  - preprod
  - integration
  - prod

build:
  stage: build
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py check

test:
  stage: test
  image: python:3.6
  before_script:
   - pip3 install --upgrade virtualenv
  script:
   - virtualenv env
   - source env/bin/activate
   - pip install -r requirements.txt
   - python manage.py test taskManager

# Software Component Analysis
sca-frontend:
  stage: build
  image: node:alpine3.10
  script:
    - npm install
    - npm install -g retire # Install retirejs npm package.
    - retire --outputformat json --outputpath retirejs-report.json --severity high --exitwith 0
  artifacts:
    paths: [retirejs-report.json]
    when: always # What is this for?
    expire_in: one week

sca-backend:
  stage: build
  script:
    - docker pull hysnsec/safety
    - docker run --rm -v $(pwd):/src hysnsec/safety check -r requirements.txt --json > oast-results.json
  artifacts:
    paths: [oast-results.json]
    when: always # What does this do?
  allow_failure: true #<--- allow the build to fail but don't mark it as such

# Git Secrets Scanning
secrets-scanning:
  stage: build
  script:
    - apk add git
    - git checkout master
    - docker run -v $(pwd):/src --rm hysnsec/trufflehog file:///src --json | tee trufflehog-output.json
  artifacts:
    paths: [trufflehog-output.json]
    when: always # What is this for?
    expire_in: one week
  allow_failure: true   #<--- allow the build to fail but don't mark it as such

# Static Application Security Testing
sast:
  stage: build
  script:
    - docker pull hysnsec/bandit  # Download bandit docker container
    # Run docker container, please refer docker security course, if this doesn't make sense to you.
    - docker run --user $(id -u):$(id -g) -v $(pwd):/src --rm hysnsec/bandit -r /src -f json -o /src/bandit-output.json
  artifacts:
    paths: [bandit-output.json]
    when: always
  allow_failure: true   #<--- allow the build to fail but don't mark it as such

# Dynamic Application Security Testing
nikto:
  stage: integration
  script:
    - docker pull hysnsec/nikto
    - docker run --rm -v $(pwd):/tmp hysnsec/nikto -h prod-XqiHnDZ0 -o /tmp/nikto-output.xml
  artifacts:
    paths: [nikto-output.xml]
    when: always

sslscan:
  stage: integration
  script:
    - docker pull hysnsec/sslyze
    - docker run --rm -v $(pwd):/tmp hysnsec/sslyze --regular prod-XqiHnDZ0.lab.practical-devsecops.training:443 --json_out /tmp/sslyze-output.json
  artifacts:
    paths: [sslyze-output.json]
    when: always

nmap:
  stage: integration
  script:
    - docker pull hysnsec/nmap
    - docker run --rm -v $(pwd):/tmp hysnsec/nmap prod-XqiHnDZ0 -oX /tmp/nmap-output.xml
  artifacts:
    paths: [nmap-output.xml]
    when: always

zap-baseline:
  stage: integration
  script:
    - docker pull owasp/zap2docker-stable
    - docker run --user $(id -u):$(id -g) --rm -v $(pwd):/zap/wrk:rw owasp/zap2docker-stable zap-baseline.py -t https://prod-XqiHnDZ0.lab.practical-devsecops.training -J zap-output.json
  after_script:
    - docker rmi owasp/zap2docker-stable  # clean up the image to save the disk space
  artifacts:
    paths: [zap-output.json]
    when: always # What does this do?
  allow_failure: false

# Infrastructure as Code
# PLEASE ENSURE YOU HAVE SETUP THE ENVIRONMENT VARIABLES AND NEEDED FILES APPROPRIATELY
ansible-hardening:
  stage: prod
  image: willhallonline/ansible:2.9-ubuntu-18.04
  before_script:
    - mkdir -p ~/.ssh
    - echo "$DEPLOYMENT_SERVER_SSH_PRIVKEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -t rsa $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
  script:
    - echo -e "[prod]\n$DEPLOYMENT_SERVER" >> inventory.ini
    - ansible-galaxy install dev-sec.os-hardening
    - ansible-playbook -i inventory.ini ansible-hardening.yml

# Compliance as Code
# PLEASE ENSURE YOU HAVE SETUP THE ENVIRONMENT VARIABLES AND NEEDED FILES APPROPRIATELY
inspec:
  stage: prod
  only:
    - "master"
  environment: production
  before_script:
    - mkdir -p ~/.ssh
    - echo "$DEPLOYMENT_SERVER_SSH_PRIVKEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -t rsa $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
  script:
    - docker run --rm -v ~/.ssh:/root/.ssh -v $(pwd):/share hysnsec/inspec exec https://github.com/dev-sec/linux-baseline -t ssh://root@$DEPLOYMENT_SERVER -i ~/.ssh/id_rsa --chef-license accept --reporter json:inspec-output.json
  artifacts:
    paths: [inspec-output.json]
    when: always

# Vulnerability Management(VM)
sast-with-vm:
  stage: build
  before_script:
    - apk add py-pip curl
    - curl https://gitlab.practical-devsecops.training/-/snippets/3/raw -o upload-results.py
  script:
    - docker pull hysnsec/bandit  # Download bandit docker container
    - docker run --user $(id -u):$(id -g) -v $(pwd):/src --rm hysnsec/bandit -r /src -f json -o /src/bandit-output.json
  after_script:
    - python3 upload-results.py --host $DOJO_HOST --api_key $DOJO_API_TOKEN --engagement_id 1 --product_id 1 --lead_id 1 --environment "Production" --result_file bandit-output.json --scanner "Bandit Scan"
  artifacts:
    paths: [bandit-output.json]
    when: always
```

> Make sure you have added the necessary variables into your project (Settings > CI/CD) such as $DOJO_HOST, and $DOJO_API_TOKEN. Otherwise, your results are not uploaded to DefectDojo in the sast-with-vm job.

Verify the pipeline run
----------
As soon as a change is made to the repository, the pipeline starts executing the jobs.

We can see the results of this pipeline by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

You can click on the appropriate job to see the results.

Conclusion
---------
Congratulations! you have learned how to create an enterprise ready DevSecOps Pipeline that achieves DevSecOps Maturity Level 1 and 2.

> 70% of the world’s organizations do not have this kind of maturity and it takes anywhere between 3-5 years for you to implement the above things across the organization. Just SCA can take six months to roll out in any medium to large organization. We are not even talking about any customizations needed, convincing DevOps teams to use these practices.


Can you start your own DevSecOps Practice after this? Probably not. We covered a small subset of DevSecOps strategies in this course. DevSecOps is an ocean that requires constant efforts to master.


Next Steps
----------

Please explore the Certified DevSecOps Expert (CDE) Course for learning advanced DevSecOps practices including custom rulesets, authenticated DAST scans, Threat Modelling as Code and much more.

We provide a 10% discount for our students who have completed the CDP. Reach out to us via slack or email for more information.