Software Component Analysis using Snyk
================================================================================
Learn to scan dependencies for vulnerabilities using Snyk
--------------------------------------------------------------------------------

In this scenario, you will learn how to install Snyk and run Snyk Scan on a git repository.

You will need to download the code, install the OAST tool, and then finally run the OAST scan on the code.

Download the source code
----------
We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp
cd webapp
```

Install Synk
----------

> Dependency analysis tool or SCA is used to find vulnerabilities in open source dependencies and it supports multiple programming languages such as Ruby, Python, NodeJS, Java, Go, .NET. It’s easy to use, a developer can use it on his/her machine using the command line or DevOps team can embed it into CI/CD pipeline.
>
> Source: https://snyk.io
>
> You can find more details about the project at https://github.com/snyk/snyk.

Let’s download the Snyk.

```
wget -O /usr/local/bin/snyk https://github.com/snyk/snyk/releases/download/v1.573.0/snyk-linux
chmod +x /usr/local/bin/snyk
snyk --help
```
Run the Scanner
----------

As we have learned in the DevSecOps Gospel, we should save the output in a machine-readable format.

We are using –json argument to output the results in JSON format.

```
snyk test --json .
```
output

```
issingApiTokenError: `snyk` requires an authenticated account. Please run `snyk auth` and try again.
    at Object.apiTokenExists (/snapshot/snyk/dist/lib/api-token.js:19:15)
    at test (/snapshot/snyk/dist/cli/commands/test/index.js:57:21)
    at Object.method (/snapshot/snyk/dist/lib/hotload.js:14:20)
    at runCommand (/snapshot/snyk/dist/cli/index.js:32:38)
    at main (/snapshot/snyk/dist/cli/index.js:234:21)
    at Object.<anonymous> (/snapshot/snyk/dist/cli/index.js:251:13)
    at Module._compile (pkg/prelude/bootstrap.js:1320:22)
    at Object.Module._extensions..js (internal/modules/cjs/loader.js:1156:10)
    at Module.load (internal/modules/cjs/loader.js:984:32)
    at Function.Module._load (internal/modules/cjs/loader.js:877:14)
```

We are greeted with an error. Snyk is complaining about missing API Token as it’s a paid solution and wants you to register before it can run the scan.

If you haven’t registered before, you can go to Snyk website and click SIGN UP FOR FREE -> Select Google account options -> Complete sign up -> Select CLI and go to the account settings page https://app.snyk.io/account and copy the token.

Once you have the token, you can authenticate to the Snyk service using the snyk auth command.

```
snyk auth YOUR_API_TOKEN_HERE
```

Or you can also export the environment variable using the following command.

```
export SNYK_TOKEN=YOUR_TOKEN_HERE
```

Now that we are authenticated, we can now scan our code with the snyk test command.

```
snyk test --json .
```

output

```
{
  "ok": false,
  "error": "Missing node_modules folder: we can't test without dependencies.\nPlease run 'npm install' first.",
  "path": "."
}
```

But it raises another error; we need to install the dependencies using npm install.

```
npm install
```

>  Why do we need to install it? We didn’t do this with the safety tool.

Oops, one more error. It looks like we do not have npm installed. Let’s go ahead and install it using the following commands.

```
curl -sL https://deb.nodesource.com/setup_12.x | bash -
apt install nodejs -y
```

> Ensure you are in the webapp directory. If not, please use cd /webapp to change the directory.

Let’s re-run the npm install command.

```
npm install
```

Let’s re-run the scan and save the output in a file.

```
snyk test --json . > output.json
```

> If you want to get the dashboard on the Snyk website, then monitor for new vulnerabilities, please use the following command:
>
> snyk monitor
