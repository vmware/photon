/*
 * Copyright 2021 VMware, Inc.
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
 * The code uses the interface offered by OpenSSL-3
 */

#include <openssl/provider.h>

#include "backend_openssl_common.h"
#include <openssl/provider.h>

OSSL_PROVIDER *fips;
OSSL_PROVIDER *base;

ACVP_DEFINE_CONSTRUCTOR(openssl_backend_init)
static void openssl_backend_init(void)
{
	/* Explicitly load the FIPS provider as per fips_module(7) */
	fips = OSSL_PROVIDER_load(NULL, "fips");
	if (fips == NULL) {
		printf("Failed to load FIPS provider\n");
		exit(-EFAULT);
	}
	base = OSSL_PROVIDER_load(NULL, "base");
	if (base == NULL) {
		OSSL_PROVIDER_unload(fips);
		printf("Failed to load base provider\n");
		exit(-EFAULT);
	}
}

ACVP_DEFINE_DESTRUCTOR(openssl_backend_fini)
static void openssl_backend_fini(void)
{
	#pragma message "Deliberate memleak required for OpenSSL 3 - OpenSSL cleans itself using atexit"
	//OSSL_PROVIDER_unload(base);
	//OSSL_PROVIDER_unload(fips);
}

/************************************************
 * General helper functions
 ************************************************/
static void openssl_dh_get0_key(const EVP_PKEY *r, BIGNUM **pub_key,
				BIGNUM **priv_key)
{
	EVP_PKEY_get_bn_param(r,OSSL_PKEY_PARAM_PRIV_KEY, priv_key);
	EVP_PKEY_get_bn_param(r,OSSL_PKEY_PARAM_PUB_KEY, pub_key);
}

static int openssl_pkey_get_bn_bytes(EVP_PKEY *pkey, const char *name,
				     struct buffer *out)
{
	BIGNUM *bn = NULL;
	int sz;
	int ret = 0;

	CKNULL(EVP_PKEY_get_bn_param(pkey, name, &bn), -EINVAL);
	sz = BN_num_bytes(bn);
	CKINT(alloc_buf(sz, out));
	CKNULL(BN_bn2binpad(bn, out->buf, sz), EINVAL);

out:
	if (bn)
		BN_free(bn);
	return ret;
}

/************************************************
 * CMAC/HMAC cipher interface functions
 ************************************************/
static int openssl_mac_generate_helper(struct hmac_data *data, char *mac_algo,
				       char *param_name, char *param_val)
{
	EVP_MAC_CTX *ctx = NULL;
	EVP_MAC *mac = NULL;
	OSSL_PARAM params[3], *p;
	int ret = 0;

	mac = EVP_MAC_fetch(NULL, mac_algo, NULL);
	CKNULL(mac, -EFAULT);
	ctx = EVP_MAC_CTX_new(mac);
	CKNULL(ctx, -EFAULT);

	p = params;
	// OpenSSL wants us to use the cipher name here...
	*p++ = OSSL_PARAM_construct_octet_string(OSSL_MAC_PARAM_KEY, data->key.buf, data->key.len);
	*p++ = OSSL_PARAM_construct_utf8_string(param_name, param_val, 0);
	*p = OSSL_PARAM_construct_end();

	CKINT_O_LOG(EVP_MAC_CTX_set_params(ctx, params),
			"EVP_MAC_CTX_set_params failed\n");
	CKINT_O_LOG(EVP_MAC_init(ctx, NULL, 0, NULL),
			"EVP_MAC_init failed\n");

	CKINT_O_LOG(EVP_MAC_update(ctx, data->msg.buf, data->msg.len),
			"EVP_MAC_update failed\n");
	CKINT_LOG(alloc_buf((size_t)EVP_MAC_CTX_get_mac_size(ctx), &data->mac),
			"%s buffer cannot be allocated\n", mac_algo);
	CKINT_O_LOG(EVP_MAC_final(ctx, data->mac.buf, &data->mac.len, data->mac.len),
			"EVP_MAC_final failed\n");

	logger(LOGGER_DEBUG, "taglen = %zu\n", data->mac.len);
	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, mac_algo);

	ret = 0;

out:
	if (mac)
		EVP_MAC_free(mac);
	if (ctx)
		EVP_MAC_CTX_free(ctx);
	return ret;
}

static int openssl_cmac_generate(struct hmac_data *data)
{
	const EVP_CIPHER *type = NULL;
	int ret = 0;

	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");
	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");

	CKINT(openssl_cipher(data->cipher, data->key.len, &type));

	if (openssl_mac_generate_helper(data, "CMAC", OSSL_MAC_PARAM_CIPHER,
		(char *)EVP_CIPHER_name(type)))
	{
		ret = -EFAULT;
		goto out;
	}

	// Truncate to desired macLen, which is in bits
	if (data->mac.len > data->maclen / 8) {
		data->mac.buf[data->maclen / 8] = '\0';
		data->mac.len = data->maclen / 8;
		logger(LOGGER_DEBUG, "Truncated mac to maclen: %d\n", data->maclen);
		logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "mac");
	}

	ret = 0;

out:
	return ret;
}

static int openssl_hmac_generate(struct hmac_data *data)
{
	const EVP_MD *md = NULL;
	int ret = 0;

	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");
	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");

	CKINT(openssl_md_convert(data->cipher, &md));

	if (openssl_mac_generate_helper(data, "HMAC", OSSL_MAC_PARAM_DIGEST,
		(char *)EVP_MD_name(md)))
	{
		ret = -EFAULT;
		goto out;
	}

	ret = 0;

out:
	return ret;
}

static int openssl_mac_generate(struct hmac_data *data, flags_t parsed_flags)
{
	(void)parsed_flags;

	switch(data->cipher) {
	case ACVP_AESCMAC:
	case ACVP_TDESCMAC:
		return openssl_cmac_generate(data);
		break;
	default:
		return openssl_hmac_generate(data);
		break;
	}

	return -EFAULT;
}

static struct hmac_backend openssl_mac =
{
	openssl_mac_generate,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_mac_backend)
static void openssl_mac_backend(void)
{
	register_hmac_impl(&openssl_mac);
}

/************************************************
 * KMAC cipher interface functions
 ************************************************/
static int openssl_kmac_generate(struct kmac_data *data, flags_t parsed_flags)
{
	EVP_MAC_CTX *ctx = NULL;
	EVP_MAC *mac = NULL;
	OSSL_PARAM params[4], *p;
	int blocklen = (int) data->maclen/8;
	int ret =0;
	int xof_enabled =0;
	const char *algo;
	(void)parsed_flags;

	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");
	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");

	convert_cipher_algo(data->cipher & ACVP_KMACMASK, ACVP_CIPHERTYPE_KMAC, &algo);

	mac = EVP_MAC_fetch(NULL, algo, NULL);
	CKNULL(mac, -EFAULT);
	ctx = EVP_MAC_CTX_new(mac);
	CKNULL(ctx, -EFAULT);

	p=params;
	*p++ = OSSL_PARAM_construct_octet_string(OSSL_MAC_PARAM_KEY, data->key.buf, data->key.len);
	if (data->customization.buf != NULL && data->customization.len != 0)
		*p++ = OSSL_PARAM_construct_octet_string(OSSL_MAC_PARAM_CUSTOM, data->customization.buf, data->customization.len);
	*p = OSSL_PARAM_construct_end();

	CKINT_O_LOG(EVP_MAC_CTX_set_params(ctx, params),
			"EVP_MAC_CTX_set_params failed\n");
	CKINT_O_LOG(EVP_MAC_init(ctx, NULL, 0, NULL),
			"EVP_MAC_init failed\n");

	xof_enabled =(int)data->xof_enabled;

	p = params;
	*p++ = OSSL_PARAM_construct_int(OSSL_MAC_PARAM_XOF, &xof_enabled);
	*p++ = OSSL_PARAM_construct_int(OSSL_MAC_PARAM_SIZE, &blocklen);
	*p = OSSL_PARAM_construct_end();

	CKINT_O_LOG(EVP_MAC_CTX_set_params(ctx, params),
			"EVP_MAC_CTX_set_params failed\n");

	CKINT_O_LOG(EVP_MAC_update(ctx, data->msg.buf, data->msg.len),
			"EVP_MAC_update failed\n");
	CKINT_LOG(alloc_buf((size_t)blocklen, &data->mac),
			"KMAC buffer cannot be allocated\n");
	CKINT_O_LOG(EVP_MAC_final(ctx, data->mac.buf, &data->mac.len, blocklen),
			"EVP_MAC_final failed\n");

	logger(LOGGER_DEBUG, "taglen = %zu\n", data->mac.len);
	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "KMAC");
out:
	if(mac)
		EVP_MAC_free(mac);
	if(ctx)
		EVP_MAC_CTX_free(ctx);
	return 0;
}

static int openssl_kmac_ver(struct kmac_data *data, flags_t parsed_flags)
{
	EVP_MAC_CTX *ctx = NULL;
	EVP_MAC *mac = NULL;
	OSSL_PARAM params[4], *p;
	BUFFER_INIT(kmac);
	int blocklen = (int) data->maclen/8;
	size_t maclen =0;
	int ret =0;
	int xof_enabled =0;
	const char *algo;
	(void)parsed_flags;

	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");
	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");

	convert_cipher_algo(data->cipher & ACVP_KMACMASK, ACVP_CIPHERTYPE_KMAC, &algo);

	mac = EVP_MAC_fetch(NULL, algo, NULL);
	CKNULL(mac, -EFAULT);
	ctx = EVP_MAC_CTX_new(mac);
	CKNULL(ctx, -EFAULT);
	if(mac)
		EVP_MAC_free(mac);

	p=params;
	*p++ = OSSL_PARAM_construct_octet_string(OSSL_MAC_PARAM_KEY, data->key.buf, data->key.len);
	if (data->customization.buf != NULL && data->customization.len != 0)
		*p++ = OSSL_PARAM_construct_octet_string(OSSL_MAC_PARAM_CUSTOM, data->customization.buf, data->customization.len);
	*p = OSSL_PARAM_construct_end();

	CKINT_O_LOG(EVP_MAC_CTX_set_params(ctx, params),
			"EVP_MAC_CTX_set_params failed\n");
	CKINT_O_LOG(EVP_MAC_init(ctx,NULL,0,NULL),
			"EVP_MAC_init failed\n");

	xof_enabled =(int)data->xof_enabled;

	p = params;
	*p++ = OSSL_PARAM_construct_int(OSSL_MAC_PARAM_XOF, &xof_enabled);
	*p++ = OSSL_PARAM_construct_int(OSSL_MAC_PARAM_SIZE, &blocklen);
	*p = OSSL_PARAM_construct_end();

	CKINT_O_LOG(EVP_MAC_CTX_set_params(ctx, params),
			"EVP_MAC_CTX_set_params failed\n");
	CKINT_O_LOG(EVP_MAC_update(ctx, data->msg.buf, data->msg.len),
			"EVP_MAC_update failed\n");
	CKINT_LOG(alloc_buf((size_t)blocklen, &kmac),
			"KMAC buffer cannot be allocated\n");
	CKINT_O_LOG(EVP_MAC_final(ctx, kmac.buf, &maclen, blocklen),
			"EVP_MAC_update failed\n");

	logger(LOGGER_DEBUG, "taglen = %zu\n", maclen);
	logger_binary(LOGGER_DEBUG, kmac.buf, maclen, "Generated KMAC");
	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "Input KMAC");

	if(memcmp(data->mac.buf,kmac.buf,data->mac.len))
		data->verify_result = 0;
	else
		data->verify_result = 1;

	logger(LOGGER_DEBUG, "Generated result= %" PRIu32 "\n",data->verify_result);

out:
	if(ctx)
		EVP_MAC_CTX_free(ctx);
	free_buf(&kmac);
	return 0;
}

static struct kmac_backend openssl_kmac =
{
	openssl_kmac_generate,
	openssl_kmac_ver
};

ACVP_DEFINE_CONSTRUCTOR(openssl_kmac_backend)
static void openssl_kmac_backend(void)
{
	register_kmac_impl(&openssl_kmac);
}

/************************************************
 * DH interface functions
 ************************************************/
static int openssl_dh_ss_common(uint64_t cipher,
				uint64_t safeprime,
				struct buffer *P,
				struct buffer *Q,
				struct buffer *G,
				struct buffer *Yrem,
				struct buffer *Xloc,
				struct buffer *Yloc,
				struct buffer *hashzz)
{
	EVP_PKEY_CTX *pctx = NULL;
	/* Create a EVP_PKEY_CTX to perform key derivation */
	EVP_PKEY_CTX *dctx = NULL;
	EVP_PKEY *pkey = NULL;
	EVP_PKEY *peerkey = NULL;
	OSSL_PARAM_BLD *bld = NULL;
	OSSL_PARAM *params = NULL;
	OSSL_PARAM *params_peer = NULL;
	EVP_PKEY *genkey = NULL;
	EVP_PKEY_CTX *gctx = NULL;
	BIGNUM *p_bn = NULL, *q_bn = NULL,*g_bn = NULL;
	BIGNUM *bn_Yrem = NULL, *bn_Xloc = NULL, *bn_Yloc = NULL;
	BIGNUM *cbn_Xloc = NULL, *cbn_Yloc = NULL;
	BUFFER_INIT(ss);
	unsigned int localkey_consumed = 0;
	size_t keylen = 0;
	int ret = 0;
	(void) safeprime;

