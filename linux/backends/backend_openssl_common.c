/*
 * Copyright (C) 2018 - 2022, Stephan Müller <smueller@chronox.de>
 * Copyright 2022 VMware, Inc.
 *
 * License: see LICENSE file
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
 *
 * The code uses the interface offered by OpenSSL provided with
 * Fedora 29.
 */

#include "backend_openssl_common.h"
#include "parser_sha_mct_helper.h"

/************************************************
 * General helper functions
 ************************************************/
int openssl_bn2buf(const BIGNUM *number, struct buffer *buf, uint32_t bufsize)
{
	int ret;

	CKINT(alloc_buf(bufsize, buf));
	if (!BN_bn2bin(number, buf->buf + bufsize - BN_num_bytes(number)))
		return -EFAULT;

	logger_binary(LOGGER_DEBUG, buf->buf, buf->len, "bn2bin");

out:
	return ret;
}

int openssl_bn2buffer(const BIGNUM *number, struct buffer *buf)
{
	return openssl_bn2buf(number, buf, (uint32_t)BN_num_bytes(number));
}

/* Stolen from crypto/kdf/kbkdf.c */
uint32_t be32(uint32_t host)
{
	uint32_t big = 0;
	const union {
		long one;
		char little;
	} is_endian = { 1 };

	if (!is_endian.little)
		return host;

	big |= (host & 0xff000000) >> 24;
	big |= (host & 0x00ff0000) >> 8;
	big |= (host & 0x0000ff00) << 8;
	big |= (host & 0x000000ff) << 24;
	return big;
}

int openssl_cipher(uint64_t cipher, size_t keylen, const EVP_CIPHER **type)
{
	uint64_t mask;
	int ret = 0;
	const EVP_CIPHER *l_type = NULL;
	const char *algo;

	switch (cipher) {
	case ACVP_ECB:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_ecb();
			break;
		case 24:
			l_type = EVP_aes_192_ecb();
			break;
		case 32:
			l_type = EVP_aes_256_ecb();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_CBC:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_cbc();
			break;
		case 24:
			l_type = EVP_aes_192_cbc();
			break;
		case 32:
			l_type = EVP_aes_256_cbc();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_OFB:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_ofb();
			break;
		case 24:
			l_type = EVP_aes_192_ofb();
			break;
		case 32:
			l_type = EVP_aes_256_ofb();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_CFB1:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_cfb1();
			break;
		case 24:
			l_type = EVP_aes_192_cfb1();
			break;
		case 32:
			l_type = EVP_aes_256_cfb1();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_CFB8:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_cfb8();
			break;
		case 24:
			l_type = EVP_aes_192_cfb8();
			break;
		case 32:
			l_type = EVP_aes_256_cfb8();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_CFB128:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_cfb();
			break;
		case 24:
			l_type = EVP_aes_192_cfb();
			break;
		case 32:
			l_type = EVP_aes_256_cfb();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_CTR:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_ctr();
			break;
		case 24:
			l_type = EVP_aes_192_ctr();
			break;
		case 32:
			l_type = EVP_aes_256_ctr();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;

	case ACVP_GMAC:
	case ACVP_GCM:
		mask = ACVP_CIPHERTYPE_AEAD;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_gcm();
			break;
		case 24:
			l_type = EVP_aes_192_gcm();
			break;
		case 32:
			l_type = EVP_aes_256_gcm();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_CCM:
		mask = ACVP_CIPHERTYPE_AEAD;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_ccm();
			break;
		case 24:
			l_type = EVP_aes_192_ccm();
			break;
		case 32:
			l_type = EVP_aes_256_ccm();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_XTS:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 32:
			l_type = EVP_aes_128_xts();
			break;
		case 64:
			l_type = EVP_aes_256_xts();
			break;
		case 48:
			logger(LOGGER_WARN, "Key size not supported\n");
			ret = -EINVAL;
			goto out;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_TDESECB:
		mask = ACVP_CIPHERTYPE_TDES;
		l_type = EVP_des_ede3_ecb();
		break;
	case ACVP_TDESCBC:
		mask = ACVP_CIPHERTYPE_TDES;
		l_type = EVP_des_ede3_cbc();
		break;
	case ACVP_TDESCFB1:
		mask = ACVP_CIPHERTYPE_TDES;
		l_type = EVP_des_ede3_cfb1();
		break;
	case ACVP_TDESCFB8:
		mask = ACVP_CIPHERTYPE_TDES;
		l_type = EVP_des_ede3_cfb8();
		break;
	case ACVP_TDESCFB64:
		mask = ACVP_CIPHERTYPE_TDES;
		l_type = EVP_des_ede3_cfb64();
		break;
	case ACVP_TDESOFB:
		mask = ACVP_CIPHERTYPE_TDES;
		l_type = EVP_des_ede3_ofb();
		break;

	case ACVP_AESCMAC:
		mask = ACVP_CIPHERTYPE_CMAC;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_cbc();
			break;
		case 24:
			l_type = EVP_aes_192_cbc();
			break;
		case 32:
			l_type = EVP_aes_256_cbc();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_TDESCMAC:
		mask = ACVP_CIPHERTYPE_CMAC;
		l_type = EVP_des_ede3_cbc();
		break;
#ifdef OPENSSL_AESKW
	case ACVP_KW:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_wrap();
			break;
		case 24:
			l_type = EVP_aes_192_wrap();
			break;
		case 32:
			l_type = EVP_aes_256_wrap();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
	case ACVP_KWP:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_aes_128_wrap_pad();
			break;
		case 24:
			l_type = EVP_aes_192_wrap_pad();
			break;
		case 32:
			l_type = EVP_aes_256_wrap_pad();
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
#endif
#ifdef OPENSSL_30X
	case ACVP_CBC_CS1:
	case ACVP_CBC_CS2:
	case ACVP_CBC_CS3:
		mask = ACVP_CIPHERTYPE_AES;
		switch (keylen) {
		case 16:
			l_type = EVP_CIPHER_fetch(NULL, "AES-128-CBC-CTS", NULL);
			break;
		case 24:
			l_type = EVP_CIPHER_fetch(NULL, "AES-192-CBC-CTS", NULL);
			break;
		case 32:
			l_type = EVP_CIPHER_fetch(NULL, "AES-256-CBC-CTS", NULL);
			break;
		default:
			logger(LOGGER_WARN, "Unknown key size\n");
			ret = -EINVAL;
			goto out;
		}
		break;
#endif
	default:
		logger(LOGGER_WARN, "Unknown cipher\n");
		ret = -EINVAL;
		goto out;
	}

	CKINT(convert_cipher_algo(cipher, mask, &algo));

	logger(LOGGER_DEBUG, "Key size = %zu\n", keylen);
	logger(LOGGER_DEBUG, "Cipher = %s\n", algo);

	*type = l_type;

out:
	return ret;
}

