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

#include "conversion_be_le.h"
#include "parser.h"
#include "stringhelper.h"
#include "read_json.h"
#include "logger.h"

#include "parser_common.h"
#include "parser_sha.h"
#include "parser_sha_mct_helper.h"

static struct sha_backend *sha_backend = NULL;

#define min(x, y)	(((size_t)x < (size_t)y) ? x : y)

static int shake_mct_helper(const struct json_array *processdata,
			    flags_t parsed_flags,
			    struct json_object *testvector,
			    struct json_object *testresults,
			    int (*callback)(struct sha_data *vector,
					    flags_t parsed_flags),
			    struct sha_data *vector)
{
	uint32_t maxoutbytes = vector->maxoutlen / 8;
	unsigned int i;
	int ret;
	struct json_object *testresult, *resultsarray = NULL;

	(void)callback;
	(void)processdata;

	CKNULL(sha_backend->hash_generate, -EOPNOTSUPP);
	CKNULL(maxoutbytes, -EOPNOTSUPP);

	/* Create output stream. */
	resultsarray = json_object_new_array();
	CKNULL(resultsarray, -ENOMEM);
	testresult = json_object_new_object();
	CKNULL(testresult, -ENOMEM);
	CKINT(json_add_test_data(testvector, testresult));

	vector->outlen = maxoutbytes * 8;

	/*
	 * Ensure that we only look at the leftmost 16 bytes. This should be
	 * a noop these days, but keep the check to be sure.
	 */
	vector->msg.len = min(vector->msg.len, 16);

	for (i = 0; i < 100; i++) {
		struct json_object *single_mct_result;

		/*
		 * Create the output JSON stream holding the test
		 * results.
		 */
		single_mct_result = json_object_new_object();
		CKNULL(single_mct_result, -ENOMEM);
		/* Append the output JSON stream with test results. */
		CKINT(json_object_array_add(resultsarray, single_mct_result));

		if (sha_backend->hash_mct_inner_loop) {
			ret = sha_backend->hash_mct_inner_loop(vector,
							parsed_flags);

			/*
			 * If the execution failed, we fall back
			 * to execute the inner loop with the code
			 * below.
			 */
			if (ret != 0) {
				CKINT(parser_shake_inner_loop(vector,
					parsed_flags,
					sha_backend->hash_generate));
			}

		} else {
			CKINT(parser_shake_inner_loop(vector,
					parsed_flags,
					sha_backend->hash_generate));
		}

		CKINT(json_add_bin2hex(single_mct_result, "md",
				       &vector->mac));
		CKINT(json_object_object_add(single_mct_result, "outLen",
				json_object_new_int((int)vector->mac.len * 8)));

		/* hash becomes new message */
		memcpy(vector->msg.buf, vector->mac.buf,
		       min(vector->mac.len, vector->msg.len));
	}

	CKINT(json_object_object_add(testresult, "resultsArray", resultsarray));
	/* Append the output JSON stream with test results. */
	CKINT(json_object_array_add(testresults, testresult));

	/* We have written data, generic parser should not write it. */
	ret = FLAG_RES_DATA_WRITTEN;

out:
	if (ret && ret != FLAG_RES_DATA_WRITTEN) {
		if (resultsarray)
			json_object_put(resultsarray);
	}

	return ret;
}

static int sha3_mct_helper(const struct json_array *processdata,
			   flags_t parsed_flags,
			   struct json_object *testvector,
			   struct json_object *testresults,
			   int (*callback)(struct sha_data *vector,
					   flags_t parsed_flags),
			   struct sha_data *vector)
{
	unsigned int i = 0;
	int ret;
	struct json_object *testresult, *resultsarray = NULL;

	(void)callback;
	(void)processdata;

	CKNULL(sha_backend->hash_generate, -EOPNOTSUPP);

	/* Create output stream. */
	resultsarray = json_object_new_array();
	CKNULL(resultsarray, -ENOMEM);
	testresult = json_object_new_object();
	CKNULL(testresult, -ENOMEM);
	CKINT(json_add_test_data(testvector, testresult));

