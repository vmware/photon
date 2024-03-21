/*
 * Copyright (C) 2019 - 2022, Stephan Mueller <smueller@chronox.de>
 *
 * License: see LICENSE file in root directory
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 */

#include <errno.h>
#include <string.h>
#include <strings.h>

#include "cipher_definitions.h"
#include "logger.h"
#include "algorithms.h"

static const struct { char *algo; uint64_t cipher; } conv[] = {
	{"ACVP-AES-ECB", ACVP_ECB},
	{"ACVP-AES-CBC-CS1", ACVP_CBC_CS1 },
	{"ACVP-AES-CBC-CS2", ACVP_CBC_CS2 },
	{"ACVP-AES-CBC-CS3", ACVP_CBC_CS3 },
	{"ACVP-AES-CBC", ACVP_CBC},
	{"ACVP-AES-OFB", ACVP_OFB},
	{"ACVP-AES-CFB8", ACVP_CFB8},
	{"ACVP-AES-CFB128", ACVP_CFB128},
	{"ACVP-AES-CFB1", ACVP_CFB1},
	{"ACVP-AES-CTR", ACVP_CTR},
	{"ACVP-AES-GCM-SIV", ACVP_GCMSIV},
	{"ACVP-AES-GCM", ACVP_GCM},
	{"ACVP-AES-GMAC", ACVP_GMAC},
	{"ACVP-AES-CCM", ACVP_CCM},
	{"ACVP-AES-XTS", ACVP_XTS},
	{"ACVP-AES-KWP", ACVP_KWP},
	{"ACVP-AES-KW", ACVP_KW},
	{"AES-128", ACVP_AES128},
	{"AES-192", ACVP_AES192},
	{"AES-256", ACVP_AES256},

	{"ACVP-TDES-ECB", ACVP_TDESECB},
	{"ACVP-TDES-CBC", ACVP_TDESCBC},
	{"ACVP-TDES-OFB", ACVP_TDESOFB},
	{"ACVP-TDES-CFB1", ACVP_TDESCFB1},
	{"ACVP-TDES-CFB8", ACVP_TDESCFB8},
	{"ACVP-TDES-CFB64", ACVP_TDESCFB64},
	{"ACVP-TDES-CTR", ACVP_TDESCTR},
	{"ACVP-TDES-KW", ACVP_TDESKW},
	/* CTR DRBG */
	{"3keyTDEA", ACVP_TDESECB},

	{"CMAC-AES", ACVP_AESCMAC},
	{"CMAC-AES128", ACVP_AESCMAC},
	{"CMAC-AES192", ACVP_AESCMAC},
	{"CMAC-AES256", ACVP_AESCMAC},
	{"CMAC-TDES", ACVP_TDESCMAC},
	{"HMAC-SHA-1", ACVP_HMACSHA1},
	{"HMAC-SHA2-224", ACVP_HMACSHA2_224},
	{"HMAC-SHA2-256", ACVP_HMACSHA2_256},
	{"HMAC-SHA2-384", ACVP_HMACSHA2_384},
	{"HMAC-SHA2-512/224", ACVP_HMACSHA2_512224},
	{"HMAC-SHA2-512/256", ACVP_HMACSHA2_512256},
	{"HMAC-SHA2-512\\/224", ACVP_HMACSHA2_512224},
	{"HMAC-SHA2-512\\/256", ACVP_HMACSHA2_512256},
	{"HMAC-SHA2-512", ACVP_HMACSHA2_512},
	{"HMAC-SHA3-224", ACVP_HMACSHA3_224},
	{"HMAC-SHA3-256", ACVP_HMACSHA3_256},
	{"HMAC-SHA3-384", ACVP_HMACSHA3_384},
	{"HMAC-SHA3-512", ACVP_HMACSHA3_512},
	{"KMAC-256", ACVP_KMAC256},
	{"KMAC-128", ACVP_KMAC128},

	{"RSA", ACVP_RSA},
	{"ECDSA", ACVP_ECDSA},
	{"EDDSA", ACVP_EDDSA},
	{"DSA", ACVP_DSA},
	{"safePrimes", ACVP_SAFEPRIMES},

	{"SHA-1", ACVP_SHA1},

	{"SHA3-224", ACVP_SHA3_224},
	{"SHA3-256", ACVP_SHA3_256},
	{"SHA3-384", ACVP_SHA3_384},
	{"SHA3-512", ACVP_SHA3_512},
	{"CSHAKE-128", ACVP_CSHAKE128},
	{"CSHAKE-256", ACVP_CSHAKE256},
	{"SHAKE-128", ACVP_SHAKE128},
	{"SHAKE-256", ACVP_SHAKE256},
	{"SHA2-224", ACVP_SHA224},
	{"SHA2-256", ACVP_SHA256},
	{"SHA2-384", ACVP_SHA384},
	{"SHA2-512/224", ACVP_SHA512224},
	{"SHA2-512/256", ACVP_SHA512256},
	{"SHA2-512\\/224", ACVP_SHA512224},
	{"SHA2-512\\/256", ACVP_SHA512256},
	{"SHA2-512", ACVP_SHA512},
	{"ctrDRBG", ACVP_DRBGCTR},
	{"hashDRBG", ACVP_DRBGHASH},
	{"hmacDRBG", ACVP_DRBGHMAC},

	{"KAS-ECC-SSC", ACVP_KAS_ECC_R3_SSC},
	{"KAS-ECC", ACVP_ECDH},
	{"KAS-FFC-SSC", ACVP_KAS_FFC_R3_SSC},
	{"KAS-FFC", ACVP_DH},
	{"KAS-IFC-SSC", ACVP_KAS_IFC_SSC},
	{"KAS-ED", ACVP_ECDH_ED},

	{"kdf-components", ACVP_KDF_COMPONENT},
	{"PBKDF", ACVP_PBKDF},
	{"KAS-KDF", ACVP_HKDF},
	{"KDA", ACVP_HKDF},
	{"KDF", ACVP_KDF_800_108},
	{"TLS-v1.3", ACVP_KDF_TLS13},
	{"TLS-v1.2", ACVP_KDF_TLS12},
	{"double pipeline iteration", ACVP_KDF_108_DOUBLE_PIPELINE},
	{"feedback", ACVP_KDF_108_FEEDBACK},
	{"counter", ACVP_KDF_108_COUNTER},
	{"after fixed data", ACVP_KDF_108_AFTER_FIXED},
	{"before fixed data", ACVP_KDF_108_BEFORE_FIXED},
	{"middle fixed data", ACVP_KDF_108_MIDDLE_FIXED},
	{"before iterator", ACVP_KDF_108_BEFORE_ITERATOR},

	{"P-192", ACVP_NISTP192},
	{"P-224", ACVP_NISTP224},
	{"P-256", ACVP_NISTP256},
	{"P-384", ACVP_NISTP384},
	{"P-521", ACVP_NISTP521},
	{"K-163", ACVP_NISTK163},
	{"K-233", ACVP_NISTK233},
	{"K-283", ACVP_NISTK283},
	{"K-409", ACVP_NISTK409},
	{"K-571", ACVP_NISTK571},
	{"B-163", ACVP_NISTB163},
	{"B-233", ACVP_NISTB233},
	{"B-283", ACVP_NISTB283},
	{"B-409", ACVP_NISTB409},
	{"B-571", ACVP_NISTB571},

	{"ED-25519", ACVP_ED25519},
	{"ED-448", ACVP_ED448},

	{"KTS-IFC", ACVP_KTS_IFC},
	/* KTS schema */
	{"KTS-OAEP-basic", ACVP_KTS_SCHEMA_OAEP_BASIC},
	{"KTS-OAEP-Party_V-confirmation", ACVP_KTS_SCHEMA_OAEP_PARTY_V_CONF},
	{"KAS1", ACVP_KAS1_SCHEMA_BASIC},
	{"KAS1-basic", ACVP_KAS1_SCHEMA_BASIC},
	{"KAS1-Party_V-confirmation", ACVP_KAS1_SCHEMA_PARTY_V_CONF},
	{"KAS2-basic", ACVP_KAS2_SCHEMA_BASIC},
	{"KAS2-bilateral-confirmation", ACVP_KAS2_SCHEMA_BILATERAL_CONF},
	{"KAS2-Party_U-confirmation", ACVP_KAS2_SCHEMA_PARTY_U_CONF},
	{"KAS2-Party_V-confirmation", ACVP_KAS2_SCHEMA_PARTY_V_CONF},
	/* KTS key generation method */
	{"rsakpg1-basic", ACVP_KAS_KEYGEN_RSAKPG1_BASIC},
	{"rsakpg1-prime-factor", ACVP_KAS_KEYGEN_RSAKPG1_PRIME_FACTOR},
	{"rsakpg1-crt", ACVP_KAS_KEYGEN_RSAKPG1_CRT},
	{"rsakpg2-basic", ACVP_KAS_KEYGEN_RSAKPG2_BASIC},
	{"rsakpg2-prime-factor", ACVP_KAS_KEYGEN_RSAKPG2_PRIME_FACTOR},
	{"rsakpg2-crt", ACVP_KAS_KEYGEN_RSAKPG2_CRT},
	{"None", ACVP_KAS_ENCODING_NONE},
	{"concatenation", ACVP_KAS_ENCODING_CONCATENATION},

	/* SSH */
	{"TDES", ACVP_TDESECB},

	/* Conversion from uint64_t back to a name */
	{"ctrDRBG_AES128", ACVP_DRBGCTR | ACVP_AES128},
	{"ctrDRBG_AES192", ACVP_DRBGCTR | ACVP_AES192},
	{"ctrDRBG_AES256", ACVP_DRBGCTR | ACVP_AES256},
	{"ctrDRBG_TDES", ACVP_DRBGCTR | ACVP_TDESECB},
	{"hashDRBG_SHA-1", ACVP_DRBGHASH | ACVP_SHA1},
	{"hashDRBG_SHA-224", ACVP_DRBGHASH | ACVP_SHA224},
	{"hashDRBG_SHA-256", ACVP_DRBGHASH | ACVP_SHA256},
	{"hashDRBG_SHA-384", ACVP_DRBGHASH | ACVP_SHA384},
	{"hashDRBG_SHA-512", ACVP_DRBGHASH | ACVP_SHA512},
	{"hashDRBG_SHA-512224", ACVP_DRBGHASH | ACVP_SHA512224},
	{"hashDRBG_SHA-512256", ACVP_DRBGHASH | ACVP_SHA512256},
	{"hmacDRBG_SHA-1", ACVP_DRBGHMAC | ACVP_SHA1},
	{"hmacDRBG_SHA-224", ACVP_DRBGHMAC | ACVP_SHA224},
	{"hmacDRBG_SHA-256", ACVP_DRBGHMAC | ACVP_SHA256},
	{"hmacDRBG_SHA-384", ACVP_DRBGHMAC | ACVP_SHA384},
	{"hmacDRBG_SHA-512", ACVP_DRBGHMAC | ACVP_SHA512},
	{"hmacDRBG_SHA-512224", ACVP_DRBGHMAC | ACVP_SHA512224},
	{"hmacDRBG_SHA-512256", ACVP_DRBGHMAC | ACVP_SHA512256},

	{"MODP-2048", ACVP_DH_MODP_2048},
	{"MODP-3072", ACVP_DH_MODP_3072},
	{"MODP-4096", ACVP_DH_MODP_4096},
	{"MODP-6144", ACVP_DH_MODP_6144},
	{"MODP-8192", ACVP_DH_MODP_8192},
	{"ffdhe2048", ACVP_DH_FFDHE_2048},
	{"ffdhe3072", ACVP_DH_FFDHE_3072},
	{"ffdhe4096", ACVP_DH_FFDHE_4096},
	{"ffdhe6144", ACVP_DH_FFDHE_6144},
	{"ffdhe8192", ACVP_DH_FFDHE_8192},
	{"FB", ACVP_DH_FB},
	{"FC", ACVP_DH_FC},
};

