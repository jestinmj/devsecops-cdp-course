Software Component Analysis using Safety
============================================================================

Learn to scan python dependencies for vulnerabilities using Safety
------------------------------------------------------------------------------

In this scenario, you will learn how to install the Safety tool against a git repository.

You will need to download the code, install the OAST tool, and then finally run the OAST scan on the code

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp
cd webapp
```

Install Safety Tool
----------

> Safety checks your installed dependencies for known security vulnerabilities.
>
> By default, it uses the open Python vulnerability database Safety DB but can be upgraded to use pyup.io’s Safety API using the –key option.
>
> Source: [Safety Website.](https://pypi.org/project/safety/)
>
> You can find more details about the project at [Safety](https://github.com/pyupio/safety).

Let’s install the safety tool on the system to scan the python dependencies.

```
pip3 install safety
safety check --help
```
Run the Scanner
----------

As we have learned in the DevSecOps Gospel, we should save the output in a machine-readable format.

We are using the tee command to show the output and store it in a file simultaneously.

```
safety check -r requirements.txt --json | tee safety_output.json
```
- -r flag used to specify the input file.
- --json flag tells that output should be in the JSON format.

output

```
[
    [
        "django",
        "<1.11.27",
        "1.8.3",
        "Django before 1.11.27, 2.x before 2.2.9, and 3.x before 3.0.1 allows account takeover. A suitably crafted email address (that is equal to an existing user's email address after case transformation of Unicode characters) would allow an attacker to be sent a password reset token for the matched user account. (One mitigation in the new releases is to send password reset tokens only to the registered user email address.) See CVE-2019-19844.",
        "37771"
    ],
    [
        "django",
        "<1.8.10",
        "1.8.3",
        "The password hasher in contrib/auth/hashers.py in Django before 1.8.10 and 1.9.x before 1.9.3 allows remote attackers to enumerate users via a timing attack involving login requests.",
        "33074"
    ],
    [
        "django",
        "<1.8.10",
        "1.8.3",
        "The utils.http.is_safe_url function in Django before 1.8.10 and 1.9.x before 1.9.3 allows remote attackers to redirect users to arbitrary web sites and conduct phishing attacks or possibly conduct cross-site scripting (XSS) attacks via a URL containing basic authentication, as demonstrated by http://mysite.example.com\\@attacker.com.",
        "33073"
    ],
    [
        "django",
        "<1.8.15",
        "1.8.3",
        "The cookie parsing code in Django before 1.8.15 and 1.9.x before 1.9.10, when used on a site with Google Analytics, allows remote attackers to bypass an intended CSRF protection mechanism by setting arbitrary cookies.",
        "25718"
    ],
    [
        "django",
        ">=1.8,<1.8.16",
        "1.8.3",
        "Django before 1.8.x before 1.8.16, 1.9.x before 1.9.11, and 1.10.x before 1.10.3, when settings.DEBUG is True, allow remote attackers to conduct DNS rebinding attacks by leveraging failure to validate the HTTP Host header against settings.ALLOWED_HOSTS.",
        "33075"
    ],
    [
        "django",
        ">=1.8,<1.8.16",
        "1.8.3",
        "Django 1.8.x before 1.8.16, 1.9.x before 1.9.11, and 1.10.x before 1.10.3 use a hardcoded password for a temporary database user created when running tests with an Oracle database, which makes it easier for remote attackers to obtain access to the database server by leveraging failure to manually specify a password in the database settings TEST dictionary.",
        "33076"
    ],
    [
        "django",
        ">=1.8,<1.8.18",
        "1.8.3",
        "Django 1.8.18 fixes two security issues in 1.8.17.\r\n\r\nCVE-2017-7233: Open redirect and possible XSS attack via user-supplied numeric redirect URLs\r\n============================================================================================\r\n\r\nDjango relies on user input in some cases  (e.g.\r\n:func:`django.contrib.auth.views.login` and :doc:`i18n </topics/i18n/index>`)\r\nto redirect the user to an \"on success\" URL. The security check for these\r\nredirects (namely ``django.utils.http.is_safe_url()``) considered some numeric\r\nURLs (e.g. ``http:999999999``) \"safe\" when they shouldn't be.\r\n\r\nAlso, if a developer relies on ``is_safe_url()`` to provide safe redirect\r\ntargets and puts such a URL into a link, they could suffer from an XSS attack.\r\n\r\nCVE-2017-7234: Open redirect vulnerability in ``django.views.static.serve()``\r\n=============================================================================\r\n\r\nA maliciously crafted URL to a Django site using the\r\n:func:`~django.views.static.serve` view could redirect to any other domain. The\r\nview no longer does any redirects as they don't provide any known, useful\r\nfunctionality.\r\n\r\nNote, however, that this view has always carried a warning that it is not\r\nhardened for production use and should be used only as a development aid.",
        "33301"
    ],
    [
        "django",
        ">=1.8,<1.8.19",
        "1.8.3",
        "The ``django.utils.html.urlize()`` function was extremely slow to evaluate\r\ncertain inputs due to a catastrophic backtracking vulnerability in a regular\r\nexpression. The ``urlize()`` function is used to implement the ``urlize`` and\r\n``urlizetrunc`` template filters, which were thus vulnerable.\r\n\r\nThe problematic regular expression is replaced with parsing logic that behaves\r\nsimilarly.",
        "35797"
    ],
```