	bld = OSSL_PARAM_BLD_new();
	p_bn = BN_bin2bn((const unsigned char *)P->buf, (int)P->len, NULL);
	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_FFC_P, p_bn);
	q_bn = BN_bin2bn((const unsigned char *)Q->buf, (int)Q->len, NULL);
	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_FFC_Q, q_bn);
	g_bn = BN_bin2bn((const unsigned char *)G->buf, (int)G->len, NULL);
	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_FFC_G, g_bn);

	if (!Xloc->len || !Yloc->len) {
		pctx = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
		CKNULL(pctx, -EFAULT);
		CKINT_O_LOG(EVP_PKEY_fromdata_init(pctx),
			    "EVP_PKEY_fromdata_init failed\n");

		params = OSSL_PARAM_BLD_to_param(bld);
		CKINT_O_LOG(EVP_PKEY_fromdata(pctx, &genkey,
					      EVP_PKEY_KEYPAIR, params),
			    "EVP_PKEY_keygen failed\n");
		gctx = EVP_PKEY_CTX_new_from_pkey(NULL, genkey, NULL);
		CKNULL(gctx, -EFAULT);
		CKINT_O_LOG(EVP_PKEY_keygen_init(gctx),
			    "EVP_PKEY_keygen_init failed\n");
		CKINT_O_LOG(EVP_PKEY_generate(gctx, &pkey),
			    "EVP_PKEY_generate failed\n");

		openssl_dh_get0_key(pkey, &cbn_Yloc, &cbn_Xloc);
		CKINT(openssl_bn2buffer(cbn_Yloc, Yloc));
		logger_binary(LOGGER_DEBUG, Yloc->buf, Yloc->len,
			      "generated Yloc");
	} else {
		logger_binary(LOGGER_DEBUG, Xloc->buf, Xloc->len, "used Xloc");
		bn_Xloc = BN_bin2bn((const unsigned char *)Xloc->buf,
				    (int)Xloc->len, NULL);
		CKNULL_LOG(bn_Xloc, -ENOMEM, "BN_bin2bn() failed\n");
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_PRIV_KEY, bn_Xloc);
		localkey_consumed = 1;
		params = OSSL_PARAM_BLD_to_param(bld);

		pctx = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
		CKNULL(pctx, -EFAULT);
		CKINT_O_LOG(EVP_PKEY_fromdata_init(pctx),
			    "EVP_PKEY_fromdata_init failed\n");
		EVP_PKEY_fromdata(pctx, &pkey, EVP_PKEY_KEYPAIR, params);
	}

	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_FFC_P, p_bn);
	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_FFC_Q, q_bn);
	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_FFC_G, g_bn);
	logger_binary(LOGGER_DEBUG, Yrem->buf, Yrem->len, "Yremote");
	bn_Yrem = BN_bin2bn((const unsigned char *)Yrem->buf, (int)Yrem->len,
			    NULL);
	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_PUB_KEY, bn_Yrem);
	params_peer = OSSL_PARAM_BLD_to_param(bld);

	pctx = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
	CKNULL(pctx, -EFAULT);
	CKINT_O_LOG(EVP_PKEY_fromdata_init(pctx),
		    "EVP_PKEY_fromdata_init failed\n");
	CKINT_O_LOG(EVP_PKEY_fromdata(pctx, &peerkey, EVP_PKEY_PUBLIC_KEY,
				      params_peer),
		    "EVP_PKEY_fromdata failed\n");
	CKINT_LOG(alloc_buf(keylen, &ss), "Cannot allocate ss\n");

	/* Compute the shared secret */
	dctx = EVP_PKEY_CTX_new_from_pkey(NULL, pkey, NULL);
	CKNULL(dctx, -EFAULT);
	CKINT_O_LOG(EVP_PKEY_derive_init(dctx),
		    "EVP_PKEY_derive_init failed\n");
	if(EVP_PKEY_derive_set_peer(dctx, peerkey)<0){
		ERR_print_errors_fp(stderr);
		goto out;
	}
	CKINT_O_LOG(EVP_PKEY_derive(dctx, NULL, &ss.len),
		    "EVP_PKEY_derive failed\n");
	CKINT(alloc_buf(ss.len, &ss));
	if(EVP_PKEY_derive(dctx, ss.buf, &ss.len)<=0){
		ERR_print_errors_fp(stderr);
		goto out;
	}
	ret = openssl_hash_ss(cipher, &ss, hashzz);
	logger_binary(LOGGER_DEBUG, ss.buf, ss.len, "Generated shared secret");

	/* We do not use CKINT here, because -ENOENT is no real error */
out:
	if(pkey)
		EVP_PKEY_free(pkey);
	if(peerkey)
		EVP_PKEY_free(peerkey);
	if(pctx)
		EVP_PKEY_CTX_free(pctx);
	if(dctx)
		EVP_PKEY_CTX_free(dctx);
	if(params_peer)
		OSSL_PARAM_free(params_peer);
	if(params)
		OSSL_PARAM_free(params);
	if(bld)
		OSSL_PARAM_BLD_free(bld);
	if (bn_Yrem)
		BN_free(bn_Yrem);
	if (!localkey_consumed && bn_Xloc)
		BN_free(bn_Xloc);
	if (!localkey_consumed && bn_Yloc)
		BN_free(bn_Yloc);
	free_buf(&ss);
	return ret;
}

static int openssl_dh_ss(struct dh_ss_data *data, flags_t parsed_flags)
{
	(void)parsed_flags;

	return openssl_dh_ss_common(data->cipher, data->safeprime,
					&data->P, &data->Q, &data->G,
					&data->Yrem,
					&data->Xloc, &data->Yloc,
					&data->hashzz);
}

static int openssl_dh_ss_ver(struct dh_ss_ver_data *data,
			       flags_t parsed_flags)
{
	int ret = openssl_dh_ss_common(data->cipher, data->safeprime,
					&data->P, &data->Q,
					&data->G,
					&data->Yrem,
					&data->Xloc, &data->Yloc,
					&data->hashzz);

	(void)parsed_flags;

	if (ret == -EOPNOTSUPP || ret == -ENOENT) {
		data->validity_success = 0;
		logger(LOGGER_DEBUG, "DH validity test failed\n");
		return 0;
	} else if (!ret) {
		data->validity_success = 1;
		logger(LOGGER_DEBUG, "DH validity test passed\n");
		return 0;
	}

	logger(LOGGER_DEBUG, "DH validity test: general error\n");
	return ret;
}

static struct dh_backend openssl_dh =
{
	openssl_dh_ss,
	openssl_dh_ss_ver,
	// TODO: implement DH keygen and keyver for OpenSSL 3.
	NULL,
	NULL,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_dh_backend)
static void openssl_dh_backend(void)
{
	register_dh_impl(&openssl_dh);
}

/************************************************
 * ECDH cipher interface functions
 ************************************************/

static int
openssl_ecdh_ss_common(uint64_t cipher,
		       struct buffer *Qxrem, struct buffer *Qyrem,
		       struct buffer *privloc,
		       struct buffer *Qxloc, struct buffer *Qyloc,
		       struct buffer *hashzz)
{
	int nid = 0, ret = 0;
	EVP_PKEY_CTX *kactx = NULL, *dctx = NULL;
	EVP_PKEY *pkey = NULL, *remotekey = NULL;
	OSSL_PARAM *params = NULL;
	OSSL_PARAM *params_remote = NULL;
	OSSL_PARAM_BLD *bld = NULL;
	BUFFER_INIT(ss);
	BUFFER_INIT(publoc);
	BUFFER_INIT(pubrem);
	BIGNUM  *privloc_bn = NULL;
	char dgst[50];

	bld = OSSL_PARAM_BLD_new();

	CKINT_LOG(_openssl_ecdsa_curves(cipher, &nid , dgst),
			"Conversion of curve failed\n");
	const char *digest = dgst;
	OSSL_PARAM_BLD_push_utf8_string(bld, OSSL_PKEY_PARAM_GROUP_NAME, digest,
					0);
	OSSL_PARAM_BLD_push_int(bld, OSSL_PKEY_PARAM_USE_COFACTOR_ECDH, 1);
	if(Qxloc->len){
		CKINT(alloc_buf(Qxloc->len + Qyloc->len + 1, &publoc));
		publoc.buf[0]= POINT_CONVERSION_UNCOMPRESSED;
		memcpy(publoc.buf + 1, Qxloc->buf, Qxloc->len);
		memcpy(publoc.buf + 1 + Qxloc->len, Qyloc->buf, Qyloc->len);
		logger_binary(LOGGER_DEBUG, publoc.buf, publoc.len, "publoc");
		OSSL_PARAM_BLD_push_octet_string(bld, OSSL_PKEY_PARAM_PUB_KEY,
						 publoc.buf,publoc.len);
	}
	if(privloc->len){
		privloc_bn = BN_bin2bn((const unsigned char *)privloc->buf,
				       (int)privloc->len, NULL);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_PRIV_KEY, privloc_bn);
	}
	params = OSSL_PARAM_BLD_to_param(bld);
	CKNULL_LOG(params, -ENOMEM, "bld to param failed\n");
	kactx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
	CKNULL_LOG(kactx, -ENOMEM, "EVP_PKEY_CTX_new_from_name failed\n");
	CKINT_O_LOG(EVP_PKEY_fromdata_init(kactx),
		    "EVP_PKEY_fromdata_init failed with status=%d\n", ret);

	if(!(Qxloc->len) && !(privloc->len)) {
		pkey = EVP_PKEY_Q_keygen(NULL, NULL, "EC", digest);
		CKNULL_LOG(pkey, -EFAULT, "EVP_PKEY_Q_keygen failed\n");
	} else {
		CKINT_O_LOG(EVP_PKEY_fromdata(kactx, &pkey, EVP_PKEY_KEYPAIR,
					      params),
					      "EVP_PKEY_fromdata failed\n");
	}

	OSSL_PARAM_BLD_push_utf8_string(bld, OSSL_PKEY_PARAM_GROUP_NAME,
					digest, strlen(digest)+1);

	CKINT(alloc_buf(Qxrem->len + Qyrem->len + 1, &pubrem));
	pubrem.buf[0]= POINT_CONVERSION_UNCOMPRESSED;
	memcpy(pubrem.buf + 1, Qxrem->buf, Qxrem->len);
	memcpy(pubrem.buf + 1 + Qxrem->len, Qyrem->buf, Qyrem->len);

	logger_binary(LOGGER_DEBUG, Qxrem->buf, Qxrem->len, "Qxrem");
	logger_binary(LOGGER_DEBUG, Qyrem->buf, Qyrem->len, "Qyrem");
	logger_binary(LOGGER_DEBUG, pubrem.buf, pubrem.len, "pubrem");

	OSSL_PARAM_BLD_push_octet_string(bld, OSSL_PKEY_PARAM_PUB_KEY,
			pubrem.buf,pubrem.len);

	params_remote = OSSL_PARAM_BLD_to_param(bld);
	CKNULL_LOG(params_remote, -ENOMEM, "bld to param failed\n");
	kactx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
	CKNULL_LOG(kactx, -ENOMEM, "EVP_PKEY_CTX_new_from_name failed\n");

	CKINT_O_LOG(EVP_PKEY_fromdata_init(kactx),
				"EVP_PKEY_fromdata_init failed\n");
	CKINT_O_LOG(EVP_PKEY_fromdata(kactx, &remotekey, EVP_PKEY_PUBLIC_KEY,
			params_remote), "EVP_PKEY_fromdata failed\n");
	dctx = EVP_PKEY_CTX_new_from_pkey(NULL, pkey, NULL);
	CKNULL_LOG(dctx, -ENOMEM, "EVP_PKEY_CTX_new_from_pkey failed\n");

	ret = EVP_PKEY_derive_init(dctx);
	if(ret <= 0) {
		logger(LOGGER_ERR, "EVP_PKEY_derive_init filed: %d\n", ret);
		goto out;
	}
	ret = EVP_PKEY_derive_set_peer(dctx, remotekey);
	if(ret <= 0) {
		logger(LOGGER_ERR, "EVP_PKEY_derive_set_peer filed: %d\n", ret);
		goto out;
	}
	ret = EVP_PKEY_derive(dctx, NULL, &ss.len);
	if(ret <= 0) {
		logger(LOGGER_ERR, "EVP_PKEY_derive filed: %d\n", ret);
		goto out;
	}
	CKINT(alloc_buf(ss.len, &ss));
	ret = EVP_PKEY_derive(dctx, ss.buf, &ss.len);
	if(ret <= 0) {
		logger(LOGGER_ERR, "EVP_PKEY_derive filed: %d\n", ret);
		goto out;
	}
	logger_binary(LOGGER_DEBUG, ss.buf, ss.len, "Generated shared secret");

	/* We do not use CKINT here, because -ENOENT is no real error */
	ret = openssl_hash_ss(cipher, &ss, hashzz);

out:
	if(pkey)
		EVP_PKEY_free(pkey);
	if(remotekey)
		EVP_PKEY_free(remotekey);
	if(kactx)
		EVP_PKEY_CTX_free(kactx);
	if(dctx)
		EVP_PKEY_CTX_free(dctx);
	if(params_remote)
		OSSL_PARAM_free(params_remote);
	if(params)
		OSSL_PARAM_free(params);
	if(bld)
		OSSL_PARAM_BLD_free(bld);
	if(privloc_bn)
		BN_free(privloc_bn);
	free_buf(&ss);
	free_buf(&publoc);
	free_buf(&pubrem);
	return ret;
}

static int openssl_ecdh_ss(struct ecdh_ss_data *data, flags_t parsed_flags)
{
	(void)parsed_flags;

	return openssl_ecdh_ss_common(data->cipher, &data->Qxrem, &data->Qyrem,
			&data->privloc,
			&data->Qxloc, &data->Qyloc,
			&data->hashzz);
}

static int openssl_ecdh_ss_ver(struct ecdh_ss_ver_data *data,
		flags_t parsed_flags)
{
	int ret = openssl_ecdh_ss_common(data->cipher, &data->Qxrem,
			&data->Qyrem,
			&data->privloc,
			&data->Qxloc, &data->Qyloc,
			&data->hashzz);

	(void)parsed_flags;

	if (ret == -EOPNOTSUPP || ret == -ENOENT) {
		data->validity_success = 0;
		logger(LOGGER_DEBUG, "ECDH validity test failed\n");
		return 0;
	} else if (!ret) {
		data->validity_success = 1;
		logger(LOGGER_DEBUG, "ECDH validity test passed\n");
		return 0;
	}
	logger(LOGGER_DEBUG, "ECDH validity test: general error\n");
	return ret;
}

static struct ecdh_backend openssl_ecdh =
{
	openssl_ecdh_ss,
	openssl_ecdh_ss_ver,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_ecdh_backend)
