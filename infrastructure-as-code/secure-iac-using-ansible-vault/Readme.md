Secure IaC using Ansible Vault
=======================

Learn how to use Ansible Vault to do secure IaC
---------

In this scenario, you will learn how to use Ansible to do secure IaC.

You will learn how to use ansible-vault to encrypt your secrets when provisioning the infrastructure.

Install Ansible and Ansible Vault
---------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to install the ansible, ansible-vault is installed by default when you install ansible.

```
pip3 install ansible==2.10.4
```

Create the inventory file
----------

Let’s create the inventory or CMDB file for Ansible using the following command.

```
cat > inventory.ini <<EOL

# DevSecOps Studio Inventory
[devsecops]
devsecops-box-XqiHnDZ0

[prod]
prod-XqiHnDZ0

EOL
```

Next, we will have to ensure the SSH’s yes/no prompt is not shown while running the ansible commands so we will be using ssh-keyscan to capture the key signatures beforehand.

```
ssh-keyscan -t rsa prod-XqiHnDZ0 devsecops-box-XqiHnDZ0 >> ~/.ssh/known_hosts
```
Run the ansible commands
----------

Let’s run the ansible ad-hoc command to check the production machine’s uptime. We can use the uptime command to find the uptime.

```
ansible -i inventory.ini prod -m shell -a "uptime"
```

For example, if we want to copy a file into the production machine.

```
echo "hello" > example
ansible -i inventory.ini prod -m copy -a "src=example dest=/opt/example"
```

Let’s check the file is copied to the production machine.

```
ssh root@prod-XqiHnDZ0
cat /opt/example
exit
```

In the next step, you will learn how to send the file securely with ansible-vault.

Encrypted Data with Ansible Vault
---------

Ansible provides the ability to store secrets securely using Ansible Vault. Ansible can even send this file securely over the network using secure mechanisms like SSH and AES. For example, securely send a file containing a password over the network.

```
echo "StrongP@ssw0rd" > /secret
ansible-vault encrypt /secret --ask-vault-pass
```

You can use the following password as your password or anything you desire but ensure you remember this password as its needed when running ansible-playbook command.

> Password: C0mpl3xp@sswOrd

output

```
New Vault password: 
Confirm New Vault password: 
Encryption successful
```

The above command encrypts the file using the AES algorithm, we can verify it by using the cat command.

```
cat /secret
```

No one but folks who know the ansible vault’s password can edit or view the file. Ansible provides an easy way to provide this password when the encrypted files need to be decrypted. This option/flag is called --ask-vault-pass.

```
ansible -i inventory.ini prod --ask-vault-pass -m copy -a "src=/secret dest=/opt/secret"
```
Remember the decryption password for this file is `C0mpl3xp@sswOrd`.

Let’s SSH into our production machine.
```
ssh root@prod-XqiHnDZ0 "cat /opt/secret"
```
As you can see, the file was transferred to the remote machine after Ansible Vault decrypted the file.