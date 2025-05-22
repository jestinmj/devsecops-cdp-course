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
wget https://packages.chef.io/files/stable/inspec/5.22.29/ubuntu/18.04/inspec_5.22.29-1_amd64.deb

# Install the downloaded package.
dpkg -i inspec_4.37.8-1_amd64.deb
inspec --help
```

```
Commands:
  inspec archive PATH                                  # Archive a profile to a tar file (default) or zip file.
  inspec automate SUBCOMMAND or compliance SUBCOMMAND  # Chef Automate commands
  inspec check PATH                                    # Verify the metadata in the `inspec.yml` file, verif...
  inspec clear_cache                                   # clears the InSpec cache. Useful for debugging.
  inspec detect                                        # detects the target OS.
  inspec env                                           # Outputs shell-appropriate completion configuration.
  inspec exec LOCATIONS                                # Run all test files at the specified locations.
  inspec export PATH                                   # read the profile in PATH and generate a summary in ...
  inspec habitat SUBCOMMAND                            # Manage Habitat with Chef InSpec
  inspec help [COMMAND]                                # Describe available commands or one specific command
  inspec init SUBCOMMAND                               # Generate InSpec code
  inspec json PATH                                     # read all tests in the PATH and generate a JSON summ...
  inspec plugin SUBCOMMAND                             # Manage Chef InSpec and Train plugins
  inspec shell                                         # open an interactive debugging shell.
  inspec sign SUBCOMMAND                               # Manage Chef InSpec profile signing.
  inspec supermarket SUBCOMMAND ...                    # Supermarket commands
  inspec vendor PATH                                   # Download all dependencies and generate a lockfile i...
  inspec version                                       # prints the version of this tool.

Options:
  l, [--log-level=LOG_LEVEL]                        # Set the log level: info (default), debug, warn, error
     [--log-location=LOG_LOCATION]                  # Location to send diagnostic log messages to. (default: $stdout or Inspec::Log.error)
     [--diagnose], [--no-diagnose]                  # Show diagnostics (versions, configurations)
     [--color], [--no-color]                        # Use colors in output.
     [--interactive], [--no-interactive]            # Allow or disable user interaction
     [--disable-user-plugins]                       # Disable loading all plugins that the user installed.
     [--enable-telemetry], [--no-enable-telemetry]  # Allow or disable telemetry
     [--chef-license=CHEF_LICENSE]                  # Accept the license for this product and any contained products: accept, accept-no-persist, accept-silent


About Chef InSpec:
  Patents: chef.io/patents
```

Run the Inspec profile
----------

Let’s try to check whether our servers follow the linux-baseline best practices. We will be using the Dev-Sec’s linux-baseline Inspec profile.

Before executing the profile, we need to run the below command:

```
echo "StrictHostKeyChecking accept-new" >> ~/.ssh/config
```
This command prevents the ssh agent from prompting YES or NO question.

Let’s run the Inspec against the production server.
```
inspec exec https://github.com/dev-sec/linux-baseline.git -t ssh://root@prod-p30jrhut -i ~/.ssh/id_rsa --chef-license accept
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

Profile: DevSec Linux Security Baseline (linux-baseline)
Version: 2.8.0
Target:  ssh://root@prod-p30jrhut:22

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
   ↺  sysctl-34: Ensure links are protected
     ↺  Skipped control due to only_if condition.


Profile Summary: 17 successful controls, 3 control failures, 38 controls skipped
Test Summary: 65 successful, 8 failures, 38 skipped
```
You can see, that the output does inform us about 17 successful controls and 3 control failures.

Exercise 8.1/8.2 Using Ansible/Inspec to achieve compliance.
--------------------------------

This exercise is to do continuous compliance scanning for the production server (prod-p30jrhut). We will be embedding a dedicated Compliance as Code tool called Inspec in the CI/CD pipeline.

Doing so will provide immediate feedback to the DevOps teams of any deviation from standard policies.

You can use the following URL and credentials to log into GitLab CI/CD.
Let’s login into the GitLab and configure the production machine https://gitlab-ce-p30jrhut.lab.practical-devsecops.training/root/django-nv/-/settings/ci_cd.

Click the Expand button under the Variables section, then click on the Add Variable button.

Add the following key/value pair in the form.
![image](https://github.com/user-attachments/assets/5b8d558e-6c86-41dd-94ad-ddd515e387b6)

1. Use hysnsec/inspec docker image to perform continuous compliance scanning with [https://github.com/dev-sec/linux-baseline](https://github.com/dev-sec/linux-baseline) profile and embed it as part of the prod stage with job name as inspec
```
inspec:
  stage: prod
  before_script:
    - mkdir -p ~/.ssh
    - echo "$DEPLOYMENT_SERVER_SSH_PRIVKEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -H $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
  script:
    - docker run --rm -v ~/.ssh:/root/.ssh -v $(pwd):/share hysnsec/inspec exec https://github.com/dev-sec/linux-baseline.git -t ssh://root@$DEPLOYMENT_SERVER -i ~/.ssh/id_rsa --chef-license accept
```
2. The job should only be triggered when changes are pushed to the main branch (don’t use rules attribute)
```
inspec:
  stage: prod
  only:
    - main
  before_script:
    - mkdir -p ~/.ssh
    - echo "$DEPLOYMENT_SERVER_SSH_PRIVKEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -H $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
  script:
    - docker run --rm -v ~/.ssh:/root/.ssh -v $(pwd):/share hysnsec/inspec exec https://github.com/dev-sec/linux-baseline.git -t ssh://root@$DEPLOYMENT_SERVER -i ~/.ssh/id_rsa --chef-license accept
```
Referecnce: https://docs.gitlab.com/ee/ci/yaml/#only--except

3. Save the output as JSON file at /share/inspec-output.json and upload it using artifacts attribute
```
inspec:
  stage: prod
  only:
    - main
  environment: production
  before_script:
    - mkdir -p ~/.ssh
    - echo "$DEPLOYMENT_SERVER_SSH_PRIVKEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -H $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
  script:
    - docker run --rm -v ~/.ssh:/root/.ssh -v $(pwd):/share hysnsec/inspec exec https://github.com/dev-sec/linux-baseline.git -t ssh://root@$DEPLOYMENT_SERVER -i ~/.ssh/id_rsa --chef-license accept --reporter json:/share/inspec-output.json
  artifacts:
    paths: [inspec-output.json]
    when: always
```
Reference: https://docs.chef.io/inspec/reporters


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
    - main
  environment: production
  before_script:
    - mkdir -p ~/.ssh
    - echo "$DEPLOYMENT_SERVER_SSH_PRIVKEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -H $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
  script:
    - docker run --rm -v ~/.ssh:/root/.ssh -v $(pwd):/share hysnsec/inspec exec https://github.com/dev-sec/linux-baseline.git -t ssh://root@$DEPLOYMENT_SERVER -i ~/.ssh/id_rsa --chef-license accept --reporter json:/share/inspec-output.json
  artifacts:
    paths: [inspec-output.json]
    when: always
```
> /share directory should be used when using hysnsec/inspec image. Because it’s a custom image adding another directory would not work when you are saving the inspec output.

> Reference: https://docs.chef.io/inspec/reporters.

Save changes to the file using the Commit changes button.

> Don’t forget to set DEPLOYMENT_SERVER variable under Settings (Project Settings > CI/CD > Variables > Expand > Add Variable), otherwise your build will fail.

We can see the results by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv/pipelines.

Click on the appropriate job name to see the output.

There you have it. We have run the Inspec locally and then embedded it into a CI/CD pipeline.
