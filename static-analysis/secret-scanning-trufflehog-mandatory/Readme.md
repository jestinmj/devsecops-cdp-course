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
----- NEW
```
wget https://github.com/trufflesecurity/trufflehog/releases/download/v3.79.0/trufflehog_3.79.0_linux_amd64.tar.gz
tar -xvf trufflehog_3.79.0_linux_amd64.tar.gz
chmod +x trufflehog
mv trufflehog /usr/local/bin/
```
----- OLD
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

TruffleHog has been upgraded to version 3 and written in Golang. It has a feature to scan the repository directly instead of cloning the repository locally, and it also brings authentication when scanning against the repository.

Let’s run the scan on the django.nv project.

`trufflehog git http://gitlab-ce-cxlx0c4v.lab.practical-devsecops.training/root/django-nv.git --json`

```
{"level":"info-0","ts":"2024-07-06T06:29:42Z","logger":"trufflehog","msg":"running source","source_manager_worker_id":"5NutY","with_units":true}
{"level":"info-0","ts":"2024-07-06T06:29:42Z","logger":"trufflehog","msg":"scanning repo","source_manager_worker_id":"5NutY","unit":"/tmp/trufflehog-1541-1960078102","unit_kind":"dir","repo":"http://gitlab-ce-rmaa3gra.lab.practical-devsecops.training/root/django-nv.git"}
{"SourceMetadata":{"Data":{"Git":{"commit":"bf10953956e328f232d444c9ead87da715f18614","file":"taskManager/settings.py","email":"root \u003croot@gitlab-ce-rmaa3gra.lab.practical-devsecops.training\u003e","repository":"http://gitlab-ce-rmaa3gra.lab.practical-devsecops.training/root/django-nv.git","timestamp":"2024-07-06 06:27:24 +0000","line":22}}},"SourceID":1,"SourceType":16,"SourceName":"trufflehog - git","DetectorType":13,"DetectorName":"Slack","DecoderName":"PLAIN","Verified":false,"VerificationError":"unexpected error auth response token_revoked","Raw":"xoxp-4797898847-4799393255-4778181812-f140b6","RawV2":"","Redacted":"","ExtraData":{"rotation_guide":"https://howtorotate.com/docs/tutorials/slack/","token_type":"Slack User Token"},"StructuredData":null}
{"SourceMetadata":{"Data":{"Git":{"commit":"bf10953956e328f232d444c9ead87da715f18614","file":"taskManager/settings.py","email":"root \u003croot@gitlab-ce-rmaa3gra.lab.practical-devsecops.training\u003e","repository":"http://gitlab-ce-rmaa3gra.lab.practical-devsecops.training/root/django-nv.git","timestamp":"2024-07-06 06:27:24 +0000","line":19}}},"SourceID":1,"SourceType":16,"SourceName":"trufflehog - git","DetectorType":2,"DetectorName":"AWS","DecoderName":"PLAIN","Verified":true,"Raw":"AKIAYVP4CIPPERUVIFXG","RawV2":"AKIAYVP4CIPPERUVIFXGZt2U1h267eViPnuSA+JO5ABhiu4T7XUMSZ+Y2Oth","Redacted":"AKIAYVP4CIPPERUVIFXG","ExtraData":{"account":"595918472158","arn":"arn:aws:iam::595918472158:user/canarytokens.com@@mirux23ppyky6hx3l6vclmhnj","is_canary":"true","message":"This is an AWS canary token generated at canarytokens.org, and was not set off; learn more here: https://trufflesecurity.com/canaries","resource_type":"Access key"},"StructuredData":null}
{"level":"info-0","ts":"2024-07-06T06:29:43Z","logger":"trufflehog","msg":"finished scanning","chunks":235,"bytes":1567555,"verified_secrets":1,"unverified_secrets":1,"scan_duration":"742.511464ms","trufflehog_version":"3.79.0"}
```

We are using the tee command here to show the output and store it in a file simultaneously.
```
trufflehog --json . | tee secret.json
```
- **--json**: tells that output should be in the JSON format

```
#     username = password = ''\n-#     if request.POST:\n-#         username = request.POST.get('username')\n-#         password = request.POST.get('password')\n-\n-#         user = authenticate(username=username, password=password)\n-#         if user is not None:\n-#             if user.is_active:\n-#                 login(request, user)\n-#                 state = \"You're successfully logged in!\"\n-#             else:\n-#                 state = \"Your account is not active, please contact the site admin.\"\n-#         else:\n-#             state = \"Your username and/or password were incorrect.\"\n+def login(request):\n+    state = \"Please log in below...\"\n+    username = password = ''\n+    if request.POST:\n+        username = request.POST.get('username')\n+        password = request.POST.get('password')\n+\n+        user = authenticate(username=username, password=password)\n+        if user is not None:\n+            if user.is_active:\n+                login(request, user)\n+                state = \"You're successfully logged in!\"\n+            else:\n+                state = \"Your account is not active, please contact the site admin.\"\n+        else:\n+            state = \"Your username and/or password were incorrect.\"\n \n-#     return render_to_response('login.html',{'state':state, 'username': username})\n+    return render_to_response('login.html',{'state':state, 'username': username})\n \n \n def proj_details(request, project_id):\n@@ -114,7 +86,15 @@ def the_comments(request, task_id):\n \tresponse = \"You're looking at the comments of question %s.\"\n \treturn HttpResponse(response % task_id)\n \n-def detail(request, task_id, project_id):\n+def detail(request, task_id, foreign_key):\n+\t#try:\n+\tif request.method == 'POST':\n+\t\tform = CommentForm(request.POST)\n+\t\tif form.is_valid():\n+\t\t\treturn HttpResponseRedirect('/thanks/')\n+\t\telse:\n+\t\t\tform = CommentForm()\n+\n \ttask = Task.objects.get(pk = task_id)\n \t#except Task.DoesNotExist:\n \t#\traise Http404\n", "reason": "High Entropy", "stringsFound": ["20821e4abaea95268880f020c9f6768288f3725a"]}
```