int openssl_md_convert(uint64_t cipher, const EVP_MD **type)
{
	int ret = 0;
	const EVP_MD *l_type = NULL;
	const char *algo;

	CKINT(convert_cipher_algo(cipher & (ACVP_HASHMASK | ACVP_HMACMASK |
					    ACVP_SHAKEMASK),
				  ACVP_CIPHERTYPE_HASH | ACVP_CIPHERTYPE_HMAC | ACVP_CIPHERTYPE_XOF,
				  &algo));

	logger(LOGGER_DEBUG, "SHA = %s\n", algo);

	switch (cipher & (ACVP_HASHMASK | ACVP_HMACMASK | ACVP_SHAKEMASK)) {
	case ACVP_HMACSHA1:
	case ACVP_SHA1:
		l_type = EVP_sha1();
		break;
	case ACVP_HMACSHA2_224:
	case ACVP_SHA224:
		l_type = EVP_sha224();
		break;
	case ACVP_HMACSHA2_256:
	case ACVP_SHA256:
		l_type = EVP_sha256();
		break;
	case ACVP_HMACSHA2_384:
	case ACVP_SHA384:
		l_type = EVP_sha384();
		break;
	case ACVP_HMACSHA2_512:
	case ACVP_SHA512:
		l_type = EVP_sha512();
		break;
#ifdef OPENSSL_30X
	case ACVP_HMACSHA2_512224:
	case ACVP_SHA512224:
		l_type = EVP_sha512_224();
		break;
	case ACVP_HMACSHA2_512256:
	case ACVP_SHA512256:
		l_type = EVP_sha512_256();
		break;
#endif
#ifdef OPENSSL_SSH_SHA3
	case ACVP_HMACSHA3_224:
	case ACVP_SHA3_224:
		l_type = EVP_sha3_224();
		break;
	case ACVP_HMACSHA3_256:
	case ACVP_SHA3_256:
		l_type = EVP_sha3_256();
		break;
	case ACVP_HMACSHA3_384:
	case ACVP_SHA3_384:
		l_type = EVP_sha3_384();
		break;
	case ACVP_HMACSHA3_512:
	case ACVP_SHA3_512:
		l_type = EVP_sha3_512();
		break;

	case ACVP_SHAKE128:
		l_type = EVP_shake128();
		break;
	case ACVP_SHAKE256:
		l_type = EVP_shake256();
		break;
#endif

	default:
		logger(LOGGER_WARN, "Unknown cipher\n");
		ret = -EINVAL;
	}

	*type = l_type;

out:
	return ret;
}

int openssl_hash_ss(uint64_t cipher, struct buffer *ss, struct buffer *hashzz)
{
	const EVP_MD *md = NULL;
	EVP_MD_CTX *ctx = NULL;
	int ret = 0;

	if (cipher & ACVP_HASHMASK) {
		unsigned char hashzz_tmp[64];
		unsigned int hashlen;
		unsigned int compare = 0;

		CKINT(openssl_md_convert(cipher & ACVP_HASHMASK, &md));

		if (hashzz->len) {
			compare = 1;
		} else {
			CKINT_LOG(alloc_buf((size_t)EVP_MD_size(md), hashzz),
					"Cannot allocate hashzz buffer\n");
			logger(LOGGER_DEBUG,
					"Hash buffer of size %zu allocated\n",
					hashzz->len);
		}

		ctx = EVP_MD_CTX_create();
		CKNULL(ctx, -ENOMEM);

		CKINT_O_LOG(EVP_DigestInit(ctx, md),
				"EVP_DigestInit() failed\n");
		CKINT_O_LOG(EVP_DigestUpdate(ctx, ss->buf, ss->len),
				"EVP_DigestUpdate() failed\n");
		CKINT_O_LOG(EVP_DigestFinal(ctx, hashzz_tmp, &hashlen),
				"EVP_DigestFinal() failed\n");

		logger_binary(LOGGER_DEBUG, hashzz_tmp, hashlen,
				"shared secret hash");

		if (compare) {
			logger_binary(LOGGER_DEBUG, hashzz->buf, hashzz->len,
					"expected shared secret hash");
			if (memcmp(hashzz->buf, hashzz_tmp, hashzz->len))
				ret = -ENOENT;
			else
				ret = 0;
		} else {
			memcpy(hashzz->buf, &hashzz_tmp, hashzz->len);
		}
	} else {
		if (hashzz->len) {
			if (ss->len != hashzz->len) {
				logger(LOGGER_ERR, "expected shared secret length is different from calculated shared secret\n");
				ret = -ENOENT;
				goto out;
			}
			logger_binary(LOGGER_DEBUG, hashzz->buf, hashzz->len,
					"expexted shared secret hash");
			if (memcmp(hashzz->buf, ss->buf, hashzz->len))
				ret = -ENOENT;
			else
				ret = 0;
		} else {
			hashzz->buf = ss->buf;
			hashzz->len = ss->len;

			/* ensure that free_buf does not free the buffer */
			ss->buf = NULL;
			ss->len = 0;

			logger_binary(LOGGER_DEBUG, hashzz->buf, hashzz->len,
					"Shared secret");
		}
	}

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);

	return ret;
}

int _openssl_ecdsa_curves(uint64_t curve, int *out_nid, char *digest)
{
	int nid;
	char dgst[50];
	logger(LOGGER_DEBUG, "curve : %" PRIu64 "\n", curve);

	switch (curve & ACVP_CURVEMASK) {
		case ACVP_NISTB163:
			nid = NID_sect163r2;
			strcpy(dgst, "B-163");
			break;
		case ACVP_NISTK163:
			nid = NID_sect163k1;
			strcpy(dgst, "K-163");
			break;
		case ACVP_NISTB233:
			nid = NID_sect233r1;
			strcpy(dgst, "B-233");
			break;
		case ACVP_NISTK233:
			nid = NID_sect233k1;
			strcpy(dgst, "K-233");
			break;
		case ACVP_NISTB283:
			nid = NID_sect283r1;
			strcpy(dgst, "B-283");
			break;
		case ACVP_NISTK283:
			nid = NID_sect283k1;
			strcpy(dgst, "K-283");
			break;
		case ACVP_NISTB409:
			nid = NID_sect409r1;
			strcpy(dgst, "B-409");
			break;
		case ACVP_NISTK409:
			nid = NID_sect409k1;
			strcpy(dgst, "K-409");
			break;
		case ACVP_NISTB571:
			nid = NID_sect571r1;
			strcpy(dgst, "B-571");
			break;
		case ACVP_NISTK571:
			nid = NID_sect571k1;
			strcpy(dgst, "K-571");
			break;
		case ACVP_NISTP192:
			nid = NID_X9_62_prime192v1;
			strcpy(dgst, "P-192");
			break;
		case ACVP_NISTP224:
			nid = NID_secp224r1;
			strcpy(dgst, "P-224");
			break;
		case ACVP_NISTP256:
			nid = NID_X9_62_prime256v1;
			strcpy(dgst, "P-256");
			break;
		case ACVP_NISTP384:
			nid = NID_secp384r1;
			strcpy(dgst, "P-384");
			break;
		case ACVP_NISTP521:
			nid = NID_secp521r1;
			strcpy(dgst, "P-521");
			break;
		default:
			logger(LOGGER_ERR, "Unknown curve\n");
			return -EINVAL;
	}

	*out_nid = nid;
	if(digest != NULL){
		strcpy(digest, dgst);
	}
	return 0;
}

#ifdef OPENSSL_SSH_SHA3
static int openssl_shake_cb(EVP_MD_CTX *ctx, unsigned char *md, size_t size)
{
	return EVP_DigestFinalXOF(ctx, md, size);
}
#else
static int openssl_shake_cb(EVP_MD_CTX *ctx, unsigned char *md, size_t size)
{
	(void)ctx;
	(void)md;
	(void)size;
	return -EOPNOTSUPP;
}
#endif

/************************************************
 * Symmetric cipher interface functions
 ************************************************/
