Create Inspec Profile for CIS Benchmark
===============================

Create and Run custom Inspec profile based on CIS Ubuntu Benchmark
----------

In this scenario, you will learn how to create a custom Inspec profile to check for your organization’s policies as code. You will also learn how to test this profile against a server.

Install Inspec Tool
----------
Let’s install the Inspec on the system.

Download the Inspec Debian package from the InSpec website

```
wget https://packages.chef.io/files/stable/inspec/4.18.114/ubuntu/16.04/inspec_4.18.114-1_amd64.deb
dpkg -i inspec_4.18.114-1_amd64.deb
```
We have successfully installed the Inspec tool, let’s explore the functionality it provides us.

```
inspec --help
```

Create the profile with CIS Benchmark
-----------

We will create a custom profile for Inspec using the commands and best practices mentioned in CIS Ubuntu 18.04 Benchmark; you can download the CIS Ubuntu 18.04 Benchmark PDF from [here](https://downloads.cisecurity.org/#/).

Please refer the page no. 80, “Configure Sudo” for more information. Let’s convert the audit steps mentioned in the CIS Benchmark into a custom Inspec profile.

In short, we need to do two things to create a profile.
1. Figure out the command/tool that needs to be run to ascertain the state of the system.
2. Add the above command to the Inspec profile.

Let’s go ahead and create the Inspec profile.

To store our Inspec profile, we will create a new folder and cd into the newly created folder.

```
mkdir cis-ubuntu && cd cis-ubuntu
```

Use the inspec init command to create an Ubuntu Inspec profile.

```
inspec init profile ubuntu --chef-license accept
```
Run the following command to append the inspec task to the ubuntu/controls/configure_sudo.rb file. If you wish, you can edit the file using nano or any text editor.

```
cat >> ubuntu/controls/configure_sudo.rb <<EOL
control 'ubuntu-1.3.1' do
   title 'Ensure sudo is installed'
   desc 'sudo allows a permitted user to execute a command as the superuser or another user, as specified by the security policy.'
   describe package('sudo') do
      it { should be_installed }
   end
end

control 'ubuntu-1.3.2' do
   title 'Ensure sudo commands use pty'
   desc 'Attackers can run a malicious program using sudo, which would again fork a background process that remains even when the main program has finished executing.'
   describe command('grep -Ei "^\s*Defaults\s+([^#]+,\s*)?use_pty(,\s+\S+\s*)*(\s+#.*)?$" /etc/sudoers').stdout do
      it { should include 'Defaults use_pty' }
   end
end

control 'ubuntu-1.3.3' do
   title 'Ensure sudo log file exists'
   desc 'Attackers can run a malicious program using sudo, which would again fork a background process that remains even when the main program has finished executing.'
   describe command('grep -Ei "^\s*Defaults\s+logfile=\S+" /etc/sudoers').stdout do
      it { should include 'Defaults logfile=' }
   end
end
EOL
```

Remove the ubuntu/controls/example.rb file, as we will not use it in this profile.

```
rm ubuntu/controls/example.rb
```

> Can you use the command resource to check if the package is installed or not in the system?

If you notice in the above Inspec profile script, you will see a couple of new terms like package and command. These terms are called resources; think of them as modules or plugins that help you achieve something in the system.

- [command resource](https://docs.chef.io/inspec/resources/command/)
- [package resource](https://docs.chef.io/inspec/resources/package/)

For now, let’s move forward. If you wish to explore these resources further, you can use the above links.

The above code checks if the sudo package is installed. We are also checking if the file /etc/sudoers contain some sane security defaults. The CIS benchmark PDF provides us the needed commands to audit the system’s state, and we are using these commands to convert them into Inspec checks.

We tried to keep everything simple in this exercise for the sake of simplicity, but you do need to implement most of these checks in your organization. If we have a few hundred ubuntu servers to patch, maintain or ensure compliance, do you think we can/should do these manually? No, we should create an Inspec profile to automate our compliance checks. This process is what most people call Compliance as Code.

Let’s validate the profile to ensure there are no syntax errors.

```
inspec check ubuntu
```
Now run the profile on the local machine before executing it against a server. If we do not provide any server details, it runs on the local machine by default.

```
inspec exec ubuntu
```
output
```
Profile: InSpec Profile (ubuntu)
Version: 0.1.0
Target:  local://

  ✔  ubuntu-1.3.1: Ensure sudo is installed
     ✔  System Package sudo is expected to be installed
  ×  ubuntu-1.3.2: Ensure sudo commands use pty
     ×  is expected to include "Defaults use_pty"
     expected "" to include "Defaults use_pty"
  ×  ubuntu-1.3.3: Ensure sudo log file exists
     ×  is expected to include "Defaults logfile="
     expected "" to include "Defaults logfile="


Profile Summary: 1 successful control, 2 control failures, 0 controls skipped
Test Summary: 1 successful, 2 failures, 0 skipped
/cis-ubuntu# 
```

Run the Inspec against a remote server
----------

Let’s try to run the custom profile we just created against a remote server.

Before executing the profile, we need to implement the password-less SSH login mechanism between the local machine and the remote machine.

To configure passwordless SSH login, we need to implement the following two steps.
1. Get rid of the SSH key verification checks.
2. Copy your local SSH public key into the remote machine.

We have already taken care of step 2 for you, so you only have to deal with step 1. Obviously, we can achieve step 1 objectives in multiple ways. Here, we are disabling host key checks, but it’s a bad idea to do it in production. Please research why it’s a bad idea!

```
echo "StrictHostKeyChecking no" >> ~/.ssh/config
inspec exec ubuntu -t ssh://root@prod-XqiHnDZ0 -i ~/.ssh/id_rsa --chef-license accept
```
output

```
Profile: InSpec Profile (ubuntu)
Version: 0.1.0
Target:  ssh://root@prod-XqiHnDZ0:22

  ×  ubuntu-1.3.1: Ensure sudo is installed
     ×  System Package sudo is expected to be installed
     expected that `System Package sudo` is installed
  ×  ubuntu-1.3.2: Ensure sudo commands use pty
     ×  is expected to include "Defaults use_pty"
     expected "" to include "Defaults use_pty"
  ×  ubuntu-1.3.3: Ensure sudo log file exists
     ×  is expected to include "Defaults logfile="
     expected "" to include "Defaults logfile="


Profile Summary: 0 successful controls, 3 control failures, 0 controls skipped
Test Summary: 0 successful, 3 failures, 0 skipped
```

Woah! Lot is going on here. Let’s explore these options one by one.

The flags/options used in the above commands are
- -t specifies the target machine to run the Inspec profile against. Here, we are using SSH as a remote login mechanism, but we can also use winrm (windows), container (docker), etc.,
- -i provides the path where the remote/local machine’s ssh key is stored.
- --chef-license option ensures that we are accepting the license agreement automatically.

We can see that we have about 1 successful control check and 2 control failures.

Exercise
---------
    
1. Read the documentation about [OS Resources](https://docs.chef.io/inspec/resources/)
2. Understand the difference between command and service resource
3. Please do whatever it takes on the production machine to achieve the following Inspec output

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

```
Profile: InSpec Profile (ubuntu)
Version: 0.1.0
Target:  ssh://root@prod-jftfefdf:22

✔  ubuntu-1.3.1: Ensure sudo is installed
   ✔  System Package sudo is expected to be installed
✔  ubuntu-1.3.2: Ensure sudo commands use pty
   ✔  Defaults use_pty
      is expected to include "Defaults use_pty"
✔  ubuntu-1.3.3: Ensure sudo log file exists
   ✔  Defaults logfile="/var/log/sudo.log"
      is expected to include "Defaults logfile="

Profile Summary: 3 successful controls, 0 control failures, 0 controls skipped
Test Summary: 3 successful, 0 failures, 0 skipped
```
