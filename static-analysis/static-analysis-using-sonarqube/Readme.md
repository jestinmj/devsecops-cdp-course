Use SonarQube for Code Quality Analysis
================================================

In this scenario, you will learn how to run code quality scan on Python code using Sonarqube.

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp

cd webapp
```

Install SonarScanner
----------

> SonarScanner is the scanner command line for SonarQube. SonarScanner helps to run code analysis on the source code and integrate the scan results with SonarQube Server to present them in a dashboard.
> 
> You can find more details about the Sonar Scanner project at https://github.com/SonarSource/sonar-scanner-cli.

Let’s install sonar-scanner on the system to perform static analysis.

```
export SONAR_VERSION="4.4.0.2170"

wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_VERSION}-linux.zip -O /opt/sonar-scanner.zip
```
Extract the source code and add the tool to the PATH, so we can use Sonar Scanner on the command line without having to type the entire path.

```
unzip /opt/sonar-scanner.zip -d /opt/
chmod +x /opt/sonar-scanner-${SONAR_VERSION}-linux/bin/sonar-scanner
export PATH=/opt/sonar-scanner-${SONAR_VERSION}-linux/bin/:$PATH
```
We have successfully installed sonar-scanner.

Run the Scanner
----------
Let’s login into SonarQube using the following details.

> Sonarqube URL: https://sonarqube-xqihndz0.lab.practical-devsecops.training/sessions/new
> 
> login: admin
>
> password: admin

First, we need to create a project by clicking on the Create new project button. Fill in the form with the following details.

> project key : Django
>
> display name: Django


> Note: the project key is a unique identifier for your project and has to be different for each project.

On the next screen, please provide a suitable name for the token. We will use Django as the token name and click on the Generate button.

Provide a token: Django

output
```
Django: bfcfb8c18312818591606d4c1830c5152d33941c

The token is used to identify you when an analysis is performed. If it has been compromised, you can revoke it at any point of time in your user account.
```

Click on the continue button, choose the language as Other, select Linux, and run the following command to export the SonarQube token in an environment variable. However, your token will be different, so please ensure you use your token in the following command.

```
export SONARQUBE_TOKEN=INSERT_YOUR_TOKEN_HERE
```

> Did you replace the token in the above command?

```
sonar-scanner -Dsonar.projectKey=Django -Dsonar.sources=. -Dsonar.host.url=https://sonarqube-XqiHnDZ0.lab.practical-devsecops.training -Dsonar.login=$SONARQUBE_TOKEN
```

output
```
INFO: Scanner configuration file: /opt/sonar-scanner-4.4.0.2170-linux/conf/sonar-scanner.properties
INFO: Project root configuration file: NONE
INFO: SonarScanner 4.4.0.2170
INFO: Java 11.0.3 AdoptOpenJDK (64-bit)
INFO: Linux 4.15.0-112-generic amd64
INFO: User cache: /root/.sonar/cache
INFO: Scanner configuration file: /opt/sonar-scanner-4.4.0.2170-linux/conf/sonar-scanner.properties
INFO: Project root configuration file: NONE
INFO: Analyzing on SonarQube server 8.4.2
INFO: Default locale: "en", source code encoding: "UTF-8" (analysis is platform dependent)
INFO: Load global settings
INFO: Load global settings (done) | time=118ms
INFO: Server id: 9CFC3560-AXRneJm1L3yQMaNLOebb
INFO: User cache: /root/.sonar/cache
INFO: Load/download plugins
INFO: Load plugins index
INFO: Load plugins index (done) | time=114ms

...[SNIP]...

INFO: Sensor JavaScript analysis [javascript]
ERROR: Error when running: 'node -v'. Is Node.js available during analysis?
org.sonarsource.nodejs.NodeCommandException: Error when running: 'node -v'. Is Node.js available during analysis?
        at org.sonarsource.nodejs.NodeCommand.start(NodeCommand.java:83)
        at org.sonarsource.nodejs.NodeCommandBuilderImpl.getVersion(NodeCommandBuilderImpl.java:196)
        at org.sonarsource.nodejs.NodeCommandBuilderImpl.checkNodeCompatibility(NodeCommandBuilderImpl.java:169)
        at org.sonarsource.nodejs.NodeCommandBuilderImpl.build(NodeCommandBuilderImpl.java:144)
        at org.sonar.plugins.javascript.eslint.EslintBridgeServerImpl.initNodeCommand(EslintBridgeServerImpl.java:149)

...[SNIP]...

INFO: Analysis report compressed in 318ms, zip size=599 KB
INFO: Analysis report uploaded in 199ms
INFO: ANALYSIS SUCCESSFUL, you can browse https://sonarqube-XqiHnDZ0.lab.practical-devsecops.training/dashboard?id=django
INFO: Note that you will be able to access the updated dashboard once the server has processed the submitted analysis report
INFO: More about the report processing at https://sonarqube-XqiHnDZ0.lab.practical-devsecops.training/api/ce/task?id=AXRnmtmgL3yQMaNLOjE6
INFO: Analysis total time: 18.312 s
INFO: ------------------------------------------------------------------------
INFO: EXECUTION SUCCESS
INFO: ------------------------------------------------------------------------
INFO: Total time: 22.683s
INFO: Final Memory: 64M/296M
INFO: ------------------------------------------------------------------------
```

> Notice the errors? Please fix those errors and re-run the scan again.

> Hint : Do we have NodeJS installed?
>
> maybe you can install nodejs

After the scanner is done, you can check SonarQube dashboard to see scan results including Bugs, Vulnerabilities, Code Smells, Coverage and other details.

Also, we can integrate SonarQube into CI/CD pipeline and fail the builds based on your Quality Gate policies, we will learn this in the next exercises.