Linux Exit Code
=======================

We will learn how to work with exit code
--------------

In this scenario, you will learn how to work with exit code that are essential for our other courses like DevSecOps Professional, DevSecOps Expert and Continuous Compliance.


Exit code basics
----------

A program or a script that completed its execution indicates whether it executed successfully or unsuccessfully through what is called an exit code.

Conventionally an exit code 0 denotes a program’s successful execution; A non-zero exit code denotes an unsuccessful execution of a program.

The exit code returned by a program could be obtained through echo $?

When CI/CD systems such as GitLab execute a certain command, after the command completes its execution, the CI/CD system checks the exit code of the last executed command to indicate whether the build job executed successfully or not.

Try a simple directory listing of the current directory and review the exit code
----------

```
ls
----------
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
----------
echo $?
-------
0
```

Apparently, after running ls where the directory listing was successful, the exit code is 0 (zero)

Try listing a directory that does not exist and review the exit code
----------

```
ls non-existent-dir
-------
ls: cannot access 'non-existent-dir': No such file or directory
-------
echo $?
-------
2
```
Since the directory non-existent-dir did not exist, the ls command was unsuccessful in listing the directory contents.

Hence, a non-zero exist code is returned. 2 is definitely non-zero.

Let’s go ahead and try some other commands, and see how they behave. 

Try removing a file and review the exit code
--------------

Before we remove a file, let’s create a new with the touch command.

```
touch newfile
```
A file named newfile would have been created for us. To verify, try an ls.
Now, let’s remove the newfile and review the exit code.

```
rm newfile
echo $?
-------
0
```
Since the remove operation using rm newfile succeeded, an exit code of 0 (zero) was returned indicating a successful program/command execution.

Try running the remove file command again.

```
rm newfile
-------
rm: cannot remove 'newfile': No such file or directory
----
echo $?
-------
1
```
Since the newfile was removed previously, the rm command could not successfully remove the newfile because the newfile simply did not exist in the file system.

Hence, an exit code of 1 is returned indicating an unsuccessful operation. 1 is definitely non-zero.

Try a command that does not exist and review the exit code
----------

Try typing gibberish and hit Enter/Return.

```
gibberish
---------
bash: gibberish: command not found
-------
echo $?
-------
127
```

Since the gibberish command did not exist bash could not execute it successfully.

Hence, an exit code of 127 is returned indicating a unsuccessful program/command execution. Again, 127 is definitely non-zero.

Recap
---------

In all the above scenarios, if there was one thing that was common, it was:

1. Zero meant success
2. Non-Zero meant failure

Some commands chose to exit with 1 indicating an unsuccessful execution or failure.
Some commands chose to exit with 2 indicating an unsuccessful execution or failure.
Some commands chose to exit with 127 indicating an unsuccessful execution or failure.

Some common conventions of exit-codes are documented here - https://tldp.org/LDP/abs/html/exitcodes.html

Exit code advanced
----------

In the context of security tooling, unsuccessful execution generally means that the security tool found vulnerabilities.

In many cases, a mature security tool would return an exit code of zero indicating that the tool found no vulnerabilities. A mature security tool would return a non zero exit code indicating that the tool found one or more security vulnerabilities.

> Note
>
> Developers of a security tool are liberal in choosing to return non-zero exit codes. That is, when a vulnerability is found, some security tools return an exit code of 13, some security tools return an exit code of 255, some security tools return an exit code of 1. In all cases, 13, 255, and 1 are non-zero exit codes indicating the presence of a vulnerability.


On the other hand, some security tools however choose to simply return zero as an exit code irrespective of whether it found vulnerabilities or not. From an automation, and DevSecOps tooling perspective, these security tools need to be improved, or we might be required to write custom scripts to check the security tool’s output to decide what exit code needs to be returned.

Let’s try to mock a security tool to understand how a tool’s developer might choose to return non-zero exit codes. 

Writing an simple exit code logic
-----------

The below example is purely fictional, and it is intended to mock how a security tooling might choose a return a non-zero exit code. 

> Note
>
> The best way to understand an exit code returned by a certain tool is to read the tool’s documentation. 

The fake security tool below written as a bash script simulates the number of vulnerabilities using a random number.

1. If the vulnerability count is zero, the tool returns an exit code of zero, indicating success.
2. If the vulnerability count is not zero, then the tool returns an exit code of 99, that is a non-zero exit code, indicating failure.

> Why choose 99 as an exit code? Rather conventional, it simply is a matter of the developer’s choice.

Create the myfaketool as below:

```
cat > myfaketool << EOL
#!/bin/bash
vulncount=\$((0 + \$RANDOM % 3)); #randomly fake vulnerability count
if [ \$vulncount -eq 0 ];
then
        echo "No Vulnerabilities";
        exit 0
else
        echo "Vulnerabilities found: \$vulncount";
        exit 99
fi
EOL
```
Provide executable file permissions for myfaketool.
```
chmod +x myfaketool
./myfaketool
-------
Vulnerabilities found: 1
----
echo $?
------
99
```

Since vulnerabilities were found, a non-zero exit code is returned.

Let’s run the myfaketool a few more times, and review the exit code

```
./myfaketool
-----
No Vulnerabilities
---------
echo $?
------
0
```
When the myfaketool finds no vulnerabilities, it returns an exit code 0 indicating success.

Recap
---------

Now, that’s a wrap. Here are a few key points to remember:

1. Zero exit code indicates a success
2. Non-Zero exit code indicates a failure
3. In the context of most security tooling, zero exit code means no vulnerabilities found, non-zero exit code means vulnerabilities found
4. Non-Zero exit code can either be 1, or 13, or 99, or 255, or just any integer that is not a zero

As you progress through the later exercises, you will learn how CI/CD systems such as GitLab interpret a job’s exit code to determine whether the build job succeeded or failed.