static void openssl_ecdh_backend(void)
{
	register_ecdh_impl(&openssl_ecdh);
}

/************************************************
 * DRBG cipher interface functions
 ************************************************/
static int openssl_get_drbg_name(struct drbg_data *data, char *cipher,
		char *drbg_name)
{
	logger(LOGGER_DEBUG, "cipher: %" PRIu64 "\n", data->cipher);
	if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA1) {
		strcpy(cipher, "SHA1");
		strcpy(drbg_name, ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				"HMAC-DRBG" : "HASH-DRBG");
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA224) {
		strcpy(cipher,  "SHA224");
		strcpy(drbg_name, ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				"HMAC-DRBG" : "HASH-DRBG");
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA256) {
		strcpy(cipher, "SHA256");
		strcpy(drbg_name, ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				"HMAC-DRBG" : "HASH-DRBG");
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA384) {
		strcpy(cipher,  "SHA384");
		strcpy(drbg_name, ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				"HMAC-DRBG" : "HASH-DRBG");
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA512224) {
		strcpy(cipher,  "SHA512-224");
		strcpy(drbg_name, ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				"HMAC-DRBG" : "HASH-DRBG");
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA512256) {
		strcpy(cipher, "SHA512-256");
		strcpy(drbg_name, ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				"HMAC-DRBG" : "HASH-DRBG");
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA512) {
		strcpy(cipher,  "SHA512");
		strcpy(drbg_name, ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				"HMAC-DRBG" : "HASH-DRBG");
	} else if ((data->cipher & ACVP_AESMASK) == ACVP_AES128) {
		strcpy(cipher, "AES-128-CTR");
		strcpy(drbg_name, "CTR-DRBG");
	} else if ((data->cipher & ACVP_AESMASK) == ACVP_AES192) {
		strcpy(cipher, "AES-192-CTR");
		strcpy(drbg_name, "CTR-DRBG");
	} else if ((data->cipher & ACVP_AESMASK) == ACVP_AES256) {
		strcpy(cipher, "AES-256-CTR");
		strcpy(drbg_name, "CTR-DRBG");
	} else {
		logger(LOGGER_WARN, "DRBG with unhandled cipher detected\n");
		return -EFAULT;
	}
	return 0;
}

static int openssl_drbg_generate(struct drbg_data *data, flags_t parsed_flags)
{

	OSSL_PARAM params[4];
	char cipher[50];
	char drbg_name[50];
	EVP_RAND *rand = NULL;
	EVP_RAND_CTX *ctx = NULL, *parent = NULL;
	int df = 0;
	int ret = 0;
	unsigned int strength = 256;
	unsigned char *z;
	int res = 0;
	(void)parsed_flags;

	if (openssl_get_drbg_name(data, cipher, drbg_name) < 0)
		goto out;
	df = !!data->df;

	/* Create the seed source */
	rand = EVP_RAND_fetch(NULL, "TEST-RAND", "-fips");
	CKNULL(rand, -ENOMEM);
	parent = EVP_RAND_CTX_new(rand, NULL);
	CKNULL(parent, -ENOMEM);
	EVP_RAND_free(rand);
	rand = NULL;

	params[0] = OSSL_PARAM_construct_uint(OSSL_RAND_PARAM_STRENGTH, &strength);
	params[1] = OSSL_PARAM_construct_end();
	CKINT(EVP_RAND_CTX_set_params(parent, params));
	/* Get the DRBG */
	rand = EVP_RAND_fetch(NULL, drbg_name, NULL);
	CKNULL(rand, -ENOMEM);
	ctx = EVP_RAND_CTX_new(rand, parent);
	CKNULL(ctx, -ENOMEM);
	/* Set the DRBG up */
	strength = EVP_RAND_get_strength(ctx);
	params[0] = OSSL_PARAM_construct_int(OSSL_DRBG_PARAM_USE_DF,
			(int *)(&df));
	if(!strcmp(drbg_name,"CTR-DRBG")){
		params[1] = OSSL_PARAM_construct_utf8_string(OSSL_DRBG_PARAM_CIPHER,
				(char *)cipher, 0);
	}
	else {
		params[1] = OSSL_PARAM_construct_utf8_string(OSSL_DRBG_PARAM_DIGEST,
				(char *)cipher, strlen(cipher));
	}

	params[2] = OSSL_PARAM_construct_utf8_string(OSSL_DRBG_PARAM_MAC, "HMAC", 0);
	params[3] = OSSL_PARAM_construct_end();

	CKINT(EVP_RAND_CTX_set_params(ctx, params));
	/* Feed in the entropy and nonce */
	logger_binary(LOGGER_DEBUG, data->entropy.buf, data->entropy.len, "entropy");
	logger_binary(LOGGER_DEBUG, data->nonce.buf, data->nonce.len, "nonce");

	params[0] = OSSL_PARAM_construct_octet_string(OSSL_RAND_PARAM_TEST_ENTROPY,
			(void *)data->entropy.buf,
			data->entropy.len);
	params[1] = OSSL_PARAM_construct_octet_string(OSSL_RAND_PARAM_TEST_NONCE,
			(void *)data->nonce.buf,
			data->nonce.len);
	params[2] = OSSL_PARAM_construct_end();

	if (!EVP_RAND_instantiate(parent, strength, 0, NULL, 0, params)) {
		EVP_RAND_CTX_free(ctx);
		goto out;
	}
	/*
	 * Run the test
	 * A NULL personalisation string defaults to the built in so something
	 * non-NULL is needed if there is no personalisation string
	 */
	logger_binary(LOGGER_DEBUG, data->pers.buf, data->pers.len,
			"personalization string");

	z = data->pers.buf != NULL ? data->pers.buf : (unsigned char *)"";
	if (!EVP_RAND_instantiate(ctx, strength, data->pr, z, data->pers.len, NULL)) {
		logger(LOGGER_DEBUG, "DRBG instantiation failed: %s\n",
				ERR_error_string(ERR_get_error(), NULL));
		EVP_RAND_CTX_free(ctx);
		goto out;
	}

	if (data->entropy_reseed.buffers[0].len) {
		logger_binary(LOGGER_DEBUG,
				data->entropy_reseed.buffers[0].buf,
				data->entropy_reseed.buffers[0].len,
				"entropy reseed");

		params[0] = OSSL_PARAM_construct_octet_string
			(OSSL_RAND_PARAM_TEST_ENTROPY, data->entropy_reseed.buffers[0].buf,
			 data->entropy_reseed.buffers[0].len);
		params[1] = OSSL_PARAM_construct_end();
		CKINT(EVP_RAND_CTX_set_params(parent, params));
		if (data->addtl_reseed.buffers[0].len) {
			logger_binary(LOGGER_DEBUG,
					data->addtl_reseed.buffers[0].buf,
					data->addtl_reseed.buffers[0].len,
					"addtl reseed");
		}
		CKINT_O(EVP_RAND_reseed(ctx,data->pr,
					NULL, 0,
					data->addtl_reseed.buffers[0].buf,
					data->addtl_reseed.buffers[0].len));
	}
	if (data->entropy_generate.buffers[0].len) {
		logger_binary(LOGGER_DEBUG,
				data->entropy_generate.buffers[0].buf,
				data->entropy_generate.buffers[0].len,
				"entropy generate 1");
		params[0] = OSSL_PARAM_construct_octet_string
			(OSSL_RAND_PARAM_TEST_ENTROPY,
			 data->entropy_generate.buffers[0].buf,
			 data->entropy_generate.buffers[0].len);
		params[1] = OSSL_PARAM_construct_end();
		CKINT(EVP_RAND_CTX_set_params(parent, params));
	}

	logger_binary(LOGGER_DEBUG, data->addtl_generate.buffers[0].buf,
			data->addtl_generate.buffers[0].len, "addtl generate 1");
	CKINT(alloc_buf(data->rnd_data_bits_len / 8, &data->random));
	CKINT_O_LOG(EVP_RAND_generate(ctx, data->random.buf, data->random.len, strength,
				data->entropy_generate.buffers[0].len?1:0,
				data->addtl_generate.buffers[0].buf,
				data->addtl_generate.buffers[0].len),
			"FIPS_drbg_generate failed\n");
	logger_binary(LOGGER_DEBUG, data->random.buf, data->random.len,
			"random tmp");
	if (data->entropy_generate.buffers[1].len) {
		logger_binary(LOGGER_DEBUG, data->entropy_generate.buffers[1].buf,
				data->entropy_generate.buffers[1].len,
				"entropy generate 1");
		params[0] = OSSL_PARAM_construct_octet_string
			(OSSL_RAND_PARAM_TEST_ENTROPY,
			 data->entropy_generate.buffers[1].buf,
			 data->entropy_generate.buffers[1].len);
		params[1] = OSSL_PARAM_construct_end();
		CKINT(EVP_RAND_CTX_set_params(parent, params));
	}

	logger_binary(LOGGER_DEBUG, data->addtl_generate.buffers[1].buf,
			data->addtl_generate.buffers[1].len, "addtl generate 2");
	CKINT_O_LOG(EVP_RAND_generate(ctx, data->random.buf, data->random.len, strength,
				data->entropy_generate.buffers[1].len?1:0,
				data->addtl_generate.buffers[1].buf,
				data->addtl_generate.buffers[1].len),
			"FIPS_drbg_generate failed\n");
	logger_binary(LOGGER_DEBUG, data->random.buf, data->random.len,
			"random");

	/* Verify the output */
	res = 0;
out:
	if (ctx) {
		EVP_RAND_uninstantiate(ctx);
		EVP_RAND_CTX_free(ctx);
	}
	if(parent) {
		EVP_RAND_uninstantiate(parent);
		EVP_RAND_CTX_free(parent);
	}
	if(rand)
		EVP_RAND_free(rand);
	return res;
}

static struct drbg_backend openssl_drbg =
{
	openssl_drbg_generate,  /* drbg_generate */
};

ACVP_DEFINE_CONSTRUCTOR(openssl_drbg_backend)
static void openssl_drbg_backend(void)
{
	register_drbg_impl(&openssl_drbg);
}

/************************************************
 * TLS cipher interface functions
 ************************************************/

static int openssl_kdf_tls_op(struct kdf_tls_data *data, flags_t parsed_flags)
{
	EVP_PKEY_CTX *pctx = NULL;
	const EVP_MD *md;
	int ret;

	(void)parsed_flags;

	CKINT(openssl_md_convert(data->hashalg, &md));

	/* Special case */
	if ((data->hashalg & ACVP_HASHMASK) == ACVP_SHA1) {
		logger(LOGGER_ERR, "TLS 1.0/1.1 is not supported\n");
		ret = -EINVAL;
		goto out;
	}

	CKNULL_LOG(md, -EFAULT, "Cipher implementation not found\n");

	CKINT(alloc_buf(data->pre_master_secret.len, &data->master_secret));

	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_TLS1_PRF, NULL);
	CKNULL_LOG(pctx, -EFAULT, "Cannot allocate TLS1 PRF\n");

	CKINT_O(EVP_PKEY_derive_init(pctx));
	CKINT_O(EVP_PKEY_CTX_set_tls1_prf_md(pctx, md));
	CKINT_O(EVP_PKEY_CTX_set1_tls1_prf_secret(pctx,
						  data->pre_master_secret.buf,
						  data->pre_master_secret.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
			(const unsigned char *)TLS_MD_MASTER_SECRET_CONST,
			TLS_MD_MASTER_SECRET_CONST_SIZE));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->client_hello_random.buf,
						data->client_hello_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->server_hello_random.buf,
						data->server_hello_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_derive(pctx, data->master_secret.buf,
				&data->master_secret.len));

	logger_binary(LOGGER_DEBUG, data->master_secret.buf,
		      data->master_secret.len, "master_secret");

	EVP_PKEY_CTX_free(pctx);
	pctx = NULL;

	CKINT(alloc_buf(data->key_block_length / 8, &data->key_block));

	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_TLS1_PRF, NULL);
	CKNULL_LOG(pctx, -EFAULT, "Cannot allocate TLS1 PRF\n");

	CKINT_O(EVP_PKEY_derive_init(pctx));
	CKINT_O(EVP_PKEY_CTX_set_tls1_prf_md(pctx, md));
	CKINT_O(EVP_PKEY_CTX_set1_tls1_prf_secret(pctx,
						  data->master_secret.buf,
						  data->master_secret.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
			(const unsigned char *)TLS_MD_KEY_EXPANSION_CONST,
			TLS_MD_KEY_EXPANSION_CONST_SIZE));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->server_random.buf,
						data->server_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->client_random.buf,
						data->client_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_derive(pctx, data->key_block.buf,
				&data->key_block.len));

	logger_binary(LOGGER_DEBUG, data->key_block.buf, data->key_block.len,
		      "keyblock");

	ret = 0;

out:
	if (pctx)
		EVP_PKEY_CTX_free(pctx);
	return (ret);
}

static struct kdf_tls_backend openssl_kdf_tls =
{
	openssl_kdf_tls_op,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_kdf_tls_backend)
static void openssl_kdf_tls_backend(void)
{
	register_kdf_tls_impl(&openssl_kdf_tls);
}

/************************************************
 * SSHv2 KDF
 ************************************************/

static int openssl_kdf_ssh_internal(struct kdf_ssh_data *data,
				    int id, const EVP_MD *md,
				    struct buffer *out)
{
	EVP_KDF *kdf = NULL;
	EVP_KDF_CTX *ctx = NULL;
	OSSL_PARAM params[6], *p;
	int ret = 0;

	kdf = EVP_KDF_fetch(NULL, "SSHKDF", NULL);
	CKNULL_LOG(kdf, -EFAULT, "Cannot allocate SSHv2 KDF\n");
	ctx = EVP_KDF_CTX_new(kdf);
	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate SSHv2 PRF\n");

	p = params;
	*p++ = OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_DIGEST,
						(char *)EVP_MD_name(md), 0);
	*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_KEY,
						 data->k.buf, data->k.len);
	*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SSHKDF_XCGHASH,
						 data->h.buf, data->h.len);
	*p++ = OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_SSHKDF_TYPE,
						(char *) &id, 0);
	*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SSHKDF_SESSION_ID,
						 data->session_id.buf,
						 data->session_id.len);
	*p = OSSL_PARAM_construct_end();

	CKINT_O(EVP_KDF_derive(ctx, out->buf, out->len, params));

