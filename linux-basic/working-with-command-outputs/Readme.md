Basics of Command Outputs
================================


We will learn how to redirect, store, filter, and process output from a command
----------

In this scenario, you will learn how to redirect, store, filter, and process command outputs in Linux.

The information taught in this exercise are essential for our courses like DevSecOps Professional, DevSecOps Expert and Continuous Compliance.


Output Redirection
----------

Linux allows you to save the output of a command to a file or send it to another command for further processing. It does it by using redirection.

```
cat /etc/passwd > mypasswd.txt
```

In the above command, we are reading a file located at /etc/passwd using the cat command, and saving the output (the entire content of /etc/passwd) into a new file (as instructed by the > symbol) called mypasswd.txt.

You can verify the content of the newly created mypasswd.txt file by using the following command.

```
cat mypasswd.txt
```

You can also append to an existing file using >> characters. If you want to append the content of the /etc/passwd file to the mypasswd.txt file, you can use the following command.

```
cat /etc/passwd >> mypasswd.txt
```

Let’s verify if the contents are appended, not overwritten using the cat command.

```
cat mypasswd.txt
```

Similarly, there is a handy echo command to look at the contents of variables, or create smaller files using the echo command.

```
echo "this is a string"
```

We can see the contents of the pre-defined variable called HOSTNAME using the echo command.

```
echo $HOSTNAME
echo "this is a string" > file.txt
cat file.txt
```

Piping the Output
----------

In piping, you take a command’s output and send it to another command for further processing.

Lets take an example of mypasswd.txt file that we created in the previous step, and parse the contents of the file using cat and cut command to extract the usernames.

```
cat mypasswd.txt
```

If you wish to extract only usernames from the above output, you can use the cut command with delimiter as colon (:).

```
cat mypasswd.txt | cut -d ':' -f 1
```

Behind the scenes, the cat command’s output was sent to the cut command as an input, and it used -d (delimiter) flag with a colon as a separator/delimiter and -f (field) option to get the 1st field.

> More info is available at https://opensource.com/article/18/8/introduction-pipes-linux.

Another common usage of pipe is to to search for a given string in a command output.

For example, as indicated below, we can get a list of running processes using the ps command, and send it to the grep command to identify a particular process (bash process in this case). 

```
ps -aux | grep bash
```

