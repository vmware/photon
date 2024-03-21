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

#include "parser_common.h"
#include "parser.h"
#include "logger.h"
#include "read_json.h"
#include "stringhelper.h"

static struct aead_backend *aead_backend = NULL;

static int aead_gcm_helper(const struct json_array *processdata,
			   flags_t parsed_flags,
			   struct json_object *testvector,
			   struct json_object *testresults, int enc,
	int (*callback)(struct aead_data *vector, flags_t parsed_flags),
			struct aead_data *vector)
{
	struct json_object *testresult = NULL;
	const struct json_entry *entry;
	unsigned int i;
	int ret;

	(void)testvector;

	CKNULL_LOG(callback, -EINVAL, "GCM handler missing\n");

	CKINT(callback(vector, parsed_flags));

	/* Free the buffer that may be left by the backend. */
	if (vector->integrity_error)
		free_buf(&vector->data);

	testresult = json_object_new_object();
	CKNULL(testresult, -ENOMEM);
	/* Append the output JSON stream with test results. */
	json_object_array_add(testresults, testresult);

	CKINT(json_add_test_data(testvector, testresult));

	/* Iterate over each write definition and invoke it. */
	for_each_testresult(processdata->testresult, entry, i)
		CKINT(write_one_entry(entry, testresult, parsed_flags));

	if (vector->cipher != ACVP_GMAC) {
		if (!vector->integrity_error && !vector->data.len)
			CKINT(json_add_bin2hex(testresult, enc ? "ct" : "pt",
					       &vector->data));
	}

	if (vector->cipher == ACVP_GMAC && !enc && !vector->integrity_error) {
		CKINT(json_object_object_add(testresult, "testPassed",
					     json_object_new_boolean(true)));
	}

	ret = FLAG_RES_DATA_WRITTEN;

out:
	return ret;
}

static int aead_gcm_encrypt_helper(const struct json_array *processdata,
				   flags_t parsed_flags,
				   struct json_object *testvector,
				   struct json_object *testresults,
	int (*callback)(struct aead_data *vector, flags_t parsed_flags),
			struct aead_data *vector)
{
	return aead_gcm_helper(processdata, parsed_flags, testvector,
			       testresults, 1, callback, vector);
}

static int aead_gcm_decrypt_helper(const struct json_array *processdata,
				   flags_t parsed_flags,
				   struct json_object *testvector,
				   struct json_object *testresults,
	int (*callback)(struct aead_data *vector, flags_t parsed_flags),
			struct aead_data *vector)
{
	return aead_gcm_helper(processdata, parsed_flags, testvector,
			       testresults, 0, callback, vector);
}

