/*
 * Copyright (C) 2018 - 2022, Stephan Mueller <smueller@chronox.de>
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
 */

#include "bool.h"
#include "stringhelper.h"
#include "binhexbin.h"
#include "logger.h"
#include "read_json.h"

#include "parser_common.h"

/******************************************************************************
 * ANSI X9.63 callback definitions
 ******************************************************************************/
static struct ansi_x963_backend *ansi_x963_backend = NULL;

static int kdf_tester_ansi_x963(struct json_object *in, struct json_object *out,
				uint64_t cipher)
{
	(void)cipher;

	/**********************************************************************
	 * ANSI X9.63 operation
	 **********************************************************************/
	DEF_CALLBACK(ansi_x963, ansi_x963, FLAG_OP_AFT | FLAG_OP_KDF_TYPE_ANSI_X963);

	const struct json_entry ansi_x963_testresult_entries[] = {
		{"keyData",		{.data.buf = &ansi_x963_vector.key_data, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_ANSI_X963 },
	};
	const struct json_testresult ansi_x963_testresult =
		SET_ARRAY(ansi_x963_testresult_entries, &ansi_x963_callbacks);

	const struct json_entry ansi_x963_test_entries[] = {
		{"z",			{.data.buf = &ansi_x963_vector.z, PARSER_BIN},			FLAG_OP_AFT | FLAG_OP_KDF_TYPE_ANSI_X963 },
		{"sharedInfo",		{.data.buf = &ansi_x963_vector.shared_info, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_ANSI_X963 },
	};

	/* search for empty arrays */
	const struct json_array ansi_x963_test = SET_ARRAY(ansi_x963_test_entries, &ansi_x963_testresult);

	const struct json_entry ansi_x963_testgroup_entries[] = {
		{"hashAlg",		{.data.largeint = &ansi_x963_vector.hashalg, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_ANSI_X963 },
		{"keyDataLength",	{.data.integer = &ansi_x963_vector.key_data_len, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_ANSI_X963 },
		{"fieldSize",		{.data.integer = &ansi_x963_vector.field_size, PARSER_UINT}, 	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_ANSI_X963 },
		{"tests",		{.data.array = &ansi_x963_test, PARSER_ARRAY},			FLAG_OP_AFT | FLAG_OP_KDF_TYPE_ANSI_X963 },
	};
	const struct json_array ansi_x963_testgroup = SET_ARRAY(ansi_x963_testgroup_entries, NULL);

	/**********************************************************************
	 * KDF common test group
	 **********************************************************************/
	const struct json_entry ansi_x963_testanchor_entries[] = {
		{"testGroups",			{.data.array = &ansi_x963_testgroup, PARSER_ARRAY},	FLAG_OP_KDF_TYPE_ANSI_X963 },
	};
	const struct json_array ansi_x963_testanchor = SET_ARRAY(ansi_x963_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&ansi_x963_testanchor, "1.0", in, out);
}

/******************************************************************************
 * KDF TLS callback definitions
 ******************************************************************************/
static struct kdf_tls_backend *kdf_tls_backend = NULL;

static int kdf_tester_tls(struct json_object *in, struct json_object *out,
			  uint64_t cipher)
{
	(void)cipher;

	/**********************************************************************
	 * KDF TLS operation
	 **********************************************************************/
	DEF_CALLBACK(kdf_tls, kdf_tls, FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS);

	const struct json_entry kdf_tls_testresult_entries[] = {
		{"masterSecret",		{.data.buf = &kdf_tls_vector.master_secret, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS},
		{"keyBlock",			{.data.buf = &kdf_tls_vector.key_block, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS},
	};
	const struct json_testresult kdf_tls_testresult =
		SET_ARRAY(kdf_tls_testresult_entries, &kdf_tls_callbacks);

	const struct json_entry kdf_tls_test_entries[] = {
		{"clientHelloRandom",		{.data.buf = &kdf_tls_vector.client_hello_random, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS},
		{"serverHelloRandom",		{.data.buf = &kdf_tls_vector.server_hello_random, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS},
		{"clientRandom",		{.data.buf = &kdf_tls_vector.client_random, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS},
		{"serverRandom",		{.data.buf = &kdf_tls_vector.server_random, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS},
		{"preMasterSecret",		{.data.buf = &kdf_tls_vector.pre_master_secret, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS},
	};

	/* search for empty arrays */
	const struct json_array kdf_tls_test = SET_ARRAY(kdf_tls_test_entries, &kdf_tls_testresult);

	const struct json_entry kdf_tls_testgroup_entries[] = {
		{"hashAlg",			{.data.largeint = &kdf_tls_vector.hashalg, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS },
		{"preMasterSecretLength",	{.data.integer = &kdf_tls_vector.pre_master_secret_length, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS },
		{"keyBlockLength",		{.data.integer = &kdf_tls_vector.key_block_length, PARSER_UINT}, FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS },
		{"tests",			{.data.array = &kdf_tls_test, PARSER_ARRAY},			FLAG_OP_AFT | FLAG_OP_KDF_TYPE_TLS },
	};
	const struct json_array kdf_tls_testgroup = SET_ARRAY(kdf_tls_testgroup_entries, NULL);

	/**********************************************************************
	 * KDF common test group
	 **********************************************************************/
	const struct json_entry kdf_tls_testanchor_entries[] = {
		{"testGroups",			{.data.array = &kdf_tls_testgroup, PARSER_ARRAY},	FLAG_OP_KDF_TYPE_TLS},
	};
	const struct json_array kdf_tls_testanchor = SET_ARRAY(kdf_tls_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&kdf_tls_testanchor, "1.0", in, out);
}

/******************************************************************************
 * KDF SSH callback definitions
 ******************************************************************************/
static struct kdf_ssh_backend *kdf_ssh_backend = NULL;

static int kdf_tester_ssh(struct json_object *in, struct json_object *out,
			  uint64_t cipher)
{
	(void)cipher;

	/**********************************************************************
	 * KDF SSH operation
	 **********************************************************************/
	DEF_CALLBACK(kdf_ssh, kdf_ssh, FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH);

	const struct json_entry kdf_ssh_testresult_entries[] = {
		{"initialIvClient",		{.data.buf = &kdf_ssh_vector.initial_iv_client, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH},
		{"encryptionKeyClient",		{.data.buf = &kdf_ssh_vector.encryption_key_client, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH},
		{"integrityKeyClient",		{.data.buf = &kdf_ssh_vector.integrity_key_client, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH},
		{"initialIvServer",		{.data.buf = &kdf_ssh_vector.initial_iv_server, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH},
		{"encryptionKeyServer",		{.data.buf = &kdf_ssh_vector.encryption_key_server, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH},
		{"integrityKeyServer",		{.data.buf = &kdf_ssh_vector.integrity_key_server, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH},
	};
	const struct json_testresult kdf_ssh_testresult =
		SET_ARRAY(kdf_ssh_testresult_entries, &kdf_ssh_callbacks);

	const struct json_entry kdf_ssh_test_entries[] = {
		{"k",		{.data.buf = &kdf_ssh_vector.k, PARSER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH},
		{"h",		{.data.buf = &kdf_ssh_vector.h, PARSER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH},
		{"sessionId",	{.data.buf = &kdf_ssh_vector.session_id, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH},
	};

	/* search for empty arrays */
	const struct json_array kdf_ssh_test = SET_ARRAY(kdf_ssh_test_entries, &kdf_ssh_testresult);

	const struct json_entry kdf_ssh_testgroup_entries[] = {
		{"hashAlg",	{.data.largeint = &kdf_ssh_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH },
		{"cipher",	{.data.largeint = &kdf_ssh_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH },
		{"tests",	{.data.array = &kdf_ssh_test, PARSER_ARRAY},			FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SSH },
	};
	const struct json_array kdf_ssh_testgroup = SET_ARRAY(kdf_ssh_testgroup_entries, NULL);

	/**********************************************************************
	 * KDF common test group
	 **********************************************************************/
	const struct json_entry kdf_ssh_testanchor_entries[] = {
		{"testGroups",			{.data.array = &kdf_ssh_testgroup, PARSER_ARRAY},	FLAG_OP_KDF_TYPE_SSH},
	};
	const struct json_array kdf_ssh_testanchor = SET_ARRAY(kdf_ssh_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&kdf_ssh_testanchor, "1.0", in, out);
}

/******************************************************************************
 * KDF IKEV1 callback definitions
 ******************************************************************************/
static struct kdf_ikev1_backend *kdf_ikev1_backend = NULL;

static int kdf_tester_ikev1(struct json_object *in, struct json_object *out,
			  uint64_t cipher)
{
	(void)cipher;

	/**********************************************************************
	 * KDF IKEV1 operation
	 **********************************************************************/
	DEF_CALLBACK(kdf_ikev1, kdf_ikev1, FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT);

	const struct json_entry kdf_ikev1_testresult_entries[] = {
		{"sKeyId",	{.data.buf = &kdf_ikev1_vector.s_key_id,   WRITER_BIN},	FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
		{"sKeyIdD",	{.data.buf = &kdf_ikev1_vector.s_key_id_d, WRITER_BIN},	FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
		{"sKeyIdA",	{.data.buf = &kdf_ikev1_vector.s_key_id_a, WRITER_BIN},	FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
		{"sKeyIdE",	{.data.buf = &kdf_ikev1_vector.s_key_id_e, WRITER_BIN},	FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
	};
	const struct json_testresult kdf_ikev1_testresult =
		SET_ARRAY(kdf_ikev1_testresult_entries, &kdf_ikev1_callbacks);

	const struct json_entry kdf_ikev1_test_entries[] = {
		{"nInit",	{.data.buf = &kdf_ikev1_vector.n_init, PARSER_BIN},		FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
		{"nResp",	{.data.buf = &kdf_ikev1_vector.n_resp, PARSER_BIN},		FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
		{"ckyInit",	{.data.buf = &kdf_ikev1_vector.cookie_init, PARSER_BIN},	FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
		{"ckyResp",	{.data.buf = &kdf_ikev1_vector.cookie_resp, PARSER_BIN},	FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
		{"gxy",		{.data.buf = &kdf_ikev1_vector.gxy, PARSER_BIN},		FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
		{"preSharedKey",{.data.buf = &kdf_ikev1_vector.pre_shared_key, PARSER_BIN},	FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
	};

	/* search for empty arrays */
	const struct json_array kdf_ikev1_test = SET_ARRAY(kdf_ikev1_test_entries, &kdf_ikev1_testresult);

	const struct json_entry kdf_ikev1_testgroup_entries[] = {
		{"hashAlg",			{.data.largeint = &kdf_ikev1_vector.hashalg, PARSER_CIPHER},	FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK | FLAG_OP_AFT},
		{"tests",			{.data.array = &kdf_ikev1_test, PARSER_ARRAY},			FLAG_OP_KDF_TYPE_IKEV1 | FLAG_OP_KDF_TYPE_IKEV1_DSA | FLAG_OP_KDF_TYPE_IKEV1_PKE | FLAG_OP_KDF_TYPE_IKEV1_PSK  | FLAG_OP_AFT},
	};
	const struct json_array kdf_ikev1_testgroup = SET_ARRAY(kdf_ikev1_testgroup_entries, NULL);

	/**********************************************************************
	 * KDF common test group
	 **********************************************************************/
	const struct json_entry kdf_ikev1_testanchor_entries[] = {
		{"testGroups",			{.data.array = &kdf_ikev1_testgroup, PARSER_ARRAY},	FLAG_OP_KDF_TYPE_IKEV1},
	};
	const struct json_array kdf_ikev1_testanchor = SET_ARRAY(kdf_ikev1_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&kdf_ikev1_testanchor, "1.0", in, out);
}

/******************************************************************************
 * KDF IKEV2 callback definitions
 ******************************************************************************/
static struct kdf_ikev2_backend *kdf_ikev2_backend = NULL;

static int kdf_tester_ikev2(struct json_object *in, struct json_object *out,
			  uint64_t cipher)
{
	(void)cipher;

	/**********************************************************************
	 * KDF IKEV2 operation
	 **********************************************************************/
	DEF_CALLBACK(kdf_ikev2, kdf_ikev2, FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT);

	const struct json_entry kdf_ikev2_testresult_entries[] = {
		{"sKeySeed",			{.data.buf = &kdf_ikev2_vector.s_key_seed, WRITER_BIN},		FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"sKeySeedReKey",		{.data.buf = &kdf_ikev2_vector.s_key_seed_rekey, WRITER_BIN},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"derivedKeyingMaterial",	{.data.buf = &kdf_ikev2_vector.dkm, WRITER_BIN},		FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"derivedKeyingMaterialChild",	{.data.buf = &kdf_ikev2_vector.dkm_child, WRITER_BIN},		FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"derivedKeyingMaterialDh",{.data.buf = &kdf_ikev2_vector.dkm_child_dh, WRITER_BIN},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
	};
	const struct json_testresult kdf_ikev2_testresult =
		SET_ARRAY(kdf_ikev2_testresult_entries, &kdf_ikev2_callbacks);

	const struct json_entry kdf_ikev2_test_entries[] = {
		{"nInit",	{.data.buf = &kdf_ikev2_vector.n_init, PARSER_BIN},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"nResp",	{.data.buf = &kdf_ikev2_vector.n_resp, PARSER_BIN},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"spiInit",	{.data.buf = &kdf_ikev2_vector.spi_init, PARSER_BIN},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"spiResp",	{.data.buf = &kdf_ikev2_vector.spi_resp, PARSER_BIN},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"gir",		{.data.buf = &kdf_ikev2_vector.gir, PARSER_BIN},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"girNew",	{.data.buf = &kdf_ikev2_vector.gir_new, PARSER_BIN},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
	};

	/* search for empty arrays */
	const struct json_array kdf_ikev2_test = SET_ARRAY(kdf_ikev2_test_entries, &kdf_ikev2_testresult);

	const struct json_entry kdf_ikev2_testgroup_entries[] = {
		{"hashAlg",			{.data.largeint = &kdf_ikev2_vector.hashalg, PARSER_CIPHER},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT},
		{"derivedKeyingMaterialLength",	{.data.integer = &kdf_ikev2_vector.dkmlen, PARSER_UINT},	FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT },
		{"tests",			{.data.array = &kdf_ikev2_test, PARSER_ARRAY},			FLAG_OP_KDF_TYPE_IKEV2 | FLAG_OP_AFT },
	};
	const struct json_array kdf_ikev2_testgroup = SET_ARRAY(kdf_ikev2_testgroup_entries, NULL);

	/**********************************************************************
	 * KDF common test group
	 **********************************************************************/
	const struct json_entry kdf_ikev2_testanchor_entries[] = {
		{"testGroups",			{.data.array = &kdf_ikev2_testgroup, PARSER_ARRAY},	FLAG_OP_KDF_TYPE_IKEV2},
	};
	const struct json_array kdf_ikev2_testanchor = SET_ARRAY(kdf_ikev2_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&kdf_ikev2_testanchor, "1.0", in, out);
}

/******************************************************************************
 * KDF SRTP callback definitions
 ******************************************************************************/
static struct kdf_srtp_backend *kdf_srtp_backend = NULL;

static int kdf_tester_kdf_srtp(struct json_object *in, struct json_object *out,
			       uint64_t cipher)
{
	(void)cipher;

	/**********************************************************************
	 * KDF SRTP operation
	 **********************************************************************/
	DEF_CALLBACK(kdf_srtp, kdf_srtp, FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP);

	const struct json_entry kdf_srtp_testresult_entries[] = {
		{"srtpKe",		{.data.buf = &kdf_srtp_vector.srtp_ke, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"srtpKa",		{.data.buf = &kdf_srtp_vector.srtp_ka, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"srtpKs",		{.data.buf = &kdf_srtp_vector.srtp_ks, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"srtcpKe",		{.data.buf = &kdf_srtp_vector.srtcp_ke, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"srtcpKa",		{.data.buf = &kdf_srtp_vector.srtcp_ka, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"srtcpKs",		{.data.buf = &kdf_srtp_vector.srtcp_ks, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
	};
	const struct json_testresult kdf_srtp_testresult =
		SET_ARRAY(kdf_srtp_testresult_entries, &kdf_srtp_callbacks);

	const struct json_entry kdf_srtp_test_entries[] = {
		{"masterKey",		{.data.buf = &kdf_srtp_vector.master_key, PARSER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"masterSalt",		{.data.buf = &kdf_srtp_vector.master_salt, PARSER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"index",		{.data.buf = &kdf_srtp_vector.index, PARSER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"srtcpIndex",		{.data.buf = &kdf_srtp_vector.srtcp_index, PARSER_BIN},		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
	};

	/* search for empty arrays */
	const struct json_array kdf_srtp_test = SET_ARRAY(kdf_srtp_test_entries, &kdf_srtp_testresult);

	const struct json_entry kdf_srtp_testgroup_entries[] = {
		{"aesKeyLength",	{.data.integer = &kdf_srtp_vector.aes_key_length, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"kdr",			{.data.buf = &kdf_srtp_vector.kdr, PARSER_BIN}, 		FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
		{"tests",		{.data.array = &kdf_srtp_test, PARSER_ARRAY},			FLAG_OP_AFT | FLAG_OP_KDF_TYPE_SRTP },
	};
	const struct json_array kdf_srtp_testgroup = SET_ARRAY(kdf_srtp_testgroup_entries, NULL);

	/**********************************************************************
	 * KDF common test group
	 **********************************************************************/
	const struct json_entry kdf_srtp_testanchor_entries[] = {
		{"testGroups",			{.data.array = &kdf_srtp_testgroup, PARSER_ARRAY},	FLAG_OP_KDF_TYPE_SRTP },
	};
	const struct json_array kdf_srtp_testanchor = SET_ARRAY(kdf_srtp_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&kdf_srtp_testanchor, "1.0", in, out);
}

/******************************************************************************
 * KDF generic parser definitions
 ******************************************************************************/
static int kdf_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	int ret = 0;
	struct json_object *acvpdata, *versiondata;
	const char *mode;
	bool executed = false;

	/* Get version and ACVP test vector data */
	CKINT(json_split_version(in, &acvpdata, &versiondata));
	CKINT(json_get_string(acvpdata, "mode", &mode));

	if (kdf_ssh_backend && !strncmp(mode, "ssh", 3)) {
		CKINT(kdf_tester_ssh(in, out, cipher));
		executed = true;
	}
	if (kdf_tls_backend && !strncmp(mode, "tls", 3)) {
		CKINT(kdf_tester_tls(in, out, cipher));
		executed = true;
	}
	if (kdf_ikev1_backend && !strncmp(mode, "ikev1", 5)) {
		CKINT(kdf_tester_ikev1(in, out, cipher));
		executed = true;
	}
	if (kdf_ikev2_backend && !strncmp(mode, "ikev2", 5)) {
		CKINT(kdf_tester_ikev2(in, out, cipher));
		executed = true;
	}
	if (ansi_x963_backend && !strncmp(mode, "ansix9.63", 9)) {
		CKINT(kdf_tester_ansi_x963(in, out, cipher));
		executed = true;
	}
	if (kdf_srtp_backend && !strncmp(mode, "srtp", 4)) {
		CKINT(kdf_tester_kdf_srtp(in, out, cipher));
		executed = true;
	}

	/*
	 * If !executed -> None of the backends were registered -> -EOPNOTSUPP.
	 *
	 * If executed, then we have at least one successful run and data
	 * -> clear out any -EOPNOTSUPP.
	 */
	if (!executed)
		ret = -EOPNOTSUPP;
	else
		ret = 0;

out:
	return ret;
}

static struct cavs_tester kdf =
{
	ACVP_KDF_COMPONENT,
	0,
	kdf_tester,
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_kdf)
static void register_kdf(void)
{
	register_tester(&kdf, "KDF");
}

void register_kdf_tls_impl(struct kdf_tls_backend *implementation)
{
	register_backend(kdf_tls_backend, implementation, "KDF_TLS");
}

void register_kdf_ssh_impl(struct kdf_ssh_backend *implementation)
{
	register_backend(kdf_ssh_backend, implementation, "KDF_SSH");
}

void register_kdf_ikev1_impl(struct kdf_ikev1_backend *implementation)
{
	register_backend(kdf_ikev1_backend, implementation, "KDF_IKEv1");
}

void register_kdf_ikev2_impl(struct kdf_ikev2_backend *implementation)
{
	register_backend(kdf_ikev2_backend, implementation, "KDF_IKEv2");
}

void register_ansi_x963_impl(struct ansi_x963_backend *implementation)
{
	register_backend(ansi_x963_backend, implementation, "ANSI_X9.63");
}

void register_kdf_srtp_impl(struct kdf_srtp_backend *implementation)
{
	register_backend(kdf_srtp_backend, implementation, "KDF_SRTP");
}