static int openssl_mct_init(struct sym_data *data, flags_t parsed_flags)
{
	EVP_CIPHER_CTX *ctx = NULL;
	const EVP_CIPHER *type = NULL;
	int ret = 0;

	CKINT(openssl_cipher(data->cipher, data->key.len, &type));

	ctx = EVP_CIPHER_CTX_new();
	CKNULL(ctx, -ENOMEM);

	if (parsed_flags & FLAG_OP_ENC)
		ret = EVP_EncryptInit_ex(ctx, type, NULL, data->key.buf,
					 data->iv.buf);
	else
		ret = EVP_DecryptInit_ex(ctx, type, NULL, data->key.buf,
					 data->iv.buf);
	CKINT_O_LOG(ret, "Cipher init failed\n");

	EVP_CIPHER_CTX_set_padding(ctx, 0);

	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");
	logger_binary(LOGGER_DEBUG, data->iv.buf, data->iv.len, "iv");

	if (data->cipher == ACVP_TDESCFB1 || data->cipher == ACVP_CFB1)
		EVP_CIPHER_CTX_set_flags(ctx, EVP_CIPH_FLAG_LENGTH_BITS);

	data->priv = ctx;

	return 0;

out:
	if (ctx)
		EVP_CIPHER_CTX_free(ctx);
	return ret;
}

#define SEMIBSIZE 8
static int openssl_mct_update(struct sym_data *data, flags_t parsed_flags)
{
	EVP_CIPHER_CTX *ctx = (EVP_CIPHER_CTX *) data->priv;
	size_t origlen = data->data.len;
	int outl;

	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      (parsed_flags & FLAG_OP_ENC) ?
		      "plaintext" : "ciphertext");

	/* For CFB-1 the data is given in bits */
	if ((data->cipher == ACVP_TDESCFB1 || data->cipher == ACVP_CFB1) &&
	    data->data_len_bits) {
		if (data->data_len_bits > (data->data.len << 3)) {
			logger(LOGGER_ERR,
			       "Data length bits (%u bits) is larger than provided data (%zu bytes)\n",
			       data->data_len_bits, data->data.len);
			return -EINVAL;
		}
		origlen = data->data.len;
		data->data.len = data->data_len_bits;
	}

	if (!EVP_CipherUpdate(ctx, data->data.buf, &outl, data->data.buf,
			      (int)data->data.len)) {
		logger(LOGGER_WARN, "Update failed\n");
		return -EFAULT;
	}

	if (!EVP_CipherFinal_ex(ctx, data->data.buf, &outl)) {
		logger(LOGGER_WARN, "Final failed: %s\n",
		       ERR_error_string(ERR_get_error(), NULL));
		return -EFAULT;
	}

	if (data->data.len != origlen)
		data->data.len = origlen;

	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      (parsed_flags & FLAG_OP_ENC) ?
		      "ciphertext" : "plaintext");

	return 0;
}

/*
 * Example for AES MCT inner loop handling in backend
 *
 * This code is meant to be an example - it is meaningless for OpenSSL (but it
 * works!), but when having, say, an HSM where ACVP handling code invoking the
 * HSM crypto code is also found within the HSM, moving this function into that
 * HSM handling code reduces the round trip between the host executing the ACVP
 * parser code and the HSM executing the ACVP handling code a 1000-fold.
 *
 * The MCT inner loop handling logic must return the final cipher text C[j] and
 * the last but one cipher text C[j-1].
 *
 * This code should be invoked when the mct_update function pointer
 * is called by the ACVP parser.
 */
#if 0
static int openssl_mct_update_inner_loop(struct sym_data *data,
					 flags_t parsed_flags)
{
	unsigned int i;
	uint8_t tmp[16];
	int ret;

	/* This code is only meant for AES */
	if (data->cipher &~ ACVP_AESMASK)
		return openssl_mct_update(data, parsed_flags);

	if (data->cipher == ACVP_CFB1 || data->cipher == ACVP_CFB8)
		return openssl_mct_update(data, parsed_flags);

	if (data->cipher != ACVP_ECB && data->iv.len != sizeof(tmp))
		return -EINVAL;
	if (data->data.len != sizeof(tmp))
		return -EINVAL;

	CKINT(alloc_buf(sizeof(tmp), &data->inner_loop_final_cj1));

	memcpy(data->inner_loop_final_cj1.buf, data->iv.buf, data->iv.len);

	/* 999 rounds where the data shuffling is applied */
	for (i = 0; i < 999; i++) {
		CKINT(openssl_mct_update(data, parsed_flags));
		if (data->cipher != ACVP_ECB) {
			memcpy(tmp, data->data.buf, data->data.len);
			memcpy(data->data.buf, data->inner_loop_final_cj1.buf,
			       data->data.len);
			memcpy(data->inner_loop_final_cj1.buf, tmp,
			       data->data.len);
		}
	}

	if (data->cipher == ACVP_ECB)
		memcpy(data->inner_loop_final_cj1.buf, data->data.buf,
		       data->data.len);

	/* final round of calculation without data shuffle */
	CKINT(openssl_mct_update(data, parsed_flags));

out:
	return ret;
}
#endif

static int openssl_mct_fini(struct sym_data *data, flags_t parsed_flags)
{
	EVP_CIPHER_CTX *ctx = (EVP_CIPHER_CTX *) data->priv;

	(void)parsed_flags;

	if (ctx)
		EVP_CIPHER_CTX_free(ctx);
	data->priv = NULL;

	return 0;
}

static int openssl_kw_encrypt(struct sym_data *data, flags_t parsed_flags)
{
	EVP_CIPHER_CTX *ctx = NULL;
	const EVP_CIPHER *type = NULL;
	BUFFER_INIT(ct);
	size_t ctlen;
	int outl;
	int ret = 0;

	(void)parsed_flags;

	CKINT(openssl_cipher(data->cipher, data->key.len, &type));

	ctx = EVP_CIPHER_CTX_new();
	CKNULL(ctx, -ENOMEM);

	EVP_CIPHER_CTX_set_padding(ctx, 0);
	EVP_CIPHER_CTX_set_flags(ctx, EVP_CIPHER_CTX_FLAG_WRAP_ALLOW);

	CKINT_O_LOG(EVP_EncryptInit_ex(ctx, type, NULL, data->key.buf,
			       	       data->iv.buf),
		    "AES KW init failed\n");

	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");
	logger_binary(LOGGER_DEBUG, data->iv.buf, data->iv.len, "iv");
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "plaintext");

	/*
	 * Round up to the nearest AES block boundary as input data for KWP
	 * is not block-aligned.
	 */
	// TODO: should this be ((data->data.len + 15) / 16) * 16; ?
	ctlen = ((data->data.len + 7) / 8) * 8;
	ctlen += SEMIBSIZE;

	CKINT(alloc_buf(ctlen, &ct));

	if (!EVP_CipherUpdate(ctx, ct.buf, &outl, data->data.buf,
			      (int)data->data.len)) {
		logger(LOGGER_WARN, "AES KW encrypt update failed\n");
		ret = -EFAULT;
		goto out;
	}

	ct.len = (size_t)outl;

	if (!EVP_CipherFinal_ex(ctx, ct.buf, &outl)) {
		logger(LOGGER_WARN, "AES KW encrypt final failed\n");
		ret = -EFAULT;
		goto out;
	}

	free_buf(&data->data);
	copy_ptr_buf(&data->data, &ct);

	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "ciphertext");

	ret = 0;

out:
	if (ctx)
		EVP_CIPHER_CTX_free(ctx);
	return ret;
}

