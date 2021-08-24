Use njsscan to find insecure code pattern
================================================================================

Learn how to run static analysis scans on NodeJS code using njsscan
--------------------------------------------------------------------------------

In this scenario, you will learn how to run static analysis scan on a NodeJS code.

You will need to download the code, install the tool, run the scan on the code and analysis the result of nodejsscan.

Download the source code
----------
We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from our git repository.

```
git clone https://github.com/OWASP/NodeGoat.git webapp
cd webapp
```

Installing njsscan
----------

> njsscan is a semantic aware SAST tool that can find insecure code patterns in your Node.js applications using a simple pattern matcher from libsast and pattern search tool like semgrep (lightweight static analysis for many languages).
> 
> You can find more details about the project at https://github.com/ajinabraham/njsscan.

Let’s install njsscan on the system to perform static analysis.
```
pip install njsscan
njsscan --help
```

Run the scanner
----------

As we have learned in DevSecOps Gospel, we would like to store the content in a JSON file.

```
njsscan --json -o output.json /webapp
```
njsscan ran successfully and it found some security issues and false positives.

output
```
  ...
  ...
      "metadata": {
        "cwe": "CWE-522: Insufficiently Protected Credentials",
        "description": "Default session middleware settings: `httpOnly` not set. It ensures the sensitive cookies cannot be accessed by client side JavaScript and helps to protect against cross-site scripting attacks.",
        "owasp": "A2: Broken Authentication",
        "severity": "WARNING"
      }
    },
    "cookie_session_no_path": {
      "files": [
        {
          "file_path": "/NodeGoat/server.js",
          "match_lines": [
            78,
            102
          ],
          "match_position": [
            13,
            7
          ],
          "match_string": "    app.use(session({\n        // genid: (req) => {\n        //    return genuuid() // use UUIDs for session IDs\n        //},\n        secret: cookieSecret,\n        // Both mandatory in Express v4\n        saveUninitialized: true,\n        resave: true\n        /*\n        // Fix for A5 - Security MisConfig\n        // Use generic cookie name\n        key: \"sessionId\",\n        */\n\n        /*\n        // Fix for A3 - XSS\n        // TODO: Add \"maxAge\"\n        cookie: {\n            httpOnly: true\n            // Remember to start an HTTPS server to get this working\n            // secure: true\n        }\n        */\n\n    }));"
        }
      ],
  ...
  ...
```

Exercise

1. Use appropriate njsscan options to reduce false positives
2. Ensure it follows all DevSecOps Gospel Practices
3. How would you embed this in CI pipeline?

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

