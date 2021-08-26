Use TFLint to find security issues in IaC
=======================

Learn how to use TFLint
--------------

In this scenario, you will learn how to install an IaC static analysis tool called TFLint and run it on the Terraform (IaC) code.

You will need to download the sample code, install the TFLint tool, and then finally run static analysis scan on the Terraform resource.

Install TFLint
----------

> TFLint is a framework to find possible errors (like illegal instance types) for Major Cloud providers (AWS/Azure/GCP, warn about deprecated syntax, unused declarations and enforce best practices, naming conventions.
>
> You can find more details about the project at https://github.com/terraform-linters/tflint.

We will do all the exercises locally first in DevSecOps-Box, so lets start the exercise.

Let’s install tflint on the system to perform static analysis on your IaC.

```
curl https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash
```

We have successfully installed tflint.

Download vulnerable infrastructure
----------

Let’s clone an example IaC (terraform) repository with the following command.

```
git clone https://gitlab.practical-devsecops.training/pdso/terraform.git
cd terraform
tflint -h
```

Run the TFLint tool
----------

TFLint performs static analysis on our Terraform resources. In this scenario, we will try to scan aws directory to find any possible errors, and review if we are following best practices in Terraform resources.

```
tflint aws
```
output

```
Failed to load configurations. 6 error(s) occurred:

Error: Invalid quoted type constraints

  on aws/consts.tf line 29, in variable "availability_zone":
  29:   type    = "string"

Terraform 0.11 and earlier required type constraints to be given in quotes, but that form is now deprecated and will be removed in a future version of Terraform. Remove the quotes around "string".

Error: Invalid quoted type constraints

  on aws/consts.tf line 34, in variable "availability_zone2":
  34:   type    = "string"

Terraform 0.11 and earlier required type constraints to be given in quotes, but that form is now deprecated and will
 be removed in a future version of Terraform. Remove the quotes around "string".

Error: Invalid quoted type constraints

  on aws/consts.tf line 40, in variable "ami":
  40:   type    = "string"

Terraform 0.11 and earlier required type constraints to be given in quotes, but that form is now deprecated and will
 be removed in a future version of Terraform. Remove the quotes around "string".

Error: Invalid quoted type constraints

  on aws/consts.tf line 45, in variable "dbname":
  45:   type        = "string"

Terraform 0.11 and earlier required type constraints to be given in quotes, but that form is now deprecated and will
 be removed in a future version of Terraform. Remove the quotes around "string".

Error: Invalid quoted type constraints

  on aws/consts.tf line 51, in variable "password":
  51:   type        = "string"

Terraform 0.11 and earlier required type constraints to be given in quotes, but that form is now deprecated and will be removed in a future version of Terraform. Remove the quotes around "string".

Error: Invalid quoted type constraints

  on aws/consts.tf line 57, in variable "neptune-dbname":
  57:   type        = "string"

Terraform 0.11 and earlier required type constraints to be given in quotes, but that form is now deprecated and will be removed in a future version of Terraform. Remove the quotes around "string".

Warning: Quoted references are deprecated

  on aws/db-app.tf line 30, in resource "aws_db_instance" "default":
  30:     ignore_changes = ["password"]

In this context, references are expected literally rather than in quotes. Terraform 0.11 and earlier required quotes, but quoted references are now deprecated and will be removed in a future version of Terraform. Remove the quotes surrounding this reference to silence this warning.

Warning: Quoted references are deprecated

  on aws/eks.tf line 74, in resource "aws_eks_cluster" "eks_cluster":
  74:     "aws_iam_role_policy_attachment.policy_attachment-AmazonEKSClusterPolicy",

In this context, references are expected literally rather than in quotes. Terraform 0.11 and earlier required quotes, but quoted references are now deprecated and will be removed in a future version of Terraform. Remove the quotes surrounding this reference to silence this warning.

Warning: Quoted references are deprecated

  on aws/eks.tf line 75, in resource "aws_eks_cluster" "eks_cluster":
  75:     "aws_iam_role_policy_attachment.policy_attachment-AmazonEKSServicePolicy",

In this context, references are expected literally rather than in quotes. Terraform 0.11 and earlier required quotes, but quoted references are now deprecated and will be removed in a future version of Terraform. Remove the quotes surrounding this reference to silence this warning.
```

As you can see, tflint found several errors that we need to fix in our Terraform configurations/code. Fixing errors when writing terraform resources will prevent errors occurring during runtime when executing with the terraform run command.