static int openssl_kw_decrypt(struct sym_data *data, flags_t parsed_flags)
{
	EVP_CIPHER_CTX *ctx = NULL;
	const EVP_CIPHER *type = NULL;
	int outl;
	int ret = 0;

	(void)parsed_flags;

	CKINT(openssl_cipher(data->cipher, data->key.len, &type));

	ctx = EVP_CIPHER_CTX_new();
	CKNULL(ctx, -ENOMEM);

	EVP_CIPHER_CTX_set_padding(ctx, 0);
	EVP_CIPHER_CTX_set_flags(ctx, EVP_CIPHER_CTX_FLAG_WRAP_ALLOW);

	CKINT_O_LOG(EVP_DecryptInit_ex(ctx, type, NULL, data->key.buf,
			       	       data->iv.buf),
		    "AES KW init failed\n");

	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");
	logger_binary(LOGGER_DEBUG, data->iv.buf, data->iv.len, "iv");
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "ciphertext");


	if (!EVP_CipherUpdate(ctx, data->data.buf, &outl, data->data.buf,
			      (int)data->data.len)) {
		if (data->data.len >= CIPHER_DECRYPTION_FAILED_LEN) {
			memcpy(data->data.buf, CIPHER_DECRYPTION_FAILED,
			       CIPHER_DECRYPTION_FAILED_LEN);
			data->data.len = CIPHER_DECRYPTION_FAILED_LEN;
			ret = 0;
			goto out;
		} else {
			logger(LOGGER_WARN, "AES KW encrypt update failed\n");
			ret = -EFAULT;
			goto out;
		}
	}

	/* Plaintext data block is smaller by one semiblock */
	data->data.len = (size_t)outl;

	if (!EVP_CipherFinal_ex(ctx, data->data.buf, &outl)) {
		logger(LOGGER_WARN, "AES KW encrypt final failed\n");
		ret = -EFAULT;
		goto out;
	}

	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "plaintext");

	ret = 0;

out:
	if (ctx)
		EVP_CIPHER_CTX_free(ctx);
	return ret;
}

static int openssl_encrypt(struct sym_data *data, flags_t parsed_flags)
{
	int ret;

	if (data->cipher == ACVP_KW || data->cipher == ACVP_KWP)
		return openssl_kw_encrypt(data, parsed_flags);

	CKINT(openssl_mct_init(data, parsed_flags));

	ret = openssl_mct_update(data, parsed_flags);

	openssl_mct_fini(data, parsed_flags);

out:
	return ret;
}

static int openssl_decrypt(struct sym_data *data, flags_t parsed_flags)
{
	int ret;

	if (data->cipher == ACVP_KW || data->cipher == ACVP_KWP)
		return openssl_kw_decrypt(data, parsed_flags);

	CKINT(openssl_mct_init(data, parsed_flags));

	ret = openssl_mct_update(data, parsed_flags);

	openssl_mct_fini(data, parsed_flags);

out:
	return ret;
}

static struct sym_backend openssl_sym =
{
	openssl_encrypt,
	openssl_decrypt,
	openssl_mct_init,
	openssl_mct_update, /* or openssl_mct_update_inner_loop */
	openssl_mct_fini,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_sym_backend)
static void openssl_sym_backend(void)
{
	register_sym_impl(&openssl_sym);
}

/************************************************
 * AEAD cipher interface functions
 ************************************************/
#define OPENSSL_USE_OFFICIAL_INTERNAL_IV_GEN
static int openssl_gcm_encrypt(struct aead_data *data, flags_t parsed_flags)
{
	EVP_CIPHER_CTX *ctx = NULL;
	const EVP_CIPHER *type = NULL;
	uint32_t taglen = data->taglen / 8;
	uint32_t ivlen = data->ivlen / 8;
	int ret = 0;

	(void)parsed_flags;

	if (data->iv.len && data->iv.len < 12) {
		logger(LOGGER_WARN,
		       "IV length must be 12 or higher (see code for EVP_CTRL_AEAD_SET_IVLEN)\n");
		return -EINVAL;
	}

	logger_binary(LOGGER_DEBUG, data->iv.buf, data->iv.len, "iv");
	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");
	logger_binary(LOGGER_DEBUG, data->assoc.buf, data->assoc.len, "AAD");
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "plaintext");

	CKINT(alloc_buf(taglen, &data->tag));

	CKINT(openssl_cipher(data->cipher, data->key.len, &type));

	ctx = EVP_CIPHER_CTX_new();
	CKNULL(ctx, -ENOMEM);

	CKINT_O_LOG(EVP_CipherInit_ex(ctx, type, NULL, NULL, NULL, 1),
		    "EVP_CipherInit() during first call failed\n");

	if (data->iv.len) {
		CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN,
						(int)data->iv.len, NULL),
			    "EVP_CIPHER_CTX_ctrl() failed to set the IV length %zu\n",
			    data->iv.len);
	} else {
		if (ivlen < 4) {
			logger(LOGGER_WARN, "IV size too small\n");
			ret = -EINVAL;
			goto out;
		}
		CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN,
						(int)ivlen, NULL),
			    "EVP_CIPHER_CTX_ctrl() failed to set the IV length %zu\n",
			    data->iv.len);

		/*
		 * This code extracts the generated IV and sets it
		 * again with the EVP_CipherInit_ex. The implementation is not
		 * used by the TLS layer.
		 */
#ifndef OPENSSL_USE_OFFICIAL_INTERNAL_IV_GEN
		logger(LOGGER_DEBUG, "Internal IV generation (IV size %u)\n",
		       ivlen);
		/* 96 bit IV */
		CKINT(alloc_buf(ivlen, &data->iv));

		CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN,
						data->iv.len, NULL),
			    "EVP_CIPHER_CTX_ctrl() failed to set the IV length %u\n",
			    data->iv.len);

		CKINT_O(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IV_FIXED, 4,
					    data->iv.buf));
		memcpy(data->iv.buf, EVP_CIPHER_CTX_iv_noconst(ctx),
		       data->iv.len);
#endif
	}

	CKINT_O_LOG(EVP_CipherInit_ex(ctx, NULL, NULL, data->key.buf,
				      data->iv.buf, 1),
		    "EVP_CipherInit_ex() during second call failed (%s)\n",
		    ERR_error_string(ERR_get_error(), NULL));

	/*
	 * Generation of IV must come after setting key due to
	 * EVP_CTRL_GCM_IV_GEN implementation and we set a NULL buffer for IV
	 * above.
	 *
	 * This code is used by the TLS layer.
	 */
#ifdef OPENSSL_USE_OFFICIAL_INTERNAL_IV_GEN
	if (!data->iv.len) {
		logger(LOGGER_DEBUG, "Internal IV generation (IV size %u)\n",
		       ivlen);
		/* 96 bit IV */
		CKINT(alloc_buf(ivlen, &data->iv));

		CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IV_FIXED, 4,
						data->iv.buf),
			    "EVP_CTRL_GCM_SET_IV_FIXED setting fixed value failed\n");
		CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_IV_GEN,
						0, data->iv.buf),
			    "EVP_CIPHER_CTX_ctrl() failed to generate IV %d\n",
			    ret);
	}
