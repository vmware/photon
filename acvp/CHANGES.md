v2.1.4
- enhancement: add OpenSSL DH keygen
- enhancement: add regression test support for GCM internal IV, keyGen, sigGen, pqgGen, KAS-ECC, KAS-FFC, SP800-108 KDF
- enhancement: add TLS 1.2 RFC7627 support to OpenSSL
- enhancement: use C11
- enhancement: add regression tests for non-KAT tests (see REGRESSION_VECTOR_REPLACE in helper/exec_lib.sh for list of supported algorithms)
- enhancement: add ANSI X9.63 parser
- fix: update HKDF parser to match current specification

v2.1.3
- fix: LDT
- enhancement: allow parser to be compiled as a library - patch provided by Daniel Ojalvo
- enhancement: add OpenSSL 3 support - patch provided by VMWare

v2.1.2
- fix: strlcpy behaves differently than strncpy leading to an off-by-one
- fix: OpenSSL header files to allow it being built on the FIPS canister
- fix: add IV to GMAC test result if an IV is provided
- enhancement: add full LRNG testing

v2.1.1
- fix: update TLS v1.3 response following the spec update
- enhancement: RSA OAEP testing added
- enhancement: add FB/FC support for SP800-56A rev 3

v2.1.0
- fix: KTS OAEP responder validation test result reporting
- enhancement: add TLS v1.3 parser
- enhancement: add SP800-56C rev 1 parser
- enhancement: add SP800-56C rev 1 test (in lieu for TLS v1.3 KDF) for OpenSSL
- enhancement: add working RSADP test

v2.0.0
- fix OpenSSL ECDH with B/K curves
- enhancement: allow SHA/SHAKE inner loop to be implemented in backend - note, this change mandates a backend to add an initializer to the SHA backend definition. Use the sha_backend->hash_mct_inner_loop function pointer to implement the inner loop in the backend. To support the MCT implementation, parser_sha_mct_helper.h may be used.
- enhancement: parse the HMAC/CMAC MAC length field and provide it to backends

v1.2.0
- fix: TDES CFB64 and OFB produce the right IVs
- enhancement: add LDT support

v1.1.0
- split out PBKDF from kdf-components to comply with ACVP server structure
- enhancement: add -t - this currently only applies to ECDSA siggen to create a sigver test vector
- enhancement: add KTS IFC testing (note, the OpenSSL backend currently is intended to show that the KTS IFC parsing works)
- enhancement: allow compilation with C++
- fix: OpenSSL 1.0.2 DRBG without DF works

v1.0.0
- reorganization of cipher flags - for matching ciphers, you MUST use convert_cipher_match or convert_cipher_contains, respectively. See cipher_definitions.h for details
- move safeprimes to parser/safeprime.h which is automatically included to backends with backend_common.h
- addition of KAS_FFC_SSC parser
- addition of KAS_ECC_SSC parser
- OpenSSL: addition of KAS_FFC_SSC testing
- OpenSSL: addition of KAS_ECC_SSC testing
- enhancement: The parser can hand off the AES MCT inner loop to the backend. For that, the inner_loop_final_cj1 buffer is added to struct sym_data allowing the backend to decide whether it handles the inner loop of the MCT - an example how to extract the MCT inner loop is given with function openssl_mct_update_inner_loop
- enhancement: add RFC7919 primes

v0.8.0
- add DH safeprime keygen test support
- API change, enhancement: add DH safeprime keyver test support - struct dsa_backend now contains a dsa_keyver entry that must be filled in
- OpenSSL: add DH safeprime keygen implementation
- OpenSSL: add DH safeprime keyver implementation
- OpenSSL: fix DSA PQG verification invocation

v0.7.0
- OpenSSL: fix memory corruption in ECDH component testing
- add P-192 support
- OpenSSL: add DH_generate_key testing
- DSA keygen: fix padding of PQG values leading to spurious DSA keygen errors
- fix SHA-512/224 and SHA-512/256 parsing
- fix DRBG definition: add data->type to hold the DRBG type

v0.6.3
- OpenSSL: support for invcation of P224 and P192 (P192 is deactivated in OpenSSL though)
- AES: updated key shuffle for MCT to follow specification precisely
- add ARM64 support for OpenSSL

v0.6.2
- fix exec_lib.sh
- OpenSSL: increase number of RSA keygen retries
- addition of ECDSA sigver component for OpenSSL
- addition of RSA PSS / X9.31 for OpenSSL

v0.6.1
- addition of RSADP for OpenSSL
- add first bits of ECDSA primitive testing
- add HKDF and Curve25519 internal testing

v0.6.0
- remove requirement for mct_get_last_iv
- PBKDF: data->password.len now truly contains the correct length of the password
- add RSA signature primitive and decryption primitive support
- ACVP server sample files can be used in regression testing (-e option)
- fix: Invoke RSA_generate_key_ex multiple times if one invocation fails
- add private version of HKDF protocol
- add private version of ED-ECDH
- fixes for -Wconversion and -Wdocumentation

v0.5.3
- reenable OpenSSL FIPS mode
- add new TLS KDF and SSH KDF implementations to OpenSSL
- add OpenSSL 1.0.x support
- add AES GMAC support
- rename test case references from Common to "Generic C" to be compliant with
  ACVP Proxy

v0.5.2
- add PBKDF2 support for OpenSSL

v0.5.1
- OpenSSL add support for upstream CTR DRBG
- Add support for AES-CBC-CS*
- add color-coded logging
- fix some documentation

v0.5.0
- Add SHAKE support for OpenSSL
- Add Ubuntu-specific OpenSSL handling
- ACVP v1.0 support

v0.4.4:
- Compile ACVP parser tool with -m32 for 32 bit testing
- Fix DSA siggen helper to generate PQG and DSA key at the same time
- constify data in parser_common.c

v0.4.3
- OpenSSL: enable SHA3/HMAC SHA3

Changes 0.4.2
- add helper convert_cipher_algo
- use specific initializations for static variables (some compilers cannot handle generic initializations)
- statically link JSON-C

Changes 0.4.1
 * Addition of helper function to turn an MPI into a byte array

Changes 0.4.0
 * First public release with support for ACVP v0.5
