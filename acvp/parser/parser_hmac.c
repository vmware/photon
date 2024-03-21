/*
 * Copyright (C) 2017 - 2022, Stephan Mueller <smueller@chronox.de>
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

#include <string.h>

#include "stringhelper.h"
#include "read_json.h"
#include "logger.h"

#include "parser_common.h"
#include "parser_hmac.h"

static struct hmac_backend *hmac_backend = NULL;

#undef ACVP_PARSER_CMAC_TDES_3_KEYS

#ifdef ACVP_PARSER_CMAC_TDES_3_KEYS
static int sym_tdes_concatenate_keys(const struct json_array *processdata,
				     flags_t parsed_flags,
				     struct json_object *testvector,
				     struct json_object *testresults,
	int (*callback)(struct hmac_data *vector, flags_t parsed_flags),
				     struct hmac_data *vector)
{
	struct buffer tmp, tmp2;
	int ret;

	(void)processdata;
	(void)testvector;
	(void)testresults;

	memset(&tmp, 0, sizeof(tmp));
	memset(&tmp2, 0, sizeof(tmp2));

	if (vector->cipher == ACVP_TDESCMAC) {
		ret = alloc_buf(vector->key.len + vector->key2.len +
				vector->key3.len, &tmp);
		if (ret)
			return ret;
		memcpy(tmp.buf, vector->key.buf, vector->key.len);
		memcpy(tmp.buf + vector->key.len, vector->key2.buf,
		       vector->key2.len);
		memcpy(tmp.buf + vector->key.len + vector->key2.len,
		       vector->key3.buf, vector->key3.len);

		logger_binary(LOGGER_DEBUG, tmp.buf, tmp.len,
			      "Concatenated key");

		/* save original key pointer */
		copy_ptr_buf(&tmp2, &vector->key);
		/* move new key pointer into vector->key */
		copy_ptr_buf(&vector->key, &tmp);
		ret = callback(vector, parsed_flags);
		/* restore original key pointer */
		copy_ptr_buf(&vector->key, &tmp2);
		free_buf(&tmp);
	} else {
		ret = callback(vector, parsed_flags);
	}

	return ret;
}
#endif

static int cmac_ver_helper(const struct json_array *processdata,
			   flags_t parsed_flags,
			   struct json_object *testvector,
			   struct json_object *testresults,
			   int (*callback)(struct hmac_data *vector,
					   flags_t parsed_flags),
			   struct hmac_data *vector)
{
	struct buffer buf;
	int ret = 0;

	(void)processdata;
	(void)testvector;
	(void)testresults;

	copy_ptr_buf(&buf, &vector->mac);
	vector->mac.buf = NULL;
	vector->mac.len = 0;

#ifdef ACVP_PARSER_CMAC_TDES_3_KEYS
	CKINT(sym_tdes_concatenate_keys(processdata, parsed_flags, testvector,
					testresults, callback, vector));
#endif

	CKINT(callback(vector, parsed_flags));

	if (vector->mac.buf && !memcmp(buf.buf, vector->mac.buf, buf.len))
		vector->verify_result = 1;
	else
		vector->verify_result = 0;

	logger(LOGGER_DEBUG, "CMAC verify: %s\n",
	       vector->verify_result ? "matched" : "not matched");

out:
	free_buf(&buf);
	return ret;
}

