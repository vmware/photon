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

#include "stringhelper.h"
#include "logger.h"
#include "read_json.h"

#include "parser_common.h"

#define DH_DEF_CALLBACK(name, flags)	DEF_CALLBACK(dh, name, flags)
#define DH_DEF_CALLBACK_HELPER(name, flags, helper)			       \
				DEF_CALLBACK_HELPER(dh, name, flags, helper)

static struct dh_backend *dh_backend = NULL;

static int dh_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	(void)cipher;

	if (!dh_backend) {
		logger(LOGGER_WARN, "No DH backend set\n");
		return -EOPNOTSUPP;
	}

	/**********************************************************************
	 * DH shared secret verification
	 **********************************************************************/
	DH_DEF_CALLBACK(dh_ss_ver, FLAG_OP_VAL | FLAG_OP_MASK_DH | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER);

	/*
	 * Ephemeral
	 * TODO: No KDF/KC support
	 */
	const struct json_entry dh_e_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dh_ss_ver_vector.validity_success, WRITER_BOOL},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_e_ver_testresult =
		SET_ARRAY(dh_e_ver_testresult_entries, &dh_ss_ver_callbacks);

	const struct json_entry dh_e_ver_test_entries[] = {
		{"ephemeralPublicServer",	{.data.buf = &dh_ss_ver_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicIut",		{.data.buf = &dh_ss_ver_vector.Yloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPrivateIut",		{.data.buf = &dh_ss_ver_vector.Xloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",			{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_e_ver_test =
			SET_ARRAY(dh_e_ver_test_entries, &dh_e_ver_testresult);

	/*
	 * Static
	 * TODO: No KDF/KC support
	 */
	const struct json_entry dh_s_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dh_ss_ver_vector.validity_success, WRITER_BOOL},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_s_ver_testresult =
		SET_ARRAY(dh_s_ver_testresult_entries, &dh_ss_ver_callbacks);

	const struct json_entry dh_s_ver_test_entries[] = {
		{"staticPublicServer",		{.data.buf = &dh_ss_ver_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIut",		{.data.buf = &dh_ss_ver_vector.Yloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",		{.data.buf = &dh_ss_ver_vector.Xloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",			{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_s_ver_test =
			SET_ARRAY(dh_s_ver_test_entries, &dh_s_ver_testresult);

	/*
	 * One Flow Initiator
	 * TODO: No KDF/KC support
	 */
	const struct json_entry dh_of_i_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dh_ss_ver_vector.validity_success, WRITER_BOOL},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult dh_of_i_ver_testresult =
		SET_ARRAY(dh_of_i_ver_testresult_entries, &dh_ss_ver_callbacks);

	const struct json_entry dh_of_i_ver_test_entries[] = {
		{"staticPublicServer",		{.data.buf = &dh_ss_ver_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"ephemeralPublicIut",		{.data.buf = &dh_ss_ver_vector.Yloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"ephemeralPrivateIut",		{.data.buf = &dh_ss_ver_vector.Xloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"hashZIut",			{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_array dh_of_i_ver_test =
			SET_ARRAY(dh_of_i_ver_test_entries, &dh_of_i_ver_testresult);

	/*
	 * One Flow Responder
	 * TODO: No KDF/KC support
	 */
	const struct json_entry dh_of_r_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dh_ss_ver_vector.validity_success, WRITER_BOOL},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_of_r_ver_testresult =
		SET_ARRAY(dh_of_r_ver_testresult_entries, &dh_ss_ver_callbacks);

	const struct json_entry dh_of_r_ver_test_entries[] = {
		{"ephemeralPublicServer",	{.data.buf = &dh_ss_ver_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIut",		{.data.buf = &dh_ss_ver_vector.Yloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",		{.data.buf = &dh_ss_ver_vector.Xloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",			{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_of_r_ver_test =
			SET_ARRAY(dh_of_r_ver_test_entries, &dh_of_r_ver_testresult);

	/**********************************************************************
	 * DH shared secret generation
	 **********************************************************************/
	DH_DEF_CALLBACK(dh_ss, FLAG_OP_AFT | FLAG_OP_MASK_DH | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER);

	/*
	 * Ephemeral
	 * TODO: No KDF/KC support
	 */
	const struct json_entry dh_e_testresult_entries[] = {
		{"ephemeralPublicIut",	{.data.buf = &dh_ss_vector.Yloc, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER },
		{"hashZIut",		{.data.buf = &dh_ss_vector.hashzz, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_e_testresult =
			SET_ARRAY(dh_e_testresult_entries, &dh_ss_callbacks);

	const struct json_entry dh_e_test_entries[] = {
		{"ephemeralPublicServer",	{.data.buf = &dh_ss_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_e_test =
			SET_ARRAY(dh_e_test_entries, &dh_e_testresult);

	/*
	 * Static
	 * TODO: No KDF/KC support
	 */
	const struct json_entry dh_s_testresult_entries[] = {
		{"staticPublicIut",	{.data.buf = &dh_ss_vector.Yloc, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER },
		{"hashZIut",		{.data.buf = &dh_ss_vector.hashzz, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_s_testresult =
			SET_ARRAY(dh_s_testresult_entries, &dh_ss_callbacks);

	const struct json_entry dh_s_test_entries[] = {
		{"staticPublicServer",	{.data.buf = &dh_ss_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_s_test =
			SET_ARRAY(dh_s_test_entries, &dh_s_testresult);


	/*
	 * One Flow Initiator
	 * TODO: No KDF/KC support
	 */
	const struct json_entry dh_of_i_testresult_entries[] = {
		{"ephemeralPublicIut",	{.data.buf = &dh_ss_vector.Yloc, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"hashZIut",		{.data.buf = &dh_ss_vector.hashzz, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult dh_of_i_testresult =
			SET_ARRAY(dh_of_i_testresult_entries, &dh_ss_callbacks);

	const struct json_entry dh_of_i_test_entries[] = {
		{"staticPublicServer",		{.data.buf = &dh_ss_vector.Yrem, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_array dh_of_i_test =
			SET_ARRAY(dh_of_i_test_entries, &dh_of_i_testresult);

	/*
	 * One Flow Responder
	 * TODO: No KDF/KC support
	 */
	const struct json_entry dh_of_r_testresult_entries[] = {
		{"staticPublicIut",	{.data.buf = &dh_ss_vector.Yloc, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",		{.data.buf = &dh_ss_vector.hashzz, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_of_r_testresult =
			SET_ARRAY(dh_of_r_testresult_entries, &dh_ss_callbacks);

	const struct json_entry dh_of_r_test_entries[] = {
		{"ephemeralPublicServer",		{.data.buf = &dh_ss_vector.Yrem, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_of_r_test =
			SET_ARRAY(dh_of_r_test_entries, &dh_of_r_testresult);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test ss_vectors.
	 *
	 * As this definition does not mark specific individual test ss_vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry dh_testgroup_entries[] = {
		/* Common entries */
		{"hashAlg",	{.data.largeint = &dh_ss_vector.cipher, PARSER_CIPHER},		FLAG_OP_MASK_DH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"macType",	{.data.largeint = &dh_ss_vector.cipher, PARSER_CIPHER},		FLAG_OPTIONAL | FLAG_OP_MASK_DH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"p",		{.data.buf = &dh_ss_vector.P, PARSER_BIN},			FLAG_OP_MASK_DH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"q",		{.data.buf = &dh_ss_vector.Q, PARSER_BIN},			FLAG_OP_MASK_DH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"g",		{.data.buf = &dh_ss_vector.G, PARSER_BIN},			FLAG_OP_MASK_DH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"hashAlg",	{.data.largeint = &dh_ss_ver_vector.cipher, PARSER_CIPHER},	FLAG_OP_MASK_DH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"macType",	{.data.largeint = &dh_ss_ver_vector.cipher, PARSER_CIPHER},	FLAG_OPTIONAL | FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_MASK_DH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"p",		{.data.buf = &dh_ss_ver_vector.P, PARSER_BIN},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_MASK_DH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"q",		{.data.buf = &dh_ss_ver_vector.Q, PARSER_BIN},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_MASK_DH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"g",		{.data.buf = &dh_ss_ver_vector.G, PARSER_BIN},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_MASK_DH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &dh_e_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &dh_e_ver_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &dh_s_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &dh_s_ver_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &dh_of_i_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"tests",	{.data.array = &dh_of_r_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &dh_of_i_ver_test, PARSER_ARRAY},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR },
		{"tests",	{.data.array = &dh_of_r_ver_test, PARSER_ARRAY},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER },
	};
	const struct json_array dh_testgroup = SET_ARRAY(dh_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry dh_testanchor_entries[] = {
		{"testGroups",	{.data.array = &dh_testgroup, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST}
	};
	const struct json_array dh_testanchor = SET_ARRAY(dh_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&dh_testanchor, "1.0", in, out);
}

static struct cavs_tester dh =
{
	ACVP_DH,
	0,
	dh_tester,	/* process_req */
	NULL
};

static int kas_ffc_r3_ssc_helper(const struct json_array *processdata,
				 flags_t parsed_flags,
				 struct json_object *testvector,
				 struct json_object *testresults,
	int (*callback)(struct dh_ss_data *vector, flags_t parsed_flags),
			struct dh_ss_data *vector)
{
	struct json_object *testresult = NULL;
	const struct json_entry *entry;
	unsigned int i;
	int ret;

	(void)processdata;
	(void)testresults;

	CKINT(callback(vector, parsed_flags));

	testresult = json_object_new_object();
	CKNULL(testresult, -ENOMEM);
	/* Append the output JSON stream with test results. */
	json_object_array_add(testresults, testresult);

	CKINT(json_add_test_data(testvector, testresult));

	/* Iterate over each write definition and invoke it. */
	for_each_testresult(processdata->testresult, entry, i)
		CKINT(write_one_entry(entry, testresult, parsed_flags));

	/* Add shared secret result */
	CKINT(json_add_bin2hex(testresult, vector->cipher ? "hashZ" : "z",
			       &vector->hashzz));
	free_buf(&vector->hashzz);

	ret = FLAG_RES_DATA_WRITTEN;

out:
	return ret;
}

static int kas_ffc_r3_ssc_tester(struct json_object *in,
				 struct json_object *out,
				 uint64_t cipher)
{
	(void)cipher;

	if (!dh_backend) {
		logger(LOGGER_WARN, "No DH backend set\n");
		return -EOPNOTSUPP;
	}

	/**********************************************************************
	 * DH key generation
	 **********************************************************************/
	DH_DEF_CALLBACK(dh_keygen, FLAG_OP_AFT | FLAG_OP_MASK_DH | FLAG_OP_ASYM_TYPE_KEYGEN);

	const struct json_entry dh_keygen_testresult_entries[] = {
		{"x",		{.data.buf = &dh_keygen_vector.X, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN},
		{"y",		{.data.buf = &dh_keygen_vector.Y, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN},
	};
	const struct json_testresult dh_keygen_testresult =
	SET_ARRAY(dh_keygen_testresult_entries, &dh_keygen_callbacks);

	const struct json_array dh_keygen_test =
					{ NULL, 0, &dh_keygen_testresult};

	const struct json_entry dh_keygen_testgroup_entries[] = {
		{"safePrimeGroup",	{.data.largeint = &dh_keygen_vector.safeprime, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OPTIONAL},

		{"tests",	{.data.array = &dh_keygen_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN},
	};

	const struct json_array dh_keygen_testgroup = SET_ARRAY(dh_keygen_testgroup_entries, NULL);

	/**********************************************************************
	 * DH key verification
	 **********************************************************************/
	DH_DEF_CALLBACK(dh_keyver, FLAG_OP_AFT | FLAG_OP_MASK_DH | FLAG_OP_ASYM_TYPE_KEYVER);

	const struct json_entry dh_keyver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dh_keyver_vector.keyver_success, WRITER_BOOL},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
	};
	const struct json_testresult dh_keyver_testresult =
	SET_ARRAY(dh_keyver_testresult_entries, &dh_keyver_callbacks);

	const struct json_entry dh_keyver_test_entries[] = {
		{"x",		{.data.buf = &dh_keyver_vector.X, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
		{"y",		{.data.buf = &dh_keyver_vector.Y, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
	};

	/* search for empty arrays */
	const struct json_array dh_keyver_test = SET_ARRAY(dh_keyver_test_entries, &dh_keyver_testresult);

	const struct json_entry dh_keyver_testgroup_entries[] = {
		/* safeprime cipher is provided */
		{"safePrimeGroup",	{.data.largeint = &dh_keyver_vector.safeprime, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER },

		{"tests",	{.data.array = &dh_keyver_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
	};

	const struct json_array dh_keyver_testgroup = SET_ARRAY(dh_keyver_testgroup_entries, NULL);


	/**********************************************************************
	 * DH shared secret verification
	 **********************************************************************/
	DH_DEF_CALLBACK(dh_ss_ver, FLAG_OP_VAL | FLAG_OP_MASK_DH | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER);

	/*
	 * Ephemeral
	 */
	const struct json_entry dh_e_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dh_ss_ver_vector.validity_success, WRITER_BOOL},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_e_ver_testresult =
		SET_ARRAY(dh_e_ver_testresult_entries, &dh_ss_ver_callbacks);

	const struct json_entry dh_e_ver_test_entries[] = {
		{"ephemeralPublicServer",	{.data.buf = &dh_ss_ver_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicIut",		{.data.buf = &dh_ss_ver_vector.Yloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPrivateIut",		{.data.buf = &dh_ss_ver_vector.Xloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZ",			{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"z",				{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_e_ver_test =
			SET_ARRAY(dh_e_ver_test_entries, &dh_e_ver_testresult);

	/*
	 * Static
	 */
	const struct json_entry dh_s_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dh_ss_ver_vector.validity_success, WRITER_BOOL},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_s_ver_testresult =
		SET_ARRAY(dh_s_ver_testresult_entries, &dh_ss_ver_callbacks);

	const struct json_entry dh_s_ver_test_entries[] = {
		{"staticPublicServer",		{.data.buf = &dh_ss_ver_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIut",		{.data.buf = &dh_ss_ver_vector.Yloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",		{.data.buf = &dh_ss_ver_vector.Xloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZ",			{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"z",				{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_s_ver_test =
			SET_ARRAY(dh_s_ver_test_entries, &dh_s_ver_testresult);

	/*
	 * One Flow Initiator
	 */
	const struct json_entry dh_of_i_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dh_ss_ver_vector.validity_success, WRITER_BOOL},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult dh_of_i_ver_testresult =
		SET_ARRAY(dh_of_i_ver_testresult_entries, &dh_ss_ver_callbacks);

	const struct json_entry dh_of_i_ver_test_entries[] = {
		{"staticPublicServer",		{.data.buf = &dh_ss_ver_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"ephemeralPublicIut",		{.data.buf = &dh_ss_ver_vector.Yloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"ephemeralPrivateIut",		{.data.buf = &dh_ss_ver_vector.Xloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"hashZ",			{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"z",				{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_array dh_of_i_ver_test =
			SET_ARRAY(dh_of_i_ver_test_entries, &dh_of_i_ver_testresult);

	/*
	 * One Flow Responder
	 */
	const struct json_entry dh_of_r_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dh_ss_ver_vector.validity_success, WRITER_BOOL},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_of_r_ver_testresult =
		SET_ARRAY(dh_of_r_ver_testresult_entries, &dh_ss_ver_callbacks);

	const struct json_entry dh_of_r_ver_test_entries[] = {
		{"ephemeralPublicServer",	{.data.buf = &dh_ss_ver_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIut",		{.data.buf = &dh_ss_ver_vector.Yloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",		{.data.buf = &dh_ss_ver_vector.Xloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZ",			{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"z",				{.data.buf = &dh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_of_r_ver_test =
			SET_ARRAY(dh_of_r_ver_test_entries, &dh_of_r_ver_testresult);

	/**********************************************************************
	 * DH shared secret generation
	 **********************************************************************/
	DH_DEF_CALLBACK_HELPER(dh_ss, FLAG_OP_AFT | FLAG_OP_MASK_DH | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER,
				kas_ffc_r3_ssc_helper);

	/*
	 * Ephemeral
	 */
	const struct json_entry dh_e_testresult_entries[] = {
		{"ephemeralPublicIut",	{.data.buf = &dh_ss_vector.Yloc, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER },
	};
	const struct json_testresult dh_e_testresult =
			SET_ARRAY(dh_e_testresult_entries, &dh_ss_callbacks);

	const struct json_entry dh_e_test_entries[] = {
		{"ephemeralPublicServer",	{.data.buf = &dh_ss_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_e_test =
			SET_ARRAY(dh_e_test_entries, &dh_e_testresult);

	/*
	 * Static
	 */
	const struct json_entry dh_s_testresult_entries[] = {
		{"staticPublicIut",	{.data.buf = &dh_ss_vector.Yloc, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER },
	};
	const struct json_testresult dh_s_testresult =
			SET_ARRAY(dh_s_testresult_entries, &dh_ss_callbacks);

	const struct json_entry dh_s_test_entries[] = {
		{"staticPublicServer",	{.data.buf = &dh_ss_vector.Yrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_s_test =
			SET_ARRAY(dh_s_test_entries, &dh_s_testresult);


	/*
	 * One Flow Initiator
	 */
	const struct json_entry dh_of_i_testresult_entries[] = {
		{"ephemeralPublicIut",	{.data.buf = &dh_ss_vector.Yloc, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult dh_of_i_testresult =
			SET_ARRAY(dh_of_i_testresult_entries, &dh_ss_callbacks);

	const struct json_entry dh_of_i_test_entries[] = {
		{"staticPublicServer",		{.data.buf = &dh_ss_vector.Yrem, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_array dh_of_i_test =
			SET_ARRAY(dh_of_i_test_entries, &dh_of_i_testresult);

	/*
	 * One Flow Responder
	 */
	const struct json_entry dh_of_r_testresult_entries[] = {
		{"staticPublicIut",	{.data.buf = &dh_ss_vector.Yloc, WRITER_BIN},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult dh_of_r_testresult =
			SET_ARRAY(dh_of_r_testresult_entries, &dh_ss_callbacks);

	const struct json_entry dh_of_r_test_entries[] = {
		{"ephemeralPublicServer",		{.data.buf = &dh_ss_vector.Yrem, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array dh_of_r_test =
			SET_ARRAY(dh_of_r_test_entries, &dh_of_r_testresult);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test ss_vectors.
	 *
	 * As this definition does not mark specific individual test ss_vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry dh_testgroup_entries[] = {
		/* Common entries */
		{"hashFunctionZ",	{.data.largeint = &dh_ss_vector.cipher, PARSER_CIPHER},		FLAG_OPTIONAL | FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"domainParameterGenerationMode",	{.data.largeint = &dh_ss_vector.safeprime, PARSER_CIPHER},	 FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"p",	{.data.buf = &dh_ss_vector.P, PARSER_BIN},	 FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},
		{"q",	{.data.buf = &dh_ss_vector.Q, PARSER_BIN},	 FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},
		{"g",	{.data.buf = &dh_ss_vector.G, PARSER_BIN},	 FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},

		{"hashFunctionZ",	{.data.largeint = &dh_ss_ver_vector.cipher, PARSER_CIPHER},		FLAG_OPTIONAL | FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"domainParameterGenerationMode",	{.data.largeint = &dh_ss_ver_vector.safeprime, PARSER_CIPHER},	 FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"p",	{.data.buf = &dh_ss_ver_vector.P, PARSER_BIN},	 FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},
		{"q",	{.data.buf = &dh_ss_ver_vector.Q, PARSER_BIN},	 FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},
		{"g",	{.data.buf = &dh_ss_ver_vector.G, PARSER_BIN},	 FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},

		{"tests",	{.data.array = &dh_e_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &dh_e_ver_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_EPHEMERAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &dh_s_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &dh_s_ver_test, PARSER_ARRAY},			FLAG_OP_VAL | FLAG_OP_DH_SCHEME_STATIC | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &dh_of_i_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR},
		{"tests",	{.data.array = &dh_of_r_test, PARSER_ARRAY},			FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &dh_of_i_ver_test, PARSER_ARRAY},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_INITIATOR },
		{"tests",	{.data.array = &dh_of_r_ver_test, PARSER_ARRAY},		FLAG_OP_KAS_SCHEME_TEST |FLAG_OP_VAL | FLAG_OP_DH_SCHEME_ONE_FLOW | FLAG_OP_KAS_ROLE_RESPONDER },
	};
	const struct json_array dh_testgroup = SET_ARRAY(dh_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry dh_testanchor_entries[] = {
		{"testGroups",	{.data.array = &dh_testgroup, PARSER_ARRAY},	0},
		{"testGroups",	{.data.array = &dh_keygen_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_KEYGEN},
		{"testGroups",	{.data.array = &dh_keyver_testgroup, PARSER_ARRAY}, FLAG_OP_ASYM_TYPE_KEYVER}
	};
	const struct json_array dh_testanchor = SET_ARRAY(dh_testanchor_entries, NULL);

	/* Process all. */

	return process_json(&dh_testanchor, "1.0", in, out);
}

static struct cavs_tester kas_ffc_r3_ssc =
{
	ACVP_KAS_FFC_R3_SSC,
	0,
	kas_ffc_r3_ssc_tester,	/* process_req */
	NULL
};

static struct cavs_tester safeprimes =
{
	ACVP_SAFEPRIMES,
	0,
	kas_ffc_r3_ssc_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_dh)
static void register_dh(void)
{
	register_tester(&dh, "DH");
	register_tester(&kas_ffc_r3_ssc, "KAS FFC R3 SSC");
	register_tester(&safeprimes, "Safe Primes");
}

void register_dh_impl(struct dh_backend *implementation)
{
	register_backend(dh_backend, implementation, "DH");
}
