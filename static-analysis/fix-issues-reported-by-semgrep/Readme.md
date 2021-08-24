Fix the issues reported by SAST tools
============================================================================

We will learn how to fix the issues reported by Semgrep tools
--------------------------------------------------------------------------------

In this scenario, you will learn how to fix issues reported by the semgrep tool in Django source code.

You will do the following in this activity.
1. Download the source code from the git repository.
2. Install the Semgrep tool.
3. Run the SAST scan on the code.
4. Fix the issues found by Semgrep.

Download the source code
----------
We will do all the exercises locally first in DevSecOps-Box, so lets start the activity.

First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/dvpa webapp
cd webapp
```

Installing Semgrep
----------
```
pip3 install semgrep
```

Run the scanner
----------
Before we run semgrep, we need to create the rules file, semgrep_rules.yaml. These rules will help us find vulnerabilities in the code. You can use any text editor to create this file with the following content.

```
rules:
- id: avoid-pyyaml-load
  metadata:
    owasp: 'A8: Insecure Deserialization'
    cwe: 'CWE-502: Deserialization of Untrusted Data'
    references:
    - https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
    - https://nvd.nist.gov/vuln/detail/CVE-2017-18342
  languages:
  - python
  message: |
    Avoid using `load()`. `PyYAML.load` can create arbitrary Python
    objects. A malicious actor could exploit this to run arbitrary
    code. Use `safe_load()` instead.
  fix: yaml.safe_load($FOO)
  severity: ERROR
  patterns:
  - pattern-inside: |
      import yaml
      ...
      yaml.load($FOO)
  - pattern: yaml.load($FOO)

- id: possible-sqli
  metadata:
    owasp: 'A1: Injection'
    references:
    - https://owasp.org/www-community/attacks/SQL_Injection
  languages:
  - python
  message: |
    Possible SQL Injection
  severity: WARNING
  patterns:
  - pattern: $X.execute(...)
  - pattern-not: $X.execute(..., [...])
  - pattern-not: $X.execute("...")
```

In the above file, we have created rules to find Insecure Deserialization and SQL Injection attacks. Let’s run the Semgrep tool against the current working directory.

```
semgrep -f semgrep_rules.yaml .
```
output
```
running 2 rules...
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████|2/2
flaskblog/auth.py
severity:warning rule:possible-sqli: Possible SQL Injection

14:    cur.execute(f"SELECT * FROM users WHERE email='{username}' AND password='{hashsed_password}'")

flaskblog/dashboard/post.py
severity:error rule:avoid-pyyaml-load: Avoid using `load()`. `PyYAML.load` can create arbitrary Python
objects. A malicious actor could exploit this to run arbitrary
code. Use `safe_load()` instead.

autofix: yaml.safe_load(import_data)
204:                import_post_data = yaml.load(import_data)
--------------------------------------------------------------------------------
severity:warning rule:possible-sqli: Possible SQL Injection

60:            cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")

flaskblog/user.py
severity:warning rule:possible-sqli: Possible SQL Injection

57:        cur.execute(
58:            f"INSERT INTO users (`email`, `full_name`, `password`) VALUES ('{email}', '{full_name}', '{hashed_pas
sword}')")

flaskblog/views.py
severity:warning rule:possible-sqli: Possible SQL Injection

37:        cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")
--------------------------------------------------------------------------------
68:        cur.execute(f"SELECT * FROM posts WHERE title LIKE '%{query}%'")
ran 2 rules on 15 files: 6 findings
```

We got 6 findings, one insecure deserialization, and five SQL Injections. We must fix all of these issues to keep this app secure.

Fixing Insecure Deserialization
---------------------------------

Python yaml library has a known vulnerability around YAML deserialization. We can search for this known security issue on the [CVE website.](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=python%20yaml)

For more details, please visit [CVE-2020-1747](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-1747). As mentioned before, our code is vulnerable to [Deserialization Attacks.](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)

If you recall, one of the findings in the previous step was unsafe YAML load, and the following was the code snippet for the same.

```
flaskblog/dashboard/post.py
severity:error rule:avoid-pyyaml-load: Avoid using `load()`. `PyYAML.load` can create arbitrary Python
objects. A malicious actor could exploit this to run arbitrary
code. Use `safe_load()` instead.

