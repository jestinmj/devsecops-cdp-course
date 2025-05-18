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
```
usage: bandit [-h] [-r] [-a {file,vuln}] [-n CONTEXT_LINES] [-c CONFIG_FILE] [-p PROFILE] [-t TESTS] [-s SKIPS]
              [-l | --severity-level {all,low,medium,high}] [-i | --confidence-level {all,low,medium,high}]
              [-f {csv,custom,html,json,screen,txt,xml,yaml}] [--msg-template MSG_TEMPLATE] [-o [OUTPUT_FILE]] [-v]
              [-d] [-q] [--ignore-nosec] [-x EXCLUDED_PATHS] [-b BASELINE] [--ini INI_PATH] [--exit-zero] [--version]
              [targets [targets ...]]

Bandit - a Python source code security analyzer

positional arguments:
  targets               source file(s) or directory(s) to be tested

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       find and process files in subdirectories
  -a {file,vuln}, --aggregate {file,vuln}
                        aggregate output by vulnerability (default) or by filename
  -n CONTEXT_LINES, --number CONTEXT_LINES
                        maximum number of code lines to output for each issue
  -c CONFIG_FILE, --configfile CONFIG_FILE
                        optional config file to use for selecting plugins and overriding defaults
  -p PROFILE, --profile PROFILE
                        profile to use (defaults to executing all tests)
  -t TESTS, --tests TESTS
                        comma-separated list of test IDs to run
  -s SKIPS, --skip SKIPS
                        comma-separated list of test IDs to skip
  -l, --level           report only issues of a given severity level or higher (-l for LOW, -ll for MEDIUM, -lll for
                        HIGH)
  --severity-level {all,low,medium,high}
                        report only issues of a given severity level or higher. "all" and "low" are likely to produce
                        the same results, but it is possible for rules to be undefined which will not be listed in
                        "low".
  -i, --confidence      report only issues of a given confidence level or higher (-i for LOW, -ii for MEDIUM, -iii for
                        HIGH)
  --confidence-level {all,low,medium,high}
                        report only issues of a given confidence level or higher. "all" and "low" are likely to
                        produce the same results, but it is possible for rules to be undefined which will not be
                        listed in "low".
  -f {csv,custom,html,json,screen,txt,xml,yaml}, --format {csv,custom,html,json,screen,txt,xml,yaml}
                        specify output format
  --msg-template MSG_TEMPLATE
                        specify output message template (only usable with --format custom), see CUSTOM FORMAT section
                        for list of available values
  -o [OUTPUT_FILE], --output [OUTPUT_FILE]
                        write report to filename
  -v, --verbose         output extra information like excluded and included files
  -d, --debug           turn on debug mode
  -q, --quiet, --silent
                        only show output in the case of an error
  --ignore-nosec        do not skip lines with # nosec comments
  -x EXCLUDED_PATHS, --exclude EXCLUDED_PATHS
                        comma-separated list of paths (glob patterns supported) to exclude from scan (note that these
                        are in addition to the excluded paths provided in the config file) (default:
                        .svn,CVS,.bzr,.hg,.git,__pycache__,.tox,.eggs,*.egg)
  -b BASELINE, --baseline BASELINE
                        path of a baseline report to compare against (only JSON-formatted files are accepted)
  --ini INI_PATH        path to a .bandit file that supplies command line arguments
  --exit-zero           exit with 0, even with results found
  --version             show program's version number and exit

...[SNIP]...
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

# Filtering Vulnerabilities by Severity Level
In the previous step, we learned how to run Bandit and, based on the information provided in the bandit –help command, we can filter vulnerabilities by their severity levels. Bandit categorizes vulnerabilities into multiple severity levels: LOW, MEDIUM, and HIGH. You can customize your scan to target specific severity levels. Here are some examples:

To filter, you can use this command:
<br>`bandit -r <path_to_code> -l`

However, since we are already in the directory, you can use a dot (“.”) instead.

To filter for low-level vulnerabilities:<br>
`bandit -r . -l`

This command filters vulnerabilities with a severity level from low to high.
![image](https://github.com/user-attachments/assets/90da94a8-7877-444c-99ea-735833a4a1a6)

To filter for medium-level vulnerabilities:<br>
`bandit -r . -ll`

This command filters vulnerabilities with a severity level from medium to high.
![image](https://github.com/user-attachments/assets/bdd7af22-6b94-4e13-ae68-68e61ea1c001)

To filter for high-level vulnerabilities:<br>
`bandit -r . -lll`

![image](https://github.com/user-attachments/assets/5b36d210-5225-4a26-ac0d-91ce058e2391)

By specifying the number of l, you can filter vulnerabilities of the desired severity level and higher. This is useful for customizing your security analysis based on your project’s requirements.

With these additional steps, you’ll have a better understanding of Bandit’s exit codes and how to filter vulnerabilities by severity level when running the tool. This knowledge will help you make informed decisions and automate security checks in your CI/CD pipeline.

# Understanding Bandit Exit Codes
It’s crucial to grasp how Bandit’s exit codes function and what they signify. These exit codes play a significant role in automating security checks within your CI/CD pipeline and making informed decisions about the results. You can refer to this understanding in the linked exercise, Introduction to Exit Codes(https://portal.practical-devsecops.training/courses/devsecops-professional/introduction-to-the-tools-of-the-trade/learn-to-work-with-exit-code), to enhance your knowledge further.

![image](https://github.com/user-attachments/assets/ca89f938-f84b-4178-8300-578262610bd2)

Understanding these exit codes is crucial for the exercise mentioned in Introduction to Exit Codes. It will help you effectively integrate Bandit into your CI/CD pipeline and make informed decisions based on the scan results.
https://portal.practical-devsecops.training/courses/devsecops-professional/introduction-to-the-tools-of-the-trade/learn-to-work-with-exit-code

In the next exercise, we will explore how to Embed Bandit to the CI/CD pipeline.