static int aead_tester(struct json_object *in, struct json_object *out,
		       struct aead_data *vector,
		       const struct json_callbacks *callbacks)
{
	if (!aead_backend) {
		logger(LOGGER_ERR,
		       "No backend implementation for AEAD ciphers available\n");
		return EOPNOTSUPP;
	}

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry aead_testresult_entries[] = {
		{"iv",		{.data.buf = &vector->iv, WRITER_BIN},		FLAG_OP_ENC | FLAG_OP_AFT},
		/* also write empty CT (in case we only perform auth tests) */
		{"ct",		{.data.buf = &vector->data, WRITER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"tag",		{.data.buf = &vector->tag, WRITER_BIN},		FLAG_OP_ENC | FLAG_OP_AFT},
		/* also write empty PT (in case we only perform auth tests) */
		{"pt",		{.data.buf = &vector->data, WRITER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"testPassed",	{.data.integer = &vector->integrity_error, WRITER_BOOL_TRUE_TO_FALSE},	FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_testresult aead_testresult = SET_ARRAY(aead_testresult_entries, callbacks);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file. For example:
	 * {
         *   "tcId": 2171,
         *   "key": "1529BAC6229586F057FAA59353851686",
         *   "pt": "",
         *   "aad": "4B11160620475D8EE440C3795CF62D26"
         * },
	 *
	 * After parsing each individual test vector, the test should be
	 * executed and the result should be written to a JSON file.
	 */
	const struct json_entry aead_test_entries[] = {
		{"iv",		{.data.buf = &vector->iv, PARSER_BIN},		FLAG_OPTIONAL  | FLAG_OP_ENC | FLAG_OP_AFT},
		{"key",		{.data.buf = &vector->key, PARSER_BIN}, 	FLAG_OP_ENC | FLAG_OP_AFT},
		{"aad",		{.data.buf = &vector->assoc, PARSER_BIN}, 	FLAG_OP_ENC | FLAG_OP_AFT},
		{"pt",		{.data.buf = &vector->data, PARSER_BIN}, 	FLAG_OP_ENC | FLAG_OP_AFT},

		{"iv",		{.data.buf = &vector->iv, PARSER_BIN}, 		FLAG_OP_DEC | FLAG_OP_AFT},
		{"key",		{.data.buf = &vector->key, PARSER_BIN},		FLAG_OP_DEC | FLAG_OP_AFT},
		{"aad",		{.data.buf = &vector->assoc, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"ct",		{.data.buf = &vector->data, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		/* Tag present for GCM, missing for CCM */
		{"tag",		{.data.buf = &vector->tag, PARSER_BIN},		FLAG_OP_DEC | FLAG_OP_AFT | FLAG_OPTIONAL},
	};
	const struct json_array aead_test = SET_ARRAY(aead_test_entries, &aead_testresult);

	const struct json_entry aead_testgroup_entries[] = {
		{"tagLen",	{.data.integer = &vector->taglen, PARSER_UINT},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"payloadLen",	{.data.integer = &vector->ptlen, PARSER_UINT},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"ivLen",	{.data.integer = &vector->ivlen, PARSER_UINT},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"tests",	{.data.array = &aead_test, PARSER_ARRAY},	FLAG_OP_ENC | FLAG_OP_AFT},

		{"tagLen",	{.data.integer = &vector->taglen, PARSER_UINT},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"payloadLen",	{.data.integer = &vector->ptlen, PARSER_UINT},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"ivLen",	{.data.integer = &vector->ivlen, PARSER_UINT},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"tests",	{.data.array = &aead_test, PARSER_ARRAY},	FLAG_OP_DEC | FLAG_OP_AFT}
	};
	const struct json_array aead_testgroup = SET_ARRAY(aead_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data. For example:
	 * {
	 *   "acvVersion": "0.2",
	 *   "vsId": 1564,
	 *   "algorithm": "AES-GCM",
	 *   "direction": "encrypt",
	 *   "testGroups": [
	 */
	const struct json_entry aead_testanchor_entries[] = {
		{"testGroups",	{.data.array = &aead_testgroup, PARSER_ARRAY}, 0 }
	};
	const struct json_array aead_testanchor = SET_ARRAY(aead_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&aead_testanchor, "1.0", in, out);
}


static int aead_gmac_tester(struct json_object *in, struct json_object *out,
			    struct aead_data *vector,
			    const struct json_callbacks *callbacks)
{
	if (!aead_backend) {
		logger(LOGGER_ERR,
		       "No backend implementation for AEAD ciphers available\n");
		return EOPNOTSUPP;
	}

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry aead_testresult_entries[] = {
		{"iv",		{.data.buf = &vector->iv, WRITER_BIN},		FLAG_OP_ENC | FLAG_OP_AFT},
		{"tag",		{.data.buf = &vector->tag, WRITER_BIN},		FLAG_OP_ENC | FLAG_OP_AFT},
		{"testPassed",	{.data.integer = &vector->integrity_error, WRITER_BOOL_TRUE_TO_FALSE},	FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_testresult aead_testresult = SET_ARRAY(aead_testresult_entries, callbacks);

	const struct json_entry aead_test_entries[] = {
		{"iv",		{.data.buf = &vector->iv, PARSER_BIN},		 FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_AFT},
		{"key",		{.data.buf = &vector->key, PARSER_BIN}, 	FLAG_OP_ENC | FLAG_OP_AFT},
		{"aad",		{.data.buf = &vector->assoc, PARSER_BIN}, 	FLAG_OP_ENC | FLAG_OP_AFT},

		{"iv",		{.data.buf = &vector->iv, PARSER_BIN}, 		FLAG_OP_DEC | FLAG_OP_AFT},
		{"key",		{.data.buf = &vector->key, PARSER_BIN},		FLAG_OP_DEC | FLAG_OP_AFT},
		{"aad",		{.data.buf = &vector->assoc, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"tag",		{.data.buf = &vector->tag, PARSER_BIN},		FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_array aead_test = SET_ARRAY(aead_test_entries, &aead_testresult);

	const struct json_entry aead_testgroup_entries[] = {
		{"tagLen",	{.data.integer = &vector->taglen, PARSER_UINT},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"ivLen",	{.data.integer = &vector->ivlen, PARSER_UINT},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"tests",	{.data.array = &aead_test, PARSER_ARRAY},	FLAG_OP_ENC | FLAG_OP_AFT},

		{"tagLen",	{.data.integer = &vector->taglen, PARSER_UINT},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"ivLen",	{.data.integer = &vector->ivlen, PARSER_UINT},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"tests",	{.data.array = &aead_test, PARSER_ARRAY},	FLAG_OP_DEC | FLAG_OP_AFT}
	};
	const struct json_array aead_testgroup = SET_ARRAY(aead_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data. For example:
	 * {
	 *   "acvVersion": "0.2",
	 *   "vsId": 1564,
	 *   "algorithm": "AES-GCM",
	 *   "direction": "encrypt",
	 *   "testGroups": [
	 */
	const struct json_entry aead_testanchor_entries[] = {
		{"testGroups",	{.data.array = &aead_testgroup, PARSER_ARRAY}, 0 }
	};
	const struct json_array aead_testanchor = SET_ARRAY(aead_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&aead_testanchor, "1.0", in, out);
}

static int aead_siv_tester(struct json_object *in, struct json_object *out,
			   struct aead_data *vector,
			   const struct json_callbacks *callbacks)
{
	if (!aead_backend) {
		logger(LOGGER_ERR,
		       "No backend implementation for AEAD ciphers available\n");
		return EOPNOTSUPP;
	}

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry aead_testresult_entries[] = {
		/* also write empty CT (in case we only perform auth tests) */
		{"ct",		{.data.buf = &vector->data, WRITER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},
		/* also write empty PT (in case we only perform auth tests) */
		{"pt",		{.data.buf = &vector->data, WRITER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"testPassed",	{.data.integer = &vector->integrity_error, WRITER_BOOL_TRUE_TO_FALSE},	FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_testresult aead_testresult = SET_ARRAY(aead_testresult_entries, callbacks);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file. For example:
	 * {
         *   "tcId": 2171,
         *   "key": "1529BAC6229586F057FAA59353851686",
         *   "pt": "",
         *   "aad": "4B11160620475D8EE440C3795CF62D26"
         * },
	 *
	 * After parsing each individual test vector, the test should be
	 * executed and the result should be written to a JSON file.
	 */
	const struct json_entry aead_test_entries[] = {
		{"iv",		{.data.buf = &vector->iv, PARSER_BIN},		FLAG_OPTIONAL  | FLAG_OP_ENC | FLAG_OP_AFT},
		{"key",		{.data.buf = &vector->key, PARSER_BIN}, 	FLAG_OP_ENC | FLAG_OP_AFT},
		{"aad",		{.data.buf = &vector->assoc, PARSER_BIN}, 	FLAG_OP_ENC | FLAG_OP_AFT},
		{"pt",		{.data.buf = &vector->data, PARSER_BIN}, 	FLAG_OP_ENC | FLAG_OP_AFT},

		{"iv",		{.data.buf = &vector->iv, PARSER_BIN}, 		FLAG_OP_DEC | FLAG_OP_AFT},
		{"key",		{.data.buf = &vector->key, PARSER_BIN},		FLAG_OP_DEC | FLAG_OP_AFT},
		{"aad",		{.data.buf = &vector->assoc, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"ct",		{.data.buf = &vector->data, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_array aead_test = SET_ARRAY(aead_test_entries, &aead_testresult);

	const struct json_entry aead_testgroup_entries[] = {
		{"payloadLen",	{.data.integer = &vector->ptlen, PARSER_UINT},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"tests",	{.data.array = &aead_test, PARSER_ARRAY},	FLAG_OP_ENC | FLAG_OP_AFT},

		{"payloadLen",	{.data.integer = &vector->ptlen, PARSER_UINT},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"tests",	{.data.array = &aead_test, PARSER_ARRAY},	FLAG_OP_DEC | FLAG_OP_AFT}
	};
	const struct json_array aead_testgroup = SET_ARRAY(aead_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data. For example:
	 * {
	 *   "acvVersion": "0.2",
	 *   "vsId": 1564,
	 *   "algorithm": "AES-GCM",
	 *   "direction": "encrypt",
	 *   "testGroups": [
	 */
	const struct json_entry aead_testanchor_entries[] = {
		{"testGroups",	{.data.array = &aead_testgroup, PARSER_ARRAY}, 0 }
	};
	const struct json_array aead_testanchor = SET_ARRAY(aead_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&aead_testanchor, "1.0", in, out);
}

static int gcm_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	struct aead_data vector;

	if (!aead_backend) {
		logger(LOGGER_WARN, "No AEAD backend set\n");
		return -EOPNOTSUPP;
	}

	/* Referencing the GCM backend functions */
	const struct aead_callback gcm_encrypt = { aead_backend->gcm_encrypt, &vector, aead_gcm_encrypt_helper};
	const struct aead_callback gcm_decrypt = { aead_backend->gcm_decrypt, &vector, aead_gcm_decrypt_helper};
	const struct json_callback gcm_callback[] = {
		{ .callback.aead = gcm_encrypt, CB_TYPE_aead, FLAG_OP_ENC | FLAG_OP_AFT },
		{ .callback.aead = gcm_decrypt, CB_TYPE_aead, FLAG_OP_DEC | FLAG_OP_AFT },
	};
	const struct json_callbacks gcm_callbacks = SET_CALLBACKS(gcm_callback);

	memset(&vector, 0, sizeof(struct aead_data));
	vector.cipher = cipher;

	if (cipher == ACVP_GCMSIV)
		return aead_siv_tester(in, out, &vector, &gcm_callbacks);

	if (cipher == ACVP_GMAC)
		return aead_gmac_tester(in, out, &vector, &gcm_callbacks);

	return aead_tester(in, out, &vector, &gcm_callbacks);
}

static int ccm_decrypt_helper(const struct json_array *processdata,
			      flags_t parsed_flags,
			      struct json_object *testvector,
			      struct json_object *testresults,
			      int (*callback)(struct aead_data *vector,
					      flags_t parsed_flags),
			      struct aead_data *vector)
{
	struct json_object *testresult;
	const struct json_entry *entry;
	uint32_t taglen = vector->taglen / 8;
	unsigned int i;
	int ret;

	/*
	 * Find the ciphertext and the tag (which are merged into one string)
	 */
	if (vector->data.len < taglen) {
		logger(LOGGER_ERR, "CT length is shorter than taglen?!\n");
		return -EINVAL;
	}
	vector->tag.len = taglen;
	vector->tag.buf = vector->data.buf + vector->data.len - taglen;
	vector->data.len -= taglen;

	testresult = json_object_new_object();
	CKNULL(testresult, -ENOMEM);
	CKINT(json_add_test_data(testvector, testresult));
	json_object_array_add(testresults, testresult);

	ret = callback(vector, parsed_flags);

	/* Prevent the parser from freeing that buffer pointer. */
	vector->tag.buf = NULL;
	vector->tag.len = 0;

	if (ret)
		goto out;

	/* Release the IV to not print it */
	free_buf(&vector->iv);

	/*
	 * If there is an integrity error, free the data now to prevent
	 * an empty data entry being written to JSON.
	 */
	if (vector->integrity_error)
		free_buf(&vector->data);

	/* Iterate over each write definition and invoke it. */
	for_each_testresult(processdata->testresult, entry, i)
		CKINT(write_one_entry(entry, testresult, parsed_flags));

	/* Write empty PT entry */
	if (vector->integrity_error == 0 && vector->data.len == 0)
		json_object_object_add(testresult, "pt",
				       json_object_new_string(""));

	/* We have written data, generic parser should not write it. */
	ret = FLAG_RES_DATA_WRITTEN;

out:
	return ret;
}

static int ccm_encrypt_helper(const struct json_array *processdata,
			      flags_t parsed_flags,
			      struct json_object *testvector,
			      struct json_object *testresults,
			      int (*callback)(struct aead_data *vector,
					      flags_t parsed_flags),
			      struct aead_data *vector)
{
	BUFFER_INIT(tmpbuf);
	uint32_t taglen = vector->taglen / 8;
	int ret;

	(void)processdata;
	(void)testvector;
	(void)testresults;

	CKINT(callback(vector, parsed_flags));

	/* Concatenate ciphertext and tag into one string */
	CKINT(alloc_buf(vector->data.len + taglen, &tmpbuf));
	memcpy(tmpbuf.buf, vector->data.buf, vector->data.len);
	memcpy(tmpbuf.buf + vector->data.len, vector->tag.buf, vector->tag.len);
	free_buf(&vector->data);

	/* Free the tag buffer to prevent the parser from writing it to JSON. */
	free_buf(&vector->tag);

	/* The concatenation of ciphertext and tag is now the new data buffer */
	copy_ptr_buf(&vector->data, &tmpbuf);

	/* Release the IV to not print it */
	free_buf(&vector->iv);

out:
	return ret;
}

static int ccm_tester(struct json_object *in, struct json_object *out,
		       uint64_t cipher)
{
	struct aead_data vector;

	if (!aead_backend) {
		logger(LOGGER_WARN, "No AEAD backend set\n");
		return -EOPNOTSUPP;
	}

	/* Referencing the GCM backend functions */
	const struct aead_callback ccm_encrypt = { aead_backend->ccm_encrypt, &vector, ccm_encrypt_helper};
	const struct aead_callback ccm_decrypt = { aead_backend->ccm_decrypt, &vector, ccm_decrypt_helper};
	const struct json_callback ccm_callback[] = {
		{ .callback.aead = ccm_encrypt, CB_TYPE_aead, FLAG_OP_ENC | FLAG_OP_AFT },
		{ .callback.aead = ccm_decrypt, CB_TYPE_aead, FLAG_OP_DEC | FLAG_OP_AFT },
	};
	const struct json_callbacks ccm_callbacks = SET_CALLBACKS(ccm_callback);

	memset(&vector, 0, sizeof(struct aead_data));
	vector.cipher = cipher;

	return aead_tester(in, out, &vector, &ccm_callbacks);
}

static struct cavs_tester gcm =
{
	ACVP_GCM,
	0,
	gcm_tester,	/* process_req */
	NULL
};

static struct cavs_tester gcm_siv =
{
	ACVP_GCMSIV,
	0,
	gcm_tester,	/* process_req */
	NULL
};

static struct cavs_tester gcm_gmac =
{
	ACVP_GMAC,
	0,
	gcm_tester,	/* process_req */
	NULL
};

static struct cavs_tester ccm =
{
	ACVP_CCM,
	0,
	ccm_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_aead)
static void register_aead(void)
{
	register_tester(&gcm, "GCM");
	register_tester(&gcm_siv, "GCM-SIV");
	register_tester(&gcm_gmac, "GCM-GMAC");
	register_tester(&ccm, "CCM");
}

void register_aead_impl(struct aead_backend *implementation)
{
	register_backend(aead_backend, implementation, "AEAD ciphers");
}
