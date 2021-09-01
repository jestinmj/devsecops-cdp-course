Basics of Running Commands
================================================================

We will learn the basics of running commands in linux
----------------------------------------------------------------

In this scenario, you will learn the basics of running commands in linux.

The information taught in this exercise are essential for our courses like DevSecOps Professional, DevSecOps Expert and Continuous Compliance.

Successful and Un-successful command runs
----------------------------------------------------------------

Let’s first run some simple commands that work with the file system to see how they behave.

1. Let’s start with simple directory listing

ls is the linux command that helps in listing files and directories.

```
ls
ls -l
ls -l abracadabra
```

2. Try creating a new directory, and review what happens

mkdir is the command used to make (or create) a new directory.

```
mkdir my-directory
```
After running the above command, there is no indication of whether the command ran successfully or not.

Since the mkdir command completed successfully by creating a directory named my-directory, there was no indication of a success message.

Now, try running the same mkdir command again, as below:

```
mkdir my-directory
```
output

```
mkdir: cannot create directory ‘my-directory’: File exists
```
This time however, because my-directory already exists, mkdir could not successfully create the directory, hence an error message is shown. Unsuccessful command execution in this case, resulted in an indication of an error.

Successful command execution did not indicate whether a directory was created or not.

3. Try removing a directory, and review what happens

rmdir is the command used to remove (or delete) a directory.

```
rmdir my-directory
```

After running the above command, there is no indication of whether the command ran successfully or not.

Since the rmdir command completed successfully by removing the directory named my-directory, there was no indication of a success message.

Now, try running the same rmdir command again, as below:

```
rmdir my-directory
```

output
```
rmdir: failed to remove 'my-directory': No such file or directory
```

This time however, because my-directory was already removed, rmdir could not successfully remove the directory, hence an error message is shown. Unsuccessful command execution in this case, resulted in an indication of an error.

Successful command execution did not indicate whether the directory was removed or not.

Blocking and non-blocking command runs
--------------------------------

Sometimes a command or a program might take more time to run, and when a command takes more time to run there may be no indication whether the command or program is running or not, for a brief period of time.

Let’s explore some examples.

1. Try a long running operation, Eg: Installing Ansible

In the below example, we will try installing ansible. For now, you do not have to understand pip3 or ansible. We are just trying to install a software named ansible using the command below:

```
pip3 install ansible==2.10.4 ansible-lint==4.3.7
```

Now, as the command runs, you can either wait till the command finishes, or you can ask the command to run in the background as a background process.

2. Try a long running operation in the background, Eg: Installing Ansible

Adding ampersand (&) symbol towards the end of a command instructs the operating system to run the desired command in the background. 

```
pip3 install ansible==2.10.4 ansible-lint==4.3.7 &
```
Just so you know there is also nohup, but we will let you explore it yourself [here](https://stackoverflow.com/questions/15595374/whats-the-difference-between-nohup-and-ampersand).