#endif

	if (data->assoc.len) {
		CKINT_LOG(EVP_Cipher(ctx, NULL, data->assoc.buf,
				     (unsigned int)data->assoc.len),
			  "EVP_EncryptUpdate() AAD failed\n");
	}

	if (data->data.len) {
		if (EVP_Cipher(ctx, data->data.buf, data->data.buf,
			       (unsigned int)data->data.len) !=
		    (int)data->data.len) {
			logger(LOGGER_WARN,"EVP_Cipher() finaliztion failed\n");
			ret = -EFAULT;
			goto out;
		}
		logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
			      "ciphertext");
	}

	if (EVP_Cipher(ctx, NULL, NULL, 0) < 0) {
		logger(LOGGER_ERR, "EVP_Cipher failed %s\n",
		       ERR_error_string(ERR_get_error(), NULL));
		ret = -EFAULT;
		goto out;
	}

	/* Get the tag */
	CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG,
					(int)data->tag.len, data->tag.buf),
		    "EVP_CIPHER_CTX_ctrl() failed with tag length %zu\n",
		    data->tag.len);

	logger_binary(LOGGER_DEBUG, data->tag.buf, data->tag.len, "tag");

	ret = 0;

out:
	if (ctx)
		EVP_CIPHER_CTX_free(ctx);

	return ret;
}

static int openssl_gcm_decrypt(struct aead_data *data, flags_t parsed_flags)
{
	EVP_CIPHER_CTX *ctx = NULL;
	const EVP_CIPHER *type;
	int ret;

	(void)parsed_flags;

	if (data->iv.len < 12) {
		logger(LOGGER_WARN,
		       "IV length must be 12 or higher (see code for EVP_CTRL_AEAD_SET_IVLEN)\n");
		return -EINVAL;
	}

	logger_binary(LOGGER_DEBUG, data->iv.buf, data->iv.len, "iv");
	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");
	logger_binary(LOGGER_DEBUG, data->tag.buf, data->tag.len, "tag");
	logger_binary(LOGGER_DEBUG, data->assoc.buf, data->assoc.len, "AAD");
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len, "plaintext");

	CKINT(openssl_cipher(data->cipher, data->key.len, &type));

	ctx = EVP_CIPHER_CTX_new();
	CKNULL(ctx, -ENOMEM);

	CKINT_O_LOG(EVP_CipherInit_ex(ctx, type, NULL, NULL, NULL, 0),
		    "EVP_CipherInit() failed\n");

	CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN,
					(int)data->iv.len, NULL),
		    "EVP_CIPHER_CTX_ctrl() for setting IV length failed\n");

	CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG,
					(int)data->tag.len, data->tag.buf),
		    "EVP_CIPHER_CTX_ctrl() for setting tag failed\n");

	CKINT_O_LOG(EVP_CipherInit_ex(ctx, NULL, NULL, data->key.buf,
				      data->iv.buf, 0),
		    "EVP_CipherInit_ex() failed\n");

	if (data->assoc.len) {
		CKINT_LOG(EVP_Cipher(ctx, NULL, data->assoc.buf,
				     (unsigned int)data->assoc.len),
			  "EVP_EncryptUpdate() AAD failed\n");
	}

	data->integrity_error = 0;

	if (data->data.len) {
		if (EVP_Cipher(ctx, data->data.buf, data->data.buf,
			       (unsigned int)data->data.len) !=
		    (int)data->data.len) {
			logger(LOGGER_DEBUG, "EVP_Cipher() finalization failed\n");
			data->integrity_error = 1;
		}
	}

	if (EVP_Cipher(ctx, NULL, NULL, 0) < 0) {
		logger(LOGGER_DEBUG, "EVP_Cipher() finalization failed\n");
		data->integrity_error = 1;
	}

	ret = 0;

out:
	if (ctx)
		EVP_CIPHER_CTX_free(ctx);

	return ret;
}

static int openssl_ccm_encrypt(struct aead_data *data, flags_t parsed_flags)
{
	EVP_CIPHER_CTX *ctx = NULL;
	const EVP_CIPHER *type;
	uint32_t taglen = data->taglen / 8;
	int ret = 0;

	(void)parsed_flags;

	logger_binary(LOGGER_VERBOSE, data->key.buf, data->key.len, "key");
	logger_binary(LOGGER_VERBOSE, data->iv.buf, data->iv.len, "iv");
	logger_binary(LOGGER_VERBOSE, data->assoc.buf, data->assoc.len, "AAD");
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "plaintext");

	CKINT(alloc_buf(taglen, &data->tag));

	if (!data->data.len) {
		CKINT(alloc_buf(1, &data->data));
		data->data.len = 0;
	}

	CKINT(openssl_cipher(data->cipher, data->key.len, &type));

	ctx = EVP_CIPHER_CTX_new();
	CKNULL(ctx, -ENOMEM);

	CKINT_O_LOG(EVP_CipherInit_ex(ctx, type, NULL, NULL, NULL, 1),
		    "EVP_CipherInit_ex() failed\n");

	CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_CCM_SET_IVLEN,
					(int)data->iv.len, NULL),
		    "EVP_CTRL_CCM_SET_IVLEN failed\n");

	CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_CCM_SET_TAG, (int)taglen,
					NULL),
		    "EVP_CTRL_CCM_SET_TAG failed (%u)\n", taglen);

	CKINT_O_LOG(EVP_CipherInit_ex(ctx, NULL, NULL, data->key.buf,
				      data->iv.buf, 1),
		    "EVP_CipherInit_ex() failed\n");

	/* Set the length as defined in the man page */
	if (EVP_Cipher(ctx, NULL, NULL, (unsigned int)data->data.len) !=
	    (int)data->data.len) {
		logger(LOGGER_WARN, "EVP_Cipher() setting length failed\n");
		ret = -EFAULT;
		goto out;
	}

	/*
	 * Provide any AAD data. This can be called zero or more times as
	 * required
	 */
	if (data->assoc.len) {
		CKINT_LOG(EVP_Cipher(ctx, NULL, data->assoc.buf,
				     (unsigned int)data->assoc.len),
			  "EVP_EncryptUpdate() encrypt AAD failed\n");
	}

	if (EVP_Cipher(ctx, data->data.buf, data->data.buf,
		       (unsigned int)data->data.len) !=
	    (int)data->data.len) {
		logger(LOGGER_WARN,"EVP_Cipher() finaliztion failed\n");
		ret = -EFAULT;
		goto out;
	}

	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "ciphertext");

	/* Get the tag */
	if (0 == EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_CCM_GET_TAG,
				     (int)data->tag.len, data->tag.buf)) {
		logger(LOGGER_WARN, "EVP_CIPHER_CTX_ctrl failed (len: %zu)\n",
		       data->tag.len);
		ret = -EFAULT;
		goto out;
	}
	logger_binary(LOGGER_DEBUG, data->tag.buf, data->tag.len,
		      "Generated tag");

	ret = 0;

out:
	if (ctx)
		EVP_CIPHER_CTX_free(ctx);
	return ret;
}

