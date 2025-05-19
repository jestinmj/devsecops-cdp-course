Dynamic Analysis using Nikto
================================================================


Learn how to use the Nikto tool to find security issues in an application
--------

In this scenario, you will learn how to install DAST tool and run DAST Scans on the Application.

You will need to install the DAST tool and then run the DAST scan on our Application.

Install Nikto
----------

> Nikto is a web server assessment tool. It’s designed to find various default and insecure files, configurations, and programs on any type of web server.
> 
> Nikto is built on LibWhisker2 (by RFP) and can run on any platform which has a Perl environment. It supports SSL, proxies, host authentication, attack encoding, and more.
>
> Source: [Nikto official.](https://cirt.net/Nikto2)

Let’s install Nikto to perform Dynamic Analysis.
```
apt install -y libnet-ssleay-perl
```

> The above command is needed to support SSL scan in Nikto

```
git clone https://github.com/sullo/nikto

cd nikto/program
git checkout tags/2.1.6

./nikto.pl -Help
```

```
/nikto/program# ./nikto.pl -Help

   Options:
       -ask+               Whether to ask about submitting updates
                               yes   Ask about each (default)
                               no    Don't ask, don't send
                               auto  Don't ask, just send
       -Cgidirs+           Scan these CGI dirs: "none", "all", or values like "/cgi/ /cgi-a/"
       -config+            Use this config file
       -Display+           Turn on/off display outputs:
                               1     Show redirects
                               2     Show cookies received
                               3     Show all 200/OK responses
                               4     Show URLs which require authentication
                               D     Debug output
                               E     Display all HTTP errors
                               P     Print progress to STDOUT
                               S     Scrub output of IPs and hostnames
                               V     Verbose output
       -dbcheck           Check database and other key files for syntax errors
       -evasion+          Encoding technique:
                               1     Random URI encoding (non-UTF8)
                               2     Directory self-reference (/./)
                               3     Premature URL ending
                               4     Prepend long random string
                               5     Fake parameter
                               6     TAB as request spacer
                               7     Change the case of the URL
                               8     Use Windows directory separator (\)
                               A     Use a carriage return (0x0d) as a request spacer
                               B     Use binary value 0x0b as a request spacer
        -Format+           Save file (-o) format:
                               csv   Comma-separated-value
                               htm   HTML Format
                               nbe   Nessus NBE format
                               sql   Generic SQL (see docs for schema)
                               txt   Plain text
                               xml   XML Format
                               (if not specified the format will be taken from the file extension passed to -output)
       -Help              Extended help information
       -host+             Target host
       -404code           Ignore these HTTP codes as negative responses (always). Format is "302,301".
       -404string         Ignore this string in response body content as negative response (always). Can be a regular expression.
       -id+               Host authentication to use, format is id:pass or id:pass:realm
       -key+              Client certificate key file
       -list-plugins      List all available plugins, perform no testing
       -maxtime+          Maximum testing time per host (e.g., 1h, 60m, 3600s)
       -mutate+           Guess additional file names:
                               1     Test all files with all root directories
                               2     Guess for password file names
                               3     Enumerate user names via Apache (/~user type requests)
                               4     Enumerate user names via cgiwrap (/cgi-bin/cgiwrap/~user type requests)
                               5     Attempt to brute force sub-domain names, assume that the host name is the parent domain
                               6     Attempt to guess directory names from the supplied dictionary file
       -mutate-options    Provide information for mutates
       -nointeractive     Disables interactive features
       -nolookup          Disables DNS lookups
       -nossl             Disables the use of SSL
       -no404             Disables nikto attempting to guess a 404 page
       -Option            Over-ride an option in nikto.conf, can be issued multiple times
       -output+           Write output to this file ('.' for auto-name)
       -Pause+            Pause between tests (seconds, integer or float)
       -Plugins+          List of plugins to run (default: ALL)
       -port+             Port to use (default 80)
       -RSAcert+          Client certificate file
       -root+             Prepend root value to all requests, format is /directory
       -Save              Save positive responses to this directory ('.' for auto-name)
       -ssl               Force ssl mode on port
       -Tuning+           Scan tuning:
                               1     Interesting File / Seen in logs
                               2     Misconfiguration / Default File
                               3     Information Disclosure
                               4     Injection (XSS/Script/HTML)
                               5     Remote File Retrieval - Inside Web Root
                               6     Denial of Service
                               7     Remote File Retrieval - Server Wide
                               8     Command Execution / Remote Shell
                               9     SQL Injection
                               0     File Upload
                               a     Authentication Bypass
                               b     Software Identification
                               c     Remote Source Inclusion
                               d     WebService
                               e     Administrative Console
                               x     Reverse Tuning Options (i.e., include all except specified)
       -timeout+          Timeout for requests (default 10 seconds)
       -Userdbs           Load only user databases, not the standard databases
                               all   Disable standard dbs and load only user dbs
                               tests Disable only db_tests and load udb_tests
       -useragent         Over-rides the default useragent
       -until             Run until the specified time or duration
       -update            Update databases and plugins from CIRT.net
       -useproxy          Use the proxy defined in nikto.conf, or argument http://server:port
       -Version           Print plugin and database versions
       -vhost+            Virtual host (for Host header)
                + requires a value
```

Run the Scanner
----------

As we have learned in the DevSecOps Gospel, we should save the output in the machine-readable format (CSV, JSON, XML) so it can be parsed by the machines easily.

Let’s run the Nikto with the following options.

```
./nikto.pl -output nikto_output.xml -h prod-XqiHnDZ0
```

- -h: flag used to set the target application which we want to scan
- -output: flag used to set the output file in which we want to store the result

output

```
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          10.1.30.117
+ Target Hostname:    prod-cxlx0c4v
+ Target Port:        80
+ Start Time:         2025-05-19 05:24:53 (GMT0)
---------------------------------------------------------------------------
+ Server: nginx/1.18.0 (Ubuntu)
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Web Server returns a valid response with junk HTTP methods, this may cause false positives.
+ OSVDB-17113: /SilverStream: SilverStream allows directory listing
+ 7373 requests: 0 error(s) and 4 item(s) reported on remote host
+ End Time:           2025-05-19 05:25:42 (GMT0) (49 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

Now, executing cat command on the output file will show the nikto result in XML format.

```
cat nikto_output.xml
```
output
```
<?xml version="1.0" ?>
<!DOCTYPE niktoscan SYSTEM "docs/nikto.dtd">
<niktoscan hoststest="0" options="-output nikto_output.xml -h prod-cxlx0c4v" version="2.1.6" scanstart="Mon May 19 05:24:52 2025" scanend="Thu Jan  1 00:00:00 1970" scanelapsed=" seconds" nxmlversion="1.2">

<scandetails targetip="10.1.30.117" targethostname="prod-cxlx0c4v" targetport="80" targetbanner="nginx/1.18.0 (Ubuntu)" starttime="2025-05-19 05:24:53" sitename="http://prod-cxlx0c4v:80/" siteip="http://10.1.30.117:80/" hostheader="prod-cxlx0c4v" errors="0" checks="6934">


<item id="999102" osvdbid="0" osvdblink="http://osvdb.org/0" method="GET">
<description><![CDATA[The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS]]></description>
<uri><![CDATA[/]]></uri>
<namelink><![CDATA[http://prod-cxlx0c4v:80/]]></namelink>
<iplink><![CDATA[http://10.1.30.117:80/]]></iplink>
</item>

<item id="999103" osvdbid="0" osvdblink="http://osvdb.org/0" method="GET">
<description><![CDATA[The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type]]></description>
<uri><![CDATA[/]]></uri>
<namelink><![CDATA[http://prod-cxlx0c4v:80/]]></namelink>
<iplink><![CDATA[http://10.1.30.117:80/]]></iplink>
</item>

<item id="999967" osvdbid="0" osvdblink="http://osvdb.org/0" method="MPYIZAZF">
<description><![CDATA[Web Server returns a valid response with junk HTTP methods, this may cause false positives.]]></description>
<uri><![CDATA[/]]></uri>
<namelink><![CDATA[http://prod-cxlx0c4v:80/]]></namelink>
<iplink><![CDATA[http://10.1.30.117:80/]]></iplink>
</item>

<item id="000398" osvdbid="17113" osvdblink="http://osvdb.org/17113" method="GET">
<description><![CDATA[/SilverStream: SilverStream allows directory listing]]></description>
<uri><![CDATA[/SilverStream]]></uri>
<namelink><![CDATA[http://prod-cxlx0c4v:80/SilverStream]]></namelink>
<iplink><![CDATA[http://10.1.30.117:80/SilverStream]]></iplink>
</item>

<statistics elapsed="49" itemsfound="4" itemstested="6934" endtime="2025-05-19 05:25:42" />
</scandetails>


</niktoscan>
```

# Parameters
Before diving into the challenges, let’s explore some of the important flags and options in the nikto.conf file, which is found in the /nikto/program/ directory. Understanding these options will be invaluable in running Nikto more efficiently.

Here is the list of some important parameters:
| Parameter  | Description and Usage |
| ------------- | ------------- |
| SKIPIDS | Function: Allows skipping certain false-positive checks during the scan. Usage: Specify a comma-separated list of test ID numbers to skip. For example, exclude checks that consistently produce false positives for your target application. |
| SKIPPORTS  | Function: Specifies ports that Nikto will not scan, even if they are open. Usage: Provide a comma-separated list of ports to skip during the scan. For instance, exclude secure ports like 443 (HTTPS) if you don’t want to scan them.  |
| CLIOPTS  | Function: Defines the command-line options to be used with Nikto. Usage: Customize Nikto’s behavior by specifying desired command-line options. For example, set the output format, target host, and other scan-specific settings.  |
| STATIC-COOKIE  | Function: Allows setting a static string as the Cookie: header in HTTP requests sent by Nikto. Usage: Set a static cookie value if required for authentication or accessing specific resources. Ensure Nikto includes this static cookie in its requests during the scan.  |
| TIMEOUT  | Function: Sets the timeout value (in seconds) for HTTP requests made by Nikto. Usage: Adjust the timeout based on network conditions and target server responsiveness. Longer timeouts may be necessary for slow or unreliable connections.  |
| EXTRAREQS | Function: Determines whether Nikto should use extra, non-normative HTTP methods to attempt to reveal additional information or vulnerabilities. Usage: Set to 0 (disable) or 1 (enable). Enabling may reveal additional vulnerabilities but could increase scan time and trigger security alerts on the target server.  |

Exercise
---------

Read the [Nikto documentation](https://github.com/sullo/nikto/wiki)

1. List the available plugins in Nikto<br>
   `./nikto.pl -list-plugins`
   > Once you execute this command, Nikto will output a detailed list of plugins along with their descriptions. Take your time to review this list and familiarize yourself with the various plugins that Nikto offers. This knowledge will be valuable for performing targeted scans and tests in subsequent tasks.

2. Perform Scan Using the ‘headers’ Plugin scan against prod-cxlx0c4v in Nikto   
    > `./nikto.pl -h prod-cxlx0c4v -Plugins headers` <br> This command directs Nikto to conduct a scan specifically utilizing the headers plugin on the prod-cxlx0c4v server. By focusing on HTTP headers, you can uncover security risks and misconfigurations, enhancing the overall security posture of the target server.

3. Configure Nikto (nikto.conf) in the /nikto/program/ directory to exclude ports 21, 22, and 111 from scanning, and then save the scan results in CSV format with the output file named result.csv
    > Imagine we have a specific situation where we don’t want Nikto to scan ports 21, 22, and 111 because these ports are essential and the servers running on them are already well-protected. In such cases, we can tell Nikto not to scan these ports by using the SKIPPORTS option.”
    ```
    cat >/nikto/program/nikto.conf<<EOF
    SKIPPORTS=21 22 111
    CLIOPTS=-output result.csv -Format csv
    EOF
    ```
    > Re-run the nikto command. <br> `./nikto.pl -h prod-cxlx0c4v -config nikto.conf`


> Hint : Explore the nikto config variables in this [link](https://github.com/sullo/nikto/wiki/Config-Variables)
