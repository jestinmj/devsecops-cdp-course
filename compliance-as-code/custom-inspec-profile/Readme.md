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
wget https://packages.chef.io/files/stable/inspec/4.37.8/ubuntu/18.04/inspec_4.37.8-1_amd64.deb
dpkg -i inspec_4.37.8-1_amd64.deb
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
```

Run the following command to append the inspec task to the file at ubuntu/controls/example.rb. If you wish, you can edit the file using nano or any text editor.

```
cat >> ubuntu/controls/example.rb <<EOL
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
Controls :   3
Timestamp :  2020-05-25T22:53:52+00:00
Valid :      true

No errors or warnings
```

Now run the profile on the local-machine before executing on the server.

```
inspec exec ubuntu
```
output
```
Profile: InSpec Profile (ubuntu)
Version: 0.1.0
Target:  local://

  ✔  tmp-1.0: Create /tmp directory
     ✔  File /tmp is expected to be directory

  File /tmp
     ✔  is expected to be directory
  File /etc/shadow
     ✔  is expected to exist
     ✔  is expected to be file
     ✔  is expected to be owned by "root"

Profile Summary: 1 successful control, 0 control failures, 0 controls skipped
Test Summary: 5 successful, 0 failures, 0 skipped
```

Run the Inspec tool to test for compliance against a server
----------

Let’s try to run the custom profile created by us against the server. Before executing the profile we need to execute the below command to avoid being prompted with Yes or No when connecting to a server via ssh.

```
echo "StrictHostKeyChecking no" >> ~/.ssh/config
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
Profile: InSpec Profile (ubuntu)
Version: 0.1.0
Target:  ssh://root@prod-jftfefdf:22

  ✔  tmp-1.0: Create /tmp directory
     ✔  File /tmp is expected to be directory

  File /tmp
     ✔  is expected to be directory
  File /etc/shadow
     ✔  is expected to exist
     ✔  is expected to be file
     ✔  is expected to be owned by "root"

Profile Summary: 1 successful control, 0 control failures, 0 controls skipped
Test Summary: 5 successful, 0 failures, 0 skipped
```

Exercise 8.3 Create an InSpec profile for PCI/DSS
--------

1. Use Inspec’s init command to create a new profile
2. Edit our newly created Inspec skeleton to add new functionality like checking for the content of a file on a remote machine
3. Run the tests locally before setting it up in the CI pipeline
4. Commit it to the project’s repository using either the GitLab UI or Git commands

> You can access your GitLab machine by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training and use the credentials mentioned in the first step.

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).