	for (i = 0; i < 100; i++) {
		struct json_object *single_mct_result;

		/*
		 * Create the output JSON stream holding the test
		 * results.
		 */
		single_mct_result = json_object_new_object();
		CKNULL(single_mct_result, -ENOMEM);
		/* Append the output JSON stream with test results. */
		CKINT(json_object_array_add(resultsarray, single_mct_result));

		if (sha_backend->hash_mct_inner_loop) {
			ret = sha_backend->hash_mct_inner_loop(vector,
							parsed_flags);

			/*
			 * If the execution failed, we fall back
			 * to execute the inner loop with the code
			 * below.
			 */
			if (ret != 0) {
				CKINT(parser_sha3_inner_loop(vector,
					parsed_flags,
					sha_backend->hash_generate));
			}

		} else {
			CKINT(parser_sha3_inner_loop(vector,
					parsed_flags,
					sha_backend->hash_generate));
		}

		CKINT(json_add_bin2hex(single_mct_result, "md",
				       &vector->mac));

		/* hash becomes new message */
		memcpy(vector->msg.buf, vector->mac.buf, vector->mac.len);
	}

	CKINT(json_object_object_add(testresult, "resultsArray", resultsarray));
	/* Append the output JSON stream with test results. */
	CKINT(json_object_array_add(testresults, testresult));

	/* We have written data, generic parser should not write it. */
	ret = FLAG_RES_DATA_WRITTEN;

out:
	if (ret && ret != FLAG_RES_DATA_WRITTEN) {
		if (resultsarray)
			json_object_put(resultsarray);
	}

	return ret;
}

static int sha2_mct_helper(const struct json_array *processdata,
			   flags_t parsed_flags,
			   struct json_object *testvector,
			   struct json_object *testresults,
			   int (*callback)(struct sha_data *vector,
					   flags_t parsed_flags),
			   struct sha_data *vector)
{
	unsigned int i = 0;
	BUFFER_INIT(calc);
	int ret;
	struct json_object *testresult, *resultsarray = NULL;

	(void)callback;
	(void)processdata;

	CKNULL(sha_backend->hash_generate, -EOPNOTSUPP);

	CKINT(alloc_buf(vector->msg.len * 3, &calc));
	memcpy(calc.buf, vector->msg.buf, vector->msg.len);
	memcpy(calc.buf + vector->msg.len, vector->msg.buf,
		vector->msg.len);
	memcpy(calc.buf + vector->msg.len * 2, vector->msg.buf,
		vector->msg.len);

	free_buf(&vector->msg);
	copy_ptr_buf(&vector->msg, &calc);

	/* Create output stream. */
	resultsarray = json_object_new_array();
	CKNULL(resultsarray, -ENOMEM);
	testresult = json_object_new_object();
	CKNULL(testresult, -ENOMEM);
	CKINT(json_add_test_data(testvector, testresult));

	for (i = 0; i < 100; i++) {
		struct json_object *single_mct_result;

		/*
		 * Create the output JSON stream holding the test
		 * results.
		 */
		single_mct_result = json_object_new_object();
		CKNULL(single_mct_result, -ENOMEM);

		/* Append the output JSON stream with test results. */
		CKINT(json_object_array_add(resultsarray, single_mct_result));

		if (sha_backend->hash_mct_inner_loop) {
			ret = sha_backend->hash_mct_inner_loop(vector,
							parsed_flags);

			/*
			 * If the execution failed, we fall back
			 * to execute the inner loop with the code
			 * below.
			 */
			if (ret != 0) {
				CKINT(parser_sha2_inner_loop(vector,
					parsed_flags,
					sha_backend->hash_generate));
			}

		} else {
			CKINT(parser_sha2_inner_loop(vector,
					parsed_flags,
					sha_backend->hash_generate));
		}

		CKINT(json_add_bin2hex(single_mct_result, "md",
				       &vector->mac));

		/* shuffle for next round */
		memcpy(calc.buf, vector->mac.buf, vector->mac.len);
		memcpy(calc.buf + vector->mac.len, vector->mac.buf,
			vector->mac.len);
		memcpy(calc.buf + vector->mac.len * 2, vector->mac.buf,
			vector->mac.len);
	}