static int openssl_ccm_decrypt(struct aead_data *data, flags_t parsed_flags)
{
	EVP_CIPHER_CTX *ctx = NULL;
	const EVP_CIPHER *type;
	int ret;

	(void)parsed_flags;

	CKINT(openssl_cipher(data->cipher, data->key.len, &type));

	ctx = EVP_CIPHER_CTX_new();
	CKNULL(ctx, -ENOMEM);

	logger_binary(LOGGER_DEBUG, data->iv.buf, data->iv.len, "iv");
	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len, "ciphertext");
	logger_binary(LOGGER_DEBUG, data->tag.buf, data->tag.len, "tag");

	CKINT_O_LOG(EVP_CipherInit_ex(ctx, type, NULL, NULL, NULL, 0),
		    "EVP_CipherInit_ex() failed\n");

	CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_CCM_SET_IVLEN,
					(int)data->iv.len, NULL),
		    "EVP_CTRL_CCM_SET_IVLEN failed\n");

	CKINT_O_LOG(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_CCM_SET_TAG,
					(int)data->tag.len, data->tag.buf),
		    "EVP_CTRL_CCM_SET_TAG failed (%zu)\n", data->tag.len);

	CKINT_O_LOG(EVP_CipherInit_ex(ctx, NULL, NULL, data->key.buf,
				       data->iv.buf, 0),
		    "EVP_CipherInit_ex() failed\n");

	/* Set the length as defined in the man page */
	if (EVP_Cipher(ctx, NULL, NULL, (unsigned int)data->data.len) !=
	    (int)data->data.len) {
		logger(LOGGER_WARN, "EVP_Cipher() setting length failed\n");
		ret = -EFAULT;
		goto out;
	}

	if (data->assoc.len != 0) {
		CKINT_LOG(EVP_Cipher(ctx, NULL, data->assoc.buf,
				     (unsigned int)data->assoc.len),
			  "EVP_EncryptUpdate() decrypt AAD failed\n");
	}

	data->integrity_error = 0;

	if (EVP_Cipher(ctx, data->data.buf, data->data.buf,
		       (unsigned int)data->data.len) !=
	    (int)data->data.len) {
		logger(LOGGER_DEBUG, "EVP_Cipher() finalization failed\n");
        free_buf(&data->data);
		data->integrity_error = 1;
	}

	ret = 0;

out:
	if (ctx)
		EVP_CIPHER_CTX_free(ctx);

	return ret;
}

static struct aead_backend openssl_aead =
{
	openssl_gcm_encrypt,    /* gcm_encrypt */
	openssl_gcm_decrypt,    /* gcm_decrypt */
	openssl_ccm_encrypt,    /* ccm_encrypt */
	openssl_ccm_decrypt,    /* ccm_decrypt */
};

ACVP_DEFINE_CONSTRUCTOR(openssl_aead_backend)
static void openssl_aead_backend(void)
{
	register_aead_impl(&openssl_aead);
}

/************************************************
 * SHA cipher interface functions
 ************************************************/
static int openssl_sha_generate(struct sha_data *data, flags_t parsed_flags)
{
	EVP_MD_CTX *ctx = NULL;
	const EVP_MD *md = NULL;
	unsigned int maclen = 0;
	BUFFER_INIT(msg_p);
	int mdlen;
	int ret;

	(void)parsed_flags;

	CKINT(sha_ldt_helper(data, &msg_p));

	CKINT(openssl_md_convert(data->cipher, &md));

	if (data->cipher & ACVP_SHAKEMASK)
		mdlen = data->outlen / 8;
	else
		mdlen = EVP_MD_size(md);

	CKINT_LOG(alloc_buf((size_t)mdlen, &data->mac),
		  "SHA buffer cannot be allocated\n");

	ctx = EVP_MD_CTX_create();
	CKNULL_LOG(ctx, -ENOMEM, "MD context not created\n");
	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");

	CKINT_O_LOG(EVP_DigestInit(ctx, md), "EVP_DigestInit() failed %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	CKINT_O_LOG(EVP_DigestUpdate(ctx, msg_p.buf, msg_p.len),
		    "EVP_DigestUpdate() failed\n");

	if (data->cipher & ACVP_SHAKEMASK) {
		CKINT_O_LOG(openssl_shake_cb(ctx, data->mac.buf,
					     data->mac.len),
			    "EVP_DigestFinalXOF() failed\n");
	} else {
		CKINT_O_LOG(EVP_DigestFinal(ctx, data->mac.buf,
					    &maclen),
			    "EVP_DigestFinal() failed\n");
		data->mac.len = (size_t)maclen;
	}

	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "hash");

	ret = 0;

out:
	sha_ldt_clear_buf(data, &msg_p);
	if (ctx)
		EVP_MD_CTX_destroy(ctx);

	return ret;
}

/*
 * Example for SHA MCT inner loop handling in backend
 *
 * This code is meant to be an example - it is meaningless for OpenSSL (but it
 * works!), but when having, say, an HSM where ACVP handling code invoking the
 * HSM crypto code is also found within the HSM, moving this function into that
 * HSM handling code reduces the round trip between the host executing the ACVP
 * parser code and the HSM executing the ACVP handling code a 1000-fold.
 *
 * This code should be invoked with the hash_mct_inner_loop function pointer.
 */
#if 0

static int openssl_hash_inner_loop(struct sha_data *data, flags_t parsed_flags)
{
	switch (data->cipher & (ACVP_HASHMASK |
				ACVP_HMACMASK |
				ACVP_SHAKEMASK)) {
	case ACVP_SHA1:
	case ACVP_SHA224:
	case ACVP_SHA256:
	case ACVP_SHA384:
	case ACVP_SHA512:
		return parser_sha2_inner_loop(data, parsed_flags,
					      openssl_sha_generate);

	case ACVP_SHA3_224:
	case ACVP_SHA3_256:
	case ACVP_SHA3_384:
	case ACVP_SHA3_512:
		return parser_sha3_inner_loop(data, parsed_flags,
					      openssl_sha_generate);

	case ACVP_SHAKE128:
	case ACVP_SHAKE256:
		return parser_shake_inner_loop(data, parsed_flags,
					       openssl_sha_generate);

	default:
		return -EOPNOTSUPP;
	}
}
#endif

static struct sha_backend openssl_sha =
{
	openssl_sha_generate,   /* hash_generate */
	NULL,			/* or use openssl_hash_inner_loop */
};

ACVP_DEFINE_CONSTRUCTOR(openssl_sha_backend)
static void openssl_sha_backend(void)
{
	register_sha_impl(&openssl_sha);
}

/************************************************
 * SP800-132 PBKDF cipher interface functions
 ************************************************/
static int openssl_pbkdf_generate(struct pbkdf_data *data,
				  flags_t parsed_flags)
{
	const EVP_MD *md = NULL;
	uint32_t derived_key_bytes = data->derived_key_length / 8;
	int ret;

	(void)parsed_flags;

	if (data->derived_key_length % 8) {
		logger(LOGGER_WARN, "Derived key must be byte-aligned\n");
		ret = -EINVAL;
		goto out;
	}

	CKINT(openssl_md_convert(data->hash & ACVP_HASHMASK, &md));

	CKINT(alloc_buf(derived_key_bytes, &data->derived_key));

	CKINT_O_LOG(PKCS5_PBKDF2_HMAC((const char *)data->password.buf,
				      (int)data->password.len,
				      data->salt.buf, (int)data->salt.len,
				      (int)data->iteration_count,
				      md, (int)data->derived_key.len,
				      data->derived_key.buf), "PBKDF failed\n");

out:
	return ret;
}

static struct pbkdf_backend openssl_pbkdf =
{
	openssl_pbkdf_generate,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_pbkdf_backend)
static void openssl_pbkdf_backend(void)
{
	register_pbkdf_impl(&openssl_pbkdf);
}

#ifdef OPENSSL_ENABLE_TLS13
#include <openssl/kdf.h>
/************************************************
 * RFC8446 TLS v1.3 KDF
 ************************************************/