out:
	if (kdf)
		EVP_KDF_free(kdf);
	if (ctx)
		EVP_KDF_CTX_free(ctx);
	return ret;
}

static int openssl_kdf_ssh(struct kdf_ssh_data *data, flags_t parsed_flags)
{
	const EVP_MD *md;
	unsigned int ivlen, enclen, maclen;
	int ret;

	(void)parsed_flags;

	CKINT(openssl_md_convert(data->cipher, &md));

	switch (data->cipher & ACVP_SYMMASK) {
	case ACVP_AES128:
		enclen = 16;
		ivlen = 16;
		break;
	case ACVP_AES192:
		enclen = 24;
		ivlen = 16;
		break;
	case ACVP_AES256:
		enclen = 32;
		ivlen = 16;
		break;
	case ACVP_TDESECB:
		enclen = 24;
		ivlen = 8;
		break;
	default:
		logger(LOGGER_WARN, "Cipher not identified\n");
		ret = -EINVAL;
		goto out;
	}

	switch (data->cipher & ACVP_HASHMASK) {
	case ACVP_SHA1:
		maclen = 20;
		break;
	case ACVP_SHA256:
		maclen = 32;
		break;
	case ACVP_SHA384:
		maclen = 48;
		break;
	case ACVP_SHA512:
		maclen = 64;
		break;
	default:
		logger(LOGGER_WARN, "Mac not identified\n");
		ret = -EINVAL;
		goto out;
	}

	CKINT(alloc_buf(ivlen, &data->initial_iv_client));
	CKINT(alloc_buf(ivlen, &data->initial_iv_server));
	CKINT(alloc_buf(enclen, &data->encryption_key_client));
	CKINT(alloc_buf(enclen, &data->encryption_key_server));
	CKINT(alloc_buf(maclen, &data->integrity_key_client));
	CKINT(alloc_buf(maclen, &data->integrity_key_server));

	CKINT(openssl_kdf_ssh_internal(data,  'A' + 0, md,
				       &data->initial_iv_client));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 1, md,
				       &data->initial_iv_server));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 2, md,
				       &data->encryption_key_client));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 3, md,
				       &data->encryption_key_server));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 4, md,
				       &data->integrity_key_client));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 5, md,
				       &data->integrity_key_server));

out:
	return ret;
}

static struct kdf_ssh_backend openssl_kdf =
{
	openssl_kdf_ssh,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_kdf_ssh_backend)
static void openssl_kdf_ssh_backend(void)
{
	register_kdf_ssh_impl(&openssl_kdf);
}

#ifdef OPENSSL_KBKDF
/************************************************
 * SP 800-108 KBKDF interface functions
 ************************************************/

static int openssl_kdf108(struct kdf_108_data *data, flags_t parsed_flags)
{
	EVP_KDF *kdf = NULL;
	EVP_KDF_CTX *ctx = NULL;
	OSSL_PARAM params[8], *p;
	const EVP_MD *md = NULL;
	const EVP_CIPHER *type = NULL;
	uint32_t derived_key_bytes = data->derived_key_length / 8;
	uint32_t l = be32(data->derived_key_length);
	BUFFER_INIT(label);
	BUFFER_INIT(context);
	int ret = 0, alloced = 0;
	(void)parsed_flags;

	logger(LOGGER_VERBOSE, "data->kdfmode = %" PRIu64 "\n", data->kdfmode);
	if (!(data->kdfmode & ACVP_CIPHERTYPE_KDF)) {
		logger(LOGGER_ERR, "The cipher type isn't a KDF");
		ret = -EINVAL;
		goto out;
	}

	if (data->kdfmode == ACVP_KDF_108_DOUBLE_PIPELINE) {
		logger(LOGGER_ERR, "Double pipeline mode is not supported");
		ret = -EINVAL;
		goto out;
	}

	kdf = EVP_KDF_fetch(NULL, "KBKDF", NULL);
	CKNULL_LOG(kdf, -EFAULT, "Cannot allocate KB KDF\n");
	ctx = EVP_KDF_CTX_new(kdf);
	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate KB PRF\n");


	p = params;
	*p++ = OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_MODE,
				(data->kdfmode == ACVP_KDF_108_COUNTER) ?
				"counter" : "feedback", 0);

	logger(LOGGER_VERBOSE, "data->mac = %" PRIu64 "\n", data->mac);
	if (data->mac & ACVP_CIPHERTYPE_HMAC) {
		CKINT(openssl_md_convert(data->mac, &md));
		CKNULL(md, -ENOMEM);

		*p++ = OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_DIGEST,
						(char *)EVP_MD_name(md), 0);
		*p++ = OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_MAC,
							"HMAC", 0);
	} else if (data->mac & ACVP_CIPHERTYPE_CMAC) {
		CKINT(openssl_cipher(data->mac == ACVP_AESCMAC ? ACVP_AESCMAC :
				     ACVP_TDESCMAC, data->key.len, &type));
		CKNULL(type, -ENOMEM);

		*p++ = OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_CIPHER,
						(char *)EVP_CIPHER_name(type),
						0);
		*p++ = OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_MAC,
							"CMAC", 0);
	}

	logger_binary(LOGGER_VERBOSE, data->key.buf, data->key.len, "data->key");
	*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_KEY,
						 data->key.buf, data->key.len);

	logger(LOGGER_VERBOSE, "L = %u\n", derived_key_bytes);
	logger_binary(LOGGER_VERBOSE, (unsigned char *)&l, sizeof(l), "[L]_2");

	if (data->fixed_data.len) {
		if (data->fixed_data.len != (data->key.len * 2 + 1 + sizeof(l))) {
			logger(LOGGER_ERR, "KBKDF fixed data unexpected length for regression testing\n");
			ret = -EINVAL;
			goto out;
		}
		label.buf = data->fixed_data.buf;
		label.len = data->key.len;
		context.buf = data->fixed_data.buf + 1 + label.len;
		context.len = data->key.len;
	} else {
		alloced = 1;

		CKINT(alloc_buf(data->key.len, &label));
		CKINT(alloc_buf(data->key.len, &context));
		/*
		 * Allocate the fixed_data to hold
		 * Label || 0x00 || Context || [L]_2
		 */
		CKINT(alloc_buf(label.len + 1 + context.len + sizeof(l),
			&data->fixed_data));

		/* Randomly choose the label and context */
		RAND_bytes(label.buf, (int)label.len);
		RAND_bytes(context.buf, (int)context.len);

		/*
		 * Fixed data = Label || 0x00 || Context || [L]_2
		 * The counter i is not part of it
		 */
		memcpy(data->fixed_data.buf, label.buf, label.len);
		       data->fixed_data.buf[label.len] = 0x00;
		memcpy(data->fixed_data.buf + label.len + 1, context.buf,
		       context.len);
		memcpy(data->fixed_data.buf + label.len + 1 + context.len,
		       (unsigned char *)&l, sizeof(l));

		logger_binary(LOGGER_VERBOSE, data->fixed_data.buf,
			      data->fixed_data.len, "data->fixed_data");
	}

	logger_binary(LOGGER_VERBOSE, label.buf, label.len, "label");
	*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SALT, label.buf,
						 label.len);

	logger_binary(LOGGER_VERBOSE, context.buf, context.len, "context");
	*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_INFO,
						 context.buf, context.len);

	if (data->iv.len) {
		logger_binary(LOGGER_VERBOSE, data->iv.buf, data->iv.len,
			      "data->iv");
		*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SEED,
							 data->iv.buf,
							 data->iv.len);
	}

	*p = OSSL_PARAM_construct_end();

	CKINT(alloc_buf(derived_key_bytes, &data->derived_key));
	CKINT_O_LOG(EVP_KDF_derive(ctx, data->derived_key.buf,
				   derived_key_bytes, params),
		    "EVP_KDF_derive failed\n");
	logger_binary(LOGGER_VERBOSE, data->derived_key.buf,
                      derived_key_bytes, "data->derived_key");

out:
	if (kdf)
		EVP_KDF_free(kdf);
	if (ctx)
		EVP_KDF_CTX_free(ctx);

	if (alloced) {
		free_buf(&label);
		free_buf(&context);
	}
	return ret;
}

static struct kdf_108_backend openssl_kdf108_backend =
{
	openssl_kdf108,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_kdf_108_backend)
static void openssl_kdf_108_backend(void)
{
	register_kdf_108_impl(&openssl_kdf108_backend);
}
#endif

/************************************************
 * DSA interface functions
 ************************************************/
static int openssl_get_safeprime_group(uint64_t safeprime, const char **group)
{
	int ret = 0;

	switch (safeprime)
	{
	case ACVP_DH_FFDHE_2048:
		*group = "ffdhe2048";
		break;
	case ACVP_DH_FFDHE_3072:
		*group = "ffdhe3072";
		break;
	case ACVP_DH_FFDHE_4096:
		*group = "ffdhe4096";
		break;
	case ACVP_DH_FFDHE_6144:
		*group = "ffdhe6144";
		break;
	case ACVP_DH_FFDHE_8192:
		*group = "ffdhe8192";
		break;
	default:
		logger(LOGGER_ERR,
		       "Safeprime testing with DSA not supported (Q not set)\n");
		ret = -EFAULT;
		goto out;
	}
out:
	return ret;
}

static int openssl_sig_gen(EVP_PKEY *pkey, const EVP_MD *md, struct buffer *msg,
			   struct buffer *sig)
{
	int ret = 0;
	EVP_MD_CTX *md_ctx = NULL;
	size_t sz = EVP_PKEY_size(pkey);

	CKINT(alloc_buf(sz, sig));
	md_ctx = EVP_MD_CTX_new();
	CKNULL(md_ctx, -EFAULT);

	CKINT_O(EVP_DigestSignInit(md_ctx, NULL, md, NULL, pkey));
	CKINT_O(EVP_DigestSign(md_ctx, sig->buf, &sig->len, msg->buf,
			       msg->len));

out:
	if (md_ctx)
		EVP_MD_CTX_free(md_ctx);
	return ret;
}

static int openssl_pkey_get_octet_bytes(EVP_PKEY *pkey, const char *name,
					struct buffer *out)
{
	int ret = 0;
	size_t len = 0;

	CKNULL(EVP_PKEY_get_octet_string_param(pkey, name, NULL, 0, &len),
	       -EFAULT);
	CKINT(alloc_buf(len, out));
	CKNULL(EVP_PKEY_get_octet_string_param(pkey, name, out->buf, len,
					       &out->len), -EFAULT);

out:
	return ret;
}

static int _openssl_dsa_pqg_gen(struct buffer *P,
				struct buffer *Q,
				struct buffer *G,
				struct buffer *firstseed,
				uint32_t *counter,
				uint32_t L, uint32_t N, uint64_t cipher)
{
	int ret = 0;
	EVP_PKEY *key = NULL;
	EVP_PKEY_CTX *ctx = NULL;
	const EVP_MD *md = NULL;

	ctx = EVP_PKEY_CTX_new_from_name(NULL, "DSA", NULL);
	CKNULL(ctx, -EFAULT);
	CKINT_O(EVP_PKEY_paramgen_init(ctx));
	CKINT(openssl_md_convert(cipher & ACVP_HASHMASK, &md));

	CKINT_O(EVP_PKEY_CTX_set_dsa_paramgen_md(ctx, md));
	CKINT_O(EVP_PKEY_CTX_set_dsa_paramgen_bits(ctx, L));
	CKINT_O(EVP_PKEY_CTX_set_dsa_paramgen_q_bits(ctx, N));

	CKINT_O(EVP_PKEY_paramgen(ctx, &key));

	CKINT(openssl_pkey_get_bn_bytes(key, OSSL_PKEY_PARAM_FFC_P, P));
	CKINT(openssl_pkey_get_bn_bytes(key, OSSL_PKEY_PARAM_FFC_Q, Q));
	CKINT(openssl_pkey_get_bn_bytes(key, OSSL_PKEY_PARAM_FFC_G, G));
	CKINT_O(EVP_PKEY_get_int_param(key, OSSL_PKEY_PARAM_FFC_PCOUNTER,
				       (int *)counter));
	if (firstseed) {
		CKINT(openssl_pkey_get_octet_bytes(key,
						   OSSL_PKEY_PARAM_FFC_SEED,
						   firstseed));
	}

out:
	if (key)
		EVP_PKEY_free(key);
	if(ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static int openssl_dsa_pq_gen(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	(void)parsed_flags;
	return _openssl_dsa_pqg_gen(&data->P, &data->Q, &data->G,
				    &data->domainseed, &data->pq_prob_counter,
				    data->L, data->N, data->cipher);
}

static int openssl_dsa_create_pkey(EVP_PKEY **pkey, struct buffer *p,
				   struct buffer *q, struct buffer *g,
				   struct buffer *seed, int counter,
				   struct buffer *h, struct buffer *index,
				   int validate_pq, int validate_g,
				   struct buffer *pub, BN_CTX *bn_ctx,
				   const EVP_MD *md)
{
	int ret = 0;
	EVP_PKEY_CTX *ctx = NULL;
	OSSL_PARAM_BLD *bld = NULL;
	OSSL_PARAM *params = NULL;
	BIGNUM *p_bn = NULL, *q_bn = NULL, *g_bn = NULL, *pub_bn = NULL;
	char* hex_index = NULL;
	size_t hex_index_size = 0;
	bld = OSSL_PARAM_BLD_new();
	CKINT_O(OSSL_PARAM_BLD_push_int(bld, OSSL_PKEY_PARAM_FFC_VALIDATE_PQ,
					validate_pq));
	CKINT_O(OSSL_PARAM_BLD_push_int(bld, OSSL_PKEY_PARAM_FFC_VALIDATE_G,
					validate_g));
	p_bn = BN_CTX_get(bn_ctx);
	BN_bin2bn(p->buf, p->len, p_bn);
	CKINT_O(OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_FFC_P, p_bn));
	q_bn = BN_CTX_get(bn_ctx);
	BN_bin2bn(q->buf, q->len, q_bn);
	CKINT_O(OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_FFC_Q, q_bn));

	CKINT_O(OSSL_PARAM_BLD_push_int(bld, OSSL_PKEY_PARAM_FFC_PCOUNTER,
					counter));

	if (g && g->len) {
		g_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(g->buf, g->len, g_bn);
		CKINT_O(OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_FFC_G,
					       g_bn));
	}

	if (h && h->len) {
		int number = (int)strtol((const char *)h->buf, NULL, 10);
		CKINT_O(OSSL_PARAM_BLD_push_int(bld, OSSL_PKEY_PARAM_FFC_H,
						number));
	}

	if (index && index->len) {
		bin2hex_alloc(index->buf, index->len, &hex_index,
			      &hex_index_size);
		int number = (int)strtol((const char *)hex_index, NULL, 16);
		CKINT_O(OSSL_PARAM_BLD_push_int(bld, OSSL_PKEY_PARAM_FFC_GINDEX,
						number));
	}

	if (seed && seed->len) {
		CKINT_O(OSSL_PARAM_BLD_push_octet_string(bld,
							 OSSL_PKEY_PARAM_FFC_SEED,
							 seed->buf, seed->len));
	}
	
	if (md) {
		CKINT_O(OSSL_PARAM_BLD_push_utf8_string(bld,
							OSSL_PKEY_PARAM_FFC_DIGEST,
							EVP_MD_name(md), 0));
	}
	
	if (pub && pub->len) {
		pub_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(pub->buf, pub->len, pub_bn);
		CKINT_O(OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_PUB_KEY,
						pub_bn));
	}

	params = OSSL_PARAM_BLD_to_param(bld);
	ctx = EVP_PKEY_CTX_new_from_name(NULL, "DSA", NULL);
	CKNULL(ctx, -EFAULT);
	CKINT_O(EVP_PKEY_fromdata_init(ctx));
	CKINT_O(EVP_PKEY_fromdata(ctx, pkey, EVP_PKEY_PUBLIC_KEY, params));

