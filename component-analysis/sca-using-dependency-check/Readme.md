Software Component Analysis using Dependency-Check
================================================================

Learn to scan Java dependencies for vulnerabilities using Dependency Check
--------------------------------

In this scenario, you will learn how to install OWASP Dependency Check and run OAST Scans on a Java code.

You will need to download the code, install the OAST tool, and then finally run the OAST scan on the code.

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from the git repository.

```
git clone https://github.com/WebGoat/WebGoat.git webapp
```

Install OWASP Dependency Check Tool
----------

> Dependency-Check is SCA tool that attempts to detect publicly disclosed vulnerabilities contained within a project’s dependencies.
>
> You can find more details about the project at https://github.com/jeremylong/DependencyCheck.

Before installing Dependency-Check, we need to ensure if java is installed in our system.

```
java -h
apt update
apt install openjdk-8-jre -y
wget -O /opt/v6.1.6.zip https://github.com/jeremylong/DependencyCheck/releases/download/v6.1.6/dependency-check-6.1.6-release.zip
unzip /opt/v6.1.6.zip -d /opt/
export PATH=/opt/dependency-check/bin:$PATH
dependency-check.sh -h
```

Run the OAST Scan
----------

Perform the scan on the webgoat source code directory using the following command.

```
dependency-check.sh --scan /webapp --format "CSV" --project "Webgoat" --failOnCVSS 8 --out /opt
```

At first, Dependency-Check will update its database before scanning the code.

output
```
[INFO] Checking for updates
[INFO] NVD CVE requires several updates; this could take a couple of minutes.
[INFO] Download Started for NVD CVE - 2003
[INFO] Download Started for NVD CVE - 2002
[INFO] Download Complete for NVD CVE - 2002  (122 ms)
[INFO] Download Started for NVD CVE - 2004

...[SNIP]...

Dependency-Check is an open source tool performing a best effort analysis of 3rd party dependencies; false positives and false negatives may exist in the analysis performed by the tool. Use of the tool and the reporting provided constitutes acceptance for use in an AS IS condition, and there are NO warranties, implied or otherwise, with regard to the analysis or its use. Any use of the tool and the reporting provided is at the user’s risk. In no event shall the copyright holder or OWASP be held liable for any damages whatsoever arising out of or in connection with the use of this tool, the analysis performed, or the resulting report.


   About ODC: https://jeremylong.github.io/DependencyCheck/general/internals.html
   False Positives: https://jeremylong.github.io/DependencyCheck/general/suppression.html

💖 Sponsor: https://github.com/sponsors/jeremylong


[INFO] Analysis Started
[INFO] Finished Archive Analyzer (0 seconds)
[INFO] Finished File Name Analyzer (0 seconds)
[INFO] Finished Dependency Merging Analyzer (0 seconds)
[INFO] Finished Version Filter Analyzer (0 seconds)
[INFO] Finished Hint Analyzer (0 seconds)
[INFO] Created CPE Index (1 seconds)
[INFO] Finished CPE Analyzer (1 seconds)
[INFO] Finished False Positive Analyzer (0 seconds)
[INFO] Finished NVD CVE Analyzer (0 seconds)
00:00  INFO: Vulnerability found: bootstrap below 3.4.1
00:00  INFO: Vulnerability found: bootstrap below 3.4.0
00:00  INFO: Vulnerability found: bootstrap below 3.4.0
00:00  INFO: Vulnerability found: bootstrap below 3.4.0
00:00  INFO: Vulnerability found: jquery below 3.0.0-beta1
00:00  INFO: Vulnerability found: jquery below 2.2.0
00:00  INFO: Vulnerability found: jquery below 3.4.0
00:00  INFO: Vulnerability found: jquery below 3.5.0
00:00  INFO: Vulnerability found: jquery below 3.5.0
00:00  INFO: Vulnerability found: jquery below 1.12.0
00:00  INFO: Vulnerability found: jquery below 1.12.0
00:00  INFO: Vulnerability found: jquery below 3.4.0
00:00  INFO: Vulnerability found: jquery below 3.5.0
00:00  INFO: Vulnerability found: jquery below 3.5.0
00:00  INFO: Vulnerability found: jquery-ui-dialog below 1.12.0
00:00  INFO: Vulnerability found: bootstrap below 3.4.1
00:00  INFO: Vulnerability found: bootstrap below 3.4.0
00:00  INFO: Vulnerability found: bootstrap below 3.4.0
00:00  INFO: Vulnerability found: bootstrap below 3.4.0
00:00  INFO: Vulnerability found: jquery below 3.5.0
00:00  INFO: Vulnerability found: jquery below 3.5.0
00:00  INFO: Vulnerability found: jquery-ui-dialog below 1.12.0
[INFO] Finished RetireJS Analyzer (0 seconds)
[INFO] Finished Sonatype OSS Index Analyzer (0 seconds)
[INFO] Finished Vulnerability Suppression Analyzer (0 seconds)
[INFO] Finished Dependency Bundling Analyzer (0 seconds)
[INFO] Analysis Complete (2 seconds)
[INFO] Writing report to: /opt/dependency-check-report.csv
```

As we have learned in the DevSecOps Gospel, we should save the output in a machine-readable format so the output can be parsed by the machines.

You can see several vulnerabilities found in jquery from the output. Also the report was stored in the /opt/dependency-check-report.csv file.

In the next exercises, you will learn how to embed this scan on CI/CD pipelines.

Exercise
----------

Recall techniques you have learned in the previous modules.

1. Explore various options provided by the Dependency Check tool
2. What stage should you put the Dependency Check tool in the pipeline?
3. Only fail the build when CVSS score is greater than 6 (remember how to check the exit code?)
4. Please save the output as JSON file (machine-readable format)

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).
