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

#include <string.h>

#include "logger.h"
#include "parser_common.h"
#include "stringhelper.h"

#define HKDF_DEF_CALLBACK_HELPER(name, flags, helper)			       \
				 DEF_CALLBACK_HELPER(hkdf, name, flags, helper)

static struct hkdf_backend *hkdf_backend = NULL;

static int hkdf_helper(const struct json_array *processdata,
		       flags_t parsed_flags,
		       struct json_object *testvector,
		       struct json_object *testresults,
	int (*callback)(struct hkdf_data *vector, flags_t parsed_flags),
			struct hkdf_data *vector)
{
	static const uint8_t literal[] = { 0x01, 0x23, 0x45, 0x67,
					   0x89, 0xab, 0xcd, 0xef };
	int ret = 0;

	(void)testvector;
	(void)processdata;
	(void)testresults;

	/*
	 * Create fixed info field
	 *
	 * TODO: this assumes
	 * "uPartyInfo||vPartyInfo||literal[0123456789abcdef]"
	 */
	CKINT(alloc_buf(vector->fi_partyU.len + vector->fi_partyU_ephem.len +
			vector->fi_partyV.len + vector->fi_partyV_ephem.len +
			sizeof(literal),
			&vector->info));

	/* Concatenate data */
	memcpy(vector->info.buf, vector->fi_partyU.buf, vector->fi_partyU.len);
	if (vector->fi_partyU_ephem.len)
		memcpy(vector->info.buf + vector->fi_partyU.len,
		       vector->fi_partyU_ephem.buf,
		       vector->fi_partyU_ephem.len);
	memcpy(vector->info.buf +
	       vector->fi_partyU.len + vector->fi_partyU_ephem.len,
	       vector->fi_partyV.buf, vector->fi_partyV.len);
	if (vector->fi_partyV_ephem.len)
		memcpy(vector->info.buf + vector->fi_partyU.len +
		       vector->fi_partyU_ephem.len + vector->fi_partyV.len,
		       vector->fi_partyV_ephem.buf,
		       vector->fi_partyV_ephem.len);

	memcpy(vector->info.buf + vector->fi_partyU.len +
	       vector->fi_partyU_ephem.len + vector->fi_partyV.len +
	       vector->fi_partyV_ephem.len,
	       literal, sizeof(literal));

	logger_binary(LOGGER_DEBUG, vector->info.buf, vector->info.len, "info");

	CKINT(callback(vector, parsed_flags));

out:
	free_buf(&vector->info);
	return ret;
}

/* parser for home-grown data HKDF test data */
static int hkdf_tester(struct json_object *in, struct json_object *out,
		       uint64_t cipher)
{
	(void)cipher;

	if (!hkdf_backend) {
		logger(LOGGER_WARN, "No SP800-108 KDF backend set\n");
		return -EOPNOTSUPP;
	}

	HKDF_DEF_CALLBACK_HELPER(hkdf, FLAG_OP_AFT | FLAG_OP_VAL, hkdf_helper);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry hkdf_testresult_entries[] = {
		{"dkm",		{.data.buf = &hkdf_vector.dkm,			WRITER_BIN},	FLAG_OP_AFT},
		{"testPassed",	{.data.integer = &hkdf_vector.validity_success,	WRITER_BOOL},	FLAG_OP_VAL},
	};
	const struct json_testresult hkdf_testresult = SET_ARRAY(hkdf_testresult_entries, &hkdf_callbacks);

	/* fixed info party V */
	const struct json_entry hkdf_fi_partyV_entries[] = {
		{"partyId",		{.data.buf = &hkdf_vector.fi_partyV,		PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_VAL },
		{"ephemeralData",	{.data.buf = &hkdf_vector.fi_partyV_ephem,	PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OPTIONAL},
	};
	const struct json_array hkdf_fi_partyV_test =
		SET_ARRAY(hkdf_fi_partyV_entries, NULL);

	/* fixed info party U */
	const struct json_entry hkdf_fi_partyU_entries[] = {
		{"partyId",		{.data.buf = &hkdf_vector.fi_partyU,		PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_VAL},
		{"ephemeralData",	{.data.buf = &hkdf_vector.fi_partyU_ephem,	PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OPTIONAL},
	};
	const struct json_array hkdf_fi_partyU_test =
		SET_ARRAY(hkdf_fi_partyU_entries, NULL);

	/* kdfParameter */
	const struct json_entry hkdf_kdf_entries[] = {
		{"salt",		{.data.buf = &hkdf_vector.salt,			PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_VAL},
		{"z",			{.data.buf = &hkdf_vector.z,			PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_VAL},
		//TODO: what to do with l? "secondary shared secret t. For [SP800-56Cr2] only."
	};
	const struct json_array hkdf_kdf_test =
		SET_ARRAY(hkdf_kdf_entries, NULL);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file.
	 */
	const struct json_entry hkdf_test_entries[] = {
		{"kdfParameter",	{.data.array = &hkdf_kdf_test, PARSER_OBJECT}, FLAG_OP_AFT | FLAG_OP_VAL},
		{"fixedInfoPartyU",	{.data.array = &hkdf_fi_partyU_test, PARSER_OBJECT}, FLAG_OP_AFT | FLAG_OP_VAL},
		{"fixedInfoPartyV",	{.data.array = &hkdf_fi_partyV_test, PARSER_OBJECT}, FLAG_OP_AFT | FLAG_OP_VAL},
		{"dkm",			{.data.buf = &hkdf_vector.dkm,	PARSER_BIN}, FLAG_OP_VAL},
	};
	const struct json_array hkdf_test =
		SET_ARRAY(hkdf_test_entries, &hkdf_testresult);

	/* kdfConfiguration */
	const struct json_entry hkdf_kdf_config_entries[] = {
		{"l",			{.data.integer = &hkdf_vector.dkmlen,		PARSER_UINT}, FLAG_OP_AFT | FLAG_OP_VAL},
		{"fixedInfoPattern",	{.data.buf = &hkdf_vector.fixed_info_pattern,	PARSER_STRING},	FLAG_OP_AFT | FLAG_OP_VAL},
		{"hmacAlg",		{.data.largeint = &hkdf_vector.hash,		PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_VAL},
	};
	const struct json_array hkdf_kdf_config_test =
		SET_ARRAY(hkdf_kdf_config_entries, NULL);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors.
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry hkdf_testgroup_entries[] = {
		{"kdfConfiguration",	{.data.array = &hkdf_kdf_config_test, PARSER_OBJECT}, FLAG_OP_AFT | FLAG_OP_VAL},
		{"tests",	{.data.array = &hkdf_test, PARSER_ARRAY}, FLAG_OP_AFT | FLAG_OP_VAL},
	};
	const struct json_array hkdf_testgroup = SET_ARRAY(hkdf_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry hkdf_testanchor_entries[] = {
		{"testGroups",	{.data.array = &hkdf_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array hkdf_testanchor = SET_ARRAY(hkdf_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&hkdf_testanchor, "1.0", in, out);
}

static struct cavs_tester hkdf =
{
	ACVP_HKDF,
	0,
	hkdf_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_hkdf)
static void register_hkdf(void)
{
	register_tester(&hkdf, "HKDF");
}

void register_hkdf_impl(struct hkdf_backend *implementation)
{
	register_backend(hkdf_backend, implementation, "HKDF");
}
