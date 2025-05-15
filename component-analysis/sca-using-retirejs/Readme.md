Software Component Analysis using RetireJS
================================================================================

Learn how to use RetireJS to scan frontend components
--------------------------------------------------------------------------------

In this scenario, you will learn how to install RetireJS and run OAST Scans on a git repository.

You will need to download the code, install the OAST tool, and then finally run the OAST scan on the code.

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, We need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp
cd webapp
```

Install RetireJS Tool
----------------------------------------------------------------

> There are lots of JavaScript libraries for use on the Web and in Node.JS apps. The availability of these libraries greatly simplifies development, but also increases the security risks. Because of rampant abuse of these libraries, attackers are concentrating on these libraries. Realizing the need for awareness, OWASP has included “Using Components with Known Vulnerabilities” as part of the OWASP Top 10 list.
>
> RetireJS helps you in finding the insecure Javascript libraries in your code.
>
> Source: [Retirejs Github Page](https://github.com/retirejs/retire.js/).


First, we need to install Node JS and NPM.

NEW ONE:
```
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
apt update


```
![image](https://github.com/user-attachments/assets/4ed6f0e6-b07d-480d-8d09-7c27eabe19a7)
![image](https://github.com/user-attachments/assets/7c0c05c7-7708-4be1-a0b9-ae6930804277)

Then we can install the RetireJS tool on the system to find the insecure Javascript libraries.<br>
`apt install nodejs -y`<br>
`npm install -g retire@5.0.0`<br>

`retire --help`<br>
```
Usage: retire [options]

