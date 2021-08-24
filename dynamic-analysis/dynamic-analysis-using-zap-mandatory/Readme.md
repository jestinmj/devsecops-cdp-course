Learn how to run ZAP to find security issues
================================================================

In this scenario, you will learn how to use ZAP to scan a website for security issues.

OWASP Zed Attack Proxy tool
--------------

> ZAP is an open-source web application security scanner to perform security testing (Dynamic Testing) on web applications. OWASP ZAP is the flagship OWASP project used extensively by penetration testers. ZAP can also run in a daemon mode for hands-off scans for CI/CD pipeline. ZAP provides extensive API (SDK) and a REST API to help users create custom scripts.
>
> Source: [OWASP ZAP](https://www.zaproxy.org/getting-started/)

In this exercise, we will use ZAP Baseline Scan to find security issues passively.

First, we need to pull ZAP’s stable docker image.

```
docker pull owasp/zap2docker-stable
docker run --rm owasp/zap2docker-stable zap-baseline.py --help
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
2021-08-19 09:22:37,326 Could not find custom hooks file at /home/zap/.zap_hooks.py 
Aug 19, 2021 9:22:41 AM java.util.prefs.FileSystemPreferences$1 run
INFO: Created user preferences directory.
Total of 5 URLs
PASS: Vulnerable JS Library [10003]
PASS: Cookie No HttpOnly Flag [10010]
PASS: Cookie Without Secure Flag [10011]
PASS: Content-Type Header Missing [10019]
PASS: X-Frame-Options Header [10020]
PASS: Information Disclosure - Debug Error Messages [10023]
PASS: Information Disclosure - Sensitive Information in URL [10024]
PASS: Information Disclosure - Sensitive Information in HTTP Referrer Header [10025]
PASS: HTTP Parameter Override [10026]
PASS: Information Disclosure - Suspicious Comments [10027]
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
PASS: Absence of Anti-CSRF Tokens [10202]
PASS: Private IP Disclosure [2]
PASS: Session ID in URL Rewrite [3]
PASS: Script Passive Scan Rules [50001]
PASS: Insecure JSF ViewState [90001]
PASS: Charset Mismatch [90011]
PASS: Application Error Disclosure [90022]
PASS: WSDL File Detection [90030]
PASS: Loosely Scoped Cookie [90033]
WARN-NEW: Incomplete or No Cache-control Header Set [10015] x 1 
        https://prod-XqiHnDZ0.lab.practical-devsecops.training (200 OK)
WARN-NEW: Cross-Domain JavaScript Source File Inclusion [10017] x 1 
        https://prod-XqiHnDZ0.lab.practical-devsecops.training (200 OK)
WARN-NEW: X-Content-Type-Options Header Missing [10021] x 1 
        https://prod-XqiHnDZ0.lab.practical-devsecops.training (200 OK)
WARN-NEW: Strict-Transport-Security Header Not Set [10035] x 3 
        https://prod-XqiHnDZ0.lab.practical-devsecops.training/robots.txt (404 NOT FOUND)
        https://prod-XqiHnDZ0.lab.practical-devsecops.training (200 OK)
        https://prod-XqiHnDZ0.lab.practical-devsecops.training/sitemap.xml (404 NOT FOUND)
WARN-NEW: Server Leaks Version Information via "Server" HTTP Response Header Field [10036] x 3 
        https://prod-XqiHnDZ0.lab.practical-devsecops.training/robots.txt (404 NOT FOUND)
        https://prod-XqiHnDZ0.lab.practical-devsecops.training (200 OK)
        https://prod-XqiHnDZ0.lab.practical-devsecops.training/sitemap.xml (404 NOT FOUND)
WARN-NEW: Content Security Policy (CSP) Header Not Set [10038] x 3 
        https://prod-XqiHnDZ0.lab.practical-devsecops.training/robots.txt (404 NOT FOUND)
        https://prod-XqiHnDZ0.lab.practical-devsecops.training (200 OK)
        https://prod-XqiHnDZ0.lab.practical-devsecops.training/sitemap.xml (404 NOT FOUND)
WARN-NEW: Secure Pages Include Mixed Content (Including Scripts) [10040] x 1 
        https://prod-XqiHnDZ0.lab.practical-devsecops.training (200 OK)
FAIL-NEW: 0     FAIL-INPROG: 0  WARN-NEW: 7     WARN-INPROG: 0  INFO: 0 IGNORE: 0       PASS: 46
```
If you want the output in JSON format, you can use the -J option.

```
docker run --user $(id -u):$(id -g) -w /zap -v $(pwd):/zap/wrk:rw --rm owasp/zap2docker-stable zap-baseline.py -t https://prod-XqiHnDZ0.lab.practical-devsecops.training -J zap-output.json
```

The zap-output.json file is in the current directory. You can verify the existence of the output file with ls -l command.

In the next exercise, we will integrate ZAP Baseline Scan into the CI/CD pipeline.

