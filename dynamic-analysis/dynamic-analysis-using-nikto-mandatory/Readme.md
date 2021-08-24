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
./nikto.pl -Help
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
+ Target IP:          x.x.x.x
+ Target Hostname:    prod-XqiHnDZ0.lab.practical-devsecops.training
+ Target Port:        80
+ Start Time:         2021-07-11 05:46:26 (GMT0)
---------------------------------------------------------------------------
+ Server: nginx/1.14.0 (Ubuntu)
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ nginx/1.14.0 appears to be outdated (current is at least 1.18.0)
+ OSVDB-17113: /SilverStream: SilverStream allows directory listing
+ 8135 requests: 0 error(s) and 3 item(s) reported on remote host
+ End Time:           2021-07-11 05:47:14 (GMT0) (48 seconds)
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
<niktoscan>
<niktoscan hoststest="0" options="-h prod-XqiHnDZ0.lab.practical-devsecops.training -output nikto_output.xml" version="2.1.6" scanstart="Sun Jul 11 05:47:55 
2021" scanend="Thu Jan  1 00:00:00 1970" scanelapsed=" seconds" nxmlversion="1.2">

<scandetails targetip="134.209.130.45" targethostname="prod-XqiHnDZ0.lab.practical-devsecops.training" targetport="80" targetbanner="nginx/1.14.0 (Ubuntu)" s
tarttime="2021-07-11 05:47:56" sitename="http://prod-XqiHnDZ0.lab.practical-devsecops.training:80/" siteip="http://134.209.130.45:80/" hostheader="prod-wciku
6wj.lab.practical-devsecops.training" errors="0" checks="6955">


<item id="999103" osvdbid="0" osvdblink="" method="GET">
<description><![CDATA[The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion 
to the MIME type.]]></description>
<uri><![CDATA[/]]></uri>
<namelink><![CDATA[http://prod-XqiHnDZ0.lab.practical-devsecops.training:80/]]></namelink>
<iplink><![CDATA[http://134.209.130.45:80/]]></iplink>
</item>

<item id="600575" osvdbid="0" osvdblink="" method="HEAD">
<description><![CDATA[nginx/1.14.0 appears to be outdated (current is at least 1.18.0)]]></description>
<uri><![CDATA[/]]></uri>
<namelink><![CDATA[http://prod-XqiHnDZ0.lab.practical-devsecops.training:80/]]></namelink>
<iplink><![CDATA[http://134.209.130.45:80/]]></iplink>
</item>

<item id="000398" osvdbid="17113" osvdblink="https://vulners.com/osvdb/OSVDB:17113" method="GET">
<description><![CDATA[/SilverStream: SilverStream allows directory listing]]></description>
<uri><![CDATA[/SilverStream]]></uri>
<namelink><![CDATA[http://prod-XqiHnDZ0.lab.practical-devsecops.training:80/SilverStream]]></namelink>
<iplink><![CDATA[http://134.209.130.45:80/SilverStream]]></iplink>
</item>

<statistics elapsed="55" itemsfound="3" itemstested="6955" endtime="2021-07-11 05:48:51" />
</scandetails>

</niktoscan>


</niktoscan>
```

Exercise
---------

1. Read the [Nikto documentation](https://github.com/sullo/nikto/wiki)
2. List the available plugins in Nikto
3. Can you run a specific Nikto plugin to perform any scan? You can select any plugin of your choice from the list (e.g. headers, dictionary, etc)
4. Create a Nikto configuration file(nikto.conf) to satisfy the below criteria:
    - Remove the ports that would never be scanned
    - Remove the False Positives
    - Save the output in CSV format

> Please do not forget to share the answer (a screenshot and commands) with our staff via Slack Direct Message (DM).

> Hint : Explore the nikto config variables in this [link](https://github.com/sullo/nikto/wiki/Config-Variables)