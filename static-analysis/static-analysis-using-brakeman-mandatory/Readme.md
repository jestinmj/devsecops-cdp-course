Use Brakeman to find security issues
================================================================

Learn how to run static analysis scans on Ruby on Rails code using Brakeman
--------

In this scenario, you will learn how to run Brakeman scan on Rails code.

You will need to download the code, install the SAST tool called Brakeman and then finally run the SAST scan on the code.

Download the source code
----------

We will do all the exercises locally first in DevSecOps-Box, so let’s start the exercise.

First, we need to download the source code of the project from our git repository.

```
git clone https://github.com/OWASP/railsgoat.git webapp                    #### OLD
git clone https://gitlab.practical-devsecops.training/pdso/rails.git webapp
cd webapp
```

Install Brakeman
----------

> Brakeman is Static Analysis tool for Rails application to find vulnerabilities, Fast and Flexible tools with a very good report and fit to embed it in CI/CD pipeline.
> 
> You can find more details about the project at https://brakemanscanner.org/.

Basically, our system doesn’t have Ruby installed, let’s update apt first.
```
apt update
apt install ruby-full -y
gem install brakeman
```
We have successfully installed Brakeman, let’s explore the functionality it provides us.
```
brakeman -h
```
```
Usage: brakeman [options] rails/root/path
    -n, --no-threads                 Run checks and file parsing sequentially
        --[no-]progress              Show progress reports
    -p, --path PATH                  Specify path to Rails application
    -q, --[no-]quiet                 Suppress informational messages
    -z, --[no-]exit-on-warn          Exit code is non-zero if warnings found (Default)
        --[no-]exit-on-error         Exit code is non-zero if errors raised (Default)
        --ensure-latest              Fail when Brakeman is outdated
        --ensure-ignore-notes        Fail when an ignored warning does not include a note
    -3, --rails3                     Force Rails 3 mode
    -4, --rails4                     Force Rails 4 mode
    -5, --rails5                     Force Rails 5 mode
    -6, --rails6                     Force Rails 6 mode
    -7, --rails7                     Force Rails 7 mode

Scanning options:
    -A, --run-all-checks             Run all default and optional checks
    -a, --[no-]assume-routes         Assume all controller methods are actions (Default)
    -e, --escape-html                Escape HTML by default
        --faster                     Faster, but less accurate scan
        --ignore-model-output        Consider model attributes XSS-safe
        --ignore-protected           Consider models with attr_protected safe
        --[no-]index-libs            Add libraries to call index (Default)
        --interprocedural            Process method calls to known methods
        --no-branching               Disable flow sensitivity on conditionals
        --branch-limit LIMIT         Limit depth of values in branches (-1 for no limit)
        --parser-timeout SECONDS     Set parse timeout (Default: 10)
    -r, --report-direct              Only report direct use of untrusted data
    -s meth1,meth2,etc,              Set methods as safe for unescaped output in views
        --safe-methods
        --sql-safe-methods meth1,meth2,etc
                                     Do not warn of SQL if the input is wrapped in a safe method
        --url-safe-methods method1,method2,etc
                                     Do not warn of XSS if the link_to href parameter is wrapped in a safe method
        --skip-files file1,path2,etc Skip processing of these files/directories. Directories are application relative and must end in "/"
        --only-files file1,path2,etc Process only these files/directories. Directories are application relative and must end in "/"
        --[no-]skip-vendor           Skip processing vendor directory (Default)
        --skip-libs                  Skip processing lib directory
        --add-libs-path path1,path2,etc
                                     An application relative lib directory (ex. app/mailers) to process
        --add-engines-path path1,path2,etc
                                     Include these engines in the scan
    -E, --enable Check1,Check2,etc   Enable the specified checks
    -t, --test Check1,Check2,etc     Only run the specified checks
    -x, --except Check1,Check2,etc   Skip the specified checks
        --add-checks-path path1,path2,etc
                                     A directory containing additional out-of-tree checks to run

Output options:
    -d, --debug                      Lots of output
    -f, --format TYPE                Specify output formats. Default is text
        --css-file CSSFile           Specify CSS to use for HTML output
    -i, --ignore-config IGNOREFILE   Use configuration to ignore warnings
    -I, --interactive-ignore         Interactively ignore warnings
    -l, --[no-]combine-locations     Combine warning locations (Default)
        --[no-]highlights            Highlight user input in report
        --[no-]color                 Use ANSI colors in report (Default)
    -m, --routes                     Report controller information
        --message-limit LENGTH       Limit message length in HTML report
        --[no-]pager                 Use pager for output to terminal (Default)
        --table-width WIDTH          Limit table width in text report
    -o, --output FILE                Specify files for output. Defaults to stdout. Multiple '-o's allowed
        --[no-]separate-models       Warn on each model without attr_accessible (Default)
        --[no-]summary               Only output summary of warnings
        --absolute-paths             Output absolute file paths in reports
        --github-repo USER/REPO[/PATH][@REF]
                                     Output links to GitHub in markdown and HTML reports using specified repo
        --text-fields field1,field2,etc.
                                     Specify fields for text report format
    -w, --confidence-level LEVEL     Set minimal confidence level (1 - 3)
        --compare FILE               Compare the results of a previous Brakeman scan (only JSON is supported)

Configuration files:
    -c, --config-file FILE           Use specified configuration file
    -C, --create-config [FILE]       Output configuration file based on options
        --allow-check-paths-in-config
                                     Allow loading checks from configuration file (Unsafe)

    -k, --checks                     List all available vulnerability checks
        --optional-checks            List optional checks
    -v, --version                    Show Brakeman version
        --force-scan                 Scan application even if Rails is not detected
    -h, --help                       Display this message
```

Run the Scanner
----------

As we have learned in DevSecOps Gospel, we would like to store the content in a JSON file. We are using the tee command here to show the output and store it in a file simultaneously.

```
brakeman -f json | tee result1.json
```
get the number of warnings or issues - before the ignore file
```
/webapp# cat result1.json | jq .warnings | jq length
19
```

Brakeman ran successfully, and it found 17 security issues.

1. Six medium severity issues
2. Eleven high severity issues

It seems we have found quite a few issues; you can ignore issues with using the brakeman.ignore file.

> You will find fingerprints in the scan output.

```
nano brakeman.ignore
........
{
    "ignored_warnings": [
        {
          "fingerprint": "febb21e45b226bb6bcdc23031091394a3ed80c76357f66b1f348844a7626f4df",
          "note": "ignore XSS"
        }
    ]
}
```
Let’s re-run the scanner.
```
brakeman -f json -i brakeman.ignore | tee result2.json
```

Get the number of warnings or issues:
`cat result2.json | jq .warnings | jq length`

You will see the issues are reduced because we ignored the Cross-Site Scripting (XSS) vulnerability.
```
/webapp# cat result2.json | jq .warnings | jq length
18
```