int openssl_hkdf_extract(const EVP_MD *md,
			 const uint8_t *key, size_t keylen,
			 const uint8_t *salt, size_t saltlen,
			 uint8_t *secret, size_t *secretlen)
{
	EVP_PKEY_CTX *pctx = NULL;
	int ret;

	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_HKDF, NULL);
	CKNULL(pctx, -EFAULT);

	/* Extract phase */
	CKINT_O_LOG(EVP_PKEY_derive_init(pctx),
		    "Initialiation of HKDF failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_hkdf_mode(pctx,
					   EVP_PKEY_HKDEF_MODE_EXTRACT_ONLY),
		    "Setting HKDF Extract operation failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_set_hkdf_md(pctx, md), "Setting MD failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_set1_hkdf_key(pctx, key, keylen),
		    "Setting HKDF key failed\n");


	CKINT_O_LOG(EVP_PKEY_CTX_set1_hkdf_salt(pctx, salt, saltlen),
		    "Setting salt failed\n");

	CKINT_O_LOG(EVP_PKEY_derive(pctx, secret, secretlen),
		    "Deriving expand key failed\n");

out:
	if (pctx)
		EVP_PKEY_CTX_free(pctx);
	return ret;
}

int openssl_hkdf_expand(const EVP_MD *md,
			const uint8_t *fi, size_t filen,
			const uint8_t *secret, size_t secretlen,
			uint8_t *dkm, size_t *dkmlen)
{
	EVP_PKEY_CTX *pctx = NULL;
	int ret;

	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_HKDF, NULL);
	CKNULL(pctx, -EFAULT);

	CKINT_O_LOG(EVP_PKEY_derive_init(pctx),
		    "Initialiation of HKDF failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_hkdf_mode(pctx,
					   EVP_PKEY_HKDEF_MODE_EXPAND_ONLY),
		    "Setting HKDF Expand operation failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_set_hkdf_md(pctx, md), "Setting MD failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_set1_hkdf_key(pctx, secret, secretlen),
		    "Setting HKDF key failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_add1_hkdf_info(pctx, fi, filen),
		    "Setting fixed info string failed\n");

	CKINT_O_LOG(EVP_PKEY_derive(pctx, dkm, dkmlen),
		    "Deriving key material failed\n");

out:
	if (pctx)
		EVP_PKEY_CTX_free(pctx);
	return ret;
}

#define TLS13_MAX_DIGEST_SIZE	64
#define TLS13_MAX_LABEL_LEN     249

static inline void be16_to_ptr(uint8_t *p, const uint16_t value)
{
	p[0] = (uint8_t)(value >> 8);
	p[1] = (uint8_t)(value);
}

/*
 * @param secret: secret from the HKDF extract phase
 * @param label: TLS 1.3 label
 * @param data: hashed input data
 * @param out: derived key material
 */
static int tls13_hkdf_expand(const EVP_MD *md, const uint8_t *secret,
			     const uint8_t *label, size_t labellen,
			     const uint8_t *data, size_t datalen,
			     uint8_t *out, size_t outlen)
{
	static const unsigned char label_prefix[] = "tls13 ";
	int ret;
	size_t hkdflabellen;
	size_t hashlen;
	/*
	 * 2 bytes for length of derived secret + 1 byte for length of combined
	 * prefix and label + bytes for the label itself + 1 byte length of hash
	 * + bytes for the hash itself
	 */
	unsigned char hkdflabel[sizeof(uint16_t) +
				sizeof(uint8_t) +
				(sizeof(label_prefix) - 1) +
				TLS13_MAX_LABEL_LEN + 1 +
				TLS13_MAX_DIGEST_SIZE];

	if (labellen > TLS13_MAX_LABEL_LEN)
		return -EINVAL;

	hashlen = (size_t)EVP_MD_size(md);

	be16_to_ptr(hkdflabel, (uint16_t)outlen);
	hkdflabellen = sizeof(uint16_t);

	hkdflabel[hkdflabellen] = (uint8_t)labellen + 6;
	hkdflabellen++;
	memcpy(hkdflabel + hkdflabellen, label_prefix, sizeof(label_prefix) - 1);
	hkdflabellen += sizeof(label_prefix) - 1;
	memcpy(hkdflabel + hkdflabellen, label, labellen);
	hkdflabellen += labellen;

	if (data) {
		hkdflabel[hkdflabellen] = (uint8_t)datalen;
		hkdflabellen++;
		memcpy(hkdflabel + hkdflabellen, data, datalen);
		hkdflabellen += datalen;
	}

	CKINT(openssl_hkdf_expand(md, hkdflabel, hkdflabellen,
				  secret, hashlen, out, &outlen));

out:
	return ret;
}

/* Always filled with zeros */
static const unsigned char default_zeros[TLS13_MAX_DIGEST_SIZE];

/*
 * @param prevsecret: Result of previous tls13_generate_secret operations
 * 		      (during first invocation, this is NULL)
 * @param insecret: Secret (either PSK or DHE shared secret or NULL)
 * @param outsecret: secret of message digest size
 */
/* This function is copied from OpenSSL */
static int tls13_generate_secret(const EVP_MD *md,
				 const uint8_t *prevsecret,
				 const uint8_t *insecret,
				 size_t insecretlen,
				 uint8_t *outsecret)
{
	size_t mdlen, prevsecretlen;
	int mdleni;
	int ret;
	static const char derived_secret_label[] = "derived";
	unsigned char preextractsec[TLS13_MAX_DIGEST_SIZE];

	mdleni = EVP_MD_size(md);
	/* Ensure cast to size_t is safe */
	if (mdleni < 0)
		return -EFAULT;
	mdlen = (size_t)mdleni;

	if (insecret == NULL) {
		insecret = default_zeros;
		insecretlen = mdlen;
	}

	if (prevsecret == NULL) {
		prevsecret = default_zeros;
		prevsecretlen = 0;
	} else {
		EVP_MD_CTX *mctx = EVP_MD_CTX_new();
		unsigned char hash[EVP_MAX_MD_SIZE];

		/* The pre-extract derive step uses a hash of no messages */
		if (mctx == NULL
		    || EVP_DigestInit_ex(mctx, md, NULL) <= 0
		    || EVP_DigestFinal_ex(mctx, hash, NULL) <= 0) {
			logger(LOGGER_ERR, "hash generation failed\n");
			EVP_MD_CTX_free(mctx);
			return -EFAULT;
		}
		EVP_MD_CTX_free(mctx);

		/* Generate the pre-extract secret */
		if (!tls13_hkdf_expand(md, prevsecret,
				       (unsigned char *)derived_secret_label,
				       sizeof(derived_secret_label) - 1,
				       hash, mdlen, preextractsec, mdlen))
			return -EFAULT;

		prevsecret = preextractsec;
		prevsecretlen = mdlen;
	}

	CKINT(openssl_hkdf_extract(md, insecret, insecretlen,
				   prevsecret, prevsecretlen,
				   outsecret, &mdlen));

out:
	return ret;
}

static int openssl_hash(const EVP_MD *md,
			uint8_t *in, size_t inlen,
			uint8_t *in2, size_t in2len,
			uint8_t *in3, size_t in3len,
			uint8_t *in4, size_t in4len,
			uint8_t *out, unsigned int *outlen)
{
	EVP_MD_CTX *ctx = EVP_MD_CTX_create();
	int ret;

	CKNULL_LOG(ctx, -ENOMEM, "MD context not created\n");

	CKINT_O_LOG(EVP_DigestInit(ctx, md), "EVP_DigestInit() failed %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	CKINT_O_LOG(EVP_DigestUpdate(ctx, in, inlen),
		    "EVP_DigestUpdate() failed\n");

	if (in2 && in2len)
		CKINT_O_LOG(EVP_DigestUpdate(ctx, in2, in2len),
			    "EVP_DigestUpdate() failed\n");

	if (in3 && in3len)
		CKINT_O_LOG(EVP_DigestUpdate(ctx, in3, in3len),
			    "EVP_DigestUpdate() failed\n");

	if (in4 && in4len)
		CKINT_O_LOG(EVP_DigestUpdate(ctx, in4, in4len),
			    "EVP_DigestUpdate() failed\n");

	CKINT_O_LOG(EVP_DigestFinal(ctx, out, outlen),
		    "EVP_DigestFinal() failed\n");

out:
	return ret;
}

