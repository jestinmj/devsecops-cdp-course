Learn how to run ZAP to find security issues
================================================================

In this scenario, you will learn how to use ZAP to scan a website for security issues.

OWASP Zed Attack Proxy tool
--------------

> ZAP is an open-source web application security scanner to perform security testing (Dynamic Testing) on web applications. OWASP ZAP is the flagship OWASP project used extensively by penetration testers. ZAP can also run in a daemon mode for hands-off scans for CI/CD pipeline. ZAP provides extensive API (SDK) and a REST API to help users create custom scripts.
>
> Source: [OWASP ZAP](https://www.zaproxy.org/getting-started/)

In this exercise, we will use ZAP Baseline Scan to find security issues passively.

Passive scanning with ZAP involves quietly observing all messages sent to the web app without altering them, keeping things safe and not slowing down the app’s exploration.

Let’s see the usage of ZAP Docker for Baseline Scan.

```
docker run --rm softwaresecurityproject/zap-stable:2.14.0 zap-baseline.py --help
```

Run the Scanner
----------

As we have learned in the DevSecOps Gospel, we should save the output in the machine-readable format like JSON, CSV or XML.

Let’s run zap-baseline.py with basic options.
```
docker run --rm owasp/zap2docker-stable zap-baseline.py -t https://prod-XqiHnDZ0.lab.practical-devsecops.training
```
output
```
Unable to find image 'softwaresecurityproject/zap-stable:2.14.0' locally
2.14.0: Pulling from softwaresecurityproject/zap-stable
c0edef2937fa: Pull complete 
464af6119535: Pull complete 
9523b0e736f0: Pull complete 
59edb5ab4c68: Pull complete 
6f0734b3469d: Pull complete 
cc91d209bf42: Pull complete 
4f4fb700ef54: Pull complete 
daa3ce7f0200: Pull complete 
efdaff486a6a: Pull complete 
4bfb516a6f61: Pull complete 
4d8109d1478a: Pull complete 
be701932bcb9: Pull complete 
85c8d84644d5: Pull complete 
f2adc7415809: Pull complete 
15066e25658b: Pull complete 
7f68d03e45d6: Pull complete 
3372020d0fdd: Pull complete 
bad953de7f6e: Pull complete 
484d42ba9365: Pull complete 
Digest: sha256:aec6c9f65d69570aadec0d15ad0d3a24ffd2c7de5a262436c34e5009c5aa2e66
Status: Downloaded newer image for softwaresecurityproject/zap-stable:2.14.0
2025-05-20 05:33:38,669 Invalid option help : option --help not recognized
Usage: zap-baseline.py -t <target> [options]
    -t target         target URL including the protocol, e.g. https://www.example.com
Options:
    -h                print this help message
    -c config_file    config file to use to INFO, IGNORE or FAIL warnings
    -u config_url     URL of config file to use to INFO, IGNORE or FAIL warnings
    -g gen_file       generate default config file (all rules set to WARN)
    -m mins           the number of minutes to spider for (default 1)
    -r report_html    file to write the full ZAP HTML report
    -w report_md      file to write the full ZAP Wiki (Markdown) report
    -x report_xml     file to write the full ZAP XML report
    -J report_json    file to write the full ZAP JSON document
    -a                include the alpha passive scan rules as well
    -d                show debug messages
    -P                specify listen port
    -D secs           delay in seconds to wait for passive scanning 
    -i                default rules not in the config file to INFO
    -I                do not return failure on warning
    -j                use the Ajax spider in addition to the traditional one
    -l level          minimum level to show: PASS, IGNORE, INFO, WARN or FAIL, use with -s to hide example URLs
    -n context_file   context file which will be loaded prior to spidering the target
    -p progress_file  progress file which specifies issues that are being addressed
    -s                short output format - dont show PASSes or example URLs
    -T mins           max time in minutes to wait for ZAP to start and the passive scan to run
    -U user           username to use for authenticated scans - must be defined in the given context file
    -z zap_options    ZAP command line options e.g. -z "-config aaa=bbb -config ccc=ddd"
    --hook            path to python file that define your custom hooks
    --auto            use the automation framework if supported for the given parameters (this is now the default)
    --autooff         do not use the automation framework even if supported for the given parameters

For more details see https://www.zaproxy.org/docs/docker/baseline-scan/
```
> Did you notice that we did not pull the image at the beginning? The image is automatically pulled if it does not exist, without using docker pull.

# Running the Scanner

As we have learned in the DevSecOps Gospel, we should save the output in the machine-readable format like JSON, CSV or XML.

Let’s run zap-baseline.py with basic options.<br>
`docker run --rm softwaresecurityproject/zap-stable:2.14.0 zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training`<br>
```
Using the Automation Framework
Total of 59 URLs
PASS: In Page Banner Information Leak [10009]
PASS: Cookie No HttpOnly Flag [10010]
PASS: Cookie Without Secure Flag [10011]
PASS: Content-Type Header Missing [10019]
PASS: Information Disclosure - Debug Error Messages [10023]
PASS: Information Disclosure - Sensitive Information in URL [10024]
PASS: Information Disclosure - Sensitive Information in HTTP Referrer Header [10025]
PASS: HTTP Parameter Override [10026]
PASS: Open Redirect [10028]
PASS: Cookie Poisoning [10029]
PASS: User Controllable Charset [10030]
PASS: User Controllable HTML Element Attribute (Potential XSS) [10031]
PASS: Viewstate [10032]
PASS: Directory Browsing [10033]
PASS: Heartbleed OpenSSL Vulnerability (Indicative) [10034]
PASS: Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s) [10037]
PASS: X-Backend-Server Header Information Leak [10039]
PASS: HTTP to HTTPS Insecure Transition in Form Post [10041]
PASS: HTTPS to HTTP Insecure Transition in Form Post [10042]
PASS: User Controllable JavaScript Event (XSS) [10043]
PASS: Big Redirect Detected (Potential Sensitive Information Leak) [10044]
PASS: Retrieved from Cache [10050]
PASS: X-ChromeLogger-Data (XCOLD) Header Information Leak [10052]
PASS: Cookie without SameSite Attribute [10054]
PASS: CSP [10055]
PASS: X-Debug-Token Information Leak [10056]
PASS: Username Hash Found [10057]
PASS: X-AspNet-Version Response Header [10061]
PASS: PII Disclosure [10062]
PASS: Timestamp Disclosure [10096]
PASS: Hash Disclosure [10097]
PASS: Cross-Domain Misconfiguration [10098]
PASS: Weak Authentication Method [10105]
PASS: Reverse Tabnabbing [10108]
PASS: Modern Web Application [10109]
PASS: Session Management Response Identified [10112]
PASS: Verification Request Identified [10113]
PASS: Private IP Disclosure [2]
PASS: Session ID in URL Rewrite [3]
PASS: Script Passive Scan Rules [50001]
PASS: Stats Passive Scan Rule [50003]
PASS: Insecure JSF ViewState [90001]
PASS: Java Serialization Object [90002]
PASS: Insufficient Site Isolation Against Spectre Vulnerability [90004]
PASS: Charset Mismatch [90011]
PASS: Application Error Disclosure [90022]
PASS: WSDL File Detection [90030]
PASS: Loosely Scoped Cookie [90033]

...[SNIP]...

WARN-NEW: Strict-Transport-Security Header Not Set [10035] x 12 
        https://prod-p30jrhut.lab.practical-devsecops.training (200 OK)
        https://prod-p30jrhut.lab.practical-devsecops.training/ (200 OK)
        https://prod-p30jrhut.lab.practical-devsecops.training/robots.txt (404 Not Found)
        https://prod-p30jrhut.lab.practical-devsecops.training/sitemap.xml (404 Not Found)
        https://prod-p30jrhut.lab.practical-devsecops.training/static/taskManager/css/bootstrap.css (200 OK)
WARN-NEW: Server Leaks Version Information via "Server" HTTP Response Header Field [10036] x 12 
        https://prod-p30jrhut.lab.practical-devsecops.training (200 OK)
        https://prod-p30jrhut.lab.practical-devsecops.training/ (200 OK)
        https://prod-p30jrhut.lab.practical-devsecops.training/robots.txt (404 Not Found)
        https://prod-p30jrhut.lab.practical-devsecops.training/sitemap.xml (404 Not Found)
        https://prod-p30jrhut.lab.practical-devsecops.training/static/taskManager/css/bootstrap.css (200 OK)

...[SNIP]...

WARN-NEW: Permissions Policy Header Not Set [10063] x 12 
        https://prod-p30jrhut.lab.practical-devsecops.training (200 OK)
        https://prod-p30jrhut.lab.practical-devsecops.training/ (200 OK)
        https://prod-p30jrhut.lab.practical-devsecops.training/robots.txt (404 Not Found)
        https://prod-p30jrhut.lab.practical-devsecops.training/sitemap.xml (404 Not Found)
        https://prod-p30jrhut.lab.practical-devsecops.training/static/taskManager/js/bootstrap.min.js (404 Not Found)
WARN-NEW: Source Code Disclosure - SQL [10099] x 1 
        https://prod-p30jrhut.lab.practical-devsecops.training/taskManager/tutorials/injection/ (200 OK)

...[SNIP]....

FAIL-NEW: 0     FAIL-INPROG: 0  WARN-NEW: 17    WARN-INPROG: 0  INFO: 0 IGNORE: 0       PASS: 48
```
> The provided command is a Docker command that runs a Docker container using the image softwaresecurityproject/zap-stable:2.14.0. The purpose of this command is to run a Zed Attack Proxy (ZAP) baseline scan on the specified URL https://prod-p30jrhut.lab.practical-devsecops.training.

Here's a breakdown of the command:
- docker run: This is the command to run a new Docker container.
- --rm: This flag tells Docker to automatically remove the container when it exits.
- softwaresecurityproject/zap-stable:2.14.0: This is the Docker image name and version that contains the ZAP application.
- zap-baseline.py: This is the command to run inside the container. zap-baseline.py is a script that runs a baseline scan using ZAP.
- -t: This option specifies the target URL to scan. In this case, it's the URL https://prod-p30jrhut.lab.practical-devsecops.training.
In summary, this command runs a ZAP baseline scan on the specified URL, and the resulting output will be stored in the Docker container.

If you want the output in JSON format, you can use the -J option.
```
docker run --user $(id -u):$(id -g) -w /zap -v $(pwd):/zap/wrk:rw --rm softwaresecurityproject/zap-stable:2.14.0 zap-baseline.py -t https://prod-p30jrhut.lab.practical-devsecops.training -J zap-output.json
```
The provided command is a Docker command that runs a Docker container from the softwaresecurityproject/zap-stable:2.14.0 image, which is an official Docker image of the Zed Attack Proxy (ZAP) security tool.

Here's a breakdown of the command:
- docker run: This is the command to run a new Docker container.
- --user $(id -u):$(id -g): This sets the user ID and group ID of the container to the current user's ID and group ID on the host machine. This allows the container to run with the same permissions as the user running the command.
- -w /zap: This sets the working directory of the container to /zap.
- -v $(pwd):/zap/wrk:rw: This mounts the current working directory on the host machine ($(pwd)) as a volume at /zap/wrk in the container, with read-write permissions. This allows the container to access files from the host machine and write output files back to the host machine.
- --rm: This tells Docker to remove the container when it exits.
- softwaresecurityproject/zap-stable:2.14.0: This is the Docker image name and version to use.
- zap-baseline.py: This is the command to run inside the container. It runs a Python script named zap-baseline.py that performs a baseline scan of the specified URL.
- -t https://prod-p30jrhut.lab.practical-devsecops.training: This specifies the URL to scan.
- -J zap-output.json: This tells ZAP to output the scan results to a JSON file named zap-output.json in the container's /zap/wrk directory.

You can verify the existence of the output file with `cat zap-output.json command | jq`



