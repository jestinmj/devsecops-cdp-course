Run SAST Scans
--------------

Learn how to run static analysis scans on the code
------------------------------------------------

In this scenario, you will learn how to install and run SAST Scans on a git repository.

You will need to download the code, install the SAST tool called Bandit and then finally run the SAST scan on the code.

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.
First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp

cd webapp
```
Install SAST Tool
----------

> The Bandit is a tool designed to find common security issues in Python code.
> 
> To do this Bandit, processes each file, builds an AST, and runs appropriate plugins against the AST nodes. Once Bandit has finished scanning all the files it generates a report.
> 
> Bandit was originally developed within the OpenStack Security Project and later rehomed to PyCQA.
> 
> You can find more details about the project at https://github.com/PyCQA/bandit.

Let’s install the bandit scanner on the system to perform static analysis.

```
pip3 install bandit
```
We have successfully installed Bandit scanner. Let’s explore the functionality it provides us.

```
bandit --help
```

Run the scanner
----------

As we have learned in DevSecOps Gospel, we would like to store the content in a JSON file. We are using the tee command here to show the output and store it in a file simultaneously.

```
bandit -r . -f json | tee bandit-output.json
```

Bandit ran successfully, and it found three security issues.
1. Two medium severity issues
2. One high severity issue

In the next exercise, we will explore how to Embed Bandit to the CI/CD pipeline.