static int hmac_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	struct hmac_data vector;

	if (!hmac_backend) {
		logger(LOGGER_WARN, "No HMAC backend set\n");
		return -EOPNOTSUPP;
	}

	/* Referencing the backend functions */
	const struct hmac_callback hmac = { hmac_backend->hmac_generate, &vector, NULL};
	const struct json_callback hmac_callback[] = {
		{ .callback.hmac = hmac, CB_TYPE_hmac, FLAG_OP_AFT},
	};
	const struct json_callbacks hmac_callbacks = SET_CALLBACKS(hmac_callback);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry hmac_testresult_entries[] = {
		{"mac",		{.data.buf = &vector.mac, WRITER_BIN}, FLAG_OP_AFT},
	};
	const struct json_testresult hmac_testresult = SET_ARRAY(hmac_testresult_entries, &hmac_callbacks);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file.
	 */
	const struct json_entry hmac_test_entries[] = {
		{"msg",		{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_AFT},
		{"key",		{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_AFT},
	};
	const struct json_array hmac_test = SET_ARRAY(hmac_test_entries, &hmac_testresult);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors.
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry mac_testgroup_entries[] = {
		{"macLen",	{.data.integer = &vector.maclen, PARSER_UINT},	FLAG_OP_AFT},
		{"tests",	{.data.array = &hmac_test, PARSER_ARRAY},	FLAG_OP_AFT},
	};
	const struct json_array mac_testgroup = SET_ARRAY(mac_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry mac_testanchor_entries[] = {
		{"testGroups",	{.data.array = &mac_testgroup, PARSER_ARRAY},		0},
	};
	const struct json_array mac_testanchor = SET_ARRAY(mac_testanchor_entries, NULL);

	memset(&vector, 0, sizeof(struct hmac_data));
	vector.cipher = cipher;

	/* Process all. */
	return process_json(&mac_testanchor, "1.0", in, out);
}

static int cmac_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	struct hmac_data vector;

	if (!hmac_backend) {
		logger(LOGGER_WARN, "No HMAC backend set\n");
		return -EOPNOTSUPP;
	}

	/* Referencing the backend functions */
	const struct hmac_callback cmac_ver = { hmac_backend->hmac_generate, &vector, cmac_ver_helper};
	const struct json_callback cmac_callback_ver[] = {
		{ .callback.hmac = cmac_ver, CB_TYPE_hmac, FLAG_OP_CMAC_VER_TEST | FLAG_OP_AFT},
	};
	const struct json_callbacks cmac_callbacks_ver = SET_CALLBACKS(cmac_callback_ver);

#ifdef ACVP_PARSER_CMAC_TDES_3_KEYS
	const struct hmac_callback cmac_gen = { hmac_backend->hmac_generate, &vector, sym_tdes_concatenate_keys};
#else
	const struct hmac_callback cmac_gen = { hmac_backend->hmac_generate, &vector, NULL};
#endif
	const struct json_callback cmac_callback_gen[] = {
		{ .callback.hmac = cmac_gen, CB_TYPE_hmac, FLAG_OP_CMAC_GEN_TEST | FLAG_OP_AFT},
	};
	const struct json_callbacks cmac_callbacks_gen = SET_CALLBACKS(cmac_callback_gen);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry cmac_testresult_ver_entries[] = {
		{"testPassed",	{.data.integer = &vector.verify_result, WRITER_BOOL}, FLAG_OP_CMAC_VER_TEST | FLAG_OP_AFT},
	};
	const struct json_testresult cmac_testresult_ver = SET_ARRAY(cmac_testresult_ver_entries, &cmac_callbacks_ver);

	const struct json_entry cmac_testresult_gen_entries[] = {
		{"mac",		{.data.buf = &vector.mac, WRITER_BIN}, FLAG_OP_CMAC_GEN_TEST | FLAG_OP_AFT},
	};
	const struct json_testresult cmac_testresult_gen = SET_ARRAY(cmac_testresult_gen_entries, &cmac_callbacks_gen);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file.
	 */
	const struct json_entry cmac_test_gen_entries[] = {
		{"message",	{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_CMAC_GEN_TEST},

		/* AES */
		{"key",		{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_CMAC_GEN_TEST | FLAG_OPTIONAL},

		/* TDES */
		{"key1",	{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_CMAC_GEN_TEST | FLAG_OPTIONAL},
		{"key2",	{.data.buf = &vector.key2, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_CMAC_GEN_TEST | FLAG_OPTIONAL},
		{"key3",	{.data.buf = &vector.key3, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_CMAC_GEN_TEST | FLAG_OPTIONAL},
	};
	const struct json_array cmac_test_gen = SET_ARRAY(cmac_test_gen_entries, &cmac_testresult_gen);

	const struct json_entry cmac_test_ver_entries[] = {
		{"message",	{.data.buf = &vector.msg, PARSER_BIN}, FLAG_OP_CMAC_VER_TEST | FLAG_OP_AFT},
		{"mac",		{.data.buf = &vector.mac, PARSER_BIN},	FLAG_OP_CMAC_VER_TEST | FLAG_OP_AFT},

		{"key",		{.data.buf = &vector.key, PARSER_BIN},	 FLAG_OP_CMAC_VER_TEST | FLAG_OP_AFT},

#ifdef ACVP_PARSER_CMAC_TDES_3_KEYS
		/* TDES */
		{"key1",	{.data.buf = &vector.key, PARSER_BIN},	 FLAG_OP_CMAC_VER_TEST | FLAG_OP_AFT | FLAG_OPTIONAL},
		{"key2",	{.data.buf = &vector.key2, PARSER_BIN},	 FLAG_OP_CMAC_VER_TEST | FLAG_OP_AFT | FLAG_OPTIONAL},
		{"key3",	{.data.buf = &vector.key3, PARSER_BIN},	 FLAG_OP_CMAC_VER_TEST | FLAG_OP_AFT | FLAG_OPTIONAL},
#endif
	};
	const struct json_array cmac_test_ver = SET_ARRAY(cmac_test_ver_entries, &cmac_testresult_ver);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors.
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry mac_testgroup_entries[] = {
		{"macLen",	{.data.integer = &vector.maclen, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_CMAC_GEN_TEST | FLAG_OP_CMAC_VER_TEST},
		{"tests",	{.data.array = &cmac_test_gen, PARSER_ARRAY},	FLAG_OP_AFT | FLAG_OP_CMAC_GEN_TEST},
		{"tests",	{.data.array = &cmac_test_ver, PARSER_ARRAY},	FLAG_OP_AFT | FLAG_OP_CMAC_VER_TEST},
	};
	const struct json_array mac_testgroup = SET_ARRAY(mac_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry mac_testanchor_entries[] = {
		{"testGroups",	{.data.array = &mac_testgroup, PARSER_ARRAY},		0},
	};
	const struct json_array mac_testanchor = SET_ARRAY(mac_testanchor_entries, NULL);

	memset(&vector, 0, sizeof(struct hmac_data));
	vector.cipher = cipher;

	/* Process all. */
	return process_json(&mac_testanchor, "1.0", in, out);
}

static struct cavs_tester hmac =
{
	0,
	ACVP_HMACMASK,
	hmac_tester,	/* process_req */
	NULL
};

static struct cavs_tester cmac =
{
	0,
	ACVP_CMACMASK,
	cmac_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_hmac)
static void register_hmac(void)
{
	register_tester(&hmac, "HMAC");
	register_tester(&cmac, "CMAC");
}

void register_hmac_impl(struct hmac_backend *implementation)
{
	register_backend(hmac_backend, implementation, "HMAC");
}
