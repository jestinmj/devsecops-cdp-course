Hunting vulnerability with Semgrep
================================================================

We will learn how to find the vulnerabilities with a custom rule in Semgrep
----------------------------------------------------------------

In this scenario, you will learn how to use Semgrep to perform static code analysis.

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.
First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp
```
Let’s cd into the application so we can scan the app.
```
cd webapp
```

Installing Semgrep
----------

```
pip3 install semgrep
```

Cross-Site Request Forgery (CSRF)
--------------------------------
Django applications would be vulnerable to CSRF attack if we’re using csrf_exempt decorator or django.middleware.csrf.CsrfViewMiddleware middleware is not set in MIDDLEWARE_CLASSES, we can use Semgrep to find those things to mitigate the CSRF vulnerability.

```
cat > csrf_hunting.yaml <<EOF
rules:
- id: possible-csrf
  patterns:
  - pattern-inside: | 
      @csrf_exempt
      def \$FUNC(\$X):
          ...
  message: |
    Possible CSRF
  languages:
  - python
  severity: WARNING

- id: no-csrf-middleware
  patterns:
  - pattern: MIDDLEWARE_CLASSES=(...)
  - pattern-not: MIDDLEWARE_CLASSES=(...,'django.middleware.csrf.CsrfViewMiddleware',...)
  message: |
    No CSRF middleware
  languages:
  - python
  severity: WARNING
EOF
```

There are 2 rules in YAML file.

1. possible-csrf: Find all function definitions that use @csrf_exempt as decorator
2. no-csrf-middleware: Search the string MIDDLEWARE_CLASSES and see if doesn’t have ‘django.middleware.csrf.CsrfViewMiddleware’ on it

Run Semgrep with our rules against the source code.

```
semgrep --lang python -f csrf_hunting.yaml .
```
output
```
running 2 rules...
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████|2/2
taskManager/views.py
severity:warning rule:possible-csrf: Possible CSRF

739:@csrf_exempt
740:def reset_password(request):
741:
742:    if request.method == 'POST':
743:
744:        reset_token = request.POST.get('reset_token')
745:
746:        try:
747:            userprofile = UserProfile.objects.get(reset_token = reset_token)
748:            if timezone.now() > userprofile.reset_token_expiration:
-------- [hid 27 additional lines, adjust with --max-lines-per-finding] --------
779:@csrf_exempt
780:def forgot_password(request):
781:
782:    if request.method == 'POST':
783:        t_email = request.POST.get('email')
784:
785:        try:
786:            reset_user = User.objects.get(email=t_email)
787:
788:            # Generate secure random 6 digit number
-------- [hid 21 additional lines, adjust with --max-lines-per-finding] --------
813:@csrf_exempt
814:def change_password(request):
815:
816:    if request.method == 'POST':
817:        user = request.user
818:        old_password = request.POST.get('old_password')
819:        new_password = request.POST.get('new_password')
820:        confirm_password = request.POST.get('confirm_password')
821:
822:        if authenticate(username=user.username, password=old_password):
-------- [hid 12 additional lines, adjust with --max-lines-per-finding] --------
ran 2 rules on 50 files: 3 findings
```

As you can see, we found three functions where CSRF vulnerability can be exploited.

Misconfigurations
----------

> Security misconfiguration is a class of vulnerability that occurs when the software is set up incorrectly, left insecure and can happen at any level of an application stack including the platform, web server, application server, database, framework, or any custom code.
>
> Source: [OWASP Top 10](https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration)

Let’s create a rule to hunt misconfigurations in our application e.g., availability of DEBUG=True flag in `settings.py` file.

```
cat > debug_enable.yaml <<EOF 
rules:
- id: debug-enabled
  patterns:
  - pattern: DEBUG=True
  message: |
    Detected Django app with DEBUG=True. Do not deploy to production with this flag enabled
    as it will leak sensitive information.
  metadata:
    cwe: 'CWE-489: Active Debug Code'
    owasp: 'A6: Security Misconfiguration'
    references:
    - https://blog.scrt.ch/2018/08/24/remote-code-execution-on-a-facebook-server/
  severity: WARNING
  languages:
  - python
EOF
```
Run Semgrep with our rules in the source code.
```
semgrep --lang python -f debug_enable.yaml .
```
output
```
running 1 rules...
taskManager/settings.py
severity:warning rule:debug-enabled: Detected Django app with DEBUG=True. Do not deploy to production with this flag
 enabled
as it will leak sensitive information.

28:DEBUG = True
ran 1 rules on 50 files: 1 findings
```
We scanned about 51 files and found 1 security issue.

Ported Security Tools Ruleset
----------

Semgrep’s team converted the security rulesets from different tools like bandit, gosec, nodejsscan, findsecbugs, or eslint-plugin-security into Semgrep rules. Let use these rulesets to scan our application.

We will use the Bandit ruleset for semgrep in this section.

```
semgrep --config "p/bandit" .
```
output
```
using config from https://semgrep.dev/p/bandit. Visit https://semgrep.dev/registry to see all public rules.
downloading config...
running 61 rules...
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████|61/61
taskManager/misc.py
severity:warning rule:python.lang.security.audit.dangerous-system-call.dangerous-system-call: Found dynamic content 
used in a system call. This is dangerous if external data can reach this function call because it allows a malicious
 actor to execute commands. Use the 'subprocess' module instead, which is easier to use without accidentally exposin
g a command injection vulnerability.
33:    os.system(
34:        "mv " +
35:        uploaded_file.temporary_file_path() +
36:        " " +
37:        "%s/%s" %
38:        (upload_dir_path,
39:         title))

taskManager/views.py
severity:warning rule:python.lang.security.audit.formatted-sql-query.formatted-sql-query: Detected possible formatted SQL query. Use parameterized queries instead.

183:            curs.execute(
184:                "insert into taskManager_file ('name','path','project_id') values ('%s','%s',%s)" %
185:                (name, upload_path, project_id))
ran 61 rules on 50 files: 2 findings
```

Semgrep ran 60 rules from bandit rulesets and found 1 vulnerability, so we don’t rely on predefined rules.

Did it miss any vulnerabilities which bandit found? If so, why?

Exercise
---------

1. Write a semgrep rule to detect Insecure Redirect in the following code snippet
```
def logout_view(request):
    logout(request)
    return redirect(request.GET.get('redirect', '/taskManager/'))
```

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).




