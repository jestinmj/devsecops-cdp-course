Use Talisman to prevent secrets from getting checked in
================================================================

A tool to detect and prevent secrets from getting checked in
--------------------------------------------------------

In this scenario, you will learn how to install and run the talisman tool.

This tool will help you in avoiding DevOps teams accidentally commiting secrets to the git repositories.

To achieve the above objectives, you will need to do the following.

1. Install the git pre-commit and pre-push hook tool.
2. Clone/download the source code.
3. Configure the pre-commit/pre-push tool on a repo.
4. Test to ensure the utility works fine.

Install Talisman
----------

> Talisman is a tool that installs a hook to your repository to ensure that potential secrets or sensitive information do not leave the developer’s workstation.
>
>  It validates the outgoing changeset for things that look suspicious - such as potential SSH keys, authorization tokens, private keys, etc.
> 
> Source: [Talisman Repoistory.]()

This tool looks great, however it is far from perfect.

Here’s why.


1. Pre-commit/Pre-push hooks are configured only on a developer’s workstation.
2. If a developer has administrator access, he/she can easily disable these checks.
3. There’s no way to enforce it across the organization.

Please prefer to use secrets scanning tools as part of the CI/CD pipeline because of the above reasons. Embedding secret scanning tools provide the best of both worlds, i.e., enforcement and visibility.

We will do all the exercises locally in DevSecOps-Box, and before installing the tool, we need to understand what is a **git hook**.

