How to Create Custom Inspec Profile
========================================================

Create and Run custom Inspec profile
-----------

In this scenario, you will learn how to create a dummy Inspec profile and run it against a production machine.

You will need to install the Inspec tool, create the profile and then run the Compliance scan against the server.

Install Inspec Tool
----------

> Chef InSpec is an open-source framework for testing and auditing your applications and infrastructure. Chef InSpec works by comparing the actual state of your system with the desired state that you express in easy-to-read and easy-to-write Chef InSpec code. Chef InSpec detects violations and displays findings in the form of a report, but puts you in control of remediation.
>
> Source: [Inspec official website](https://www.inspec.io/docs)

Let’s install the Inspec on the system to learn Compliance as Code (CaC).

Download the Inspec debian package from the InSpec website.

```
curl https://omnitruck.chef.io/install.sh | sudo bash -s -- -v 5.22.29 -P inspec
inspec --help
```

Create the custom profile
----------

Create a new folder and cd into that folder.

```
mkdir inspec-profile && cd inspec-profile
```
create the ubuntu profile
```
inspec init profile ubuntu --chef-license accept

+---------------------------------------------+
✔ 1 product license accepted.
+---------------------------------------------+

 ─────────────────────────── InSpec Code Generator ─────────────────────────── 

Creating new profile at /inspec-profile/ubuntu
 • Creating file README.md
 • Creating directory /inspec-profile/ubuntu/controls
 • Creating file controls/example.rb
 • Creating file inspec.yml

```

Run the following command to append the inspec task to the file at ubuntu/controls/example.rb. If you wish, you can edit the file using nano or any text editor.

```
cat > ubuntu/controls/example.rb <<EOL
describe file('/etc/shadow') do
    it { should exist }
    it { should be_file }
    it { should be_owned_by 'root' }
  end
EOL
```

This code basically checks whether shadow file is owned by root or not.

To know more about Inspec, please visit the official website at [Inspec-tutorial](https://www.inspec.io/tutorials)

Let’s validate the profile to make sure there are no syntax errors.

```
inspec check ubuntu
```
output
```
Location :   ubuntu
Profile :    ubuntu
Controls :   1
Timestamp :  2025-05-22T07:11:23+00:00
Valid :      true

No errors, warnings, or offenses
```

Now run the profile on the local-machine before executing on the server.

```
inspec exec ubuntu
```
output
```
Profile:   InSpec Profile (ubuntu)
Version:   0.1.0
Target:    local://
Target ID: e74dbe5a-353c-525a-b810-1f5bd17b04b9

  File /etc/shadow
     ✔  is expected to exist
     ✔  is expected to be file
     ✔  is expected to be owned by "root"

Test Summary: 3 successful, 0 failures, 0 skipped
```

Run the Inspec tool to test for compliance against a server
----------

Let’s try to run the custom profile created by us against the server. Before executing the profile we need to execute the below command to avoid being prompted with Yes or No when connecting to a server via ssh.

```
echo "StrictHostKeyChecking accept-new" >> ~/.ssh/config
```

This commands prevent the ssh agent from prompting YES or NO question

Let’s run inspec with the following options.

```
inspec exec ubuntu -t ssh://root@prod-XqiHnDZ0 -i ~/.ssh/id_rsa --chef-license accept
```

- -t tells the target machine
- -i flag used to specify the ssh-key since we are using login in via ssh
- --chef-license option ensures that we are accepting license agreement automatically.

```
Profile:   InSpec Profile (ubuntu)
Version:   0.1.0
Target:    ssh://root@prod-p30jrhut:22
Target ID: fae01aff-6e53-59df-9938-5c5bf056258e

  File /etc/shadow
     ✔  is expected to exist
     ✔  is expected to be file
     ✔  is expected to be owned by "root"

Test Summary: 3 successful, 0 failures, 0 skipped
```

Exercise 8.3 Create an InSpec profile for PCI/DSS
--------
1. Create new inspec profile named challenge in /inspec-profile directory using inspect init
    We have created the /inspec-profile directory. To ensure you are inside this directory, use the pwd command. If you find that you are not in that directory, use the command below.
    <br>`cd /inspec-profile`
    Create a new profile named challenge inside the /inspec-profile directory.
    <br>`inspec init profile challenge --chef-license accept`
    ```
    ─────────────────────────── InSpec Code Generator ─────────────────────────── 

    Creating new profile at /inspec-profile/challenge
     • Creating file README.md
     • Creating directory /inspec-profile/challenge/controls
     • Creating file controls/example.rb
     • Creating file inspec.yml
    ```
2. Edit the newly created InSpec skeleton to include four basic checks: system, password, ssh, and useradd, based on PCI/DSS requirements. You can find details in the [PCI/DSS requirements document](https://www.chef.io/docs/default-source/whitepapers/guidetopcidsscompliance.pdf)

Run the command below to add PCI/DSS checks to your InSpec profile.
> For reference, check the [PCI/DSS requirements document](https://www.chef.io/docs/default-source/whitepapers/guidetopcidsscompliance.pdf):
> - Page 8: Compare system and password requirements with the provided hint.
> - Page 12: Review the useradd command requirements.
> - For SSH configuration, refer to the provided hint as it’s not included in the referenced document.
```
cat > /inspec-profile/challenge/controls/example.rb <<EOL
describe file('/etc/pam.d/system-auth') do
    its('content') { 
        should match(/^\s*password\s+requisite\s+pam_pwquality\.so\s+(\S+\s+)*try_first_pass/)
    }
    its('content') {
        should match(/^\s*password\s+requisite\s+pam_pwquality\.so\s+(\S+\s+)*retry=[3210]/)
    }
end

describe file('/etc/pam.d/password-auth') do
    its('content') { 
        should match(/^\s*password\s+requisite\s+pam_pwquality\.so\s+(\S+\s+)*try_first_pass/)
    }
    its('content') {
        should match(/^\s*password\s+requisite\s+pam_pwquality\.so\s+(\S+\s+)*retry=[3210]/)
    }
end

describe file('/etc/default/useradd') do
    its('content') {
        should match(/^\s*INACTIVE\s*=\s*(30|[1-2][0-9]|[1-9])\s*(\s+#.*)?$/)
    }
end

describe file('/etc/ssh/sshd_config') do
    it { should exist }
    it { should be_file }
    it { should be_owned_by 'root' }
    its('content') { should match 'PasswordAuthentication no' }
end
EOL
```

3. Test the challenge InSpec profile locally before integrating it into the CI pipeline
<br>`inspec check challenge`
```
Location :   challenge
Profile :    challenge
Controls :   4
Timestamp :  2023-12-10T00:15:21+00:00
Valid :      true

No errors, warnings, or offenses
```
<br>`inspec exec challenge`
```
...[SNIP]...

  File /etc/ssh/sshd_config
     ✔  is expected to exist
     ✔  is expected to be file
     ✔  is expected to be owned by "root"
     ✔  content is expected to match "PasswordAuthentication no"

Test Summary: 4 successful, 5 failures, 0 skipped
```


4. Commit the challenge InSpec profile to your project’s repository using GitLab UI or Git commands.

If you’re in the /inspec-profile directory, you’ll need to navigate to a different directory before cloning the repository to avoid conflicts with the existing InSpec profile.
<br>`cd`

It will switch your directory to /root. Let’s ensure we are in the correct directory.
Then, run the following commands to push challenge profile into your GitLab repository:
```
git clone git@gitlab-ce-p30jrhut:root/django-nv.git
cd django-nv
cp -r /inspec-profile/challenge challenge
git add challenge
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git commit -m "Add custom inspec profile"
git push origin main
```

5. In the .gitlab-ci.yml file, add a new job named compliance in the test stage to execute the profile using the InSpec command. Use the hysnsec/inspec Docker image to run the command.

Create a job named compliance directly in the .gitlab-ci.yml file within the django.nv repository by copying the following content.
```
image: docker:20.10

services:
  - docker:dind

stages:
  - test

compliance:
  stage: test
  script:
    - docker run -i --rm -v $(pwd):/share hysnsec/inspec check challenge --chef-license accept
    - docker run -i --rm -v $(pwd):/share hysnsec/inspec exec challenge --chef-license accept
  allow_failure: true
```
Alternatively, you can directly make changes to the repository using the command provided below in the terminal (DevSecOps Box).
```
Alternatively, you can directly make changes to the repository using the command provided below in the terminal (DevSecOps Box).
```
Push the changes to the repository.
```
git add .gitlab-ci.yml
git commit -m "Update .gitlab-ci.yml"
git push origin main
```




1. Use Inspec’s init command to create a new profile
2. Edit our newly created Inspec skeleton to add new functionality like checking for the content of a file on a remote machine
3. Run the tests locally before setting it up in the CI pipeline
4. Commit it to the project’s repository using either the GitLab UI or Git commands

> You can access your GitLab machine by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training and use the credentials mentioned in the first step.

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).
