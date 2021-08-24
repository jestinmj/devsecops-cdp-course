Use Brakeman to find security issues
================================================================

Learn how to run static analysis scans on Ruby on Rails code using Brakeman
--------

In this scenario, you will learn how to run Brakeman scan on Rails code.

You will need to download the code, install the SAST tool called Brakeman and then finally run the SAST scan on the code.

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from our git repository.

```
git clone https://github.com/OWASP/railsgoat.git webapp
cd webapp
```

Install Brakeman
----------

> Brakeman is Static Analysis tool for Rails application to find vulnerabilities, Fast and Flexible tools with a very good report and fit to embed it in CI/CD pipeline.
> 
> You can find more details about the project at https://brakemanscanner.org/.

Basically, our system doesn’t have Ruby installed, let’s update apt first.
```
apt update
apt install ruby-full -y
gem install brakeman
```
We have successfully installed Brakeman, let’s explore the functionality it provides us.
```
brakeman -h
```
Run the Scanner
----------

As we have learned in DevSecOps Gospel, we would like to store the content in a JSON file. We are using the tee command here to show the output and store it in a file simultaneously.

```
brakeman -f json | tee result.json
```

Brakeman ran successfully, and it found 17 security issues.

1. Six medium severity issues
2. Eleven high severity issues

It seems we have found quite a few issues; you can ignore issues with using the brakeman.ignore file.

> You will find fingerprints in the scan output.

```
nano brakeman.ignore
........
{
    "ignored_warnings": [
        {
          "fingerprint": "febb21e45b226bb6bcdc23031091394a3ed80c76357f66b1f348844a7626f4df",
          "note": "ignore XSS"
        }
    ]
}
```
Let’s re-run the scanner.
```
brakeman -f json -i brakeman.ignore | tee result.json
```

You will see the issues are reduced because we ignored the Cross-Site Scripting (XSS) vulnerability.