out:
	return ret;
}

static int openssl_dsa_g_gen(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	EVP_PKEY *key = NULL;
	EVP_PKEY_CTX *ctx = NULL;
	BN_CTX *bn_ctx = NULL;
	int ret = 0;
	const EVP_MD *md = NULL;

	(void)parsed_flags;
	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	bn_ctx = BN_CTX_new_ex(NULL);
	CKINT(openssl_dsa_create_pkey(&key, &data->P, &data->Q, NULL,
				      &data->domainseed, 0, NULL, NULL, 0, 1,
				      NULL, bn_ctx, md));
	CKINT(openssl_pkey_get_bn_bytes(key, OSSL_PKEY_PARAM_FFC_G, &data->G));
	logger_binary(LOGGER_DEBUG, data->G.buf, data->G.len, "G");

out:
	if (key)
		EVP_PKEY_free(key);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static int openssl_dsa_pq_ver(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	EVP_PKEY *key = NULL;
	EVP_PKEY_CTX *ctx = NULL;
	int ret = 0;
	BN_CTX *bn_ctx = NULL;
	const EVP_MD *md = NULL;

	(void)parsed_flags;
	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	bn_ctx = BN_CTX_new_ex(NULL);
	CKINT(openssl_dsa_create_pkey(&key, &data->P, &data->Q, NULL,
				      &data->domainseed, data->pq_prob_counter,
				      NULL, NULL, 1, 0, NULL, bn_ctx, md));

	ctx = EVP_PKEY_CTX_new_from_pkey(NULL, key, NULL);
	CKNULL(ctx, -EFAULT);
	ret = EVP_PKEY_param_check(ctx);

	if (1 == ret) {
		data->pqgver_success = 1;
		logger(LOGGER_DEBUG, "PQG verification successful\n");
	} else {
		data->pqgver_success = 0;
		logger(LOGGER_DEBUG, "PQG verification failed\n");
	}

	ret = 0;

out:
	if (key)
		EVP_PKEY_free(key);
	if(ctx)
		EVP_PKEY_CTX_free(ctx);

	return ret;
}

static int openssl_dsa_pqg_ver(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	EVP_PKEY *key = NULL;
	EVP_PKEY_CTX *ctx = NULL;
	BN_CTX *bn_ctx = NULL;
	int ret = 0;
	const EVP_MD *md = NULL;

	(void)parsed_flags;

	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));
	CKINT(left_pad_buf(&data->P, data->L / 8));
	CKINT(left_pad_buf(&data->Q, data->N / 8));
	CKINT(left_pad_buf(&data->G, data->L / 8));

	bn_ctx = BN_CTX_new_ex(NULL);
	CKINT(openssl_dsa_create_pkey(&key, &data->P, &data->Q, &data->G,
				      &data->domainseed, data->pq_prob_counter,
				      &data->g_unver_h, &data->g_canon_index, 0,
				      1, NULL, bn_ctx, md));

	ctx = EVP_PKEY_CTX_new_from_pkey(NULL, key, NULL);
	CKNULL(ctx, -EFAULT);
	ret = EVP_PKEY_param_check(ctx);
	if (1 == ret) {
		data->pqgver_success = 1;
		logger(LOGGER_DEBUG, "PQG verification successful\n");
	} else {
		data->pqgver_success = 0;
		logger(LOGGER_DEBUG, "PQG verification failed\n");
	}
	ret = 0;

out:
	if (key)
		EVP_PKEY_free(key);
	if(ctx)
		EVP_PKEY_CTX_free(ctx);

	return ret;
}

static int openssl_dsa_pqggen(struct dsa_pqggen_data *data,
			      flags_t parsed_flags)
{
	EVP_PKEY *dsa = NULL;
	uint32_t counter;
	int ret;

	(void)parsed_flags;
	ret = _openssl_dsa_pqg_gen(&data->P, &data->Q, &data->G, NULL,
				   &counter, data->L, data->N, data->cipher);

	if (dsa)
		EVP_PKEY_free(dsa);

	return ret;
}

static int openssl_dsa_pqg(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	parsed_flags &= ~FLAG_OP_GDT;
	if (parsed_flags ==
		(FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROBABLE_PQ_GEN))
		return openssl_dsa_pq_gen(data, parsed_flags);
	else if (parsed_flags ==
		(FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROBABLE_PQ_GEN))
		return openssl_dsa_pq_ver(data, parsed_flags);
	else if (parsed_flags ==
		(FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_UNVERIFIABLE_G_GEN))
		return openssl_dsa_g_gen(data, parsed_flags);
	else if (parsed_flags ==
		(FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_UNVERIFIABLE_G_GEN))
		return openssl_dsa_pqg_ver(data, parsed_flags);
	else if (parsed_flags ==
		(FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_CANONICAL_G_GEN))
		return openssl_dsa_g_gen(data, parsed_flags);
	else if (parsed_flags ==
		(FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_CANONICAL_G_GEN))
		return openssl_dsa_pqg_ver(data, parsed_flags);
	else {
		logger(LOGGER_WARN,
			"Unknown DSA PQG generation / verification definition (parsed flags: %" PRIu64 ")\n",
			parsed_flags);
		return -EINVAL;
	}
}

static int _openssl_dsa_keygen(struct buffer *P /* [in] */,
			       struct buffer *Q /* [in] */,
			       struct buffer *G /* [in] */,
			       uint64_t safeprime /* [in] */,
			       struct buffer *X /* [out] */,
			       struct buffer *Y /* [out] */,
			       EVP_PKEY **key)
{
	int ret = 0;
	BN_CTX *bn_ctx = NULL;
	EVP_PKEY_CTX *key_ctx = NULL;
	OSSL_PARAM params[2];
	const char *group;

	switch (safeprime) {
		case ACVP_DH_MODP_2048:
		case ACVP_DH_MODP_3072:
		case ACVP_DH_MODP_4096:
		case ACVP_DH_MODP_6144:
		case ACVP_DH_MODP_8192:
			logger(LOGGER_ERR,
			       "Safeprime testing with DSA not supported (Q not set)\n");
			ret = -EFAULT;
			break;
		case ACVP_DH_FFDHE_2048:
		case ACVP_DH_FFDHE_3072:
		case ACVP_DH_FFDHE_4096:
		case ACVP_DH_FFDHE_6144:
		case ACVP_DH_FFDHE_8192:
			CKINT(openssl_get_safeprime_group(safeprime, &group));
			params[0] = OSSL_PARAM_construct_utf8_string(
					OSSL_PKEY_PARAM_GROUP_NAME, (char *)group, 0);
			params[1] = OSSL_PARAM_construct_end();

			key_ctx = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
			CKNULL(key_ctx, -EFAULT);
			CKINT_O(EVP_PKEY_keygen_init(key_ctx));
			CKINT_O(EVP_PKEY_CTX_set_params(key_ctx, params));
			CKINT_O(EVP_PKEY_keygen(key_ctx, key));
			CKINT(openssl_pkey_get_bn_bytes(*key,
							OSSL_PKEY_PARAM_PRIV_KEY,
							X));
			CKINT(openssl_pkey_get_bn_bytes(*key,
							OSSL_PKEY_PARAM_PUB_KEY,
							Y));

			logger_binary(LOGGER_DEBUG, X->buf, X->len, "X");
			logger_binary(LOGGER_DEBUG, Y->buf, Y->len, "Y");
			if (key_ctx)
				EVP_PKEY_CTX_free(key_ctx);
			break;

		default:
			bn_ctx = BN_CTX_new_ex(NULL);
			CKINT(openssl_dsa_create_pkey(key, P, Q, G, NULL, 0,
						      NULL, NULL, 1, 0, NULL,
						      bn_ctx, NULL));
			key_ctx = EVP_PKEY_CTX_new_from_pkey(NULL, *key, NULL);
			CKNULL(key_ctx, -EFAULT);
			CKINT_O(EVP_PKEY_keygen_init(key_ctx));
			CKINT(EVP_PKEY_param_check(key_ctx));
			CKINT_O(EVP_PKEY_keygen(key_ctx, key));
			CKINT(openssl_pkey_get_bn_bytes(*key,
							OSSL_PKEY_PARAM_PUB_KEY,
							X));
			CKINT(openssl_pkey_get_bn_bytes(*key,
							OSSL_PKEY_PARAM_PRIV_KEY,
							Y));
			logger_binary(LOGGER_DEBUG, X->buf, X->len, "X");
			logger_binary(LOGGER_DEBUG, Y->buf, Y->len, "Y");
	}

out:
	return ret;
}

static int openssl_dsa_keygen(struct dsa_keygen_data *data,
				flags_t parsed_flags)
{
	struct dsa_pqggen_data *pqg = &data->pqg;
	EVP_PKEY *key = NULL;
	int ret = 0;

	(void)parsed_flags;

	CKINT(_openssl_dsa_keygen(&pqg->P, &pqg->Q, &pqg->G, pqg->safeprime,
				  &data->X, &data->Y, &key));

out:
	if (key)
		EVP_PKEY_free(key);
	return ret;
}

static int openssl_dh_create_pkey(EVP_PKEY **pkey, const char *group_name,
				  struct buffer *pub, struct buffer *priv,
				  BN_CTX *bn_ctx)
{
	int ret = 0;
	EVP_PKEY_CTX *ctx = NULL;
	OSSL_PARAM_BLD *bld = NULL;
	OSSL_PARAM *params = NULL;
	BIGNUM *pub_bn = NULL, *priv_bn = NULL;

	bld = OSSL_PARAM_BLD_new();
	OSSL_PARAM_BLD_push_utf8_string(bld, OSSL_PKEY_PARAM_GROUP_NAME,
					group_name, 0);

	if (pub->len) {
		pub_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(pub->buf, pub->len, pub_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_PUB_KEY, pub_bn);
	}
	if (priv->len) {
		priv_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(priv->buf, priv->len, priv_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_PRIV_KEY, priv_bn);
	}

	params = OSSL_PARAM_BLD_to_param(bld);
	ctx = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
	CKNULL(ctx, -EFAULT);
	CKINT_O(EVP_PKEY_fromdata_init(ctx));
	CKINT_O(EVP_PKEY_fromdata(ctx, pkey, EVP_PKEY_KEYPAIR, params));

out:
	OSSL_PARAM_free(params);
	OSSL_PARAM_BLD_free(bld);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);

	return ret;
}

static int openssl_dsa_keyver(struct dsa_keyver_data *data,
				flags_t parsed_flags){
	int ret = 0;
	BN_CTX *bn_ctx = NULL;
	EVP_PKEY_CTX *key_ctx = NULL;
	EVP_PKEY *pkey = NULL;
	const char *group;

	(void) parsed_flags;

	bn_ctx = BN_CTX_new_ex(NULL);
	CKINT(openssl_get_safeprime_group(data->pqg.safeprime, &group));
	if (openssl_dh_create_pkey(&pkey, group, &data->Y, &data->X,
				   bn_ctx) <= 0) {
		data->keyver_success = 0;
	}

	key_ctx = EVP_PKEY_CTX_new_from_pkey(NULL, pkey, "fips=yes");
	CKNULL(key_ctx, -EFAULT);

	if (EVP_PKEY_check(key_ctx) > 0) {
		data->keyver_success = 1;
	} else {
		data->keyver_success = 0;
	}

	ret = 0;

out:
	if (pkey)
		EVP_PKEY_free(pkey);
	if (key_ctx)
		EVP_PKEY_CTX_free(key_ctx);
	BN_CTX_free(bn_ctx);
	return ret;
}

static int openssl_dsa_keygen_en(struct dsa_pqggen_data *pqg, struct buffer *Y,
				 void **privkey)
{
	EVP_PKEY *key = NULL;
	BUFFER_INIT(X);
	int ret;

	CKINT(_openssl_dsa_keygen(&pqg->P, &pqg->Q, &pqg->G, pqg->safeprime,
				  &X, Y, &key));
	*privkey = key;

out:
	if (ret && key)
		EVP_PKEY_free(key);
	free_buf(&X);
	return ret;
}

