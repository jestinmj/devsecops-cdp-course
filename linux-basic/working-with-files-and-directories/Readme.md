Basics of Files and Directories
=======================

We will learn the basics of working with files and directories in linux
---------

In this scenario, you will learn the basics of working with files and directories in linux.

The information taught in this exercise are essential for our courses like DevSecOps Professional, DevSecOps Expert and Continuous Compliance.


Understanding Directories
----------

Directories are an underlying file system object. The term Folder can also be interchangeably used to mean a directory, although there might be trivial semantic differences between both the terms.

As we reviewed in some of the previous exercises, if you wish to create a directory, you can use the mkdir command.

```
mkdir new-directory
ls new-directory
pwd
```

Let’s try changing the present working directory.

You can change the present working directory using the cd command.

```
cd new-directory
```

In case the directory name is not visible on the command line, you can check it using the pwd command.

You can go back to the previous directory (or more appropriately the parent directory) by using the cd command with ..

```
cd ..
```
You can remove a directory with the rmdir command.

```
rmdir new-directory
```

Understanding Files
---------

Everything is a file in Linux, text files, configurations, services, etc., However, Linux is so powerful there are many ways of doing the exact same operation.

If you wish to create a file, you can use any text editor of your choice. We will use nano and cat in this exercise.

```
nano myfile
```
Once you are in the editor, add some text and save the file using control + O (letter o) and hit Enter or the return.

You can exit the editor using control + X

If a file exists already, you can explore the contents of a file using the nano utility.

Or you can also use the cat command (remember multiple ways of doing the exact same thing?).
cat command reads the content of a given file and displays as output.

```
cat myfile
```
If you wish to rename a file, you can use the mv (move) command.
```
mv myfile newfile
```

Here Documents
---------

The cat command is mostly used to read a file; however, using a command line magic (read as command line hack), we can even create a file in a non-interactive way (ideal for CI/CD systems).

```
cat > filename <<EOL

Some text content
Some text content 2
Some text content 3

EOL
```

There are three parts to this command.

1. The filename, here its filename
2. The here document, the << symbols are a special code block. It allows you to redirect anything between EOL into a command
3. The cat command, if it’s followed by >, allows you to create a file


> More info is available at https://www.cyberciti.biz/faq/save-file-in-linux-using-cat-command/
>
> Do not forget to try an ls to view the new file, and a cat filename to review the contents of the file.

