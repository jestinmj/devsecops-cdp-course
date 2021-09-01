Basics of File Permissions
================================

We will learn the basics of working with file permissions and running commands as different users
---------

In this scenario, you will learn the basics of file permissions and running commands as different users in Linux.

The information taught in this exercise are essential for our courses like DevSecOps Professional, DevSecOps Expert and Continuous Compliance.


Understanding File Permissions
----------

The permissions of a file or a directory could be reviewed using the ls -l or the stat command. You can provide executable permissions to a file using the chmod command.

Let’s create a file called myfile using the cat command.

```
cat > myfile <<EOL
ls
EOL
```

As you can see, we are creating a file called myfile, and its contents would be ls. We can verify its content by using the cat command.

```
cat myfile
ls -l myfile
stat myfile
chmod +x myfile
```

> More info about chmod is available at https://linuxize.com/post/chmod-command-in-linux/.


Running Commands as Different Users
--------------

> The sudo command allows you to run programs and utilities as another user (by default, as the superuser). An administrator can give temporary or permanent permission to escalate permissions using the sudoers file. This feature helps administrators to delegate some of the permissions without sharing the root password.


You can use the following sudo command to run a command with root privileges.

Since we are already the root user, you wouldn’t notice any significant differences. Let’s create a user called john.

```
echo -e "pdevsecops\npdevsecops" | adduser --gecos "" john
```

> What is –gecos? Read (here)[https://en.wikipedia.org/wiki/Gecos_field]


We can use the usermod command to add the user to the sudo group.

```
usermod -aG sudo john
sudo su - john
```

Now, try reading the content of a very sensitive file on Linux, i.e., /etc/shadow.

```
cat /etc/shadow
```
Permission denied. Even though we are logged in as john we still have to explicitly specify sudo before the actual command to try performing an operation as a high privileged user.

So let’s try reading the content of /etc/shadow again, but this time with sudo prefix.

```
sudo cat /etc/shadow
```
The password for this user is pdevsecops. You need to type the password.

output
```
root:*:18526:0:99999:7:::
daemon:*:18526:0:99999:7:::
bin:*:18526:0:99999:7:::
sys:*:18526:0:99999:7:::
sync:*:18526:0:99999:7:::
games:*:18526:0:99999:7:::
man:*:18526:0:99999:7:::
lp:*:18526:0:99999:7:::
mail:*:18526:0:99999:7:::
news:*:18526:0:99999:7:::
uucp:*:18526:0:99999:7:::
proxy:*:18526:0:99999:7:::
www-data:*:18526:0:99999:7:::
backup:*:18526:0:99999:7:::
list:*:18526:0:99999:7:::
irc:*:18526:0:99999:7:::
gnats:*:18526:0:99999:7:::
nobody:*:18526:0:99999:7:::
_apt:*:18526:0:99999:7:::
sshd:*:18739:0:99999:7:::
john:$6$hJz8BHbB$WkIBAYHTABpbnwBfFWk6nwJHhEzoGjq4Big3ciZw1NtIMEp3lUMdm8NOUKTrG8fgzQI/WzNRtd3FB88ODoIJw/:18759:0:99999:7:::
```

As you can see, sudo is a compelling feature of Linux.

Let’s exit from this user’s shell and go back to being root using the exit command.

> Do not forget to read about Permission Groups and Types (here)[https://www.linux.com/training-tutorials/understanding-linux-file-permissions/]