static int openssl_get_dsa_sig_rs_bytes(struct buffer *sig, struct buffer *r,
					struct buffer *s)
{
	int ret = 0;
	size_t r1_len, s1_len;
	const BIGNUM *r1, *s1;
	// We need a copy of the pointer here because d2i_DSA_SIG modifies it.
	const unsigned char *sig_buf = sig->buf;
	DSA_SIG *sign = d2i_DSA_SIG(NULL, &sig_buf, sig->len);

	CKNULL_LOG(sign, -EINVAL, "sign not generated\n");
	DSA_SIG_get0(sign, &r1, &s1);
	CKNULL_LOG(r1, -EINVAL, "r not generated\n");
	CKNULL_LOG(s1, -EINVAL, "s not generated\n");
	r1_len = BN_num_bytes(r1);
	s1_len = BN_num_bytes(s1);
	CKINT(alloc_buf(r1_len, r));
	CKINT(alloc_buf(s1_len, s));
	CKINT(BN_bn2binpad(r1, r->buf, r1_len));
	CKINT(BN_bn2binpad(s1, s->buf, s1_len));

out:
	if (sign)
		DSA_SIG_free(sign);
	return ret;
}

static int openssl_dsa_siggen(struct dsa_siggen_data *data,
			      flags_t parsed_flags)
{
	EVP_PKEY *key = NULL;
	int ret = 0;
	BUFFER_INIT(sig_buf);
	const EVP_MD *md = NULL;

	(void)parsed_flags;

	if (!data->privkey) {
		logger(LOGGER_ERR, "Private key missing\n");
		return -EINVAL;
	}
	key = data->privkey;
	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	CKINT(openssl_sig_gen(key, md, &data->msg, &sig_buf));
	CKINT(openssl_get_dsa_sig_rs_bytes(&sig_buf, &data->R, &data->S));

	logger_binary(LOGGER_DEBUG, data->R.buf, data->R.len, "R");
	logger_binary(LOGGER_DEBUG, data->S.buf, data->S.len, "S");

	ret = 0;
out:
	free_buf(&sig_buf);
	return ret;
}

static int openssl_dsa_SIG_set0(DSA_SIG *sig, BIGNUM *r, BIGNUM *s)
{
	return DSA_SIG_set0(sig, r, s);
}

static int openssl_dsa_sigver(struct dsa_sigver_data *data,
				flags_t parsed_flags)
{
	struct dsa_pqggen_data *pqg = &data->pqg;
	EVP_MD_CTX *ctx = NULL;
	EVP_PKEY *key = NULL;
	DSA_SIG *sig = NULL;
	BIGNUM *r = NULL, *s = NULL;
	size_t sig_len;
	int ret = 0, sig_consumed = 0;
	unsigned char sig_buf[1024];
	unsigned char *sig_buf_p = sig_buf;
	BN_CTX *bn_ctx = NULL;
	const EVP_MD *md = NULL;

	(void)parsed_flags;
	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	sig = DSA_SIG_new();
	CKNULL_LOG(sig, -ENOMEM, "DSA_SIG_new() failed\n");

	r = BN_bin2bn((const unsigned char *) data->R.buf, (int)data->R.len, r);
	CKNULL(r, -ENOMEM);
	s = BN_bin2bn((const unsigned char *) data->S.buf, (int)data->S.len, s);
	CKNULL(s, -ENOMEM);

	bn_ctx = BN_CTX_new();
	CKINT(openssl_dsa_create_pkey(&key, &pqg->P, &pqg->Q, &pqg->G, NULL, 0,
				      NULL, NULL, 1, 0, &data->Y, bn_ctx, md));

	CKINT_O_LOG(openssl_dsa_SIG_set0(sig, r, s), "DSA_SIG_set0 failed\n");
	sig_consumed = 1;

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -ENOMEM);

	if (!EVP_DigestVerifyInit_ex(ctx, NULL, EVP_MD_name(md), NULL, NULL,
				     key, NULL)) {
		ret = -EFAULT;
		goto out;
	}

	sig_len = i2d_DSA_SIG(sig, &sig_buf_p);

	ret = EVP_DigestVerify(ctx, sig_buf, sig_len, data->msg.buf,
			       data->msg.len);

	if (!ret) {
		logger(LOGGER_DEBUG, "Signature verification: signature bad\n");
		data->sigver_success = 0;
	} else if (ret == 1) {
		logger(LOGGER_DEBUG,
			"Signature verification: signature good\n");
		data->sigver_success = 1;
		ret = 0;
	} else {
		logger(LOGGER_WARN,
			"Signature verification: general error\n");
		ret = -EFAULT;
	}

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);
	if (sig)
		DSA_SIG_free(sig);
	if (key)
		EVP_PKEY_free(key);
	if (!sig_consumed && r)
		BN_free(r);
	if (!sig_consumed && s)
		BN_free(s);

	return ret;
}

static void openssl_dsa_free_key(void *privkey)
{
	EVP_PKEY *key = (EVP_PKEY *)privkey;

	if (key)
		EVP_PKEY_free(key);
}

static struct dsa_backend openssl_dsa =
{
	openssl_dsa_keygen,	/* dsa_keygen */
	openssl_dsa_keyver,
	openssl_dsa_siggen,	/* dsa_siggen */
	openssl_dsa_sigver,	/* dsa_sigver */
	openssl_dsa_pqg,	/* dsa_pqg */
	openssl_dsa_pqggen,
	openssl_dsa_keygen_en,
	openssl_dsa_free_key
};

ACVP_DEFINE_CONSTRUCTOR(openssl_dsa_backend)
static void openssl_dsa_backend(void)
{
	register_dsa_impl(&openssl_dsa);
}

/************************************************
 * ECDSA cipher interface functions
 ************************************************/
static int _openssl_ecdsa_keygen(uint64_t curve, EVP_PKEY **out_key,
				 EVP_PKEY_CTX **out_ctx)
{
	EVP_PKEY_CTX *ctx = *out_ctx;
	EVP_PKEY *key = NULL;
	int ret = 0, nid = 0;
	char dgst[50];
	CKINT_LOG(_openssl_ecdsa_curves(curve, &nid , dgst),
		  "Conversion of curve failed\n");

	char *digest = dgst;
	if (!EVP_PKEY_CTX_set_group_name(ctx, digest)) {
		logger(LOGGER_ERR, "EC_KEY_new_by_curve_name() failed\n");
		ret = -EFAULT;
		goto out;
	}

	if (!EVP_PKEY_keygen(ctx, &key)) {
		logger(LOGGER_ERR, "EC_KEY_generate_key() failed\n");
		ret = -EFAULT;
		goto out;
	}

	*out_key = key;
	*out_ctx = ctx;
out:
	return ret;
}

static int openssl_get_ecdsa_sig_rs_bytes(struct buffer *sig, struct buffer *r,
					  struct buffer *s)
{
	int ret = 0;
	size_t r1_len, s1_len;
	const BIGNUM *r1, *s1;
	// We need a copy of the pointer here because d2i_ECDSA_SIG modifies it.
	const unsigned char *sig_buf = sig->buf;
	ECDSA_SIG *sign = d2i_ECDSA_SIG(NULL, &sig_buf, sig->len);

	CKNULL_LOG(sign, -EINVAL, "sign not generated\n");
	r1 = ECDSA_SIG_get0_r(sign);
	s1 = ECDSA_SIG_get0_s(sign);
	CKNULL_LOG(r1, -EINVAL, "r not generated\n");
	CKNULL_LOG(s1, -EINVAL, "s not generated\n");
	r1_len = BN_num_bytes(r1);
	s1_len = BN_num_bytes(s1);
	CKINT(alloc_buf(r1_len, r));
	CKINT(alloc_buf(s1_len, s));
	CKINT(BN_bn2binpad(r1, r->buf, r1_len));
	CKINT(BN_bn2binpad(s1, s->buf, s1_len));

out:
	if (sign)
		ECDSA_SIG_free(sign);
	return ret;
}

static int openssl_ecdsa_keygen(struct ecdsa_keygen_data *data,
				flags_t parsed_flags)
{
	EVP_PKEY_CTX *ctx = NULL;
	EVP_PKEY *key = NULL;
	int ret = 0;

	(void)parsed_flags;

	ctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
	CKNULL(ctx, -ENOMEM);
	CKINT_O(EVP_PKEY_keygen_init(ctx));

	CKINT(_openssl_ecdsa_keygen(data->cipher, &key, &ctx));

	CKINT(openssl_pkey_get_bn_bytes(key, OSSL_PKEY_PARAM_PRIV_KEY,
					&data->d));
	CKINT(openssl_pkey_get_bn_bytes(key, OSSL_PKEY_PARAM_EC_PUB_X,
					&data->Qx));
	CKINT(openssl_pkey_get_bn_bytes(key, OSSL_PKEY_PARAM_EC_PUB_Y,
					&data->Qy));
	
	logger_binary(LOGGER_DEBUG, data->Qx.buf, data->Qx.len, "Qx");
	logger_binary(LOGGER_DEBUG, data->Qy.buf, data->Qy.len, "Qy");
	logger_binary(LOGGER_DEBUG, data->d.buf, data->d.len, "d");

out:
	if (key)
		EVP_PKEY_free(key);
	if(ctx)
		EVP_PKEY_CTX_free(ctx);

	return ret;
}

static int openssl_ecdsa_create_pkey(EVP_PKEY **pkey, const char *curve_name,
				     struct buffer *pub)
{
	int ret = 0;
	EVP_PKEY_CTX *ctx = NULL;
	OSSL_PARAM_BLD *bld = NULL;
	OSSL_PARAM *params = NULL;

	bld = OSSL_PARAM_BLD_new();
	OSSL_PARAM_BLD_push_utf8_string(bld, OSSL_PKEY_PARAM_GROUP_NAME,
					curve_name, 0);
	OSSL_PARAM_BLD_push_octet_string(bld, OSSL_PKEY_PARAM_PUB_KEY, pub->buf,
					 pub->len);
	params = OSSL_PARAM_BLD_to_param(bld);

	ctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
	EVP_PKEY_fromdata_init(ctx);
	if(EVP_PKEY_fromdata(ctx, pkey, EVP_PKEY_PUBLIC_KEY, params) == 1)
		ret = 1;