uint64_t convert_algo_cipher(const char *algo, uint64_t cipher)
{
	uint64_t p_res = 0;
	unsigned int i;

	logger(LOGGER_DEBUG, "Convert cipher %s into internal representation\n",
	       algo);

	if (!algo) return ACVP_UNKNOWN;

	for (i = 0; i < ARRAY_SIZE(conv); i++) {
		size_t len = strlen(conv[i].algo);

		if ((strlen(algo) == len) &&
		    !strncasecmp(algo, conv[i].algo, len)) {
			p_res = conv[i].cipher;
			break;
		}
	}
	if (p_res == 0)
		return ACVP_UNKNOWN;

	return (cipher | p_res);
}

int convert_cipher_match(uint64_t cipher1, uint64_t cipher2,
			 uint64_t cipher_type_mask)
{
	uint64_t typemask = cipher_type_mask | ACVP_CIPHERDEF;

	return ((cipher1 & typemask) == (cipher2 & typemask));
}

int convert_cipher_contain(uint64_t cipher1, uint64_t cipher2,
			   uint64_t cipher_type_mask)
{
	uint64_t typemask = cipher_type_mask ? cipher_type_mask :
					       ACVP_CIPHERTYPE;

	return ((cipher1 & typemask) & ((cipher2) & typemask) &&
	        (cipher1 & ACVP_CIPHERDEF) & ((cipher2) & ACVP_CIPHERDEF));
}

int convert_cipher_algo(uint64_t cipher, uint64_t cipher_type_mask,
			const char **algo)
{
	unsigned int i;
	unsigned int found = 0;

	if (!algo)
		return -EINVAL;

	for (i = 0; i < ARRAY_SIZE(conv); i++) {
		if (convert_cipher_match(cipher, conv[i].cipher,
					 cipher_type_mask)) {
			*algo = conv[i].algo;
			found = 1;
			break;
		}
	}

	if (!found)
		return -EINVAL;

	return 0;
}