204:                import_post_data = yaml.load(import_data)
--------------------------------------------------------------------------------
autofix: yaml.safe_load(import_data)
```
Lets verify this issue exists by opening up the flaskblog/dashboard/post.py file using any text editor like vim or nano. Ensure the security issue exists at line 204 and the program uses the insecure yaml.load function. To fix this issue, we need to replace yaml.load with a safe alternative yaml.safe_load.

Let’s run the semgrep scanner once again

```
semgrep -f semgrep_rules.yaml .
```
output
```
running 2 rules...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████|2/2
flaskblog/auth.py
severity:warning rule:possible-sqli: Possible SQL Injection

14:    cur.execute(f"SELECT * FROM users WHERE email='{username}' AND password='{hashsed_password}'")

flaskblog/dashboard/post.py
severity:warning rule:possible-sqli: Possible SQL Injection

60:            cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")

flaskblog/user.py
severity:warning rule:possible-sqli: Possible SQL Injection

57:        cur.execute(
58:            f"INSERT INTO users (`email`, `full_name`, `password`) VALUES ('{email}', '{full_name}', '{hashed_pa
ssword}')")

flaskblog/views.py
severity:warning rule:possible-sqli: Possible SQL Injection

37:        cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")
--------------------------------------------------------------------------------
68:        cur.execute(f"SELECT * FROM posts WHERE title LIKE '%{query}%'")
ran 2 rules on 15 files: 5 findings
```

As you can see, there is no yaml.load issue in the output. The total issue count has decreased from 6 to 5.

Fixing SQL Injection Issue
----------
Apart from Insecure Deserializatio issue, there were five possible SQL Injection issues as well. We can fix these issues in various ways, but the best way to fix SQL Injection issues is Parameterized queries, also known as Parameter Binding.

```
running 2 rules...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████|2/2
flaskblog/auth.py
severity:warning rule:possible-sqli: Possible SQL Injection

14:    cur.execute(f"SELECT * FROM users WHERE email='{username}' AND password='{hashsed_password}'")
severity:warning rule:possible-sqli: Possible SQL Injection

60:            cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")

flaskblog/user.py
severity:warning rule:possible-sqli: Possible SQL Injection

57:        cur.execute(
58:            f"INSERT INTO users (`email`, `full_name`, `password`) VALUES ('{email}', '{full_name}', '{hashed_password}')")

flaskblog/views.py
severity:warning rule:possible-sqli: Possible SQL Injection

37:        cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")
--------------------------------------------------------------------------------
68:        cur.execute(f"SELECT * FROM posts WHERE title LIKE '%{query}%'")
ran 2 rules on 15 files: 6 findings
```
First, we will try to fix the SQL Injection issue present in the flaskblog/auth.py file at line number 14. As you can see in the following code snippet, there is a SQL injection issue in the check_auth function.

```
def check_auth(username, password):
   """ This function is called to check if a username / password
       combination is valid.
   """
   cur = db.connection.cursor()
   hashsed_password = hashlib.md5(password.encode()).hexdigest()
   cur.execute(f"SELECT * FROM users WHERE email='{username}' AND password='{hashsed_password}'")
   user = cur.fetchone()

   if user is None:
      return False

   session["is_logged_in"] = True
   session["id"] = user.get("id")
   session["email"] = user.get("email")
   session["full_name"] = user.get("full_name")

   return user
```
The cur.execute function call will execute the SQL query on the database. It takes the username and password as possible inputs to the SQL query.

You can also verify this behavior dynamically by reproducing SQL query errors.

> Learn more about SQL Injection [here.](https://portswigger.net/web-security/sql-injection)

You can replace line number 14 with the following code. This code will fix the SQL Injection issue.

```
cur.execute(f"SELECT * FROM users WHERE email=%s AND password=%s", [username, hashsed_password ])
```
Then, rerun the scanner
```
semgrep -f semgrep_rules.yaml .
```
output
```
running 2 rules...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████|2/2
flaskblog/dashboard/post.py
severity:warning rule:possible-sqli: Possible SQL Injection

60:            cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")

flaskblog/user.py
severity:warning rule:possible-sqli: Possible SQL Injection

57:        cur.execute(
58:            f"INSERT INTO users (`email`, `full_name`, `password`) VALUES ('{email}', '{full_name}', '{hashed_password}')")

flaskblog/views.py
severity:warning rule:possible-sqli: Possible SQL Injection

37:        cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")
--------------------------------------------------------------------------------
68:        cur.execute(f"SELECT * FROM posts WHERE title LIKE '%{query}%'")
ran 2 rules on 15 files: 4 findings
```
As you can see(the last line), semgrep found only 4 issues. Great!

Exercise
----------

1. Please fix all SQL Injection issues, and use the semgrep tool to cross-check vulnerability fix

> Please do not forget to share the answer with our staff via Slack Direct Message (DM).