> Git hooks are scripts that run before or after git events like commit, push, rebase, etc., and are run locally. You can see a list of git hooks [here](https://github.com/git/git/tree/master/templates).


There are two types of git hooks supported by Talisman.
1. pre-commit
2. pre-push

In this exercise, we will use **pre-commit hook** to prevent our developers from adding a sensitive file to our git repository.

You can install Talisman with the pre-commit hook, using the following command.

```
curl --silent https://raw.githubusercontent.com/thoughtworks/talisman/master/global_install_scripts/install.bash > /tmp/install_talisman.bash && /bin/bash /tmp/install_talisman.bash pre-commit
```

Or you can add pre-push as an argument to use the pre-push hook.

```
curl --silent https://raw.githubusercontent.com/thoughtworks/talisman/master/global_install_scripts/install.bash > /tmp/install_talisman.bash && /bin/bash /tmp/install_talisman.bash pre-push
```

output

```
Downloading talisman binary
talisman_linux_amd64: OK


Setting up talisman binary and helper script in /root/.talisman
Setting up TALISMAN_HOME in path


PLEASE CHOOSE WHERE YOU WISH TO SET TALISMAN_HOME VARIABLE AND talisman binary PATH (Enter option number):
1) Set TALISMAN_HOME in ~/.bashrc
2) Set TALISMAN_HOME in ~/.bash_profile
3) Set TALISMAN_HOME in ~/.profile
4) I will set it later
#? 1


Setting up interaction mode

DO YOU WANT TO BE PROMPTED WHEN ADDING EXCEPTIONS TO .talismanrc FILE?
Enter y to install in interactive mode. Press any key to continue without interactive mode (y/n):m
Setting up TALISMAN_HOME in /root/.bashrc
After the installation is complete, you will need to manually restart the terminal or source /root/.bashrc file
Press any key to continue ...
Setting up pre-commit hook in git template directory
No git template directory is configured. Let's add one.
(this will override any system git templates and modify your git config file)

Git template directory: (/root/.git-template)

Setting up template pre-commit hook
'/root/.git-template/hooks/pre-commit' -> '/root/.talisman/bin/talisman_hook_script'
Talisman template hook successfully installed.

Setting up talisman hook recursively in git repos
Please enter root directory to search for git repos (Default: /root):
        Searching /root for git repositories
```

We have successfully installed the Talisman tool globally in our DevSecOps Box, so if there is any new repository that we clone or init, it will use Talisman as git hooks.

Download the source code
----------

Next, let’s clone our code from Gitlab.
```
git clone https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training/root/django-nv.git webapp

cd webapp
```

We are now in the webapp directory.

To see Talisman in action, we will try to add a sensitive file to this repository.

Let’s copy SSH Private Key into the current directory.
```
cp ~/.ssh/id_rsa .
git add id_rsa
git commit -m "Add private key"
```

Once done, you can re-execute the git commit command to see Talisman preventing us from committing the Private SSH key.

output 

```
/webapp# git commit -m "Add private key"
Talisman Scan: 3 / 3 <-----------------------------------------------------------------------------------> 100.00%  

Talisman Report:
+--------+------------------------------------------------------------------+----------+
|  FILE  |                              ERRORS                              | SEVERITY |
+--------+------------------------------------------------------------------+----------+
| id_rsa | The file name "id_rsa" failed                                    | high     |
|        | checks against the pattern                                       |          |
|        | ^.+_rsa$                                                         |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | MIIEpAIBAAKCAQEAwNpZcFqfOVT0Q486JHr7kQO7HGD2zsG...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | OUM633CIM0UYSqRTaOIRAi+HowZ5W0/8ZKW3okMQTQNjjY7...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | dAimRGlgm1ycE/ucKXShiH9iSSeIrtkUiHWxvRssxSjdT0l...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | CDoeSXRM+EtFBkc45Mbyc7VCIyYcW2gUmFCLr8js/vUuGJY...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | 5tHjKd+qNCs0HhytWbhVWDwl46uigIrvwk6gaQXgVv1djrP...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | DrPZspBia9bxShKbL+zGcyoVgAy/yvdM3peI6QIDAQABAoI...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | xY+UYXxa7OH3yChUWClXATpiKHtbzo7CTpSBcbK1WOaIYQ2...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | fzBNpKpU5I3A6rjH2AHoId2iDAvuEBaJIUeN6ijhJeMQgxJ...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | TmLJDpMl9YdoCQ8rYJ6ccP5DKu7hF9fQA/8V5/OAkj2XKjQ...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | zw/P5DnRTzKQPG58u2TMb8cPKmi9MAJUAeFd1k2uBxBWXdI...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | iYsNQtDRiVLDu1+CJ5ddo8IEFBRJVk8xUD9vjAocplINgc9...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | wv2ZJG1RAoGBAP4tdWTj2ds7TS4yBoOGLHdXDIPHHBHV8g7...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | tHR5ykp7o2OqSH+sVDzK4tGy50dWZzw+m4lR3714C4BWx89...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | OPAykJtrKBYPJZ3Lan90HnVkU5MD4blmRrdHFrq6idYaDXC...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | VGw9C1iDPz1PcLOmV3uVpNJFLud0gSaTtUyouGJPbauvwcn...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | 700OvMDH/YUCE5YB0VtZ0y/55s/qGEp8LRzYFUUxHB38Yne...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | 2veoxdT4FO/U6Stg0aLXQxakyFj7AcDKl1WcCzh9AoGAEHu...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | zAlvHFSbM2Tmb6PbAhcKlHavCgVeLvPri+oh/jaKX/o4/V6...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | ndQbaFQSmt4F0yHIUIGsP0gjzFc8gen+cUU2L34BeXy9+b+...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | ro4DoVRbf/DskjGXUzWNblkCgYAMWBMxccu3y1eIiPTrpeW...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | KaPWM6APqjLRpeb+EGgCQQTtQpqFwnZa2lXqlospGdGu1dy...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | 8uGfLRjRWwnS+q+erFI1lVp0HT1Mpu+Fj8dK2p1SBKDw7c1...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | ySD5bQKBgQDJt2QT2oxFP/UYU1OQO1Vu38U82Yw5F7XCFE5...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | sCXOqlg8u/Hat/tsAI4WNjyjXSLLdCvF85d6Sx2/pbPMfNB...               |          |
+--------+------------------------------------------------------------------+----------+
| id_rsa | Expected file to not to contain                                  | high     |
|        | base64 encoded texts such as:                                    |          |
|        | 1PSx8Bw50vWJVZFlHSC0thG7psyrflbOoLBKdwfvBkrfSrp...               |          |
+--------+------------------------------------------------------------------+----------+
            | high     |ret pattern : BEGIN RSA PRIVATE KEY-----
 |          |IEpAIBAAKCAQEAwNpZcFqfOVT0Q486JHr7kQO7HGD2zsGC4iodBxc6bdU/S1zn
|        | OUM633CIM0UYSqRTaOIRAi+HowZ5W                                    |          |
                              |          |PEi2
 |          |imRGlgm1ycE/ucKXShiH9iSSeIrtkUiHWxvRssxSjdT0lGhB/z7PN2hu0mpj2k
 |          |oeSXRM+EtFBkc45Mbyc7VCIyYcW2gUmFCLr8js/vUuGJYu/FQp8yZDvVg8+bBx
 |          |HjKd+qNCs0HhytWbhVWDwl46uigIrvwk6gaQXgVv1djrPNh9eYYLoXSwTfo//c
 |          |PZspBia9bxShKbL+zGcyoVgAy/yvdM3peI6QIDAQABAoIBAQCubpCJFB6CT7nj
 |          |+UYXxa7OH3yChUWClXATpiKHtbzo7CTpSBcbK1WOaIYQ2YrcsXyaoSrQTkyr1H
 |          |BNpKpU5I3A6rjH2AHoId2iDAvuEBaJIUeN6ijhJeMQgxJU7LaRtIFKodU3T7/M
 |          |LJDpMl9YdoCQ8rYJ6ccP5DKu7hF9fQA/8V5/OAkj2XKjQg7APEYV+nFjYvcpl6
 |          |/P5DnRTzKQPG58u2TMb8cPKmi9MAJUAeFd1k2uBxBWXdIXHqDH7fHNFKlb5vaP
 |          |sNQtDRiVLDu1+CJ5ddo8IEFBRJVk8xUD9vjAocplINgc9rRIlIKQDs4tHxoceU
 |          |2ZJG1RAoGBAP4tdWTj2ds7TS4yBoOGLHdXDIPHHBHV8g7V39TBCMO4aRfB2Xf+
 |          |R5ykp7o2OqSH+sVDzK4tGy50dWZzw+m4lR3714C4BWx89OZJw/5RJ0j2OSLpIp
 |          |AykJtrKBYPJZ3Lan90HnVkU5MD4blmRrdHFrq6idYaDXCHgBvC1undAoGBAMI8
 |          |w9C1iDPz1PcLOmV3uVpNJFLud0gSaTtUyouGJPbauvwcnVIxgeXjRO3sPMHEvI
 |          |0OvMDH/YUCE5YB0VtZ0y/55s/qGEp8LRzYFUUxHB38YnekNW9PCUZ5Fmbfcv5a
 |          |eoxdT4FO/U6Stg0aLXQxakyFj7AcDKl1WcCzh9AoGAEHuuMz67cAYmeSpxVbIr
 |          |lvHFSbM2Tmb6PbAhcKlHavCgVeLvPri+oh/jaKX/o4/V6Vj+OwVdz+NpgZ1cRR
 |          |QbaFQSmt4F0yHIUIGsP0gjzFc8gen+cUU2L34BeXy9+b+pRl6nYwGAkfYce0Nw
 |          |4DoVRbf/DskjGXUzWNblkCgYAMWBMxccu3y1eIiPTrpeWnaAI6jsUFVqUik36R
 |          |PWM6APqjLRpeb+EGgCQQTtQpqFwnZa2lXqlospGdGu1dy9Rn8ibGpbyk/S5ANl
 |          |GfLRjRWwnS+q+erFI1lVp0HT1Mpu+Fj8dK2p1SBKDw7c1E4RNVbBGDfihFXVqy
 |          |D5bQKBgQDJt2QT2oxFP/UYU1OQO1Vu38U82Yw5F7XCFE5GaUWv2n+ID/4kg6IR
 |          |XOqlg8u/Hat/tsAI4WNjyjXSLLdCvF85d6Sx2/pbPMfNBttDr6Oj0+CikklQCi
         |          |WJVZFlHSC0thG7psyrflbOoLBKdwfvBkrfSrpfyNeQGQ==
|        | -----END RSA PRIVATE KEY                                         |          |
+--------+------------------------------------------------------------------+----------+

If you are absolutely sure that you want to ignore the above files from talisman detectors, consider pasting the following format in .talismanrc file in the project root

fileignoreconfig:
- filename: id_rsa
  checksum: 416122aefc170aef929dbbd1e01626e9066d36f7cfd83c00e38d38b5b03a7c69
```

As expected, Talisman found a sensitive file(SSH private key) and stopped the file from being committed in to the repo. You can review [supported rules and other configurations here](https://github.com/thoughtworks/talisman/blob/master/detector/severity/severity_config.go).

Run the Scanner
----------

You can also use Talisman as a command-line utility instead of using it as a git hook.

Let’s explore what options Talisman provides us.

```
talisman -h
```
output
```
bash: talisman: command not found
```

What? We just installed it.

Oh, that’s right, we haven’t sourced the changes to the current bash environment.

```
source ~/.bashrc
```

There you go!

```
/webapp# talisman -h
Usage of /root/.talisman/bin/talisman_linux_amd64:
  -c, --checksum string          checksum calculator calculates checksum and suggests .talismanrc format
  -d, --debug                    enable debug mode (warning: very verbose)
  -g, --githook string           either pre-push or pre-commit (default "pre-push")
      --ignoreHistory            scanner scans all files on current head, will not scan through git commit history
  -i, --interactive              interactively update talismanrc (only makes sense with -g/--githook)
  -p, --pattern string           pattern (glob-like) of files to scan (ignores githooks)
  -r, --reportdirectory string   directory where the scan reports will be stored
  -s, --scan                     scanner scans the git commit history for potential secrets
  -w, --scanWithHtml             generate html report (**Make sure you have installed talisman_html_report to use th
is, as mentioned in Readme**)
  -v, --version                  show current version of talisman
pflag: help requested
```
Let’s run the scanner to find any secrets in our code.
```
talisman --scan
```

By default, Talisman outputs the results in the JSON format. You can check out the result file at talisman_reports/data/report.json,

Exercise
----------

1. Explore the documentation of [talisman](https://thoughtworks.github.io/talisman/docs)
2. Reduce the False Positives and embed this tool in the CI/CD pipeline
3. Remember to keep the DevSecOps Gospel best practices in mind while doing this exercise
