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

#include "stringhelper.h"
#include "binhexbin.h"
#include "logger.h"

#include "parser_common.h"
#include "parser_eddsa.h"

#define EDDSA_DEF_CALLBACK(name, flags)		DEF_CALLBACK(eddsa, name, flags)
#define EDDSA_DEF_CALLBACK_HELPER(name, flags, helper)			       \
				DEF_CALLBACK_HELPER(eddsa, name, flags, helper)

static struct eddsa_backend *eddsa_backend = NULL;

struct eddsa_static_key {
	void *key;
	uint64_t curve;
	struct buffer q;
};
static struct eddsa_static_key eddsa_key = { NULL, 0, {NULL, 0} };

static void eddsa_key_free(struct eddsa_static_key *key)
{
	if (key->key)
		eddsa_backend->eddsa_free_key(key->key);
	key->key = NULL;
	key->curve = 0;

	free_buf(&key->q);
}

static void eddsa_key_free_static(void)
{
	eddsa_key_free(&eddsa_key);
}

static int eddsa_duplicate_buf(const struct buffer *src, struct buffer *dst)
{
	int ret;

	CKINT(alloc_buf(src->len, dst));
	memcpy(dst->buf, src->buf, dst->len);

out:
	return ret;
}

static int eddsa_siggen_keygen(struct eddsa_siggen_data *data,
			       void **eddsa_privkey)
{
	int ret = 0;

	if ((eddsa_key.curve != data->cipher) || !eddsa_key.key) {
		eddsa_key_free_static();
		CKINT(eddsa_backend->eddsa_keygen_en(&data->q,
						data->cipher & ACVP_CURVEMASK,
						&eddsa_key.key));

		logger_binary(LOGGER_DEBUG, data->q.buf, data->q.len,
			      "EDDSA generated public key");

		/* Free the global variable at exit */
		atexit(eddsa_key_free_static);

		CKINT(eddsa_duplicate_buf(&data->q, &eddsa_key.q));
		eddsa_key.curve = data->cipher & ACVP_CURVEMASK;
	}

	if (!data->q.len)
		CKINT(eddsa_duplicate_buf(&eddsa_key.q, &data->q));

	*eddsa_privkey = eddsa_key.key;

out:
	return ret;
}

static int eddsa_siggen_helper(const struct json_array *processdata,
			       flags_t parsed_flags,
			       struct json_object *testvector,
			       struct json_object *testresults,
	int (*callback)(struct eddsa_siggen_data *vector, flags_t parsed_flags),
			struct eddsa_siggen_data *vector)
{
	int ret;
	void *eddsa_privkey = NULL;

	(void)processdata;
	(void)testvector;
	(void)testresults;

	if (eddsa_backend->eddsa_keygen_en && eddsa_backend->eddsa_free_key) {
		CKINT(eddsa_siggen_keygen(vector, &eddsa_privkey));
	}

	vector->privkey = eddsa_privkey;

	CKINT(callback(vector, parsed_flags));

out:
	return ret;
}

