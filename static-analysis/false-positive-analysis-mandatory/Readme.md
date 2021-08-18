False Positive Analysis
================================

We will learn how to do false positive analysis on reported issues by bandit tool
---------

In this scenario, you will learn how to do False Positive Analysis (FPA) on the Bandit tool’s reported issues.

Download the source code
----------
We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/dvpa-api webapp
cd webapp
```

Installing Bandit
----------
Let’s install the bandit scanner on the system to perform static analysis.

```
pip3 install bandit
```
We have successfully installed the bandit scanner. Let’s explore the functionality it provides us.

```
bandit --help

usage: bandit [-h] [-r] [-a {file,vuln}] [-n CONTEXT_LINES] [-c CONFIG_FILE]
              [-p PROFILE] [-t TESTS] [-s SKIPS] [-l] [-i]
              [-f {csv,custom,html,json,screen,txt,xml,yaml}]
              [--msg-template MSG_TEMPLATE] [-o [OUTPUT_FILE]] [-v] [-d] [-q]
              [--ignore-nosec] [-x EXCLUDED_PATHS] [-b BASELINE]
              [--ini INI_PATH] [--version]
              [targets [targets ...]]

Bandit - a Python source code security analyzer

positional arguments:
  targets               source file(s) or directory(s) to be tested

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       find and process files in subdirectories
  -a {file,vuln}, --aggregate {file,vuln}
                        aggregate output by vulnerability (default) or by
                        filename
  -n CONTEXT_LINES, --number CONTEXT_LINES
                        maximum number of code lines to output for each issue
  -c CONFIG_FILE, --configfile CONFIG_FILE
                        optional config file to use for selecting plugins and
                        overriding defaults
  -p PROFILE, --profile PROFILE
                        profile to use (defaults to executing all tests)
  -t TESTS, --tests TESTS
                        comma-separated list of test IDs to run
  -s SKIPS, --skip SKIPS
                        comma-separated list of test IDs to skip
  -l, --level           report only issues of a given severity level or higher
                        (-l for LOW, -ll for MEDIUM, -lll for HIGH)
  -i, --confidence      report only issues of a given confidence level or
                        higher (-i for LOW, -ii for MEDIUM, -iii for HIGH)
  -f {csv,custom,html,json,screen,txt,xml,yaml}, --format {csv,custom,html,json,screen,txt,xml,yaml}
                        specify output format
  --msg-template MSG_TEMPLATE
                        specify output message template (only usable with
                        --format custom), see CUSTOM FORMAT section for list
                        of available values
  -o [OUTPUT_FILE], --output [OUTPUT_FILE]
                        write report to filename
  -v, --verbose         output extra information like excluded and included
                        files
  -d, --debug           turn on debug mode
  -q, --quiet, --silent
                        only show output in the case of an error
  --ignore-nosec        do not skip lines with # nosec comments
  -x EXCLUDED_PATHS, --exclude EXCLUDED_PATHS
                        comma-separated list of paths (glob patterns
                        supported) to exclude from scan (note that these are
                        in addition to the excluded paths provided in the
                        config file)
  -b BASELINE, --baseline BASELINE
                        path of a baseline report to compare against (only
                        JSON-formatted files are accepted)
  --ini INI_PATH        path to a .bandit file that supplies command line
                        arguments
  --version             show program's version number and exit
```

Run the scanner
----------

Let’s scan our source code by executing the following command:

```
bandit -r .
```
output

```
[main]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: None
[main]  INFO    running on Python 3.6.9
Run started:2021-02-18 04:17:07.695129

Test results:
>> Issue: [B303:blacklist] Use of insecure MD2, MD4, MD5, or SHA1 hash function.
   Severity: Medium   Confidence: High
   Location: ./flaskblog/auth.py:13
   More Info: https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b303-md5