Options:
  -V, --version            output the version number
  -v, --verbose            Show identified files (by default only vulnerable files are shown)
  -c, --nocache            Don't use local cache
  --jspath <path>          Folder to scan for javascript files (deprecated)
  --path <path>            Folder to scan for javascript files
  --jsrepo <path|url>      Local or internal version of repo. Can be multiple comma separated. Default: 'central')
  --cachedir <path>        Path to use for local cache instead of /tmp/.retire-cache
  --proxy <url>            Proxy url (http://some.host:8080)
  --outputformat <format>  Valid formats: text, json, jsonsimple, depcheck (experimental), cyclonedx and cyclonedxJSON
  --outputpath <path>      File to which output should be written
  --ignore <paths>         Comma delimited list of paths to ignore
  --ignorefile <path>      Custom ignore file, defaults to .retireignore / .retireignore.json
  --severity <level>       Specify the bug severity level from which the process fails. Allowed levels none, low, medium, high, critical. Default:
                           none
  --exitwith <code>        Custom exit code (default: 13) when vulnerabilities are found
  --colors                 Enable color output (console output only)
  --insecure               Enable fetching remote jsrepo/noderepo files from hosts using an insecure or self-signed SSL (TLS) certificate
  --ext <extensions>       Comma separated list of file extensions for JavaScript files. The default is "js"
  --cacert <path>          Use the specified certificate file to verify the peer used for fetching remote jsrepo/noderepo files
  --includeOsv             Include OSV advisories in the output
  --deep                   Deep scan (slower and experimental)
  -h, --help               display help for command
```




Run the Scanner
----------

Front end dependencies managed via npm are stored in the package.json file. Let’s explore the contents of the package.json file.
```
cat package.json
-----
{
  ...[SNIP]...

  "main": "server.js",
  "dependencies": {
    "bcrypt-nodejs": "0.0.3",
    "body-parser": "^1.15.1",
    "consolidate": "^0.14.1",
    "csurf": "^1.8.3",
    "dont-sniff-mimetype": "^1.0.0",
    "express": "^4.13.4",
    "express-session": "^1.13.0",
    "forever": "^0.15.1",
    "helmet": "^2.0.0",
    "marked": "0.3.9",
    "mongodb": "^2.1.18",
    "node-esapi": "0.0.1",
    "serve-favicon": "^2.3.0",
    "swig": "^1.4.2",
    "underscore": "^1.8.3"
  },
  "comments": {
    "//": "a9 insecure components"
  },
  "engines": {
    "node": "4.4.x",
    "npm": "2.15.x"
  },
  "scripts": {
    "start": "node server.js",
    "test": "node node_modules/grunt-cli/bin/grunt test",
    "db:seed": "grunt db-reset",
    "precommit": "grunt precommit"
  },
  "devDependencies": {
    "async": "^2.0.0-rc.4",
    "grunt": "^1.0.1",
    "grunt-cli": "^1.2.0",
    "grunt-concurrent": "^2.3.0",
    "grunt-contrib-jshint": "^1.0.0",
    "grunt-contrib-watch": "^1.0.0",
    "grunt-env": "latest",
    "grunt-jsbeautifier": "^0.2.12",
    "grunt-mocha-test": "^0.12.7",
    "grunt-nodemon": "^0.4.2",
    "grunt-if": "https://github.com/binarymist/grunt-if/tarball/master",
    "grunt-npm-install": "^0.3.0",
    "grunt-retire": "^0.3.12",
    "mocha": "^2.4.5",
    "selenium-webdriver": "^2.53.2",
    "should": "^8.3.1",
    "zaproxy": "^0.2.0"
  },
  "repository": "https://github.com/OWASP/NodejsGoat",
  "license": "Apache 2.0"
}
```

As we can see, we are using various javascript libraries in this project. Let’s find if we are using any vulnerable libraries.

```
retire --outputformat json --outputpath no-npm-install-retire-output.json
```
output
```
DEPRECATION NOTICE: The node scanning is depreacated and will be removed soon. See https://github.com/RetireJS/retire.js/wiki/Deprecating-the-node.js-scanner

ERROR: Could not find dependencies: bcrypt-nodejs, body-parser, consolidate, csurf, dont-sniff-mimetype, express, express-session, forever, helmet, marked, m
ongodb, node-esapi, serve-favicon, swig, underscore. You may need to run npm install
```

As we have learned in the DevSecOps Gospel, we should always try to save the tool’s output in a machine-readable format. This output will enable us to parse it via script(s).

- --outputpath : flag specifies the output file path.
- --outputformat : flag specifies that output format. Here it’s the JSON format.

You will noticed we need to install the npm packages available in the package.json file using the npm install command before running the scan.

```
npm install
```
output
```
npm WARN deprecated bcrypt-nodejs@0.0.3: bcrypt-nodejs is no longer actively maintained. Please use bcrypt or bcryptjs. See https://github.com/kelektiv/node.bcrypt.js/wiki/bcrypt-vs-brypt.js to learn more about these two options
npm WARN deprecated swig@1.4.2: This package is no longer maintained

 ...[SNIP]...

added 1326 packages from 1247 contributors and audited 1328 packages in 27.38s

45 packages are looking for funding
  run `npm fund` for details

found 252 vulnerabilities (78 low, 85 moderate, 86 high, 3 critical)
  run `npm audit fix` to fix them, or `npm audit` for details
```

Then, re-run the previous command to scan the dependencies. Once done, you can use the cat command to see the RetireJS output with the help of jq command.

```
cat retire_output.json | jq .
---------
...[SNIP]...,

    {
      "file": "node_modules/forever-monitor/node_modules/utile/package.json",
      "results": [
        {
          "component": "utile",
          "version": "0.3.0",
          "vulnerabilities": [
            {
              "info": [
                "https://hackerone.com/reports/321701"
              ],
              "below": "99.999.9999",
              "severity": "low",
              "identifiers": {
                "summary": "Out-of-bounds Read"
              }
            }
          ]
        }
      ]
    }
  ],
  "messages": [],
  "errors": [],
  "time": 8.03
}
```
Oh no, we have a big issue list to work on.

# Understanding the Behavior of Severity Flags
Each security tool may have a specific flag to filter the severity of findings. In this step, we will explore into how this works using RetireJS.

As shown in the second step, we can use the --severity argument to specify the severity level we want to filter. Let’s give it a try by using this command:<br>
`retire --severity critical --outputformat json --outputpath retire_output.json`

We have successfully run the scan. Let’s check if the output contains only the severity level we are interested in, which is critical.<br>
`cat retire_output.json | jq .`

You might be wondering why retire_output.json still contains low, medium and high severity issues.

This behavior is not a bug but intentional.
> Note
>Each security tool behaves differently, and you might need to explore it further if something doesn’t work as expected.

Let’s experiment with the exit codes that RetireJS provides when we filter the severity for critical and medium issues. You will notice the difference in exit codes when issues are found.

First, filter for critical issues using the command below:<br>
`retire --severity critical --outputformat json --outputpath retire_output.json`<br>
Then, check the exit code.<br>
`echo $?`<br>
`0`<br>
This shows 0, indicating no issues found with critical severity. Now, how about filtering for medium issues?<br>
`retire --severity medium --outputformat json --outputpath retire_output.json`<br>
`echo $?`<br>
`13`<br>

Interesting! The exit code often returns 13 instead of 1 because 13 is the default exit code set by the RetireJS tool.

It’s important to note that an exit code isn’t always 1 when the tool finds security issues, it could be any number chosen by the tool’s developer.

Since each developer or organization may use different exit codes, we primarily focus on whether it’s zero or non-zero. For instance, the argument we used to filter severity returned an exit code of 13.

Let’s move to the next step.


Exercise
---------

In this exercise, you will explore and use the advanced features of Retire

1. Please configure the tool such that it only throws non zero exit code when high severity issues are present in the results
 > `retire --severity high --outputformat json --outputpath retire_output.json`  
2. Mark a high severity issue as False Positives
> RetireJS allows us to mark an issue or issues as False Positive (FP) using .retireignore.json file. .retireignore.json file needs to be created first using commands such as touch .retireignore.json or with a vi editor.
> More information about the ignore feature can be found here.
> If you have a large number of findings, as in the retire_output.json file, and you are looking to filter issues that are of high severity, you can use the jq tool for filtering.
Before creating the ignore file, let’s try to identify the components that have high severity.
`cat retire_output.json | jq '.data[].results[] | select (.vulnerabilities[]?.severity=="high") | .component,.version'`
<br>
```
cat >/webapp/.retireignore.json<<EOF
[
    {
        "component": "lodash",
        "version": "1.0.1",
        "justification" : "False Positive"
    },
    {
        "component": "dojo",
        "version": "1.4.2",
        "justification" : "False Positive"
    },
    {
        "component": "lodash",
        "version": "4.17.10",
        "justification" : "False Positive"
    },
    {
        "component": "underscore.js",
        "version": "1.8.3",
        "justification" : "False Positive"
    },
    {
        "component": "lodash",
        "version": "2.4.2",
        "justification" : "False Positive"
    },
    {
        "component":"handlebars",
        "version": "4.0.5",
        "justification" : "False Positive"
    },
    {
        "component":"tinyMCE",
        "version": "4.0.26",
        "justification" : "False Positive"
    }
]
EOF
```
Once we mark an issue as FP, we need to use the following command while scanning to avoid showing these issues in the subsequent scans.<br>
`retire --severity high --ignorefile .retireignore.json --outputformat json --outputpath retire_output.json`
Let’s try to check again if the high vulnerability still exists or not.<br>
`/webapp# `
Voila! We successfully marked all of the high severity issues as false positives.

> Hint
>
> RetireJS allows us to mark an issue or issues as False Positive (FP) using .retireignore.json file.
```
cat .retireignore.json
[
    {
        "component": "jquery",
        "identifiers" : { "issue": "2432"},
        "justification" : "We dont call external resources with jQuery"
    },
    {
        "component": "jquery",
        "version" : "2.1.4",
        "justification" : "We dont call external resources with jQuery"
    },
    {
        "path" : "node_modules",
        "justification" : "The node modules are only used for building - client side dependencies are using bower"
    }
]
```
As you can see above, we can mark an issue as False Positive (FP) using retire issue identifiers(line number 5), version of the library (line number 10) and node_modules(line number 14).

Once we mark an issue as FP, we need to use the following command while scanning to avoid showing these issuses in the subsequent scans.

```
retire --severity high --ignorefile .retireignore.json --outputformat json --outputpath retire_output.json
```

More information about the ignore feature is available [here](https://github.com/RetireJS/retire.js/tree/master/node#retireignorejson).