	CKINT(json_object_object_add(testresult, "resultsArray", resultsarray));
	/* Append the output JSON stream with test results. */
	CKINT(json_object_array_add(testresults, testresult));

	/* We have written data, generic parser should not write it. */
	ret = FLAG_RES_DATA_WRITTEN;

out:
	if (ret && ret != FLAG_RES_DATA_WRITTEN) {
		if (resultsarray)
			json_object_put(resultsarray);
	}

	return ret;

}

static int sha_mct_helper(const struct json_array *processdata,
			  flags_t parsed_flags,
			  struct json_object *testvector,
			  struct json_object *testresults,
			  int (*callback)(struct sha_data *vector,
					  flags_t parsed_flags),
			  struct sha_data *vector)
{
	switch (vector->cipher & (ACVP_HASHMASK | ACVP_SHAKEMASK)) {
	case ACVP_SHA3_224:
	case ACVP_SHA3_256:
	case ACVP_SHA3_384:
	case ACVP_SHA3_512:
		return sha3_mct_helper(processdata, parsed_flags, testvector,
				       testresults, callback, vector);
	default:
		return sha2_mct_helper(processdata, parsed_flags, testvector,
				       testresults, callback, vector);
	}
}

static int sha_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	struct sha_data vector;

	if (!sha_backend) {
		logger(LOGGER_WARN, "No SHA backend set\n");
		return -EOPNOTSUPP;
	}

	/* Referencing the backend functions */
	const struct sha_callback sha_aft = { sha_backend->hash_generate, &vector, NULL };
	const struct json_callback sha_callback_aft[] = {
		{ .callback.sha = sha_aft, CB_TYPE_sha, FLAG_OP_MASK_SHA | FLAG_OP_AFT | FLAG_OP_VOT | FLAG_OP_LDT },
	};
	const struct json_callbacks sha_callbacks_aft = SET_CALLBACKS(sha_callback_aft);

	const struct sha_callback sha_mct = { sha_backend->hash_generate, &vector, sha_mct_helper};
	const struct json_callback sha_callback_mct[] = {
		{ .callback.sha = sha_mct, CB_TYPE_sha, FLAG_OP_MASK_SHA | FLAG_OP_MCT},
	};
	const struct json_callbacks sha_callbacks_mct = SET_CALLBACKS(sha_callback_mct);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry sha_testresult_aft_entries[] = {
		{"md",		{.data.buf = &vector.mac, WRITER_BIN}, FLAG_OP_MASK_SHA | FLAG_OP_AFT},
	};
	const struct json_testresult sha_testresult_aft = SET_ARRAY(sha_testresult_aft_entries, &sha_callbacks_aft);

	const struct json_entry sha_testresult_mct_entries[] = {
		{"md",		{.data.buf = &vector.mac, WRITER_BIN}, FLAG_OP_MASK_SHA | FLAG_OP_MCT},
	};
	const struct json_testresult sha_testresult_mct = SET_ARRAY(sha_testresult_mct_entries, &sha_callbacks_mct);

	const struct json_entry sha_testresult_ldt_entries[] = {
		{"md",		{.data.buf = &vector.mac, WRITER_BIN}, FLAG_OP_MASK_SHA | FLAG_OP_LDT},
	};
	const struct json_testresult sha_testresult_ldt = SET_ARRAY(sha_testresult_ldt_entries, &sha_callbacks_aft);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file.
	 */
	const struct json_entry sha_test_aft_entries[] = {
		{"msg",		{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_MASK_SHA | FLAG_OP_AFT},
		{"len",		{.data.integer = &vector.bitlen, PARSER_UINT},	FLAG_OP_MASK_SHA | FLAG_OP_AFT},
	};
	const struct json_array sha_test_aft = SET_ARRAY(sha_test_aft_entries, &sha_testresult_aft);

	const struct json_entry sha_test_mct_entries[] = {
		{"msg",		{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_MASK_SHA | FLAG_OP_MCT},
		{"len",		{.data.integer = &vector.bitlen, PARSER_UINT},	FLAG_OP_MASK_SHA | FLAG_OP_MCT},
	};
	const struct json_array sha_test_mct = SET_ARRAY(sha_test_mct_entries, &sha_testresult_mct);

	const struct json_entry sha_test_ldt_msg_entries[] = {
		{"content",	{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_MASK_SHA | FLAG_OP_LDT},
		{"fullLength",	{.data.largeint = &vector.ldt_expansion_size, PARSER_UINT64},	FLAG_OP_MASK_SHA | FLAG_OP_LDT},
	};
	const struct json_array sha_test_ldt_msg = SET_ARRAY(sha_test_ldt_msg_entries, NULL);

	const struct json_entry sha_test_ldt_entries[] = {
		{"largeMsg",	{.data.array = &sha_test_ldt_msg, PARSER_OBJECT},	FLAG_OP_MASK_SHA | FLAG_OP_LDT},
	};
	const struct json_array sha_test_ldt = SET_ARRAY(sha_test_ldt_entries, &sha_testresult_ldt);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors.
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry sha_testgroup_entries[] = {
		{"tests",	{.data.array = &sha_test_aft, PARSER_ARRAY},	FLAG_OP_MASK_SHA | FLAG_OP_AFT},
		{"tests",	{.data.array = &sha_test_mct, PARSER_ARRAY},	FLAG_OP_MASK_SHA | FLAG_OP_MCT},
		{"tests",	{.data.array = &sha_test_ldt, PARSER_ARRAY},	FLAG_OP_MASK_SHA | FLAG_OP_LDT},
	};
	const struct json_array sha_testgroup = SET_ARRAY(sha_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry sha_testanchor_entries[] = {
		{"testGroups",	{.data.array = &sha_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array sha_testanchor = SET_ARRAY(sha_testanchor_entries, NULL);

	memset(&vector, 0, sizeof(struct sha_data));
	vector.cipher = cipher;

	/* Process all. */
	return process_json(&sha_testanchor, "1.0", in, out);
}

static int shake_tester(struct json_object *in, struct json_object *out,
			uint64_t cipher)
{
	struct sha_data vector;

	if (!sha_backend) {
		logger(LOGGER_WARN, "No SHA backend set\n");
		return -EOPNOTSUPP;
	}

	/* Referencing the backend functions */
	const struct sha_callback shake_aft = { sha_backend->hash_generate, &vector, NULL};
	const struct json_callback shake_callback_aft[] = {
		{ .callback.sha = shake_aft, CB_TYPE_sha, FLAG_OP_MASK_SHA | FLAG_OP_AFT | FLAG_OP_VOT},
	};
	const struct json_callbacks shake_callbacks_aft = SET_CALLBACKS(shake_callback_aft);

	const struct sha_callback shake_mct = { sha_backend->hash_generate, &vector, shake_mct_helper};
	const struct json_callback shake_callback_mct[] = {
		{ .callback.sha = shake_mct, CB_TYPE_sha, FLAG_OP_MASK_SHA | FLAG_OP_MCT},
	};
	const struct json_callbacks shake_callbacks_mct = SET_CALLBACKS(shake_callback_mct);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry shake_testresult_aft_entries[] = {
		{"md",		{.data.buf = &vector.mac, WRITER_BIN}, FLAG_OP_MASK_SHA | FLAG_OP_AFT},
		{"outLen",	{.data.integer = &vector.outlen, WRITER_UINT}, FLAG_OP_MASK_SHA | FLAG_OP_AFT},
	};
	const struct json_testresult shake_testresult_aft = SET_ARRAY(shake_testresult_aft_entries, &shake_callbacks_aft);

	const struct json_entry shake_testresult_mct_entries[] = {
		{"md",		{.data.buf = &vector.mac, WRITER_BIN}, FLAG_OP_MASK_SHA | FLAG_OP_MCT},
	};
	const struct json_testresult shake_testresult_mct = SET_ARRAY(shake_testresult_mct_entries, &shake_callbacks_mct);

	const struct json_entry shake_testresult_vot_entries[] = {
		{"md",		{.data.buf = &vector.mac, WRITER_BIN}, FLAG_OP_MASK_SHA | FLAG_OP_VOT},
		{"outLen",	{.data.integer = &vector.outlen, WRITER_UINT}, FLAG_OP_MASK_SHA | FLAG_OP_VOT},
	};
	const struct json_testresult shake_testresult_vot = SET_ARRAY(shake_testresult_vot_entries, &shake_callbacks_aft);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file.
	 */
	const struct json_entry shake_test_aft_entries[] = {
		{"msg",		{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_MASK_SHA | FLAG_OP_AFT},
		{"len",		{.data.integer = &vector.bitlen, PARSER_UINT},	FLAG_OP_MASK_SHA | FLAG_OP_AFT},
		{"outLen",	{.data.integer = &vector.outlen, PARSER_UINT},	FLAG_OP_MASK_SHA | FLAG_OP_AFT},
	};
	const struct json_array shake_test_aft = SET_ARRAY(shake_test_aft_entries, &shake_testresult_aft);

	const struct json_entry shake_test_mct_entries[] = {
		{"msg",		{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_MASK_SHA | FLAG_OP_MCT},
		{"len",		{.data.integer = &vector.bitlen, PARSER_UINT},	FLAG_OP_MASK_SHA | FLAG_OP_MCT},
	};
	const struct json_array shake_test_mct = SET_ARRAY(shake_test_mct_entries, &shake_testresult_mct);

	const struct json_entry shake_test_vot_entries[] = {
		{"msg",		{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_MASK_SHA | FLAG_OP_VOT},
		{"len",		{.data.integer = &vector.bitlen, PARSER_UINT},	FLAG_OP_MASK_SHA | FLAG_OP_VOT},
		{"outLen",	{.data.integer = &vector.outlen, PARSER_UINT},	FLAG_OP_MASK_SHA | FLAG_OP_VOT},
	};
	const struct json_array shake_test_vot = SET_ARRAY(shake_test_vot_entries, &shake_testresult_vot);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors.
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry shake_testgroup_entries[] = {
		{"tests",	{.data.array = &shake_test_aft, PARSER_ARRAY},	FLAG_OP_MASK_SHA | FLAG_OP_AFT},
		{"tests",	{.data.array = &shake_test_vot, PARSER_ARRAY},	FLAG_OP_MASK_SHA | FLAG_OP_VOT},

		{"maxOutLen",	{.data.integer = &vector.maxoutlen, PARSER_UINT},	FLAG_OP_MASK_SHA | FLAG_OP_MCT},
		{"minOutLen",	{.data.integer = &vector.minoutlen, PARSER_UINT},	FLAG_OP_MASK_SHA | FLAG_OP_MCT},
		{"tests",	{.data.array = &shake_test_mct, PARSER_ARRAY},	FLAG_OP_MASK_SHA | FLAG_OP_MCT},
	};
	const struct json_array shake_testgroup = SET_ARRAY(shake_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry shake_testanchor_entries[] = {
		{"testGroups",	{.data.array = &shake_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array shake_testanchor = SET_ARRAY(shake_testanchor_entries, NULL);

	memset(&vector, 0, sizeof(struct sha_data));
	vector.cipher = cipher;

	/* Process all. */
	return process_json(&shake_testanchor, "1.0", in, out);
}

static struct cavs_tester shake =
{
	0,
	ACVP_SHAKEMASK,
	shake_tester,	/* process_req */
	NULL
};

static struct cavs_tester sha =
{
	0,
	ACVP_HASHMASK,
	sha_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_sha)
static void register_sha(void)
{
	register_tester(&sha, "SHA");
	register_tester(&shake, "SHAKE");
}

void register_sha_impl(struct sha_backend *implementation)
{
	register_backend(sha_backend, implementation, "SHA");
}
