Use detect-secrets to find the secrets inside our source code
================================================================

Use detect-secrets to find secrets like token, ssh keys etc.
----------------------------------------------------------------
In this scenario, you will learn how to install and run detect-secrets to Scans for Secret on a git repository.

You will need to download the code, install the Secret Scanning tool, and then finally run the Secret scan on the code.

Download the source code
----------

First, we need to download the source code of the project from our git repository.

```
git clone https://gitlab.practical-devsecops.training/pdso/django.nv webapp

cd webapp
```

Install detect-secrets
----------

> detect-secrets is a tool that designed with the enterprise client in mind: providing a backwards compatible to preventing new secrets from entering the code base and etc.
> 
> You can find more details about the project at https://github.com/Yelp/detect-secrets.

Let’s install the **detect-secrets** tool on the system to scan for the secrets in our code.

```
pip3 install detect-secrets
```

Let’s explore what options detect-secrets provides us.

```
detect-secrets --help
```

Run the Scanner
----------

As we have learned in the DevSecOps Gospel, we should save the output in the machine-readable format. JSON, CSV, XML formats can be parsed by the machines easily.

Let’s run the detect-secrets command with the scan argument to find any secrets in our code.

```
detect-secrets scan
```
output
```
{
  "version": "1.1.0",
  "plugins_used": [
    {
      "name": "ArtifactoryDetector"
    },
    {
      "name": "AWSKeyDetector"
    },
    {
      "name": "AzureStorageKeyDetector"
    },
    {
      "name": "Base64HighEntropyString",
      "limit": 4.5
    },
    {
      "name": "BasicAuthDetector"
    },
    {
      "name": "CloudantDetector"
    },
    {
      "name": "HexHighEntropyString",
      "limit": 3.0
    },
    {
      "name": "IbmCloudIamDetector"
    },
    {
      "name": "IbmCosHmacDetector"
    },
    {
      "name": "JwtTokenDetector"
    },
    {
      "name": "KeywordDetector",
      "keyword_exclude": ""
    },
    {
      "name": "MailchimpDetector"
    },
    {
      "name": "NpmDetector"
    },
    {
      "name": "PrivateKeyDetector"
    },
    {
      "name": "SlackDetector"
    },
    {
      "name": "SoftlayerDetector"
    },
    {
      "name": "SquareOAuthDetector"
    },
    {
      "name": "StripeDetector"
    },
    {
      "name": "TwilioKeyDetector"
    }
  ],
  "filters_used": [
    {
      "path": "detect_secrets.filters.allowlist.is_line_allowlisted"
    },
    {
      "path": "detect_secrets.filters.common.is_ignored_due_to_verification_policies",
      "min_level": 2
    },
    {
      "path": "detect_secrets.filters.heuristic.is_indirect_reference"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_likely_id_string"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_lock_file"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_not_alphanumeric_string"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_potential_uuid"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_prefixed_with_dollar_sign"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_sequential_string"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_swagger_file"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_templated_secret"
    }
  ],
  "results": {
    "fixtures/users.json": [
      {
        "type": "Secret Keyword",
        "filename": "fixtures/users.json",
        "hashed_secret": "6b3e2d7677e6d4d01281c91063ce36c724ed0327",
        "is_verified": false,
        "line_number": 9
      },
      {
        "type": "Secret Keyword",
        "filename": "fixtures/users.json",
        "hashed_secret": "7a854a65fa34cf5c274f018ace6847ef64a60a0c",
        "is_verified": false,
        "line_number": 23
      },
      {
        "type": "Secret Keyword",
        "filename": "fixtures/users.json",
        "hashed_secret": "2b93f0828de9d8fa26dcf9b561df9f458d2f539c",
        "is_verified": false,
        "line_number": 37
      },
      {
        "type": "Secret Keyword",
        "filename": "fixtures/users.json",
        "hashed_secret": "aa04a3256e0f626a06d7d9de29112c3b9f5ed3be",
        "is_verified": false,
        "line_number": 51
      },
      {
        "type": "Secret Keyword",
        "filename": "fixtures/users.json",
        "hashed_secret": "02949b459aee22179d1570209d45a59fb64dcb90",
        "is_verified": false,
        "line_number": 65
      }
    ],
    "taskManager/settings.py": [
      {
        "type": "Secret Keyword",
        "filename": "taskManager/settings.py",
        "hashed_secret": "877e30c29747a7ef645f02be73bd691e8a386e82",
        "is_verified": false,
        "line_number": 24
      }
    ]
  },
  "generated_at": "2021-08-15T11:07:21Z"
}
```

It seems detect-secrets‘s default output format is JSON format. Let’s store the output/results in a file.

```
detect-secrets scan > secrets-output.json
```

We can also mark the issues/findings as false-positives in the output file using the audit command. You can accept an issue as a real issue with the letter y for yes and n for no.

Go ahead and mark the issues appropriately.

```
detect-secrets audit secrets-output.json
```
output
```
Secret:      1 of 6
Filename:    fixtures/users.json
Secret Type: Secret Keyword
----------
4:    "pk": 1,
5:    "fields": {
6:      "first_name" : "",
7:      "last_name" : "",
8:      "username" : "admin",
9:      "password": "md5$oAKvI66ce0Xq$a5c1836db3d6dedff5deca630a358d8b",
10:      "is_superuser" : true,
11:      "email" : "admin@tm.com",
12:      "is_staff" : true,
13:      "is_active" : true
14:    }
----------
Is this a valid secret? i.e. not a false-positive __(y)es, (n)o, (s)kip, (q)uit__:
```

> Did you notice it’s much more efficient than Trufflehog?

Exercise
----------

1. Explore the documentation of [detect-secrets tool](https://github.com/Yelp/detect-secrets)
2. Reduce the false positives and embed this tool in the CI/CD pipeline
3. Remember to keep the DevSecOps Gospel best practices in mind while doing this exercise