static int eddsa_tester(struct json_object *in, struct json_object *out,
			uint64_t cipher)
{
	(void)cipher;

	if (!eddsa_backend) {
		logger(LOGGER_WARN, "No EDDSA backend set\n");
		return -EOPNOTSUPP;
	}

	/**********************************************************************
	 * EDDSA key generation
	 **********************************************************************/
	EDDSA_DEF_CALLBACK(eddsa_keygen, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING);

	const struct json_entry eddsa_keygen_testresult_entries[] = {
		{"q",		{.data.buf = &eddsa_keygen_vector.q, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING},
		{"d",		{.data.buf = &eddsa_keygen_vector.d, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING},
	};
	const struct json_testresult eddsa_keygen_testresult =
	SET_ARRAY(eddsa_keygen_testresult_entries, &eddsa_keygen_callbacks);

	/* search for empty arrays */
	const struct json_array eddsa_keygen_test = {NULL, 0, &eddsa_keygen_testresult};

	const struct json_entry eddsa_keygen_testgroup_entries[] = {
		{"curve",	{.data.largeint = &eddsa_keygen_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING },
		{"tests",	{.data.array = &eddsa_keygen_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING},
	};
	const struct json_array eddsa_keygen_testgroup = SET_ARRAY(eddsa_keygen_testgroup_entries, NULL);

	/**********************************************************************
	 * EDDSA key verification
	 **********************************************************************/
	EDDSA_DEF_CALLBACK(eddsa_keyver, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER);

	const struct json_entry eddsa_keyver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &eddsa_keyver_vector.keyver_success, WRITER_BOOL},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
	};
	const struct json_testresult eddsa_keyver_testresult = SET_ARRAY(eddsa_keyver_testresult_entries, &eddsa_keyver_callbacks);

	const struct json_entry eddsa_keyver_test_entries[] = {
		{"q",		{.data.buf = &eddsa_keyver_vector.q, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
		{"d",		{.data.buf = &eddsa_keyver_vector.d, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
	};

	/* search for empty arrays */
	const struct json_array eddsa_keyver_test = SET_ARRAY(eddsa_keyver_test_entries, &eddsa_keyver_testresult);

	const struct json_entry eddsa_keyver_testgroup_entries[] = {
		{"curve",	{.data.largeint = &eddsa_keyver_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER },
		{"tests",	{.data.array = &eddsa_keyver_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER },
	};
	const struct json_array eddsa_keyver_testgroup = SET_ARRAY(eddsa_keyver_testgroup_entries, NULL);

	/**********************************************************************
	 * EDDSA signature generation
	 **********************************************************************/
	EDDSA_DEF_CALLBACK_HELPER(eddsa_siggen, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN, eddsa_siggen_helper);

	const struct json_entry eddsa_siggen_testresult_entries[] = {
		{"signature",		{.data.buf = &eddsa_siggen_vector.signature, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	const struct json_testresult eddsa_siggen_testresult = SET_ARRAY(eddsa_siggen_testresult_entries, &eddsa_siggen_callbacks);

	const struct json_entry eddsa_siggen_test_entries[] = {
		{"message",		{.data.buf = &eddsa_siggen_vector.msg, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
	};

	const struct json_entry eddsa_siggen_testgroup_result_entries[] = {
		{"q",		{.data.buf = &eddsa_siggen_vector.q, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	/*
	 * The NULL for the function callbacks implies that the qx and qy
	 * are printed at the same hierarchy level as tgID
	 */
	const struct json_testresult eddsa_siggen_testgroup_result = SET_ARRAY(eddsa_siggen_testgroup_result_entries, NULL);

	/* search for empty arrays */
	const struct json_array eddsa_siggen_test = SET_ARRAY(eddsa_siggen_test_entries, &eddsa_siggen_testresult);

	const struct json_entry eddsa_siggen_testgroup_entries[] = {
		{"curve",	{.data.largeint = &eddsa_siggen_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"tests",	{.data.array = &eddsa_siggen_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	const struct json_array eddsa_siggen_testgroup = SET_ARRAY(eddsa_siggen_testgroup_entries,
		  &eddsa_siggen_testgroup_result);

	/**********************************************************************
	 * EDDSA signature verification
	 **********************************************************************/
	EDDSA_DEF_CALLBACK(eddsa_sigver, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER);

	const struct json_entry eddsa_sigver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &eddsa_sigver_vector.sigver_success, WRITER_BOOL},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
	};
	const struct json_testresult eddsa_sigver_testresult = SET_ARRAY(eddsa_sigver_testresult_entries, &eddsa_sigver_callbacks);

	const struct json_entry eddsa_sigver_test_entries[] = {
		{"message",	{.data.buf = &eddsa_sigver_vector.msg, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
		{"q",		{.data.buf = &eddsa_sigver_vector.q, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
		{"signature",	{.data.buf = &eddsa_sigver_vector.signature, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
	};

	/* search for empty arrays */
	const struct json_array eddsa_sigver_test = SET_ARRAY(eddsa_sigver_test_entries, &eddsa_sigver_testresult);

	const struct json_entry eddsa_sigver_testgroup_entries[] = {
		{"curve",	{.data.largeint = &eddsa_sigver_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
		{"tests",	{.data.array = &eddsa_sigver_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
	};
	const struct json_array eddsa_sigver_testgroup = SET_ARRAY(eddsa_sigver_testgroup_entries, NULL);

	/**********************************************************************
	 * EDDSA common test group
	 **********************************************************************/
	const struct json_entry eddsa_testanchor_entries[] = {
		{"testGroups",	{.data.array = &eddsa_keygen_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING},
		{"testGroups",	{.data.array = &eddsa_keyver_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_KEYVER},
		{"testGroups",	{.data.array = &eddsa_siggen_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_SIGGEN},
		{"testGroups",	{.data.array = &eddsa_sigver_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_SIGVER},
	};
	const struct json_array eddsa_testanchor = SET_ARRAY(eddsa_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&eddsa_testanchor, "1.0", in, out);
}

static struct cavs_tester eddsa =
{
	ACVP_EDDSA,
	0,
	eddsa_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_eddsa)
static void register_eddsa(void)
{
	register_tester(&eddsa, "EDDSA");
}

void register_eddsa_impl(struct eddsa_backend *implementation)
{
	register_backend(eddsa_backend, implementation, "EDDSA");
}
