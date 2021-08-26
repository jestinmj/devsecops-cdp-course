Inspec Command Resources
================================================================

Create and Run custom Inspec profile with command resource
--------

In this scenario, you will learn how to about the command resources and how they help you in checking the compliance requirements.

You will need to install the Inspec tool, create the profile and then run the Compliance scan against the server.

Setup Inspec
----------

You know the drill already,

Install Inspec
----------

```
wget https://packages.chef.io/files/stable/inspec/4.18.114/ubuntu/16.04/inspec_4.18.114-1_amd64.deb
dpkg -i inspec_4.18.114-1_amd64.deb
```

Create the profile
----------

Create a new folder and cd into that folder.
```
mkdir cis-ubuntu
cd cis-ubuntu
```
Test the barebone profile
----------
```
inspec init profile ubuntu --chef-license accept
```

Understand the audit command
----------

We will create a custom profile based on CIS Ubuntu 18.04 Benchmark, you can download the benchmark PDF from [here](https://downloads.cisecurity.org/#/) and refer the page 83 “Ensure sudo commands use pty”.

Let’s add this control/security best practice into Inspec profile. But, before we create the profile we need to ensure that the command works in DevSecOps Box and understand its output.

Execute the audit command.
--------------------------------

Following is the command, we will be using to check if pty is being used.

```
grep -Ei "^\s*Defaults\s+([^#]+,\s*)?use_pty(,\s+\S+\s*)*(\s+#.*)?$" /etc/sudoers /etc/sudoers.d/*
```

Interesting! we didn’t see any output so we can assume that we didn’t find use_pty setting in our sudoers file. Lets add this security best practice to the file and see how the above command behaves. 

Edit /etc/sudoers file using nano or any text editor and add the use_pty setting.

```
cat >> /etc/sudoers <<EOL
#
# This file MUST be edited with the 'visudo' command as root.
#
# Please consider adding local content in /etc/sudoers.d/ instead of
# directly modifying this file.
#
Defaults        env_reset
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
Defaults        use_pty    # you can put it here
# Host alias specification

# User alias specification

# Cmnd alias specification

# User privilege specification
root    ALL=(ALL:ALL) ALL

# Members of the admin group may gain root privileges
%admin ALL=(ALL) ALL

# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL

# See sudoers(5) for more information on "#include" directives:

#includedir /etc/sudoers.d
EOL
```

Let’s run the audit command once again and see if it finds pty usage. In short, absense of this string is a control failure and we need to enforce its presence.

output
```
/etc/sudoers:Defaults        use_pty    # you can put it here
```

Add the command to the profile.
--------------------------------

> Basically, we need to run a command against a system to check for compliance.

To do this, inspec provides us with a command resource/method.

Let’s have a look at [Inspec documentation for the command resource](https://docs.chef.io/inspec/resources/command/).

As mentioned above, we can use this resource to execute commands like the grep we ran in the last step. Once a command returns its output, we can use stdout(aka output) to compare it against the desired/expected value in our profile.

We will use the following command to replace the inspec task in the file, ubuntu/controls/example.rb. If you wish, you can edit the file manually, using nano or any text editor. 

```
cat > ubuntu/controls/example.rb <<EOL
control 'ubuntu-1.3.2' do
   title 'Ensure sudo commands use pty'
   desc 'Attackers can run a malicious program using sudo, which would again fork a background process that remains even when the main program has finished executing.'
   describe command('grep -Ei "^\s*Defaults\s+([^#]+,\s*)?use_pty(,\s+\S+\s*)*(\s+#.*)?$" /etc/sudoers /etc/sudoers.d/*') do
      its('stdout') { should match /Defaults(\s*)use_pty/ }
   end
end
EOL
```
Ignore the should match text for now as we will be covering it shortly in the next lesson. 

> Reference: [Regex match any whitespace.](https://stackoverflow.com/questions/21974376/regex-match-any-whitespace)

Did you wonder, why are we using the regex? This is to ensure, we capture the exact match irrespective of space or tab as a seperator used between Defaults and use_pty strings.

output
```
/etc/sudoers:Defaults        use_pty    # you can put it here
```

The sudoer file can also just a space and it will be valid.

```
/etc/sudoers:Defaults use_pty    # you can put it here
```

If you haven’t fallen in love with regex yet, head over to [Rubular site](https://rubular.com/) to proclaim your love.

Jokes aside, let’s validate the profile to ensure there are no syntax errors.

```
inspec check ubuntu
```
Now, run the profile on the local-machine before executing it on the remote server

```
inspec exec ubuntu
```
output
```
Profile: InSpec Profile (ubuntu)
Version: 0.1.0
Target:  local://

  ✔  ubuntu-1.3.2: Ensure sudo commands use pty
     ✔  Command: `grep -Ei "^\s*Defaults\s+([^#]+,\s*)?use_pty(,\s+\S+\s*)*(\s+#.*)?$" /etc/sudoers /etc/sudoers.d/*` stdout is expected to match /Defau
lts(\s*)use_pty/


Profile Summary: 1 successful control, 0 control failures, 0 controls skipped
Test Summary: 1 successful, 0 failures, 0 skipped
```

You can see, we have about 1 successful control check because we just add the remediation into DevSecOps Box.

Run the Inspec Profile to test for compliance against a server
----------

Let’s try to run the custom profile created by us against the server.

Before executing the profile, we need to execute the below command.

```
echo "StrictHostKeyChecking no" >> ~/.ssh/config
```

The above command prevents the ssh agent from prompting YES or NO question.

Let’s run inspec with the following options.

```
inspec exec ubuntu -t ssh://root@prod-XqiHnDZ0 -i ~/.ssh/id_rsa --chef-license accept
```
output
```
Profile: InSpec Profile (ubuntu)
Version: 0.1.0
Target:  ssh://root@prod-XqiHnDZ0:22

  ×  ubuntu-1.3.2: Ensure sudo commands use pty
     ×  Command: `grep -Ei "^\s*Defaults\s+([^#]+,\s*)?use_pty(,\s+\S+\s*)*(\s+#.*)?$" /etc/sudoers /etc/sudoers.d/*` stdout is expected to match /Defau
lts(\s*)use_pty/
     expected "" to match /Defaults(\s*)use_pty/
     Diff:
     @@ -1,2 +1,2 @@
     -/Defaults(\s*)use_pty/
     +""

Profile Summary: 0 successful controls, 1 control failure, 0 controls skipped
Test Summary: 0 successful, 1 failure, 0 skipped
```
The flags/options used in the above commands are:

- -t : tells the target machine to run the profile against.
- -i : provides the path where the remote machine’s ssh key is stored.
- --chef-license : accept ensures that we are accepting license agreement there by preventing the inspec from prompting YES or NO question.

You can see, we got 1 control failure i.e., the production machine doesn’t follow the CIS best practice. The DevOps/Security team can run Ansible hardening scripts to ensure the production machine is hardened and continously scan the production machine for compliance.