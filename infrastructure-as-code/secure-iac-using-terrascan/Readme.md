Use Terrascan to find security issues in IaC
================================================================

Learn how to use Terrascan
--------------------------------------------------------------------------------

In this scenario, you will learn how to install an IaC static analysis tool called Terrascan and run it on the Terraform (IaC) code.

You will need to install the tool, download the code, run the scan on the code and evaluate your infrastructure’s security posture.


Install Terrascan tool
----------

> Terrascan allows us to detect compliance and security violations across Infrastructure as Code to mitigate risk before provisioning cloud-native infrastructure.
>
> You can find more details about the project at https://github.com/accurics/terrascan.


We will do all the exercises locally first in DevSecOps-Box, so let’s get started.

Let’s install terrascan on the system to perform static analysis on your IaC.

```
wget https://github.com/accurics/terrascan/releases/download/v1.8.0/terrascan_1.8.0_Linux_x86_64.tar.gz

tar -xvf terrascan_1.8.0_Linux_x86_64.tar.gz
chmod +x terrascan
mv terrascan /usr/local/bin/
```

Download vulnerable infrastructure
----------

Let’s clone an example IaC (terraform) repository with the following command.

```
git clone https://gitlab.practical-devsecops.training/pdso/terraform.git
cd terraform
terrascan -h
```

Run the Terrascan tool
----------

Terrascan performs static scan on a directory. In this scenario, we will try to scan aws/ directory to find security issues.

```
terrascan scan -t aws -d aws
----
Violation Details -

        Description    :        Ensure S3 buckets have access logging enabled.
        File           :        s3.tf
        Module Name    :        root
        Plan Root      :        ./
        Line           :        69
        Severity       :        MEDIUM
        -----------------------------------------------------------------------

        Description    :        Ensure S3 buckets have access logging enabled.
        File           :        s3.tf
        Module Name    :        root
        Plan Root      :        ./
        Line           :        1
        Severity       :        MEDIUM
        -----------------------------------------------------------------------

...[SNIP]...

Scan Summary -

        File/Folder         :   /terraform/aws
        IaC Type            :   all
        Scanned At          :   2021-07-04 06:40:18.004553725 +0000 UTC
        Policies Validated  :   143
        Violated Policies   :   43
        Low                 :   4
        Medium              :   20
        High                :   19
```

As you can see, terrascan found security issues in our Terraform configurations/code.

Exercise
---------

1. Read the [terrascan documentation](https://github.com/accurics/terrascan)
2. Mark a low severity issue as False Positive
3. How would you embed this tool in CI pipeline?

Note: you can access your GitLab machine by visiting https://gitlab-ce-XqiHnDZ0.lab.practical-devsecops.training and using the credentials below.

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).
