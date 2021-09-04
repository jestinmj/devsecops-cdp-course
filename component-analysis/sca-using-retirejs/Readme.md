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

```
curl -sL https://deb.nodesource.com/setup_12.x | bash -
apt install nodejs -y
npm install -g retire
retire --help
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
retire --outputformat json --outputpath retire_output.json
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
cat retire_output.json | jq
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

Exercise
---------

In this exercise, you will explore and use the advanced features of Retire

1. Please configure the tool such that it only throws non zero exit code when high severity issues are present in the results
2. Mark a high severity issue as False Positives

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).


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

