SSH Basics
================================================================


We will learn the basics of SSH to interact with remote systems
---------

In this scenario, you will learn how to work with SSH to interact with remote systems.

The information taught in this exercise is essential for our courses like DevSecOps Professional, DevSecOps Expert and Continuous Compliance.

Getting Started with SSH
----------

> Secure Shell (SSH) allows you to login into remote machines for administration, run commands remotely, deploy applications, upload/download files and automate system administration tasks.

Let’s explore the remote administration ability of SSH.

Assuming the necessary keys are set up already for connection (explained in the next step), you can log into a remote machine using the following command

```
ssh -i ~/.ssh/id_rsa root@prod-XqiHnDZ0
```

- -i allows us to specify the private key to use to login into a remote machine
- root is a user we want to login as
- prod-XqiHnDZ0 is the hostname of the server

> This key fingerprint is there to ensure you cross-check the signature of the remote machine, which ensures that you are connecting to a machine that you actually intended to connect to.
> 
> However, it’s a blocker if we want to run automated commands. We can avoid the host authenticity check using the following command by explicitly adding (whitelisting) the target host’s fingerprint to a list of known hosts in the ~/.ssh/known_hosts file.

```
ssh-keyscan -t rsa prod-XqiHnDZ0 >> ~/.ssh/known_hosts
```

If you had provided yes for the ssh authenticity warning, the ssh command would have logged us in the production system. We can use the hostname command to verify we are in the remote machine.

```
hostname
exit
```

Run commands remotely
----------

You can use ssh to run commands remotely on the remote machine.

```
ssh root@prod-XqiHnDZ0 "hostname"
```
Anything in quotes is run on the remote machine. The remote machine in the above example is prod-XqiHnDZ0

As you can see, the above command hostname ran on the production machine, and we got the production’s hostname instead of the devsecops-box’s hostname.

Learning to Set Up SSH (Review Only)
--------------------------------

> This step is only for review, and not intended to be practiced in the lab environment.
>
> Practicing these steps might result in loosing connections to the lab infrastructure. Proceed at own risk. In case of problems, refresh the browser and hit Start the exercise button.

SSH enables password-less logins using public-private key pairs.

Public-private key pairs are located in the ~/.ssh/ directory.

The ssh server should be configured to allow password-less login, which can be done by un-commenting or adding the following two lines to the ssh configuration file (/etc/ssh/sshd_conf).

```
RSAAuthentication yes
PubKeyAuthentication yes
```
After a configuration change of the ssh server, a restart is required.
```
/etc/init.d/sshd restart
```
If there are no key pairs that exist, or if this is the first time you are setting up ssh keys, you need to generate new pair of public-private keys (with RSA algorithm) with the command below:
```
ssh-keygen -t rsa
```
You will be prompted to provide a location and a passphrase for the public-private key pair.
If you go with the default options, the private key will be stored at ~/.ssh/id_rsa, and the public key will be stored at ~/.ssh/id_rsa.pub.

Now that we have a public-private key pair, we need to configure the remote machine to allow the connection.

The remote machine needs to know the public key from where the connection is originating from. Since we have generated the public key at ~/.ssh/id_rsa.pub let’s use the ssh-copy-id command as below to let the remote machine allow connections.

```
ssh-copy-id -i ~/.ssh/id_rsa.pub user@targetserver
```

The above command will prompt you to provide a password for the user named user in order to complete authentication.

After authentication, the ssh-copy-id command will read the public key from ~/.ssh/id_rsa.pub and adds the public key to ~/.ssh/authorized_keys on the targetserver.

That’s all there is to set up ssh. As explained in the previous step, you can login to the remote server and perform the desired operations.

Recap
---------
Here are a few key points to remember:

1. sshd server needs to be configured to allow ssh
2. ssh-keygen generates a new public-private key pair for authentication
3. private key is never shared with anyone, it is only used during authentication
4. public key needs to exported to ~/.ssh/authorized_keys on a server to which we need to connect to
5. ssh-copy-id helps in copying public keys to the authorized_keys file
