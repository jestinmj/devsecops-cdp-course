# Troubleshooting SSH Issues
This section provides assistance in troubleshooting SSH connection issues.

> Note
> At this point in the course, you are most likely to embark on CI/CD exercises that involve creating variables and using SSH keys for authentication.
> This section is meant to assist you in troubleshooting any SSH connection issues that may arise during the setup.
> This section is not a tutorial about the working details of SSH and its setup. If you would like to know the process involved in setting up SSH connections using a public-private key pair, then you would have already come across an exercise titled Working With SSH.

# Introduction to SSH
Secure Shell (SSH) is a commonly used mechanism that is used for communication between two systems.

There is an intrinsic need to authenticate one system to another in order to establish trust. Establishing trust between systems requires credentials.

Credentials can be passwords, tokens, public-private key pairs, and many others.

When using SSH connections, a popular and arguably more secure choice for authentication is using SSH Keys.

# Error 1: Could Not Resolve Hostname or Host Not Found
If you get an SSH error that says could not resolve hostname, then it probably means your lab machine is not alive, or there are typos in your machine name, or your lab machine ID might have changed.
`ssh: Could not resolve hostname prod-xxxxxxxx: Temporary failure in name resolution`

> What can you do to fix?
> 1. Try and ping the machine you are trying to connect to, if you get a ping response, then your machine exists and is alive.

# Error 2: Invalid Key Format
When using a public-private key pair for authentication, you need to share your private key with a remote server to authenticate the connection.

Private keys are typically stored in the ~/.ssh/ directory.

For example, private keys generated using the RSA algorithm are stored in the file ~/.ssh/id_rsa.

The private key file has a specific format.

The private key begins with -----BEGIN RSA PRIVATE KEY-----, followed by the contents of the private key, and ends with -----END RSA PRIVATE KEY-----.

When sharing private keys for authentication, it is essential to share the entire contents of the ~/.ssh/id_rsa file, including the -----BEGIN RSA PRIVATE KEY----- and -----END RSA PRIVATE KEY----- lines.

Invalid Key Format error occurs when:

- The private key passed is either empty
- The private key misses the -----BEGIN RSA PRIVATE KEY----- and -----END RSA PRIVATE KEY----- section
- The private key contains additional characters that may be typos, or characters that are not a part of the original private key

![image](https://github.com/user-attachments/assets/978c15f4-8151-45f6-981c-3cd6edab2039)

![Uploading image.png…]()
