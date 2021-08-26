Use Snyk tool to find security issues in your IaC
================================================

Learn to find security issues in Terraform resources using Snyk
--------------------------------


In this scenario, you will learn how to perform SAST for Infrastructure as Code (IaC) using the Snyk tool.

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s get started.

First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/terraform
cd terraform
```

Install Synk
----------

> CLI and build-time tool to find & fix known vulnerabilities in open-source dependencies, apart from Software Component Analysis (SCA), Snyk also support to perform SAST for Infrastructure as Code like Terraform.
>
> Source: [Snyk Github Page](https://github.com/snyk/snyk)

Let’s download the Snyk.
```
wget -O /usr/local/bin/snyk https://github.com/snyk/snyk/releases/download/v1.573.0/snyk-linux
chmod +x /usr/local/bin/snyk
snyk iac --help
```

Run the Scanner
----------

As we have learned in the DevSecOps Gospel, we should save the output in a machine-readable format. We are using –json argument to output the results in JSON format.

```
snyk iac test aws --json
```
output
```
FailedToGetIacOrgSettingsError: Failed to fetch IaC organization settings
    at /snapshot/snyk/dist/cli/commands/test/iac-local-execution/org-settings/get-iac-org-settings.js:26:31
    at requestWrapper (/snapshot/snyk/dist/lib/request/index.js:15:13)
    at processTicksAndRejections (internal/process/task_queues.js:97:5)
```

We are greeted with an error. Snyk is complaining about missing API Token as it’s a paid solution and wants you to register before it can run the scan.

If you haven’t registered before, you can go to Snyk website and click SIGN UP FOR FREE -> Select Google account options -> Complete sign up -> Select CLI and go to the account settings page https://app.snyk.io/account and copy the token.

> Do not use your company’s Synk Credentials/Token to practice these exercises. Please sign up for a Free Account instead.

Once you have the token, you can authenticate to the Snyk service using the snyk auth command.

```
snyk auth YOUR_API_TOKEN_HERE
```
Or you can also export the environment variable using the following command.

```
export SNYK_TOKEN=YOUR_TOKEN_HERE
```
Now that we are authenticated, we can now scan our Terraform code with the snyk iac test command.

```
snyk iac test aws --json > snyk-output.json
```

> aws is a target directory, you can change it to specific path of your Terraform resources.
