Use TruffleHog to find the secrets inside our source code
==========================================================

Use Trufflehog to find secrets like token, ssh keys, certs, etc.
----------------------------------------------------------------

In this scenario, you will learn how to install and run truffleHog. Trufflehog helps you in finding secrets committed in a git repository.

To achieve the above objectives, you will need to do the following:
1. Clone/download the source code
2. Install the secret scanning tool
3. Run the secret scanner on the code

Download the source code
------------------------
We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp
```

Let’s cd into the application so we can scan the app.

```
cd webapp
```

We are now in the webapp directory or **source code already exist in folder source-code**.

Install TruffleHog
------------------------

> TruflleHog is a tool that searches through git repositories for secrets, digging deep into commit history and branches. This tool is useful in finding the secrets accidentally committed to the repo.
>
> You can find more details about the project at https://github.com/dxa4481/truffleHog.

Let’s install the TruffleHog tool on the system to scan for the secrets in our code.

```
pip3 install trufflehog
```
Let’s explore what options Trufflehog provides us.

```
trufflehog --help
```

```
usage: trufflehog [-h] [--json] [--regex] [--rules RULES] [--allow ALLOW]
                  [--entropy DO_ENTROPY] [--since_commit SINCE_COMMIT]
                  [--max_depth MAX_DEPTH] [--branch BRANCH]
                  [-i INCLUDE_PATHS_FILE] [-x EXCLUDE_PATHS_FILE]
                  [--repo_path REPO_PATH] [--cleanup]
                  git_url

Find secrets hidden in the depths of git.

positional arguments:
  git_url               URL for secret searching

optional arguments:
  -h, --help            show this help message and exit
  --json                Output in JSON
  --regex               Enable high signal regex checks
  --rules RULES         Ignore default regexes and source from json file
  --allow ALLOW         Explicitly allow regexes from json list file
  --entropy DO_ENTROPY  Enable entropy checks
  --since_commit SINCE_COMMIT
                        Only scan from a given commit hash
  --max_depth MAX_DEPTH
                        The max commit depth to go back when searching for
                        secrets
  --branch BRANCH       Name of the branch to be scanned
  -i INCLUDE_PATHS_FILE, --include_paths INCLUDE_PATHS_FILE
                        File with regular expressions (one per line), at least
                        one of which must match a Git object path in order for
                        it to be scanned; lines starting with "#" are treated
                        as comments and are ignored. If empty or not provided
                        (default), all Git object paths are included unless
                        otherwise excluded via the --exclude_paths option.
  -x EXCLUDE_PATHS_FILE, --exclude_paths EXCLUDE_PATHS_FILE
                        File with regular expressions (one per line), none of
                        which may match a Git object path in order for it to
                        be scanned; lines starting with "#" are treated as
                        comments and are ignored. If empty or not provided
                        (default), no Git object paths are excluded unless
                        effectively excluded via the --include_paths option.
  --repo_path REPO_PATH
                        Path to the cloned repo. If provided, git_url will not
                        be used
  --cleanup             Clean up all temporary result files
```

Run the Scanner
---------------

As we have learned in the **DevSecOps Gospel**, we should save the output in the machine-readable format **(CSV, JSON, XML)** so it can be parsed by the machines easily.

We are using the tee command here to show the output and store it in a file simultaneously.

```
trufflehog --json . | tee secret.json
```
- **--json**: tells that output should be in the JSON format

```
#     username = password = ''\n-#     if request.POST:\n-#         username = request.POST.get('username')\n-#         password = request.POST.get('password')\n-\n-#         user = authenticate(username=username, password=password)\n-#         if user is not None:\n-#             if user.is_active:\n-#                 login(request, user)\n-#                 state = \"You're successfully logged in!\"\n-#             else:\n-#                 state = \"Your account is not active, please contact the site admin.\"\n-#         else:\n-#             state = \"Your username and/or password were incorrect.\"\n+def login(request):\n+    state = \"Please log in below...\"\n+    username = password = ''\n+    if request.POST:\n+        username = request.POST.get('username')\n+        password = request.POST.get('password')\n+\n+        user = authenticate(username=username, password=password)\n+        if user is not None:\n+            if user.is_active:\n+                login(request, user)\n+                state = \"You're successfully logged in!\"\n+            else:\n+                state = \"Your account is not active, please contact the site admin.\"\n+        else:\n+            state = \"Your username and/or password were incorrect.\"\n \n-#     return render_to_response('login.html',{'state':state, 'username': username})\n+    return render_to_response('login.html',{'state':state, 'username': username})\n \n \n def proj_details(request, project_id):\n@@ -114,7 +86,15 @@ def the_comments(request, task_id):\n \tresponse = \"You're looking at the comments of question %s.\"\n \treturn HttpResponse(response % task_id)\n \n-def detail(request, task_id, project_id):\n+def detail(request, task_id, foreign_key):\n+\t#try:\n+\tif request.method == 'POST':\n+\t\tform = CommentForm(request.POST)\n+\t\tif form.is_valid():\n+\t\t\treturn HttpResponseRedirect('/thanks/')\n+\t\telse:\n+\t\t\tform = CommentForm()\n+\n \ttask = Task.objects.get(pk = task_id)\n \t#except Task.DoesNotExist:\n \t#\traise Http404\n", "reason": "High Entropy", "stringsFound": ["20821e4abaea95268880f020c9f6768288f3725a"]}
```

Okay, so we got some results from the tool but are these false positives or real issues.

What can we do to improve the situation?

