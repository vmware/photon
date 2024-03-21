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
 * KDF TLS callback definitions
 ******************************************************************************/
static struct tls12_backend *tls12_backend = NULL;

static int kdf_tester_tls12(struct json_object *in, struct json_object *out,
			     uint64_t cipher)
{
	(void)cipher;

	/**********************************************************************
	 * KDF TLS operation
	 **********************************************************************/
	DEF_CALLBACK(tls12, tls12, FLAG_OP_AFT);

	const struct json_entry tls12_testresult_entries[] = {
		{"masterSecret",		{.data.buf = &tls12_vector.master_secret, WRITER_BIN},	FLAG_OP_AFT},
		{"keyBlock",			{.data.buf = &tls12_vector.key_block, WRITER_BIN},	FLAG_OP_AFT},
	};
	const struct json_testresult kdf_tls_testresult =
		SET_ARRAY(tls12_testresult_entries, &tls12_callbacks);

	const struct json_entry kdf_tls_test_entries[] = {
		{"sessionHash",			{.data.buf = &tls12_vector.session_hash, PARSER_BIN},	FLAG_OP_AFT},
		{"clientRandom",		{.data.buf = &tls12_vector.client_random, PARSER_BIN},	FLAG_OP_AFT},
		{"serverRandom",		{.data.buf = &tls12_vector.server_random, PARSER_BIN},	FLAG_OP_AFT},
		{"preMasterSecret",		{.data.buf = &tls12_vector.pre_master_secret, PARSER_BIN},	FLAG_OP_AFT},
	};

	/* search for empty arrays */
	const struct json_array kdf_tls_test = SET_ARRAY(kdf_tls_test_entries, &kdf_tls_testresult);

	const struct json_entry kdf_tls_testgroup_entries[] = {
		{"hashAlg",			{.data.largeint = &tls12_vector.hashalg, PARSER_CIPHER},	FLAG_OP_AFT },
		{"preMasterSecretLength",	{.data.integer = &tls12_vector.pre_master_secret_length, PARSER_UINT},	FLAG_OP_AFT },
		{"keyBlockLength",		{.data.integer = &tls12_vector.key_block_length, PARSER_UINT}, FLAG_OP_AFT },
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

static struct cavs_tester kdf_tls12 =
{
	ACVP_KDF_TLS12,
	0,
	kdf_tester_tls12,
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_kdf_tls12)
static void register_kdf_tls12(void)
{
	register_tester(&kdf_tls12, "KDF TLSv1.2");
}

void register_tls12_impl(struct tls12_backend *implementation)
{
	register_backend(tls12_backend, implementation, "KDF_TLS1.2");
}
