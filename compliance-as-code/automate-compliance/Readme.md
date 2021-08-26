Compliance as Code (CaC) using Inspec
====================================================

Learn how to achieve compliance automation using the Inspec tool
--------------------------------

In this scenario, you will learn how to install the Inspec and test a server for compliance.

As part of this scenario, you will need to install the Inspec tool and then run the Compliance scan against the production(prod) server.

Install Inspec Tool
----------

> Chef InSpec is an open-source framework for testing and auditing your applications and infrastructure. Chef InSpec works by comparing the actual state of your system with the desired state that you express in easy-to-read and easy-to-write Chef InSpec code. Chef InSpec detects violations and displays findings in the form of a report, but puts you in control of remediation.
>
> Source: [Inspec official website](https://www.inspec.io/docs)

Let’s install the Inspec on the system to learn Compliance as Code (CaC).

Download the Inspec debian package from the InSpec website.

```
wget https://packages.chef.io/files/stable/inspec/4.37.8/ubuntu/18.04/inspec_4.37.8-1_amd64.deb
dpkg -i inspec_4.37.8-1_amd64.deb
inspec --help
```

Run the Inspec profile
----------

Let’s try to check whether our servers follow the linux-baseline best practices. We will be using the Dev-Sec’s linux-baseline Inspec profile.

Before executing the profile, we need to run the below command:

```
echo "StrictHostKeyChecking no" >> ~/.ssh/config
```
This command prevents the ssh agent from prompting YES or NO question.

Let’s run the Inspec against the production server.
```
inspec exec https://github.com/dev-sec/linux-baseline -t ssh://root@prod-XqiHnDZ0 -i ~/.ssh/id_rsa --chef-license accept
```

- The first parameter tells the Inspec profile that we need to run against the server
- -t tells the target machine
- -i flag used to specify the ssh-key since we are using login in via ssh
- --chef-license accept tells that we are accepting license this commands prevent the inspec from prompting YES or NO question

output
```
+---------------------------------------------+
✔ 1 product license accepted.
+---------------------------------------------+
[2021-04-12T22:47:51+00:00] WARN: URL target https://github.com/dev-sec/linux-baseline transformed to https://github.com/dev-sec/linux-baseline/archive/master.tar.gz. Consider using the git fetcher

Profile: DevSec Linux Security Baseline (linux-baseline)
Version: 2.8.0
Target:  ssh://root@prod-XqiHnDZ0:22

  ✔  os-01: Trusted hosts login
     ✔  File /etc/hosts.equiv is expected not to exist
  ✔  os-02: Check owner and permissions for /etc/shadow
     ✔  File /etc/shadow is expected to exist
     ✔  File /etc/shadow is expected to be file
     ✔  File /etc/shadow is expected to be owned by "root"
     ✔  File /etc/shadow is expected not to be executable
     ✔  File /etc/shadow is expected not to be readable by other
     ✔  File /etc/shadow group is expected to eq "shadow"
     ✔  File /etc/shadow is expected to be writable by owner
     ✔  File /etc/shadow is expected to be readable by owner
     ✔  File /etc/shadow is expected to be readable by group


  ...[SNIP]...


  ↺  sysctl-31b: Secure Core Dumps - dump path
     ↺  Skipped control due to only_if condition.
  ↺  sysctl-32: kernel.randomize_va_space
     ↺  Skipped control due to only_if condition.
  ↺  sysctl-33: CPU No execution Flag or Kernel ExecShield
     ↺  Skipped control due to only_if condition.


Profile Summary: 16 successful controls, 2 control failures, 37 controls skipped
Test Summary: 60 successful, 7 failures, 37 skipped
```
You can see, the output does inform us about 16 successful controls and 2 control failures.

Exercise 8.1/8.2 Using Ansible/Inspec to achieve compliance.
--------------------------------

This exercise is to do continuous compliance scanning for production Infrastructure. We will be using the configuration management tools, i.e., Ansible and a dedicated utility like Inspec. Please embed these two tools into your DevOps pipeline.

Doing so will provide immediate feedback to the DevOps teams of any deviation from standard policies.

1. Use Ansible to achieve compliance as code (remember the changed=1 Ansible output?)
2. Use Docker Inspec to do continuous compliance scanning and save the output into JSON file
3. Embed Ansible hardening and Inspec as part of the prod stage with job names as ansible-hardening and inspec
4. Ensure you are using the following projects for this task
    - https://github.com/dev-sec/ansible-os-hardening
    - https://github.com/dev-sec/linux-baseline

> Please try to do this exercise without looking at the solution on the next page.

Embed Inspec in CI/CD pipeline
--------------------------------

> Can we put it into CI? Yes, why not?

Let’s login into the GitLab and configure production machine https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/settings/ci_cd.

We can use the GitLab credentials provided below to login i.e.,
- username: root
- password: pdso-training

Click the Expand button under the Variables section, then click on the Add Variable button.

Add the following key/value pair in the form.

- key: DEPLOYMENT_SERVER
- value : prod-XqiHnDZ0
- key: DEPLOYMENT_SERVER_SSH_PRIVKEY
- value: Copy the private key from the prod machine using SSH. The SSH key is available at /root/.ssh/id_rsa

Finally, Click on the button Add Variable.

Next, please visit https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/-/blob/master/.gitlab-ci.yml.

Click on the Edit button and append the following code to the .gitlab-ci.yml file.

```
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

> Reference: https://docs.chef.io/inspec/reporters.

Save changes to the file using the Commit changes button.

> Don’t forget to set DEPLOYMENT_SERVER variable under Settings (Project Settings > CI/CD > Variables > Expand > Add Variable), otherwise your build will fail.

We can see the results by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

There you have it. We have run the Inspec locally and then embedded it into a CI/CD pipeline.