	if(params)
		OSSL_PARAM_free(params);
	if (bld)
		OSSL_PARAM_BLD_free(bld);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static int openssl_ecdsa_pkvver(struct ecdsa_pkvver_data *data,
				flags_t parsed_flags)
{
	EVP_PKEY_CTX *ctx = NULL;
	int nid = NID_undef, ret = 0;
	EVP_PKEY *key = NULL;
	char dgst[50];
	BUFFER_INIT(pub);
	(void)parsed_flags;

	CKINT(alloc_buf(data->Qx.len + data->Qy.len + 1, &pub));

	pub.buf[0] = POINT_CONVERSION_UNCOMPRESSED;
	memcpy(pub.buf + 1, data->Qx.buf, data->Qx.len);
	memcpy(pub.buf + 1 + data->Qx.len, data->Qy.buf, data->Qy.len);

	CKINT(_openssl_ecdsa_curves(data->cipher, &nid, dgst));

	logger_binary(LOGGER_DEBUG, pub.buf, pub.len, "pub");

	const char *digest = dgst;
	ret = openssl_ecdsa_create_pkey(&key, digest, &pub);

	if(ret){
		logger(LOGGER_DEBUG, "ECDSA key successfully verified\n");
		data->keyver_success = 1;
	} else {
		logger(LOGGER_DEBUG, "ECDSA key verification failed\n");
		data->keyver_success = 0;
	}
	ret = 0;

out:
	free_buf(&pub);
	if (key)
		EVP_PKEY_free(key);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static int openssl_ecdsa_keygen_en(uint64_t curve, struct buffer *Qx_buf,
				   struct buffer *Qy_buf, void **privkey)
{
	EVP_PKEY *key = NULL;
	EVP_PKEY_CTX *ctx = NULL;
	int ret;

	ctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
	CKNULL(ctx, -ENOMEM);
	CKINT_O(EVP_PKEY_keygen_init(ctx));

	CKINT(_openssl_ecdsa_keygen(curve, &key, &ctx));

	CKINT(openssl_pkey_get_bn_bytes(key, OSSL_PKEY_PARAM_EC_PUB_X, Qx_buf));
	CKINT(openssl_pkey_get_bn_bytes(key, OSSL_PKEY_PARAM_EC_PUB_Y, Qy_buf));

	logger_binary(LOGGER_DEBUG, Qx_buf->buf, Qx_buf->len, "Qx");
	logger_binary(LOGGER_DEBUG, Qy_buf->buf, Qy_buf->len, "Qy");

	*privkey = key;

out:
	if (ret && key)
		EVP_PKEY_free(key);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static void openssl_ecdsa_free_key(void *privkey)
{
	EVP_PKEY *ecdsa = (EVP_PKEY *)privkey;
	if (ecdsa)
		EVP_PKEY_free(ecdsa);
}

static int openssl_ecdsa_siggen(struct ecdsa_siggen_data *data,
				flags_t parsed_flags)
{
	EVP_PKEY_CTX *ctx = NULL;
	EVP_PKEY *pk = NULL;
	ECDSA_SIG *sig = NULL;
	int ret = 0;
	EVP_PKEY *key;
	BUFFER_INIT(sig_buf);
	const EVP_MD *md = NULL;

	(void)parsed_flags;
	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	if (!data->privkey) {
		logger(LOGGER_ERR, "Private key missing\n");
		return -EINVAL;
	}

	key = data->privkey;
	ctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
	CKNULL(ctx, -EFAULT);
	CKINT_O(EVP_PKEY_keygen_init(ctx));

	CKINT(openssl_sig_gen(key, md, &data->msg, &sig_buf));
	
	openssl_get_ecdsa_sig_rs_bytes(&sig_buf, &data->R, &data->S);

	logger_binary(LOGGER_DEBUG, data->R.buf, data->R.len, "R");
	logger_binary(LOGGER_DEBUG, data->S.buf, data->S.len, "S");

	ret = 0;

out:
	free_buf(&sig_buf);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	if (pk)
		EVP_PKEY_free(pk);
	if (sig)
		ECDSA_SIG_free(sig);

	return ret;
}

static int openssl_ecdsa_convert(struct ecdsa_sigver_data *data,
				 ECDSA_SIG **sig_out, EVP_PKEY **key_out)
{
	ECDSA_SIG *sig = NULL;
	EVP_PKEY *key = NULL;
	BIGNUM *R = NULL, *S = NULL;
	int ret, nid = NID_undef;
	char dgst[50];
	BUFFER_INIT(pub);

	logger_binary(LOGGER_DEBUG, data->R.buf, data->R.len, "R");
	logger_binary(LOGGER_DEBUG, data->S.buf, data->S.len, "S");

	sig = ECDSA_SIG_new();
	CKNULL(sig, -EFAULT);

	R = BN_bin2bn((const unsigned char *) data->R.buf, (int)data->R.len,
		      NULL);
	CKNULL(R, -EFAULT);

	S = BN_bin2bn((const unsigned char *) data->S.buf, (int)data->S.len,
		      NULL);
	CKNULL(S, -EFAULT);

	CKINT_O(ECDSA_SIG_set0(sig, R, S));

	CKINT(_openssl_ecdsa_curves(data->cipher, &nid, dgst));

	CKINT(alloc_buf(data->Qx.len + data->Qy.len + 1, &pub));

	pub.buf[0] = POINT_CONVERSION_UNCOMPRESSED;
	memcpy(pub.buf + 1, data->Qx.buf, data->Qx.len);
	memcpy(pub.buf + 1 + data->Qx.len, data->Qy.buf, data->Qy.len);

	const char *digest = dgst;
	ret = openssl_ecdsa_create_pkey(&key, digest, &pub);
	CKNULL(key, -EFAULT);

	logger_binary(LOGGER_DEBUG, data->Qx.buf, data->Qx.len, "Qx");
	logger_binary(LOGGER_DEBUG, data->Qy.buf, data->Qy.len, "Qy");

	*key_out = key;
	*sig_out = sig;

	ret = 0;

out:
	free_buf(&pub);
	return ret;
}

static int
openssl_ecdsa_sigver_primitive(struct ecdsa_sigver_data *data,
				flags_t parsed_flags)
{
	EVP_PKEY_CTX *ctx = NULL;
	EVP_PKEY *key = NULL;
	ECDSA_SIG *sig = NULL;
	unsigned char *der_sig = NULL;
	size_t der_sig_len;
	int ret;

	(void)parsed_flags;

	CKINT(openssl_ecdsa_convert(data, &sig, &key));

	der_sig_len = (size_t)i2d_ECDSA_SIG(sig, &der_sig);

	if (!der_sig_len) {
		logger(LOGGER_ERR, "Failure to convert signature into DER\n");
		ret = -EFAULT;
		goto out;
	}

	ctx = EVP_PKEY_CTX_new(key, NULL);
	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate PKEY context\n");

	CKINT_O_LOG(EVP_PKEY_verify_init(ctx), "PKEY verify init failed\n");

	ret = EVP_PKEY_verify(ctx, der_sig, der_sig_len, data->msg.buf,
			      data->msg.len);
	if (ret == 1) {
		logger(LOGGER_DEBUG, "Signature verification successful\n");
		data->sigver_success = 1;
	} else {
		logger(LOGGER_DEBUG, "Signature verification failed %s\n",
			ERR_error_string(ERR_get_error(), NULL));
		data->sigver_success = 0;
	}
	ret = 0;

out:
	if (der_sig)
		free(der_sig);
	if (sig)
		ECDSA_SIG_free(sig);
	if (key)
		EVP_PKEY_free(key);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static int openssl_ecdsa_sigver(struct ecdsa_sigver_data *data,
				flags_t parsed_flags)
{
	EVP_MD_CTX *ctx = NULL;
	EVP_PKEY *key = NULL;
	ECDSA_SIG *sig = NULL;
	unsigned int sig_len;
	unsigned char *sig_buf_p = NULL;
	int ret = 0;
	const EVP_MD *md = NULL;
	if (data->component)
		return openssl_ecdsa_sigver_primitive(data, parsed_flags);

	CKINT(openssl_ecdsa_convert(data, &sig, &key));

	sig_len = (unsigned int)i2d_ECDSA_SIG(sig, &sig_buf_p);

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -ENOMEM);

	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	if (!EVP_DigestVerifyInit_ex(ctx, NULL, EVP_MD_name(md), NULL, NULL,
				     key, NULL)) {
		ERR_error_string(ERR_get_error(), NULL);
		data->sigver_success = 0;
		goto out;
	}

	ret = EVP_DigestVerify(ctx, sig_buf_p, sig_len, data->msg.buf,
			       data->msg.len);
	if (!ret) {
		logger(LOGGER_DEBUG, "Signature verification: signature bad\n");
		data->sigver_success = 0;
	} else if (ret == 1) {
		logger(LOGGER_DEBUG,
			"Signature verification: signature good\n");
		data->sigver_success = 1;
		ret = 0;
	} else {
		logger(LOGGER_WARN,
			"Signature verification: general error\n");
		ret = -EFAULT;
	}

out:
	if (ctx)
		EVP_MD_CTX_free(ctx);
	if (sig)
		ECDSA_SIG_free(sig);

	return ret;
}

static struct ecdsa_backend openssl_ecdsa =
{
	openssl_ecdsa_keygen,   /* ecdsa_keygen_testing */
	NULL,
	openssl_ecdsa_pkvver,   /* ecdsa_pkvver */
	openssl_ecdsa_siggen,   /* ecdsa_siggen */
	openssl_ecdsa_sigver,   /* ecdsa_sigver */
	openssl_ecdsa_keygen_en,
	openssl_ecdsa_free_key,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_ecdsa_backend)
static void openssl_ecdsa_backend(void)
{
	register_ecdsa_impl(&openssl_ecdsa);
}

static int rsa_create_pkey(EVP_PKEY **pkey,
						const unsigned char *n, size_t n_len,
						const unsigned char *e, size_t e_len,
						const unsigned char *d, size_t d_len,
						BN_CTX *bn_ctx)
{
	int ret = 0;
	EVP_PKEY_CTX *ctx = NULL;
	OSSL_PARAM_BLD *bld = NULL;
	OSSL_PARAM *params = NULL;
	unsigned char *n1 = NULL, *e1 = NULL, *d1 = NULL;
	size_t n_len1 = 0, e_len1 = 0, d_len1 = 0;
	BIGNUM *e_bn = NULL, *n_bn = NULL, *d_bn= NULL;

	bld = OSSL_PARAM_BLD_new();
	n_bn = BN_CTX_get(bn_ctx);
	BN_bin2bn(n, n_len, n_bn);
	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_N, n_bn);

	if (e != NULL) {
		e_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(e, e_len, e_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_E, e_bn);
	}
	if (d != NULL) {
		d_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(d, d_len, d_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_D, d_bn);
	}

	params = OSSL_PARAM_BLD_to_param(bld);
	ctx = EVP_PKEY_CTX_new_from_name(NULL, "RSA", NULL);
	CKINT_O(EVP_PKEY_fromdata_init(ctx));
	CKINT_O(EVP_PKEY_fromdata(ctx, pkey, EVP_PKEY_KEYPAIR, params));


	pkey_get_bn_bytes(*pkey, OSSL_PKEY_PARAM_RSA_N,  &n1, &n_len1);
	pkey_get_bn_bytes(*pkey, OSSL_PKEY_PARAM_RSA_E, &e1, &e_len1);
	pkey_get_bn_bytes(*pkey, OSSL_PKEY_PARAM_RSA_D, &d1, &d_len1);
	logger_binary(LOGGER_DEBUG, n1, n_len1, "N");
	logger_binary(LOGGER_DEBUG, e1, e_len1, "E");
	logger_binary(LOGGER_DEBUG, d1, d_len1, "D");
out:
	if(params)
		OSSL_PARAM_free(params);
	if(bld)
		OSSL_PARAM_BLD_free(bld);
	return ret;
}

static int rsa_create_pkey_crt(EVP_PKEY **pkey,
						const unsigned char *n, size_t n_len,
						const unsigned char *e, size_t e_len,
						const unsigned char *p, size_t p_len,
						const unsigned char *q, size_t q_len,
						const unsigned char *dmp1, size_t dmp1_len,
						const unsigned char *dmq1, size_t dmq1_len,
						const unsigned char *iqmp, size_t iqmp_len,
						BN_CTX *bn_ctx)
{
	int ret = 0, temp = 0;
	EVP_PKEY_CTX *ctx = NULL;
	OSSL_PARAM_BLD *bld = NULL;
	OSSL_PARAM *params = NULL;
	BIGNUM *e_bn = NULL, *n_bn = NULL, *p_bn= NULL, *q_bn= NULL, *dmp1_bn= NULL, *dmq1_bn= NULL, *iqmp_bn= NULL;
	bld = OSSL_PARAM_BLD_new();
	n_bn = BN_CTX_get(bn_ctx);
	BN_bin2bn(n, n_len, n_bn);
	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_N, n_bn);

	if (e != NULL) {
		e_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(e, e_len, e_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_E, e_bn);
	}
	if (p != NULL) {
		p_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(p, p_len, p_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_FACTOR1, p_bn);
	}
	if (q != NULL) {
		q_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(q, q_len, q_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_FACTOR2, q_bn);
	}
	if (dmp1 != NULL) {
		dmp1_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(dmp1, dmp1_len, dmp1_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_EXPONENT1, dmp1_bn);
	}
	if (dmq1 != NULL) {
		dmq1_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(dmq1, dmq1_len, dmq1_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_EXPONENT2, dmq1_bn);
	}
	if (iqmp != NULL) {
		iqmp_bn = BN_CTX_get(bn_ctx);
		BN_bin2bn(iqmp, iqmp_len, iqmp_bn);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_COEFFICIENT1, iqmp_bn);
	}
	if(p != NULL && q != NULL){
		BIGNUM *d_bn = BN_dup(n_bn);
		BN_sub(d_bn, d_bn, p_bn);
		BN_sub(d_bn, d_bn, q_bn);
		BN_add_word(d_bn, 1);
		BN_mod_inverse(d_bn, e_bn, d_bn, bn_ctx);
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_D, d_bn);
	}

	params = OSSL_PARAM_BLD_to_param(bld);
	ctx = EVP_PKEY_CTX_new_from_name(NULL, "RSA", "fips=yes");
	EVP_PKEY_fromdata_init(ctx);
	CKINT_O(EVP_PKEY_fromdata(ctx, pkey, EVP_PKEY_KEYPAIR, params));

out:
	return ret;
}

/************************************************
 * CMAC/HMAC cipher interface functions
 ************************************************/
@@ -2569,3 +2692,498 @@ static void openssl_ecdsa_backend(void)
{
	register_ecdsa_impl(&openssl_ecdsa);
}


/************************************************
 * RSA interface functions
 ************************************************/

#define RSA 		EVP_PKEY
#define RSA_free(a)		EVP_PKEY_free(a)
#define EVP_DigestSignInit(a,b,c,d,e)		EVP_DigestSignInit_ex(a,b,EVP_MD_name(c),NULL,NULL,e,NULL)
#define EVP_DigestVerifyInit(a,b,c,d,e)		EVP_DigestVerifyInit_ex(a,b,EVP_MD_name(c),NULL,NULL,e,NULL)

static int openssl_rsa_keygen_prime(struct rsa_keygen_prime_data *data,
					flags_t parsed_flags)
{
	BIGNUM *e = NULL, *p = NULL, *q = NULL;
	EVP_PKEY_CTX *ctx = NULL;
	EVP_PKEY *pkey = NULL;
	OSSL_PARAM_BLD *bld = NULL;
	OSSL_PARAM *params = NULL;
	int ret = 0;

	(void)parsed_flags;

	if (!data->e.len) {
		logger(LOGGER_WARN, "RSA E missing\n");
		return -EINVAL;
	}

	bld = OSSL_PARAM_BLD_new();
	logger_binary(LOGGER_DEBUG, data->e.buf, data->e.len, "e");
	logger_binary(LOGGER_DEBUG, data->p.buf, data->p.len, "p");
	logger_binary(LOGGER_DEBUG, data->q.buf, data->q.len, "q");

	e = BN_bin2bn((const unsigned char *) data->e.buf, (int)data->e.len, e);
	CKNULL(e, -ENOMEM);

	p = BN_bin2bn((const unsigned char *) data->p.buf, (int)data->p.len, p);
	CKNULL(p, -ENOMEM);
	if (BN_is_zero(p))
		BN_one(p);
	q = BN_bin2bn((const unsigned char *)data->q.buf, (int)data->q.len, q);
	CKNULL(q, -ENOMEM);
	OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_E, e);
	if (p != NULL) {
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_FACTOR1, p);
	}
	if (q != NULL) {
		OSSL_PARAM_BLD_push_BN(bld, OSSL_PKEY_PARAM_RSA_FACTOR2, q);
	}
	params = OSSL_PARAM_BLD_to_param(bld);
	ctx = EVP_PKEY_CTX_new_from_name(NULL, "RSA", NULL);
	EVP_PKEY_keygen_init(ctx);
	ret = EVP_PKEY_CTX_set_params(ctx, params);
	data->keygen_success = 1;

	if(EVP_PKEY_generate(ctx, &pkey) <= 0 || BN_check_prime(p, NULL, NULL) <= 0 || BN_check_prime(q, NULL, NULL) <= 0)
		data->keygen_success = 0;

