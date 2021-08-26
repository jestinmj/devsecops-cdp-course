Use tfsec to find security issues in IaC
================================================================

Learn how to use tfsec
--------------------------------------------------------------------------------

In this scenario, you will learn how to install an IaC static analysis tool called tfsec and run it on the Terraform (IaC) code.

You will need to install the tool, download the code, run the scan on the code and evaluate your infrastructure’s security posture.


Install tfsec
----------

> tfsec uses static analysis of your terraform templates to spot potential security issues.
>
> You can find more details about the project at https://github.com/aquasecurity/tfsec.


We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

Let’s install tfsec on the system to perform static analysis on your IaC.

```
wget -O /usr/local/bin/tfsec https://github.com/aquasecurity/tfsec/releases/download/v0.55.0/tfsec-linux-amd64
chmod +x /usr/local/bin/tfsec
```
Download vulnerable infrastructure
----------

Let’s clone an example IaC (terraform) repository with the following command.

```
git clone https://gitlab.practical-devsecops.training/pdso/terraform.git
cd terraform
tfsec -h
```

Run the tfsec tool
----------------------------------------------------------------

The tfsec perform the static scan on a directory. In this scenario, we will try to scan aws directory to find security issues.

```
tfsec aws
```
output

```
...[SNIP]...

Check 39

  [AWS001][WARNING] Resource 'aws_s3_bucket.data' has an ACL which allows public access.
  /terraform/aws/s3.tf:7


       4 |   # bucket does not have access logs
       5 |   # bucket does not have versioning
       6 |   bucket        = "${local.resource_prefix.value}-data"
       7 |   acl           = "public-read"
       8 |   force_destroy = true
       9 |   tags = {
      10 |     Name        = "${local.resource_prefix.value}-data"

  Impact:     The contents of the bucket can be accessed publicly
  Resolution: Apply a more restrictive bucket ACL

  See https://tfsec.dev/docs/aws/AWS001/ for more information.

Check 40

  [AWS017][ERROR] Resource 'aws_s3_bucket.financials' defines an unencrypted S3 bucket (missing server_side_encryption_configuration block).
  /terraform/aws/s3.tf:25-37


      22 |   }
      23 | }
      24 |
      25 | resource "aws_s3_bucket" "financials" {
      26 |   # bucket is not encrypted
      27 |   # bucket does not have access logs
      28 |   # bucket does not have versioning
      29 |   bucket        = "${local.resource_prefix.value}-financials"
      30 |   acl           = "private"
      31 |   force_destroy = true
      32 |   tags = {
      33 |     Name        = "${local.resource_prefix.value}-financials"
      34 |     Environment = local.resource_prefix.value
      35 |   }
      36 |
      37 | }
      38 |
      39 | resource "aws_s3_bucket" "operations" {
      40 |   # bucket is not encrypted

  Impact:     The bucket objects could be read if compromised
  Resolution: Configure bucket encryption

  See https://tfsec.dev/docs/aws/AWS017/ for more information.

Check 41

  [AWS018][ERROR] Resource 'aws_security_group.default' should include a description for auditing purposes.
  /terraform/aws/db-app.tf:80-88


      77 |   }
      78 | }
      79 |
      80 | resource "aws_security_group" "default" {
      81 |   name   = "${local.resource_prefix.value}-rds-sg"
      82 |   vpc_id = aws_vpc.web_vpc.id
      83 |
      84 |   tags = {
      85 |     Name        = "${local.resource_prefix.value}-rds-sg"
      86 |     Environment = local.resource_prefix.value
      87 |   }
      88 | }
      89 |
      90 | resource "aws_security_group_rule" "ingress" {
      91 |   type              = "ingress"

  Impact:     Descriptions provide context for the firewall rule reasons
  Resolution: Add descriptions for all security groups anf rules

  See https://tfsec.dev/docs/aws/AWS018/ for more information.

  times
  ------------------------------------------
  disk i/o             9.408914ms
  parsing HCL          61.891µs
  evaluating values    5.173796ms
  running checks       5.273408ms

  counts
  ------------------------------------------
  files loaded         13
  blocks               85
  evaluated blocks     85
  modules              0
  module blocks        0
  ignored checks       0

41 potential problems detected.
```

As you can see above, tfsec found 41 potential security issues in our Terraform configurations/code.

We can also use other formats like JSON, XML, CSV, etc to save the output in a machine-readable format.

```
tfsec aws -f json | tee tfsec-output.json
```

Exercise
----------
1. Read the [tfsec documentation](https://github.com/aquasecurity/tfsec)
2. What’s different between terrascan and tfsec? You can compare it with the result or provided arguments
3. Think how would you embed this tool in CI pipeline?

Note: you can access your GitLab machine by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training and use the credentials below.

- Username: root 
- Password: pdso-training

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).
