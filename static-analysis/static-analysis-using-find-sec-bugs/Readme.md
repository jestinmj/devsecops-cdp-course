Use FindSecBugs to find security issues
================================================================================

Learn how to run static analysis scans on Java code using FindSecBugs
--------------------------------------------------------------------------------

In this scenario, you will learn how to run FindSecBugs scan on Java code.

You will need to download the code, install the SAST tool called FindSecBugs and then finally run the SAST scan on the code

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from the git repository.

```
wget https://github.com/WebGoat/WebGoat/releases/download/v8.1.0/webgoat-server-8.1.0.jar
```

Install OWASP FindSecBugs
----------
> The SpotBugs plugin for security audits of Java web applications and Android applications.
> 
> You can find more details about the project at https://github.com/find-sec-bugs/find-sec-bugs

Before installing FindSecBugs, we need to ensure java is installed in our system.

```
java -h
```
It seems Java is not installed, so we need to install Java with the following command.
```
apt update && apt install openjdk-8-jre -y
```
Next, we need to download find-sec-bugs source code.
```
wget https://github.com/find-sec-bugs/find-sec-bugs/releases/download/version-1.9.0/findsecbugs-cli-1.9.0-fix2.zip && unzip findsecbugs-cli-1.9.0-fix2.zip -d /opt/
```
Fix the line ending in the shell script.
```
sed -i -e 's/\r$//' /opt/findsecbugs.sh
chmod +x /opt/findsecbugs.sh
```
We will add the tool to the PATH, so we can refer it on the command line.
```
export PATH=/opt/:$PATH
```

Run the SAST Scan
----------------------------------------------------------------
Let’s explore what options this tool provides us.
```
findsecbugs.sh -h
```
Perform the scan using the following command.
```
findsecbugs.sh -progress -html -output findsecbugs-report.html webgoat-server-8.1.0.jar
```
> Note: This will take several minutes to complete.

output
```
SLF4J: No SLF4J providers were found.
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#noProviders for further details.
Scanning archives (1 / 1)
2 analysis passes to perform
Pass 1: Analyzing classes (46404 / 46404) - 100% complete
Pass 2: Analyzing classes (20863 / 44219) - 47% complete
                           ...SNIP...
 [-1]==> +============================
| /!\ Warning : The taint debugging is not fully activated.
| [[ Stack ]]
Oups Accessing TOP or BOTTOM frame! @ 643

Dataflow (block 1): start fact is +============================
| /!\ Warning : The taint debugging is not fully activated.
| [[ Stack ]]
Oups Accessing TOP or BOTTOM frame!
Dataflow (block 1): orig result is +============================
| /!\ Warning : The taint debugging is not fully activated.
| [[ Stack ]]
Oups Accessing TOP or BOTTOM frame!
Dataflow (block 1): result is +============================
| /!\ Warning : The taint debugging is not fully activated.
| [[ Stack ]]
Oups Accessing TOP or BOTTOM frame! @ timestamp 19
----------------------------------------------------------------------
com.h3xstream.findsecbugs.taintanalysis.TaintDataflow iteration: 106, timestamp: 643
org.aspectj.weaver.AjcMemberMaker.interConstructor(Lorg/aspectj/weaver/ResolvedType;Lorg/aspectj/weaver/ResolvedMember;Lorg/aspectj/weaver/UnresolvedType;)Lorg/aspectj/weaver/ResolvedMember;
----------------------------------------------------------------------
Pass 2: Analyzing classes (23841 / 44219) - 53% complete
Pass 2: Analyzing classes (27720 / 44219) - 62% complete
Pass 2: Analyzing classes (27722 / 44219) - 62% complete
Pass 2: Analyzing classes (38412 / 44219) - 86% complete
```
As we have learned in the DevSecOps Gospel, we should save the output in a machine-readable format so the output can be parsed by the machines.

> Do you think the above command is following the DevSecOps best practices?

What can we do to improve it further?