12          cur = db.connection.cursor()
13          hashsed_password = hashlib.md5(password.encode()).hexdigest()
14          cur.execute(f"SELECT * FROM users WHERE email='{username}' AND password='{hashsed_password}'")

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./flaskblog/auth.py:14
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
13          hashsed_password = hashlib.md5(password.encode()).hexdigest()
14          cur.execute(f"SELECT * FROM users WHERE email='{username}' AND password='{hashsed_password}'")
15          user = cur.fetchone()

--------------------------------------------------
>> Issue: [B303:blacklist] Use of insecure MD2, MD4, MD5, or SHA1 hash function.
   Severity: Medium   Confidence: High
   Location: ./flaskblog/blogapi/dashboard.py:67
   More Info: https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b303-md5
66
67              hashed_password = hashlib.md5(password1.encode()).hexdigest()
68

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./flaskblog/blogapi/dashboard.py:85
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
84              cur = db.connection.cursor()
85              cur.execute(f"SELECT * FROM users WHERE id={request.args.get('uid')}")
86              user = cur.fetchone()

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./flaskblog/blogapi/dashboard.py:100
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
99              cur = db.connection.cursor()
100             cur.execute(f"UPDATE `users` SET `email` = '{email}', `full_name` = '{full_name}', `phone_number` = '{phone_number}', `dob` = '{dob}' WHERE `users`.`id` = {request.args.get('uid')}")
101             db.connection.commit()

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./flaskblog/blogapi/dashboard.py:133
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
132             cur.execute(
133                 f"INSERT INTO posts (`body`, `slug`, `author`, `title`) VALUES (%s, %s, %s, %s)",
134                 [body, slug, claim.get("id"), title])

--------------------------------------------------
>> Issue: [B506:yaml_load] Use of unsafe yaml load. Allows instantiation of arbitrary objects. Consider yaml.safe_load().
   Severity: Medium   Confidence: High
   Location: ./flaskblog/blogapi/dashboard.py:248
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b506_yaml_load.html
247                 elif export_format == "yaml":
248                     import_post_data = yaml.load(import_data)
249

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./flaskblog/blogapi/home.py:26
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
25              cur = db.connection.cursor()
26              cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")
27              post = cur.fetchone()

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./flaskblog/blogapi/home.py:49
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
48              cur = db.connection.cursor()
49              cur.execute(f"SELECT * FROM posts WHERE title LIKE '%{query}%'")
50              search_posts = cur.fetchall() #Post.objects(title__icontains=query)

--------------------------------------------------
>> Issue: [B303:blacklist] Use of insecure MD2, MD4, MD5, or SHA1 hash function.
   Severity: Medium   Confidence: High
   Location: ./flaskblog/blogapi/user.py:71
   More Info: https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b303-md5
70
71              hashed_password = hashlib.md5(password.encode()).hexdigest()
72              cur = db.connection.cursor()

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./flaskblog/blogapi/user.py:74
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
73              cur.execute(
74                  f"INSERT INTO users (`email`, `full_name`, `password`) VALUES ('{email}', '{full_name}', '{hashed_password}')")
75              db.connection.commit()

--------------------------------------------------
>> Issue: [B105:hardcoded_password_string] Possible hardcoded password: 'flaskblog_secret_key'
   Severity: Low   Confidence: Medium
   Location: ./flaskblog/config.py:4
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b105_hardcoded_password_string.html
3       MONGODB_SETTINGS = 'flaskblog_db'
4       SECRET_KEY = 'flaskblog_secret_key'
5
6       # Debugging & Reloader
7       debugger = True

--------------------------------------------------
>> Issue: [B105:hardcoded_password_string] Possible hardcoded password: 'secret'
   Severity: Low   Confidence: Medium
   Location: ./flaskblog/config.py:13
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b105_hardcoded_password_string.html
12      username = 'admin'
13      password = 'secret'
14
15      # Disqus Configuration
16      disqus_shortname = 'blogpythonlearning'  # please change this.

--------------------------------------------------

