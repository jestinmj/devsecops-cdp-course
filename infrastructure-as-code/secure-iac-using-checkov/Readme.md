Use Checkov to check misconfigurations in IaC
================================

Learn how to use Checkov
--------------

In this scenario, you will learn how to install and run SAST Scans on your Infrastructure as Code like Terraform.

You will need to download the code, install the tool, run the scan on the code and evaluate your infrastructure’s security posture.

Install Checkov
----------

> Checkov is a static code analysis tool for infrastructure-as-code, support several cloud such as AWS, Azure and GCP also can detect environment variables on your cloud environment.
>
> You can find more details about the project at https://github.com/bridgecrewio/checkov

We will do all the exercises locally first in DevSecOps-Box, so lets start the exercise.

Let’s install checkov on the system to perform static analysis on your IaC.

```
pip3 install checkov
```

Download vulnerable infrastructure
----------

Let’s clone an example IaC (terraform) repository with the following command.

```
git clone https://github.com/bridgecrewio/terragoat.git
cd terragoat

checkov -v
```
It should give us the list of available arguments to be used but if you found an error like this.

oh okay, its complaining about the lack of dataclasses, we need to install the module with the following command.

```
pip3 install dataclasses
```

Run Checkov tool
----------

Checkov can perform the static scan on a directory or a file. In this scenario, we will try to scan terraform/aws/s3.tf to find misconfiguration related to AWS S3 buckets.

```
checkov -f terraform/aws/s3.tf
```
output
```
       _               _
   ___| |__   ___  ___| | _______   __
  / __| '_ \ / _ \/ __| |/ / _ \ \ / /
 | (__| | | |  __/ (__|   < (_) \ V /
  \___|_| |_|\___|\___|_|\_\___/ \_/

by bridgecrew.io | version: 1.0.513

terraform scan results:

Passed checks: 19, Failed checks: 16, Skipped checks: 0

Check: CKV_AWS_70: "Ensure S3 bucket does not allow an action with any Principal"
        PASSED for resource: aws_s3_bucket.data
        File: /s3.tf:1-13
        Guide: https://docs.bridgecrew.io/docs/bc_aws_s3_23

Check: CKV_AWS_57: "S3 Bucket has an ACL defined which allows public WRITE access."
        PASSED for resource: aws_s3_bucket.data
        File: /s3.tf:1-13
        Guide: https://docs.bridgecrew.io/docs/s3_2-acl-write-permissions-everyone

Check: CKV_AWS_70: "Ensure S3 bucket does not allow an action with any Principal"
        PASSED for resource: aws_s3_bucket.financials
        File: /s3.tf:25-37
        Guide: https://docs.bridgecrew.io/docs/bc_aws_s3_23

Check: CKV_AWS_57: "S3 Bucket has an ACL defined which allows public WRITE access."
        PASSED for resource: aws_s3_bucket.financials
        File: /s3.tf:25-37
        Guide: https://docs.bridgecrew.io/docs/s3_2-acl-write-permissions-everyone

Check: CKV_AWS_20: "S3 Bucket has an ACL defined which allows public READ access."
        PASSED for resource: aws_s3_bucket.financials
        File: /s3.tf:25-37
        Guide: https://docs.bridgecrew.io/docs/s3_1-acl-read-permissions-everyone
...
...
```
As you can see, checkov found security issues in our Terraform configurations/code.

If you are interested in scanning a directory, you can use the following command.

```
checkov -d terraform/aws
```

Exercise
----------
1. Scan the entire directory (/terragoat/terraform) and save the output into a JSON file
2. How many checks failed after running checkov tool?
3. Can you skip a specific check in the target directory? Any check of your choice, but skip at least five checks.

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

