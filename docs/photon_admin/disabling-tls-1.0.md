# Disabling TLS 1.0 to Improve Transport Layer Security

Photon OS includes GnuTLS to help secure the transport layer. [GnuTLS](http://www.gnutls.org/) is a library that implements the SSL and TLS protocols to secure communications. 

On Photon OS, SSL 3.0, which contains a known vulnerability, is disabled by default. 

However, TLS 1.0, which also contains known vulnerabilities, is enabled by default.

To turn off TLS 1.0, make a directory named `/etc/gnutls` and then in `/etc/gnutls` create a file named `default-priorities`. In the `default-priorities` file, specify GnuTLS priority strings that remove TLS 1.0 and SSL 3.0 but retain TLS 1.1 and TLS 1.2.

After adding a new `default-priorities` file or after modifying it, you must restart all applications, including SSH, with an open TLS session for the changes to take effect.  

Here is an example of a `default-priorities` file that contains GnuTLS priorities to disable TLS 1.0 and SSL 3.0:  

	cat /etc/gnutls/default-priorities
	SYSTEM=NONE:!VERS-SSL3.0:!VERS-TLS1.0:+VERS-TLS1.1:+VERS-TLS1.2:+AES-128-CBC:+RSA:+SHA1:+COMP-NULL

This example priority string imposes system-specific policies. The NONE keyword means that no algorithms, protocols, or compression methods are enabled, so that you can enable specific versions individually later in the string. The example priority string then specifies that SSL version 3.0 and TLS version 1.0 be removed, as marked by the exclamation point. The priority string then enables, as marked by the plus sign, versions 1.1 and 1.2 of TLS. The cypher is AES-128-CBC. The key exchange is RSA. The MAC is SHA1. And the compression algorithm is COMP-NULL.

On Photon OS, you can verify the system-specific policies in the `default-priorities` file as follows. 

Concatenate the `default-priorities` file to check its contents: 

	root@photon-rc [ ~ ]# cat /etc/gnutls/default-priorities
	SYSTEM=NONE:!VERS-SSL3.0:!VERS-TLS1.0:+VERS-TLS1.1:+VERS-TLS1.2:+AES-128-CBC:+RSA:+SHA1:+COMP-NULL

Run the following command to check the protocols that are enabled for the system: 

	root@photon-rc [ /etc/gnutls ]# gnutls-cli --priority @SYSTEM -l
	Cipher suites for @SYSTEM
	TLS_RSA_AES_128_CBC_SHA1                                0x00, 0x2f      SSL3.0

	Certificate types: none
	Protocols: VERS-TLS1.1, VERS-TLS1.2
	Compression: COMP-NULL
	Elliptic curves: none
	PK-signatures: none

For information about the GnuTLS priority strings, see [https://gnutls.org/manual/html_node/Priority-Strings.html](https://gnutls.org/manual/html_node/Priority-Strings.html).

For information about the vulnerability in SSL 3.0, see [SSL 3.0 Protocol Vulnerability and POODLE Attack](https://www.us-cert.gov/ncas/alerts/TA14-290A).

For information about the vulnerabilities in TLS 1.0, see [Guidelines for the Selection, Configuration, and Use of Transport Layer Security (TLS) Implementations](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r1.pdf).