out:
	if(params)
		OSSL_PARAM_free(params);
	if(bld)
		OSSL_PARAM_BLD_free(bld);
	if(ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

int openssl_rsa_keygen_internal(struct buffer *ebuf, uint32_t modulus,
					EVP_PKEY **outkey, struct buffer *nbuf,
					struct buffer *dbuf, struct buffer *pbuf,
					struct buffer *qbuf)
{
	BIGNUM *e = NULL;
	EVP_PKEY_CTX *ctx = NULL;
	OSSL_PARAM_BLD *bld = NULL;
	EVP_PKEY *pkey = NULL;
	size_t p_len = 0, q_len = 0, egen_len = 0, d_len = 0, n_len = 0;
	unsigned int retry = 0;
	int ret = 0,temp = 0;
	unsigned char *n = NULL, *p = NULL, *q = NULL, *d = NULL, *egen = NULL;

	if (!ebuf->len) {
		unsigned int a;
		uint8_t bitsset = 0;

		/* WARNING Buffer must be at least 3 bytes in size ! */
		CKINT(alloc_buf(sizeof(unsigned int), ebuf));

		/* generate random odd e */
		RAND_bytes(ebuf->buf, (int)ebuf->len);
		/* make sure it is odd */
		ebuf->buf[ebuf->len - 1] |= 1;

		for (a = 0; a < ebuf->len - 2; a++)
			bitsset |= ebuf->buf[a];

		/* Make sure that value is >= 65537 */
		if (!bitsset)
			ebuf->buf[ebuf->len - 3] |= 1;
	}

	logger(LOGGER_DEBUG, "modulus: %u\n", modulus);
	logger_binary(LOGGER_DEBUG, ebuf->buf, ebuf->len, "e");

#if 1
	e = BN_bin2bn((const unsigned char *)ebuf->buf, (int)ebuf->len, e);
	CKNULL(e, -ENOMEM);
#else
	e = BN_new();
	CKNULL(e, -ENOMEM);
	if (1 != BN_set_word(e, 65537)) {
		logger(LOGGER_WARN, "BN_set_word() failed");
		ret = -EFAULT;
		goto out;
	}
#endif
	do {
		ctx = EVP_PKEY_CTX_new_from_name(NULL, "RSA", NULL);
		EVP_PKEY_keygen_init(ctx);
		EVP_PKEY_CTX_set_rsa_keygen_bits(ctx, (int)modulus);
		EVP_PKEY_CTX_set1_rsa_keygen_pubexp(ctx, e);
		temp = EVP_PKEY_keygen(ctx, &pkey);
		retry++;
	} while (temp != 1 && retry < 100);
	CKINT_O_LOG(temp, "RSA_generate_key_ex() failed: %s\n",
				ERR_error_string(ERR_get_error(), NULL));

	pkey_get_bn_bytes(pkey, OSSL_PKEY_PARAM_RSA_FACTOR1,
										&p, &p_len);
	pkey_get_bn_bytes(pkey, OSSL_PKEY_PARAM_RSA_FACTOR2,
										&q, &q_len);
	pkey_get_bn_bytes(pkey, OSSL_PKEY_PARAM_RSA_N,
										&n, &n_len);
	pkey_get_bn_bytes(pkey, OSSL_PKEY_PARAM_RSA_D,
										&d, &d_len);
	pkey_get_bn_bytes(pkey, OSSL_PKEY_PARAM_RSA_E,
										&egen, &egen_len);

	if (nbuf){
		nbuf->buf =n;
		nbuf->len = n_len;
	}
	if (dbuf){
		dbuf->buf =d;
		dbuf->len = d_len;
	}
	if (pbuf){
		pbuf->buf =p;
		pbuf->len = p_len;
	}
	if (qbuf){
		qbuf->buf =q;
		qbuf->len = q_len;
	}

	logger_binary(LOGGER_DEBUG, egen, egen_len, "egen");
	logger_binary(LOGGER_DEBUG, ebuf->buf, ebuf->len, "ebuf");
	if (outkey) {
		*outkey = pkey;
		pkey = NULL;
	}

out:
	if (e)
		BN_free(e);
	if(bld)
		OSSL_PARAM_BLD_free(bld);
	if(ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static int openssl_rsa_keygen(struct rsa_keygen_data *data,
				flags_t parsed_flags)
{
	(void)parsed_flags;

	return openssl_rsa_keygen_internal(&data->e, data->modulus, NULL,
					&data->n, &data->d, &data->p,
					&data->q);
}

static int openssl_rsa_keygen_en(struct buffer *ebuf, uint32_t modulus,
				void **privkey, struct buffer *nbuf)
{
	return openssl_rsa_keygen_internal(ebuf, modulus, (RSA **)privkey, nbuf,
					NULL, NULL, NULL);
}

static void openssl_rsa_free_key(void *privkey)
{
	RSA *rsa = (RSA *)privkey;

	if (rsa)
		RSA_free(rsa);
}

static int openssl_rsa_siggen(struct rsa_siggen_data *data,
				flags_t parsed_flags)
{
	const EVP_MD *md = NULL;
	EVP_MD_CTX *ctx = NULL;
	EVP_PKEY_CTX *pctx = NULL;
	EVP_PKEY *pk = NULL;
	size_t siglen = 0;
	int ret = 0;

	if (!data->privkey) {
		logger(LOGGER_ERR, "Private key missing\n");
		return -EINVAL;
	}

	CKINT(openssl_md_convert(data->cipher, &md));

	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");

	pk = data->privkey;
	CKNULL(pk, -ENOMEM);

	CKINT(alloc_buf((size_t)EVP_PKEY_size(pk), &data->sig));
	siglen = data->sig.len;

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -ENOMEM);

	CKINT_O_LOG(EVP_DigestSignInit(ctx, &pctx, md, NULL, pk),
			"EVP_DigestSignInit failed: %s\n",
			ERR_error_string(ERR_get_error(), NULL));

	if (parsed_flags & FLAG_OP_RSA_SIG_PKCS1PSS) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_PKCS1_PSS_PADDING),
				"Setting PSS type failed: %s\n", ERR_error_string(ERR_get_error(), NULL));
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_pss_saltlen(pctx,
						data->saltlen),
				"Setting salt length to %u failed: %s\n",
				data->saltlen,
				ERR_error_string(ERR_get_error(), NULL));
	}

	if (parsed_flags & FLAG_OP_RSA_SIG_X931) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_X931_PADDING),
				"Setting X9.31 type failed: %s\n", ERR_error_string(ERR_get_error(), NULL));
	}

	if(parsed_flags & FLAG_OP_RSA_SIG_PKCS15) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_PKCS1_PADDING),
				"Setting PKCS1 type failed: %s\n", ERR_error_string(ERR_get_error(), NULL));
	}

	CKINT_O_LOG(EVP_DigestSignUpdate(ctx, data->msg.buf, data->msg.len),
			"EVP_DigestSignUpdate failed: %s\n",
			ERR_error_string(ERR_get_error(), NULL));

	CKINT_O_LOG(EVP_DigestSignFinal(ctx, data->sig.buf, &siglen),
			"EVP_DigestSignFinal failed: %s\n",
			ERR_error_string(ERR_get_error(), NULL));

	logger_binary(LOGGER_DEBUG, data->sig.buf, data->sig.len, "sig");

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);

	return ret;
}

static int openssl_rsa_sigver(struct rsa_sigver_data *data,
				flags_t parsed_flags)
{
	const EVP_MD *md = NULL;
	EVP_MD_CTX *ctx = NULL;
	EVP_PKEY_CTX *pctx = NULL;
	BN_CTX *bn_ctx = NULL;
	EVP_PKEY *pk = NULL;
	int ret = 0;

	if (!data->n.len || !data->e.len) {
		logger(LOGGER_WARN, "RSA N or E missing\n");
		return -EINVAL;
	}

	CKINT(left_pad_buf(&data->n, data->modulus / 8));
	CKINT(left_pad_buf(&data->sig, data->modulus / 8));

	CKINT(openssl_md_convert(data->cipher, &md));

	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");

	bn_ctx = BN_CTX_new();
	ret = rsa_create_pkey(&pk, data->n.buf, data->n.len, data->e.buf, data->e.len, NULL, 0, bn_ctx);
	CKNULL(pk, -ENOMEM);

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -ENOMEM);

	CKINT_O(EVP_DigestVerifyInit(ctx, &pctx, md, NULL, pk));

	if (parsed_flags & FLAG_OP_RSA_SIG_PKCS1PSS) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_PKCS1_PSS_PADDING),
				"Setting PSS type failed: %s\n",
				ERR_error_string(ERR_get_error(), NULL));
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_pss_saltlen(pctx,
						data->saltlen),
				"Setting salt length to %u failed: %s\n",
				data->saltlen,
				ERR_error_string(ERR_get_error(), NULL));
	}

	if (parsed_flags & FLAG_OP_RSA_SIG_X931) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_X931_PADDING),
				"Setting X9.31 type failed: %s\n",
				ERR_error_string(ERR_get_error(), NULL));
	}

	if(parsed_flags & FLAG_OP_RSA_SIG_PKCS15) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_PKCS1_PADDING),
				"Setting PKCS1 type failed: %s\n", ERR_error_string(ERR_get_error(), NULL));
	}

	CKINT_O(EVP_DigestVerifyUpdate(ctx, data->msg.buf, data->msg.len));

	ret = EVP_DigestVerifyFinal(ctx, data->sig.buf, data->sig.len);
	if (!ret) {
		logger(LOGGER_DEBUG, "Signature verification: signature bad\n");
		data->sig_result = 0;
	} else if (ret == 1) {
		logger(LOGGER_DEBUG,
			"Signature verification: signature good\n");
		data->sig_result = 1;
		ret = 0;
	} else {
		logger(LOGGER_WARN,
			"Signature verification: general error\n");
		ret = -EFAULT;
	}

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);
	if (pk)
		EVP_PKEY_free(pk);
	/* n and e do not need to be freed as they belong to the RSA context. */

	return ret;
}

static int openssl_rsa_signature_primitive(struct rsa_signature_primitive_data *data,
				flags_t parsed_flags)
{
	EVP_PKEY_CTX *ctx = NULL;
	size_t outlen;
	EVP_PKEY *pkey = NULL;
	int ret = 0, temp = 0;
	unsigned char *n = NULL, *e = NULL;
	size_t n_len = 0, e_len = 0;

	(void)parsed_flags;

	BN_CTX *bn_ctx = NULL;
	bn_ctx = BN_CTX_new();
	logger_binary(LOGGER_DEBUG, data->n.buf, data->n.len, "N");
	logger_binary(LOGGER_DEBUG, data->d.buf, data->d.len, "D");

	CKINT_LOG(rsa_create_pkey_crt(&pkey, data->n.buf, data->n.len, data->e.buf, data->e.len, data->u.rsa_crt.p.buf, data->u.rsa_crt.p.len,
							data->u.rsa_crt.q.buf, data->u.rsa_crt.q.len, data->u.rsa_crt.dmp1.buf, data->u.rsa_crt.dmp1.len, 
							data->u.rsa_crt.dmq1.buf, data->u.rsa_crt.dmq1.len, data->u.rsa_crt.iqmp.buf, data->u.rsa_crt.iqmp.len, bn_ctx),
							"pkey generation failed\n");
	CKNULL(pkey, -ENOMEM);

	CKNULL_LOG(pkey, -EFAULT, "Cannot allocate PKEY\n");

	pkey_get_bn_bytes(pkey, OSSL_PKEY_PARAM_RSA_N,  &n, &n_len);
	pkey_get_bn_bytes(pkey, OSSL_PKEY_PARAM_RSA_E, &e, &e_len);
	logger_binary(LOGGER_DEBUG, n, n_len, "N");
	logger_binary(LOGGER_DEBUG, e, e_len, "E");

	ctx = EVP_PKEY_CTX_new_from_pkey(NULL, pkey, "");

	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate PKEY context\n");
	CKINT_O_LOG(EVP_PKEY_encrypt_init(ctx), "PKEY decrypt init failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_NO_PADDING),
		    "Disabling padding failed\n");

	/* Determine buffer length */
	CKINT_O_LOG(EVP_PKEY_encrypt(ctx, NULL, &outlen, data->msg.buf,
					data->msg.len),
			"Getting Ciphertext length failed\n");

	CKINT(alloc_buf(outlen, &data->signature));

	temp = EVP_PKEY_encrypt(ctx, data->signature.buf, &outlen, data->msg.buf,
				data->msg.len);

	if (temp == 1) {
		logger(LOGGER_DEBUG, "signature successful\n");
	} else {
		logger(LOGGER_DEBUG, "signature failed %s\n",
			ERR_error_string(ERR_get_error(), NULL));
	}

out:
	if (pkey)
		EVP_PKEY_free(pkey);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static int
openssl_rsa_decryption_primitive(struct rsa_decryption_primitive_data *data,
				flags_t parsed_flags)
{
	EVP_PKEY_CTX *ctx = NULL;
	EVP_PKEY *key = NULL;
	size_t outlen = 0;
	int ret = 0, temp=0;

	(void)parsed_flags;

	key = data->privkey;
	CKNULL_LOG(key, -EFAULT, "Cannot allocate PKEY\n");
	ctx = EVP_PKEY_CTX_new_from_pkey(NULL, key, "");
	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate PKEY context\n");

	CKINT_O_LOG(EVP_PKEY_decrypt_init(ctx), "PKEY decrypt init failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_NO_PADDING),
			"Disabling padding failed\n")

	/* Determine buffer length */
	CKINT_O_LOG(EVP_PKEY_decrypt(ctx, NULL, &outlen, data->msg.buf,
					data->msg.len),
			"Getting plaintext length failed\n");

	CKINT(alloc_buf(outlen, &data->s));

	temp = EVP_PKEY_decrypt(ctx, data->s.buf, &outlen, data->msg.buf,
				data->msg.len);
	if (temp == 1) {
		logger(LOGGER_DEBUG, "Decryption successful\n");
		data->dec_result = 1;
	} else {
		logger(LOGGER_DEBUG, "Decryption failed %s\n",
			ERR_error_string(ERR_get_error(), NULL));
		data->dec_result = 0;
	}

out:
	if (key)
		EVP_PKEY_free(key);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static struct rsa_backend openssl_rsa =
{
	openssl_rsa_keygen,     /* rsa_keygen */
	openssl_rsa_siggen,     /* rsa_siggen */
	openssl_rsa_sigver,     /* rsa_sigver */
	openssl_rsa_keygen_prime,              /* rsa_keygen_prime */
	NULL,		        /* rsa_keygen_prov_prime */
	openssl_rsa_keygen_en,
	openssl_rsa_free_key,
	openssl_rsa_signature_primitive,
	openssl_rsa_decryption_primitive,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_rsa_backend)
static void openssl_rsa_backend(void)
{
	register_rsa_impl(&openssl_rsa);
}