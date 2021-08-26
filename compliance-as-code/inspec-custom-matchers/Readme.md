Inspec Custom Matchers
================================

Compare/Match the desired state of the system with real state
------

In this scenario, you will learn about custom matchers that are essential to any Inspec Profile.

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
```
mkdir cis-ubuntu
cd cis-ubuntu
inspec init profile ubuntu --chef-license accept
```

Run the audit command
----------

We will learn about custom matchers in Inspec, how we can use the correct resources for our control.

Let’s choose 1 control from CIS Ubuntu 18.04 Benchmark, you can download the PDF from here and refer the page no. 384 “Ensure permissions on /etc/ssh/sshd_config are configured “.

To find the file permission, we can use the stat command.

```
stat /etc/ssh/sshd_config
```
output
```
 File: /etc/ssh/sshd_config
  Size: 285             Blocks: 8          IO Block: 4096   regular file
Device: 400014h/4194324d        Inode: 4671949     Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2020-11-18 05:26:02.758704203 +0000
Modify: 2020-09-23 08:02:23.714054949 +0000
Change: 2020-11-18 05:26:01.858728725 +0000
 Birth: -
```
As we can see, we have 0644 as permission bits.

To ensure only root has read access to this crucial file (loose permissions on this file can lead to serious security attacks), we will change its permissions and ownership.

```
chown root:root /etc/ssh/sshd_config
chmod og-rwx /etc/ssh/sshd_config
```

We’ve learned about command and file resource in the previous exercises. What would be an appropriate resource to choose in this scenario?

It really demands on what you are trying to accomplish. Ideally you must explore both of them. In this example using command resource will make our tasks complicated so let’s use file resource. Let’s refresh our memory by reading [the file resource documentation](https://docs.chef.io/inspec/resources/file/#unixlinux-properties)

As part of the documentation, we notice there are a few interesting properties such as uid, gid.

Edit the profile
----------

Run the following command to replace the Inspec task at ubuntu/controls/example.rb.

```
cat > ubuntu/controls/example.rb <<EOL
control 'ubuntu-5.2.1' do
   title 'Ensure permissions on /etc/ssh/sshd_config are configured'
   desc 'The /etc/ssh/sshd_configfile contains configuration specifications for sshd. The command below checks whether the owner and group of the file is root.'
   describe file('/etc/ssh/sshd_config') do
     its('owner') { should eq 'root'}
     its('group') { should eq 'root'}
     its('mode') { should cmp '0600' }
   end
end
EOL
```
In the above task we are checking for three things.
1. Ensure the owner of the file is root.
2. Ensure this file belongs to the root group.
3. The mode/permissions are read-only for root.

Lets validate the profile to ensure there are no syntax errors.

```
inspec check ubuntu
```
Now run the profile on the local-machine before executing it against the remote server

```
inspec exec ubuntu
```
output
```
Profile: InSpec Profile (ubuntu)
Version: 0.1.0
Target:  local://

  ✔  ubuntu-5.2.1: Ensure permissions on /etc/ssh/sshd_config are configured
     ✔  File /etc/ssh/sshd_config owner is expected to eq "root"
     ✔  File /etc/ssh/sshd_config group is expected to eq "root"
     ✔  File /etc/ssh/sshd_config mode is expected to cmp == "0600"


Profile Summary: 1 successful control, 0 control failures, 0 controls skipped
Test Summary: 3 successful, 0 failures, 0 skipped
```

Perfect, we got 1 successful control as output i.e., our machine DevSecOps Box is following compliance requirement(s).

Run the Inspec profile against a remote server
----------

Let’s try to run the custom profile created by us against the remote server

```
echo "StrictHostKeyChecking no" >> ~/.ssh/config
inspec exec ubuntu -t ssh://root@prod-XqiHnDZ0 -i ~/.ssh/id_rsa --chef-license accept
```
output

```
Profile: InSpec Profile (ubuntu)
Version: 0.1.0
Target:  ssh://root@prod-XqiHnDZ0:22

  ×  ubuntu-5.2.1: Ensure permissions on /etc/ssh/sshd_config are configured (1 failed)
     ✔  File /etc/ssh/sshd_config owner is expected to eq "root"
     ✔  File /etc/ssh/sshd_config group is expected to eq "root"
     ×  File /etc/ssh/sshd_config mode is expected to cmp == "0600"
     
     expected: 0600
          got: 0666
     
     (compared using `cmp` matcher)



Profile Summary: 0 successful controls, 1 control failure, 0 controls skipped
Test Summary: 2 successful, 1 failure, 0 skipped
```
The flags/options used in the above commands are:

- -t : tells the target machine to run the profile against.
- -i : provides the path where the remote machine’s ssh key is stored.
- --chef-license : accept ensures that we are accepting license agreement there by preventing the inspec from prompting YES or NO question.

As expected, our production machine is not hardened yet, so we have 1 control failure.

What do we need to do to fix it? thats right, fix the issue on production aka harden the production environment.