static int openssl_tls13_generate(struct tls13_data *data,
				  flags_t parsed_flags)
{
	static const unsigned char client_early_traffic[] = "c e traffic";
	static const unsigned char early_exporter_master_secret[] = "e exp master";
	static const unsigned char client_handshake_traffic[] = "c hs traffic";
	static const unsigned char client_application_traffic[] = "c ap traffic";
	static const unsigned char server_handshake_traffic[] = "s hs traffic";
	static const unsigned char server_application_traffic[] = "s ap traffic";
	static const unsigned char exporter_master_secret[] = "exp master";
	static const unsigned char resumption_master_secret[] = "res master";

	const EVP_MD *md = NULL;
	uint8_t mdbuf[EVP_MAX_MD_SIZE];
	uint8_t secret[EVP_MAX_MD_SIZE];
	unsigned int mdbuflen;
	int mdlen;

	int ret;

	if (!(parsed_flags & FLAG_OP_TLS13_RUNNING_MODE_DHE)) {
		logger(LOGGER_ERR, "Only DHE supported\n");
		return -EOPNOTSUPP;
	}

	CKINT(openssl_md_convert(data->hash, &md));
	mdlen = EVP_MD_size(md);

	CKINT(alloc_buf((size_t)mdlen, &data->client_early_traffic_secret));
	CKINT(alloc_buf((size_t)mdlen, &data->early_exporter_master_secret));
	CKINT(alloc_buf((size_t)mdlen, &data->client_application_traffic_secret));
	CKINT(alloc_buf((size_t)mdlen, &data->server_application_traffic_secret));
	CKINT(alloc_buf((size_t)mdlen, &data->client_handshake_traffic_secret));
	CKINT(alloc_buf((size_t)mdlen, &data->server_handshake_traffic_secret));
	CKINT(alloc_buf((size_t)mdlen, &data->exporter_master_secret));
	CKINT(alloc_buf((size_t)mdlen, &data->resumption_master_secret));

	/* Generate Early Secret without PSK */
	CKINT_LOG(tls13_generate_secret(md, NULL, NULL, 0, secret),
		  "Generation of Early Secret failed\n");

	/* Generate secrets */
	CKINT(openssl_hash(md, data->client_hello_random.buf,
			   data->client_hello_random.len,
			   NULL, 0,
			   NULL, 0,
			   NULL, 0,
			   mdbuf, &mdbuflen));

	CKINT_O_LOG(tls13_hkdf_expand(md, secret,
				      client_early_traffic,
				      sizeof(client_early_traffic) - 1,
				      mdbuf, mdbuflen,
				      data->client_early_traffic_secret.buf,
				      data->client_early_traffic_secret.len),
		   "Generation of client early traffic secret failed\n");

	CKINT_O_LOG(tls13_hkdf_expand(md, secret,
				      early_exporter_master_secret,
				      sizeof(early_exporter_master_secret) - 1,
				      mdbuf, mdbuflen,
				      data->early_exporter_master_secret.buf,
				      data->early_exporter_master_secret.len),
		   "Generation of early exporter master secret failed\n");


	/* Generate Handshake Secret  */
	CKINT_LOG(tls13_generate_secret(md, secret,
					data->dhe.buf, data->dhe.len,
					secret),
		  "Generation of Handshake Secret failed\n");

	/* generate the concatenated message as input */
	CKINT(openssl_hash(md, data->client_hello_random.buf,
			   data->client_hello_random.len,
			   data->server_hello_random.buf,
			   data->server_hello_random.len,
			   NULL, 0,
			   NULL, 0,
			   mdbuf, &mdbuflen));

	CKINT_O_LOG(tls13_hkdf_expand(md, secret,
				      client_handshake_traffic,
				      sizeof(client_handshake_traffic) - 1,
				      mdbuf, mdbuflen,
				      data->client_handshake_traffic_secret.buf,
				      data->client_handshake_traffic_secret.len),
		   "Generation of client handshake traffic secret failed\n");

	CKINT_O_LOG(tls13_hkdf_expand(md, secret,
				      server_handshake_traffic,
				      sizeof(server_handshake_traffic) - 1,
				      mdbuf, mdbuflen,
				      data->server_handshake_traffic_secret.buf,
				      data->server_handshake_traffic_secret.len),
		   "Generation of server handshake traffic secret failed\n");

	/* Generate Master Secret  */
	CKINT_LOG(tls13_generate_secret(md, secret, NULL, 0, secret),
		  "Generation of Master Secret failed\n");

	/* Generate the concatenated message */
	CKINT(openssl_hash(md, data->client_hello_random.buf,
			   data->client_hello_random.len,
			   data->server_hello_random.buf,
			   data->server_hello_random.len,
			   data->server_finished_random.buf,
			   data->server_finished_random.len,
			   NULL, 0,
			   mdbuf, &mdbuflen));

	CKINT_O_LOG(tls13_hkdf_expand(md, secret,
				      client_application_traffic,
				      sizeof(client_application_traffic) - 1,
				      mdbuf, mdbuflen,
				      data->client_application_traffic_secret.buf,
				      data->client_application_traffic_secret.len),
		   "Generation of client application traffic secret failed\n");

	CKINT_O_LOG(tls13_hkdf_expand(md, secret,
				      server_application_traffic,
				      sizeof(server_application_traffic) - 1,
				      mdbuf, mdbuflen,
				      data->server_application_traffic_secret.buf,
				      data->server_application_traffic_secret.len),
		   "Generation of server application traffic secret failed\n");

	CKINT_O_LOG(tls13_hkdf_expand(md, secret,
				      exporter_master_secret,
				      sizeof(exporter_master_secret) - 1,
				      mdbuf, mdbuflen,
				      data->exporter_master_secret.buf,
				      data->exporter_master_secret.len),
		   "Generation of exporter master secret failed\n");

	CKINT(openssl_hash(md, data->client_hello_random.buf,
			   data->client_hello_random.len,
			   data->server_hello_random.buf,
			   data->server_hello_random.len,
			   data->server_finished_random.buf,
			   data->server_finished_random.len,
			   data->client_finished_random.buf,
			   data->client_finished_random.len,
			   mdbuf, &mdbuflen));

	CKINT_O_LOG(tls13_hkdf_expand(md, secret,
				      resumption_master_secret,
				      sizeof(resumption_master_secret) - 1,
				      mdbuf, mdbuflen,
				      data->resumption_master_secret.buf,
				      data->resumption_master_secret.len),
		   "Generation of resumption master secret failed\n");

out:
	return ret;
}

static struct tls13_backend openssl_tls13 =
{
	openssl_tls13_generate,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_tls13_backend)
static void openssl_tls13_backend(void)
{
	register_tls13_impl(&openssl_tls13);
}

#endif /* OPENSSL_ENABLE_TLS13 */
