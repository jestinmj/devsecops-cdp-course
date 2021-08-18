Fix the issues reported by SAST tools
================================================================================

We will learn how to fix the issues reported by bandit tools
--------------------------------------------------------------------------------

In this scenario, you will learn how to fix issues reported by the Bandit tool in python source code.

You will do the following in this activity.
1. Download the source code from the git repository.
2. Install the Bandit tool.
3. Run the SAST scan on the code.
4. Fix the issues found by Bandit.

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

> The Bandit is a tool designed to find common security issues in Python code.
>
>To do this Bandit, processes each file, builds an AST, and runs appropriate plugins against the AST nodes. Once Bandit has finished scanning all the files, it generates a report.
>
> Bandit was originally developed within the OpenStack Security Project and later rehomed to PyCQA.
>
>You can find more details about the project at https://github.com/PyCQA/bandit.


Let’s install the bandit scanner on the system to perform static analysis.

```
pip3 install bandit
```

We have successfully installed the bandit scanner. Let’s explore the functionality it provides us.

```
bandit --help
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
Run started:2021-08-16 02:43:18.602029

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
                *Medium: 9.0
                *High: 4.0
Files skipped (0):
```

We got 13 issues in total (by confidence). Among these, there are two(2) hardcoded password strings, an insecure hash function issue, insecure deserialization, and 8 SQL Injections. We must fix all these issues in order to avoid security breaches in our organization.

Fixing Insecure Deserialization
----------------------------------

Python yaml library has a known vulnerability around YAML deserialization. We can search for this known security issue on the [CVE website](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=python%20yaml)

For more details, please visit [CVE-2020-1747](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-1747). As mentioned before, our code is vulnerable to [Deserialization Attacks](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html).

If you recall, one of the findings in the previous step was unsafe YAML load, and the following was the code snippet for the same.

```
--------------------------------------------------
>> Issue: [B506:yaml_load] Use of unsafe yaml load. Allows instantiation of arbitrary objects. Consider yaml.safe_load().
   Severity: Medium   Confidence: High
   Location: ./blogapi/dashboard.py:248
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b506_yaml_load.html
247                 elif export_format == "yaml":
248                     import_post_data = yaml.load(import_data)
```

Let’s verify this issue exists by opening up the flaskblog/blogapi/dashboard.py file using any text editor like vim or nano. Ensure the security issue exists at line 248 and the program uses the insecure yaml.load function. To fix this issue, we need to replace yaml.load with a safe alternative yaml.safe_load.

Let’s run the scanner once again.

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
Run started:2021-08-16 02:51:12.973690

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
                Medium: 10.0
                High: 0.0
        Total issues (by confidence):
                Undefined: 0.0
                Low: 0.0
                Medium: 9.0
                High: 3.0
Files skipped (0):
```
As you can see, there is no yaml.load issue in the output. The total High issue count (by confidence) has decreased from 4 to 3.

Fixing SQL Injection
---------------------------------

Bandit also informed us that there are 7 possible SQL Injection issues in this application. We can fix these issues in various ways, but the best way to fix SQL Injection issues is Parameterized queries, also known as Parameter Binding.

```
ain]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: None
[main]  INFO    running on Python 3.8.5
Run started:2021-01-24 08:39:43.777107

Test results:
--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./auth.py:14
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
13          hashsed_password = hashlib.md5(password.encode()).hexdigest()
14          cur.execute(f"SELECT * FROM users WHERE email='{username}' AND password='{hashsed_password}'")
15          user = cur.fetchone()

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./blogapi/dashboard.py:85
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
84              cur = db.connection.cursor()
85              cur.execute(f"SELECT * FROM users WHERE id={request.args.get('uid')}")
86              user = cur.fetchone()

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./blogapi/dashboard.py:100
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
99              cur = db.connection.cursor()
100             cur.execute(f"UPDATE `users` SET `email` = '{email}', `full_name` = '{full_name}', `phone_number` = '{phone_number}', `dob` = '{dob}' WHERE `users`.`id` = {request.args.get('uid')}")
101             db.connection.commit()

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./blogapi/dashboard.py:133
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
132             cur.execute(
133                 f"INSERT INTO posts (`body`, `slug`, `author`, `title`) VALUES (%s, %s, %s, %s)",
134                 [body, slug, claim.get("id"), title])

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./blogapi/home.py:26
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
25              cur = db.connection.cursor()
26              cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")
27              post = cur.fetchone()

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./blogapi/home.py:49
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
48              cur = db.connection.cursor()
49              cur.execute(f"SELECT * FROM posts WHERE title LIKE '%{query}%'")
50              search_posts = cur.fetchall() #Post.objects(title__icontains=query)

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   Location: ./blogapi/user.py:74
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html
73              cur.execute(
74                  f"INSERT INTO users (`email`, `full_name`, `password`) VALUES ('{email}', '{full_name}', '{hashed_password}')")
75              db.connection.commit()

...[SNIP]...
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

> You can learn more about SQL Injection [here](https://portswigger.net/web-security/sql-injection).


You can replace line number 14 with the following code. This code will fix the SQL Injection issue.

```
cur.execute(f"SELECT * FROM users WHERE email=%s AND password=%s", [username, hashsed_password ])
```

Then, re-run the bandit scanner.

```
bandit -r .
```

There’s no change in the output even after fixing this issue; hence this is a False Positive.

Exercise
1. Please fix all SQL Injection issues, and use the bandit tool to cross-check the fixes
2. Mark the findings as False Positive if you think so
