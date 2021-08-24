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

Run the Scanner
----------

As we have learned in the DevSecOps Gospel we should save the output in the machine-readable format so that It can be parsed by the computers easily.

Let’s run sslyze with the following options.

```
sslyze --regular --json_out sslyze-output.json prod-XqiHnDZ0.lab.practical-devsecops.training:443
```

Note, we are using the target as prod-XqiHnDZ0.lab.practical-devsecops.training:443

   - -regular flag used to tells tool to perform Regular HTTPS scan
   - -json_out flag is used to store the output in a json format.

output

```
 AVAILABLE PLUGINS
 -----------------

  EarlyDataPlugin
  SessionRenegotiationPlugin
  SessionResumptionPlugin
  HttpHeadersPlugin
  OpenSslCipherSuitesPlugin
  CertificateInfoPlugin
  CompressionPlugin
  FallbackScsvPlugin
  OpenSslCcsInjectionPlugin
  HeartbleedPlugin
  RobotPlugin


 CHECKING HOST(S) AVAILABILITY
 -----------------------------

   prod-XqiHnDZ0.lab.practical-devsecops.training:443                       => x.x.x.x.x 


 SCAN RESULTS FOR PROD-XqiHnDZ0.XqiHnDZ0.lab.practical-devsecops.training:443 - x.x.x.x.x
 ------------------------------------------------------------------------------------

 * Session Renegotiation:
       Client-initiated Renegotiation:    OK - Rejected
       Secure Renegotiation:              OK - Supported

 * TLSV1_1 Cipher Suites:
      Server rejected all cipher suites.

 * TLSV1_3 Cipher Suites:
       Forward Secrecy                    OK - Supported
       RC4                                OK - Not Supported

     Preferred:
        TLS_AES_256_GCM_SHA384                                           256 bits      HTTP 200 OK                                                 
     Accepted:
        TLS_CHACHA20_POLY1305_SHA256                                     256 bits      HTTP 200 OK                                                 
        TLS_AES_256_GCM_SHA384                                           256 bits      HTTP 200 OK                                                 
        TLS_AES_128_GCM_SHA256                                           128 bits      HTTP 200 OK                                                 

 * TLS 1.2 Session Resumption Support:
      With Session IDs:                  OK - Supported (5 successful, 0 failed, 0 errors, 5 total attempts).
      With TLS Tickets:                  OK - Supported

 * ROBOT Attack:
                                          OK - Not vulnerable

 * Deflate Compression:
                                          OK - Compression disabled

 * TLSV1 Cipher Suites:
      Server rejected all cipher suites.

 * Downgrade Attacks:
       TLS_FALLBACK_SCSV:                 OK - Supported

 * OpenSSL CCS Injection:
                                          OK - Not vulnerable to OpenSSL CCS injection

 * OpenSSL Heartbleed:
                                          OK - Not vulnerable to Heartbleed

 * SSLV2 Cipher Suites:
      Server rejected all cipher suites.

 * TLSV1_2 Cipher Suites:
       Forward Secrecy                    OK - Supported
       RC4                                OK - Not Supported

     Preferred:
        TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384                            256 bits      HTTP 200 OK                                                 
     Accepted:
        TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256                      256 bits      HTTP 200 OK                                                 
        TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384                            256 bits      HTTP 200 OK                                                 
        TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384                            256 bits      HTTP 200 OK                                                 
        TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256                            128 bits      HTTP 200 OK                                                 
        TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256                            128 bits      HTTP 200 OK                                                 

 * SSLV3 Cipher Suites:
      Server rejected all cipher suites.

 * Certificate Information:
     Content
       SHA1 Fingerprint:                  89d7a9d2bc1a482e0e74cb5a54b2d972733d2e1b
       Common Name:                       *.lab.practical-devsecops.training
       Issuer:                            R3
       Serial Number:                     429575392189153564980344116108018657284994
       Not Before:                        2021-02-11 07:27:08
       Not After:                         2021-05-12 07:27:08
       Signature Algorithm:               sha256
       Public Key Algorithm:              RSA
       Key Size:                          2048
       Exponent:                          65537 (0x10001)
       DNS Subject Alternative Names:     ['*.lab.practical-devsecops.training']

     Trust
       Hostname Validation:               OK - Certificate matches prod-XqiHnDZ0.lab.practical-devsecops.training
       Android CA Store (9.0.0_r9):       OK - Certificate is trusted
       Apple CA Store (iOS 12, macOS 10.14, watchOS 5, and tvOS 12):OK - Certificate is trusted
       Java CA Store (jdk-12.0.1):        OK - Certificate is trusted
       Mozilla CA Store (2019-03-14):     OK - Certificate is trusted
       Windows CA Store (2019-05-27):     OK - Certificate is trusted
       Symantec 2018 Deprecation:         WARNING: Certificate distrusted by Google and Mozilla on September 2018
       Received Chain:                    *.lab.practical-devsecops.training --> R3
       Verified Chain:                    *.lab.practical-devsecops.training --> R3 --> DST Root CA X3
       Received Chain Contains Anchor:    OK - Anchor certificate not sent
       Received Chain Order:              OK - Order is valid
       Verified Chain contains SHA1:      OK - No SHA1-signed certificate in the verified certificate chain

     Extensions
       OCSP Must-Staple:                  NOT SUPPORTED - Extension not found
       Certificate Transparency:          WARNING - Only 2 SCTs included but Google recommends 3 or more

     OCSP Stapling
                                          NOT SUPPORTED - Server did not send back an OCSP response


 SCAN COMPLETED IN 0.38 S
 ------------------------
```
We can check the scan output using the following command.
```
...[SNIP]...
                    "errored_cipher_list": [],
                    "preferred_cipher": {
                        "is_anonymous": false,
                        "key_size": 256,
                        "openssl_name": "TLS_AES_256_GCM_SHA384",
                        "post_handshake_response": "HTTP 200 OK",
                        "ssl_version": "TLSV1_3"
                    },
                    "rejected_cipher_list": [
                        {
                            "handshake_error_message": "TLS / Alert: handshake failure",
                            "is_anonymous": false,
                            "openssl_name": "TLS_AES_128_CCM_SHA256",
                            "ssl_version": "TLSV1_3"
                        },
                        {
                            "handshake_error_message": "TLS / Alert: handshake failure",
                            "is_anonymous": false,
                            "openssl_name": "TLS_AES_128_CCM_8_SHA256",
                            "ssl_version": "TLSV1_3"
                        }
                    ]
                }
            },
            "server_info": {
                "client_auth_credentials": null,
                "client_auth_requirement": "DISABLED",
                "highest_ssl_version_supported": 6,
                "hostname": "prod-XqiHnDZ0.lab.practical-devsecops.training",
                "http_tunneling_settings": null,
                "ip_address": "x.x.x.x",
                "openssl_cipher_string_supported": "TLS_AES_256_GCM_SHA384",
                "port": 443,
                "tls_server_name_indication": "prod-XqiHnDZ0.lab.practical-devsecops.training",
                "tls_wrapped_protocol": "HTTPS",
                "xmpp_to_hostname": null
            }
        }
    ],
    "invalid_targets": [],
    "sslyze_url": "https://github.com/nabla-c0d3/sslyze",
    "sslyze_version": "2.1.4",
    "total_scan_time": "0.3779592514038086"
```