However, we can conduct a scan using an SSH URL to scan the Git repository, and then convert the result into a secret.json file.
> Our devsecops-box ssh-key has been integrated into our GitLab.

`trufflehog git git@gitlab-ce-cxlx0c4v:root/django-nv.git --json | tee secret.json`

Command Output:
```
The authenticity of host 'gitlab-ce-cxlx0c4v (10.x.x.x)' can't be established.
ECDSA key fingerprint is SHA256:U1W8wQm8tgHmuF/T0uf1jNVCzHyhqeJ4MmGG/K4XmcI.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```
Type yes and hit enter to allow the host gitlab-ce-cxlx0c4v to be a trusted source.
```
{"level":"info-0","ts":"2024-07-06T06:28:10Z","logger":"trufflehog","msg":"running source","source_manager_worker_id":"3toGl","with_units":true}
{"level":"info-0","ts":"2024-07-06T06:28:10Z","logger":"trufflehog","msg":"scanning repo","source_manager_worker_id":"3toGl","unit":"/tmp/trufflehog-1485-3879622622","unit_kind":"dir","repo":"ssh://gitlab-ce-rmaa3gra/root/django-nv.git"}
{"SourceMetadata":{"Data":{"Git":{"commit":"bf10953956e328f232d444c9ead87da715f18614","file":"taskManager/settings.py","email":"root \u003croot@gitlab-ce-rmaa3gra.lab.practical-devsecops.training\u003e","repository":"ssh://gitlab-ce-rmaa3gra/root/django-nv.git","timestamp":"2024-07-06 06:27:24 +0000","line":22}}},"SourceID":1,"SourceType":16,"SourceName":"trufflehog - git","DetectorType":13,"DetectorName":"Slack","DecoderName":"PLAIN","Verified":false,"VerificationError":"unexpected error auth response token_revoked","Raw":"xoxp-4797898847-4799393255-4778181812-f140b6","RawV2":"","Redacted":"","ExtraData":{"rotation_guide":"https://howtorotate.com/docs/tutorials/slack/","token_type":"Slack User Token"},"StructuredData":null}
{"SourceMetadata":{"Data":{"Git":{"commit":"bf10953956e328f232d444c9ead87da715f18614","file":"taskManager/settings.py","email":"root \u003croot@gitlab-ce-rmaa3gra.lab.practical-devsecops.training\u003e","repository":"ssh://gitlab-ce-rmaa3gra/root/django-nv.git","timestamp":"2024-07-06 06:27:24 +0000","line":19}}},"SourceID":1,"SourceType":16,"SourceName":"trufflehog - git","DetectorType":2,"DetectorName":"AWS","DecoderName":"PLAIN","Verified":true,"Raw":"AKIAYVP4CIPPERUVIFXG","RawV2":"AKIAYVP4CIPPERUVIFXGZt2U1h267eViPnuSA+JO5ABhiu4T7XUMSZ+Y2Oth","Redacted":"AKIAYVP4CIPPERUVIFXG","ExtraData":{"account":"595918472158","arn":"arn:aws:iam::595918472158:user/canarytokens.com@@mirux23ppyky6hx3l6vclmhnj","is_canary":"true","message":"This is an AWS canary token generated at canarytokens.org, and was not set off; learn more here: https://trufflesecurity.com/canaries","resource_type":"Access key"},"StructuredData":null}
{"level":"info-0","ts":"2024-07-06T06:28:10Z","logger":"trufflehog","msg":"finished scanning","chunks":235,"bytes":1567555,"verified_secrets":1,"unverified_secrets":1,"scan_duration":"2.925706023s","trufflehog_version":"3.79.0"}
```

As we have learned in the DevSecOps Gospel, we should save the output in a machine-readable format (CSV, JSON, XML) so it can be parsed by machines easily.

To further analyze the output stored in the secret.json file, we can use the jq tool. jq is a powerful command-line JSON processor that allows us to extract and manipulate data from JSON files.

Here’s an example of how to use jq to examine the contents of the secret.json file:
`cat secret.json | jq`
Executing this command will display the contents of the secret.json file in a well-formatted and readable manner. This will allow you to view the JSON data’s structure and the information extracted by TruffleHog during the scanning process.

From the provided JSON output, it appears that the secret scan detected the following secrets:
![image](https://github.com/user-attachments/assets/9e8db846-3adf-458b-9e57-19cbea49274f)


Okay, so we got some results from the tool but are these false positives or real issues.

What can we do to improve the situation?

