Dynamic Analysis using SSLyze
================================================

Learn how to run SSLyze to find SSL/TLS misconfigurations.
----------------------------------------------------------------

In this scenario, you will learn how to install SSLyze to scan a website for SSL misconfiguration and issues.

You will need to install the SSLyze tool and then run the tool scan for SSL misconfiguration.

Install DAST Tool
----------

> SSLyze is a fast and powerful SSL/TLS scanning library.
> 
> It allows you to analyze the SSL/TLS configuration of a server by connecting to it, in order to detect various issues (bad certificate, weak cipher suites, Heartbleed, ROBOT, TLS 1.3 support, etc.).
>
> SSLyze can either be used as command line tool or as a Python library.
>
> Source [SSLyze Github](https://github.com/nabla-c0d3/sslyze)

Let’s install SSlyze to perform Dynamic analysis.

```
pip3 install sslyze
sslyze --help
```
```
/# sslyze --help
usage: sslyze [-h] [--update_trust_stores] [--cert CERTIFICATE_FILE] [--key KEY_FILE] [--keyform KEY_FORMAT]
              [--pass PASSPHRASE] [--json_out JSON_FILE] [--targets_in TARGET_FILE] [--quiet] [--slow_connection]
              [--https_tunnel PROXY_SETTINGS] [--starttls PROTOCOL] [--xmpp_to HOSTNAME]
              [--sni SERVER_NAME_INDICATION] [--tlsv1_3] [--sslv2] [--tlsv1_1] [--tlsv1_2] [--robot]
              [--http_headers] [--certinfo] [--certinfo_ca_file CERTINFO_CA_FILE] [--heartbleed] [--compression]
              [--reneg] [--elliptic_curves] [--fallback] [--sslv3] [--resum] [--resum_attempts RESUM_ATTEMPTS]
              [--tlsv1] [--openssl_ccs] [--early_data] [--mozilla_config {modern,intermediate,old,disable}]
              [target ...]

SSLyze version 5.0.3

positional arguments:
  target                The list of servers to scan.

options:
  -h, --help            show this help message and exit
  --mozilla_config {modern,intermediate,old,disable}
                        Shortcut to queue various scan commands needed to check the server's TLS configurations
                        against one of Mozilla's recommended TLS configuration. Set to "intermediate" by default.
                        Use "disable" to disable this check.

Trust stores options:
  --update_trust_stores
                        Update the default trust stores used by SSLyze. The latest stores will be downloaded from
                        https://github.com/nabla-c0d3/trust_stores_observatory. This option is meant to be used
                        separately, and will silence any other command line option supplied to SSLyze.

Client certificate options:
  --cert CERTIFICATE_FILE
                        Client certificate chain filename. The certificates must be in PEM format and must be
                        sorted starting with the subject's client certificate, followed by intermediate CA
                        certificates if applicable.
  --key KEY_FILE        Client private key filename.
  --keyform KEY_FORMAT  Client private key format. DER or PEM (default).
  --pass PASSPHRASE     Client private key passphrase.

Input and output options:
  --json_out JSON_FILE  Write the scan results as a JSON document to the file JSON_FILE. If JSON_FILE is set to
                        '-', the JSON output will instead be printed to stdout. The resulting JSON file is a
                        serialized version of the ScanResult objects described in SSLyze's Python API: the nodes
                        and attributes will be the same. See
                        https://nabla-c0d3.github.io/sslyze/documentation/available-scan-commands.html for more
                        details.
  --targets_in TARGET_FILE
                        Read the list of targets to scan from the file TARGET_FILE. It should contain one host:port
                        per line.
  --quiet               Do not output anything to stdout; useful when using --json_out.

Contectivity options:
  --slow_connection     Greatly reduce the number of concurrent connections initiated by SSLyze. This will make the
                        scans slower but more reliable if the connection between your host and the server is slow,
                        or if the server cannot handle many concurrent connections. Enable this option if you are
                        getting a lot of timeouts or errors.
  --https_tunnel PROXY_SETTINGS
                        Tunnel all traffic to the target server(s) through an HTTP CONNECT proxy. HTTP_TUNNEL
                        should be the proxy's URL: 'http://USER:PW@HOST:PORT/'. For proxies requiring
                        authentication, only Basic Authentication is supported.
  --starttls PROTOCOL   Perform a StartTLS handshake when connecting to the target server(s). StartTLS should be
                        one of: auto, smtp, xmpp, xmpp_server, pop3, imap, ftp, ldap, rdp, postgres. The 'auto'
                        option will cause SSLyze to deduce the protocol (ftp, imap, etc.) from the supplied port
                        number, for each target servers.
  --xmpp_to HOSTNAME    Optional setting for STARTTLS XMPP. XMPP_TO should be the hostname to be put in the 'to'
                        attribute of the XMPP stream. Default is the server's hostname.
  --sni SERVER_NAME_INDICATION
                        Use Server Name Indication to specify the hostname to connect to. Will only affect TLS 1.0+
                        connections.

Scan commands:
  --tlsv1_3             Test a server for TLS 1.3 support.
  --sslv2               Test a server for SSL 2.0 support.
  --tlsv1_1             Test a server for TLS 1.1 support.
  --tlsv1_2             Test a server for TLS 1.2 support.
  --robot               Test a server for the ROBOT vulnerability.
  --http_headers        Test a server for the presence of security-related HTTP headers.
  --certinfo            Retrieve and analyze a server's certificate(s) to verify its validity.
  --certinfo_ca_file CERTINFO_CA_FILE
                        To be used with --certinfo. Path to a file containing root certificates in PEM format that
                        will be used to verify the validity of the server's certificate.
  --heartbleed          Test a server for the OpenSSL Heartbleed vulnerability.
  --compression         Test a server for TLS compression support, which can be leveraged to perform a CRIME
                        attack.
  --reneg               Test a server for for insecure TLS renegotiation and client-initiated renegotiation.
  --elliptic_curves     Test a server for supported elliptic curves.
  --fallback            Test a server for the TLS_FALLBACK_SCSV mechanism to prevent downgrade attacks.
  --sslv3               Test a server for SSL 3.0 support.
  --resum               Test a server for TLS 1.2 session resumption support using session IDs and TLS tickets.
  --resum_attempts RESUM_ATTEMPTS
                        To be used with --resum. Number of session resumptions (both with Session IDs and TLS
                        Tickets) that SSLyze should attempt. The default value is 5, but a higher value such as 100
                        can be used to get a more accurate measure of how often session resumption succeeds or
                        fails with the server.
  --tlsv1               Test a server for TLS 1.0 support.
  --openssl_ccs         Test a server for the OpenSSL CCS Injection vulnerability (CVE-2014-0224).
  --early_data          Test a server for TLS 1.3 early data support.
```

Run the Scanner
----------

As we have learned in the DevSecOps Gospel we should save the output in the machine-readable format so that It can be parsed by the computers easily.

Let’s run sslyze with the following options.

```
sslyze --json_out sslyze-output.json prod-cxlx0c4v.lab.practical-devsecops.training:443
```

Note, we are using the target as prod-XqiHnDZ0.lab.practical-devsecops.training:443

   - -regular flag used to tells tool to perform Regular HTTPS scan
   - -json_out flag is used to store the output in a json format.

output

```
 CHECKING CONNECTIVITY TO SERVER(S)
 ----------------------------------

   prod-cxlx0c4v.lab.practical-devsecops.training:443 => 5.78.70.139 

 SCAN RESULTS FOR PROD-CXLX0C4V.LAB.PRACTICAL-DEVSECOPS.TRAINING:443 - 5.78.70.139
 ---------------------------------------------------------------------------------

 * Certificates Information:
       Hostname sent for SNI:             prod-cxlx0c4v.lab.practical-devsecops.training
       Number of certificates detected:   1


     Certificate #0 ( _RSAPublicKey )
       SHA1 Fingerprint:                  a0da336e05bcc2ea1b357b5af90e27a935af6626
       Common Name:                       *.lab.practical-devsecops.training
       Issuer:                            R11
       Serial Number:                     481812121895092944622458299910902194875799
       Not Before:                        2025-05-17
       Not After:                         2025-08-15
       Public Key Algorithm:              _RSAPublicKey
       Signature Algorithm:               sha256
       Key Size:                          4096
       Exponent:                          65537
       DNS Subject Alternative Names:     ['*.lab.practical-devsecops.training']

     Certificate #0 - Trust
       Hostname Validation:               OK - Certificate matches server hostname
       Android CA Store (12.1.0_r1):      OK - Certificate is trusted
       Apple CA Store (iOS 15.1, iPadOS 15.1, macOS 12.1, tvOS 15.1, and watchOS 8.1):OK - Certificate is trusted
       Java CA Store (jdk-13.0.2):        OK - Certificate is trusted
       Mozilla CA Store (2021-12-19):     OK - Certificate is trusted
       Windows CA Store (2022-02-06):     OK - Certificate is trusted
       Symantec 2018 Deprecation:         OK - Not a Symantec-issued certificate
       Received Chain:                    *.lab.practical-devsecops.training --> R11
       Verified Chain:                    *.lab.practical-devsecops.training --> R11 --> ISRG Root X1
       Received Chain Contains Anchor:    OK - Anchor certificate not sent
       Received Chain Order:              OK - Order is valid
       Verified Chain contains SHA1:      OK - No SHA1-signed certificate in the verified certificate chain

     Certificate #0 - Extensions
       OCSP Must-Staple:                  NOT SUPPORTED - Extension not found
       Certificate Transparency:          WARNING - Only 2 SCTs included but Google recommends 3 or more

     Certificate #0 - OCSP Stapling
                                          NOT SUPPORTED - Server did not send back an OCSP response

 * SSL 2.0 Cipher Suites:
     Attempted to connect using 7 cipher suites; the server rejected all cipher suites.

 * SSL 3.0 Cipher Suites:
     Attempted to connect using 80 cipher suites; the server rejected all cipher suites.

 * TLS 1.0 Cipher Suites:
     Attempted to connect using 80 cipher suites; the server rejected all cipher suites.

 * TLS 1.1 Cipher Suites:
     Attempted to connect using 80 cipher suites; the server rejected all cipher suites.

 * TLS 1.2 Cipher Suites:
     Attempted to connect using 156 cipher suites.

     The server accepted the following 5 cipher suites:
        TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256       256       ECDH: X25519 (253 bits)
        TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384             256       ECDH: prime256v1 (256 bits)
        TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA                256       ECDH: prime256v1 (256 bits)
        TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256             128       ECDH: prime256v1 (256 bits)
        TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA                128       ECDH: prime256v1 (256 bits)

     The group of cipher suites supported by the server has the following properties:
       Forward Secrecy                    OK - Supported
       Legacy RC4 Algorithm               OK - Not Supported


 * TLS 1.3 Cipher Suites:
     Attempted to connect using 5 cipher suites.

     The server accepted the following 3 cipher suites:
        TLS_CHACHA20_POLY1305_SHA256                      256       ECDH: X25519 (253 bits)
        TLS_AES_256_GCM_SHA384                            256       ECDH: X25519 (253 bits)
        TLS_AES_128_GCM_SHA256                            128       ECDH: X25519 (253 bits)


 * Deflate Compression:
                                          OK - Compression disabled

 * OpenSSL CCS Injection:
                                          OK - Not vulnerable to OpenSSL CCS injection

 * OpenSSL Heartbleed:
                                          OK - Not vulnerable to Heartbleed

 * ROBOT Attack:
                                          OK - Not vulnerable, RSA cipher suites not supported.

 * Session Renegotiation:
       Client Renegotiation DoS Attack:   OK - Not vulnerable
       Secure Renegotiation:              OK - Supported

 * Elliptic Curve Key Exchange:
       Supported curves:                  X25519, prime256v1, secp384r1, secp521r1
       Rejected curves:                   X448, prime192v1, secp160k1, secp160r1, secp160r2, secp192k1, secp224k1, secp224r1, secp256k1, sect163k1, sect163r1, sect163r2, sect193r1, sect193r2, sect233k1, sect233r1, sect239k1, sect283k1, sect283r1, sect409k1, sect409r1, sect571k1, sect571r1

 SCANS COMPLETED IN 35.667611 S
 ------------------------------

       Wrote JSON output to "/sslyze-output.json".

 COMPLIANCE AGAINST MOZILLA TLS CONFIGURATION
 --------------------------------------------

    Checking results against Mozilla's "intermediate" configuration. See https://ssl-config.mozilla.org/ for more details.

    prod-cxlx0c4v.lab.practical-devsecops.training:443: FAILED - Not compliant.
        * ciphers: Cipher suites {'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA', 'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA'} are supported, but should be rejected.
```
We can check the scan output using the following command.
`cat sslyze-output.json`<br>
```
...[SNIP]...

                "tls_1_3_early_data": {
                    "error_reason": null,
                    "error_trace": null,
                    "result": null,
                    "status": "NOT_SCHEDULED"
                },
                "tls_compression": {
                    "error_reason": null,
                    "error_trace": null,
                    "result": {
                        "supports_compression": false
                    },
                    "status": "COMPLETED"
                },
                "tls_fallback_scsv": {
                    "error_reason": null,
                    "error_trace": null,
                    "result": null,
                    "status": "NOT_SCHEDULED"
                }
            },
            "scan_status": "COMPLETED",
            "server_location": {
                "connection_type": "DIRECT",
                "hostname": "prod-cxlx0c4v.lab.practical-devsecops.training",
                "http_proxy_settings": null,
                "ip_address": "x.x.x.x",
                "port": 443
            },
            "uuid": "6038d51f-31e1-4c43-bd7a-bbbe2b032342"
        }
    ],
    "sslyze_url": "https://github.com/nabla-c0d3/sslyze",
    "sslyze_version": "5.0.3"
```