Code scanned:
        Total lines of code: 603
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0.0
                Low: 2.0
                Medium: 11.0
                High: 0.0
        Total issues (by confidence):
                Undefined: 0.0
                Low: 0.0
                Medium: 9.0
                High: 4.0
Files skipped (0):
```

We got 13 issues in total (by severity), but we need to exclude the False Positives.

False Positive Analysis (FPA)
--------------------------------

There are two ways to do the False Positive Analysis. Either by reading the source code or by exploiting the vulnerability. In this exercise, we only cover the first way.

As per Bandit’s scan results, we have hardcoded password strings, an insecure hash function issue, an insecure deserialization issue, and SQL injection vulnerability.

Let’s try to analyze if they are real issues or false positives. We will try to explore the following three issues among them.

output
```
--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: dvpa-api/flaskblog/blogapi/dashboard.py:99
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
98              cur = db.connection.cursor()
99              cur.execute(f"UPDATE `users` SET `email` = '{email}', `full_name` = '{full_name}', `phone_number` = '{phone_number}', `dob` = '{dob}' WHERE `users`.`id` = {request.args.get('uid')}")
100             db.connection.commit()

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: dvpa-api/flaskblog/blogapi/dashboard.py:132
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
131             cur.execute(
132                 f"INSERT INTO posts (`body`, `slug`, `author`, `title`) VALUES (%s, %s, %s, %s)",
133                 [body, slug, claim.get("id"), title])

--------------------------------------------------
>> Issue: [B506:yaml_load] Use of unsafe yaml load. Allows instantiation of arbitrary objects. Consider yaml.safe_load().
   Severity: Medium   Confidence: High
   Location: dvpa-api/flaskblog/blogapi/dashboard.py:242
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b506_yaml_load.html
241                 elif export_format == "yaml":
242                     import_post_data = yaml.load(import_data)
243
```

Analysis of the issues
----------
Let’s explore the first issue now.
```
98              cur = db.connection.cursor()
99              cur.execute(f"UPDATE `users` SET `email` = '{email}', `full_name` = '{full_name}', `phone_number` = '{phone_number}', `dob` = '{dob}' WHERE `users`.`id` = {request.args.get('uid')}")
100             db.connection.commit()
```

It looks like the above code is vulnerable to SQL Injection because uid is used in the query directly, so it’s not a False Positive.

Next, lets check out the second result.

```
131             cur.execute(
132                 f"INSERT INTO posts (`body`, `slug`, `author`, `title`) VALUES (%s, %s, %s, %s)",
133                 [body, slug, claim.get("id"), title])
```

The above code is definitely False Positive as we are using Parameter Binding to [create](https://www.mysqltutorial.org/sql-concat-in-mysql.aspx/) the query.

And the last one is a known vulnerability in Python’s YAML library called YAML deserialization. We can search for this known security issue on the [CVE website](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=python%20yaml).

```
241                 elif export_format == "yaml":
242                     import_post_data = yaml.load(import_data)
243
```
For more details about this issue, please visit [CVE-2020-1747](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-1747).

As mentioned before, our code is vulnerable to [Deserialization Attacks](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html) and we can mark this as not a False Positive.

Exercise
---------
1. Analyse the results and mark relevant issues as False Positive
2. Use Bandit feature to perform False Positive as Code

> Hint
>
> Checkout -b baseline.json to mark issues as False Positives.
> You can consume the bandit’s output from earlier scan to mark issues as False Positives.
> If you are still unsure, please try passing the bandit’s output to -b and see what happens.

Additional Resources
--------------------------------

For more information about False Positives in AppSec, see the following references:

- https://dev.to/johspaeth/the-myth-of-false-positives-in-static-application-security-testing-146g
- https://www.netsparker.com/false-positives-in-application-security-whitepaper
- https://www.synopsys.com/blogs/software-security/avoiding-false-positives
- https://www.contrastsecurity.com/security-influencers/accuracy-in-appsec-critical-reduce-false-positives
