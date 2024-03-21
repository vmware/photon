/*
 * Copyright (C) 2020 - 2022, Stephan Mueller <smueller@chronox.de>
 *
 * License: see LICENSE file in root directory
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
#include "parser_hmac.h"

#define KTS_IFC_DEF_CALLBACK(name, flags)				\
			DEF_CALLBACK(kts_ifc, name, flags)
#define KTS_IFC_DEF_CALLBACK_HELPER(name, flags, helper)		\
			DEF_CALLBACK_HELPER(kts_ifc, name, flags, helper)

static struct kts_ifc_backend *kts_ifc_backend = NULL;


static int kas_ifc_tester(struct json_object *in, struct json_object *out,
			  uint64_t cipher)
{
	(void)cipher;

	if (!kts_ifc_backend) {
		logger(LOGGER_WARN, "No KTS IFC backend set\n");
		return -EOPNOTSUPP;
	}

	KTS_IFC_DEF_CALLBACK(kts_ifc, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER);

	/*******************************************************************
	 * KTS IFC Responder validation test
	 *******************************************************************/
	const struct json_entry kts_ifc_resp_val_testresult_entries[] = {
		{"testPassed",	{.data.integer = &kts_ifc_vector.u.kts_ifc_resp_validation.validation_success, WRITER_BOOL},
			         FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult kts_ifc_resp_val_testresult = SET_ARRAY(kts_ifc_resp_val_testresult_entries, &kts_ifc_callbacks);

	const struct json_entry kts_ifc_resp_val_test_entries[] = {
		{"iutN",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.n, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutE",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.e, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutP",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.p, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutQ",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.q, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutD",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.d, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"serverC",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.c, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"z",		{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.dkm, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},
		{"hashZ",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.dkm_hash, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},
	};
	const struct json_array kts_ifc_resp_val_tests = SET_ARRAY(kts_ifc_resp_val_test_entries, &kts_ifc_resp_val_testresult);

	/*******************************************************************
	 * KTS IFC Initiator validation test
	 *******************************************************************/
	const struct json_entry kts_ifc_init_val_testresult_entries[] = {
		{"testPassed",	{.data.integer = &kts_ifc_vector.u.kts_ifc_init_validation.validation_success, WRITER_BOOL},
			         FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult kts_ifc_init_val_testresult = SET_ARRAY(kts_ifc_init_val_testresult_entries, &kts_ifc_callbacks);

	const struct json_entry kts_ifc_init_val_test_entries[] = {
		{"serverN",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.n, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
		{"serverE",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.e, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
		{"iutC",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.c, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
		{"serverP",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.p, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OPTIONAL},
		{"serverQ",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.q, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OPTIONAL},
		{"z",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.dkm, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_array kts_ifc_init_val_tests = SET_ARRAY(kts_ifc_init_val_test_entries, &kts_ifc_init_val_testresult);

	/*******************************************************************
	 * KTS IFC Responder test
	 *******************************************************************/
	const struct json_entry kts_ifc_resp_testresult_entries[] = {
		{"z",		{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.dkm, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult kts_ifc_resp_testresult = SET_ARRAY(kts_ifc_resp_testresult_entries, &kts_ifc_callbacks);

	const struct json_entry kts_ifc_resp_test_entries[] = {
		{"iutN",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.n, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutE",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.e, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutP",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.p, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutQ",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.q, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutD",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.d, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"serverC",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.c, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array kts_ifc_resp_tests = SET_ARRAY(kts_ifc_resp_test_entries, &kts_ifc_resp_testresult);

	/*******************************************************************
	 * KTS IFC Initiator test
	 *******************************************************************/
	const struct json_entry kts_ifc_init_testresult_entries[] = {
		{"iutC",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init.iut_c, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
		{"z",		{.data.buf = &kts_ifc_vector.u.kts_ifc_init.dkm, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult kts_ifc_init_testresult = SET_ARRAY(kts_ifc_init_testresult_entries, &kts_ifc_callbacks);

	const struct json_entry kts_ifc_init_test_entries[] = {
		{"serverN",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init.n, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
		{"serverE",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init.e, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_array kts_ifc_init_tests = SET_ARRAY(kts_ifc_init_test_entries, &kts_ifc_init_testresult);

	const struct json_entry kts_ifc_testgroup_entries[] = {
		{"scheme",		{.data.largeint = &kts_ifc_vector.schema, PARSER_CIPHER}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"keyGenerationMethod",	{.data.largeint = &kts_ifc_vector.key_generation_method, PARSER_CIPHER}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"modulo",		{.data.integer = &kts_ifc_vector.modulus, PARSER_UINT}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		/* Generation tests */
		{"tests",	{.data.array = &kts_ifc_init_tests, PARSER_ARRAY},
				FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
		{"tests",	{.data.array = &kts_ifc_resp_tests, PARSER_ARRAY},
				FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},

		/* Validation tests */
		{"tests",	{.data.array = &kts_ifc_init_val_tests, PARSER_ARRAY},
				FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
		{"tests",	{.data.array = &kts_ifc_resp_val_tests, PARSER_ARRAY},
				FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array kts_ifc_testgroup = SET_ARRAY(kts_ifc_testgroup_entries, NULL);

	const struct json_entry kts_ifc_testanchor_entries[] = {
		{"testGroups",	{.data.array = &kts_ifc_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array kts_ifc_testanchor = SET_ARRAY(kts_ifc_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&kts_ifc_testanchor, "1.0", in, out);
}

static int kts_ifc_tester(struct json_object *in, struct json_object *out,
			  uint64_t cipher)
{
	(void)cipher;

	if (!kts_ifc_backend) {
		logger(LOGGER_WARN, "No KTS IFC backend set\n");
		return -EOPNOTSUPP;
	}

	KTS_IFC_DEF_CALLBACK(kts_ifc, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER);

	/*******************************************************************
	 * KTS IFC Responder validation test
	 *******************************************************************/
	const struct json_entry kts_ifc_resp_val_testresult_entries[] = {
		{"testPassed",	{.data.integer = &kts_ifc_vector.u.kts_ifc_resp_validation.validation_success, WRITER_BOOL},
			         FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult kts_ifc_resp_val_testresult = SET_ARRAY(kts_ifc_resp_val_testresult_entries, &kts_ifc_callbacks);

	const struct json_entry kts_ifc_resp_val_test_entries[] = {
		{"iutN",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.n, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutE",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.e, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutP",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.p, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutQ",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.q, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutD",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.d, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"serverC",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.c, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
		{"dkm",		{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.dkm, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},
		{"z",		{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.dkm, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},
		{"hashZ",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp_validation.dkm_hash, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},
	};
	const struct json_array kts_ifc_resp_val_tests = SET_ARRAY(kts_ifc_resp_val_test_entries, &kts_ifc_resp_val_testresult);

	/*******************************************************************
	 * KTS IFC Initiator validation test
	 *******************************************************************/
	const struct json_entry kts_ifc_init_val_testresult_entries[] = {
		{"testPassed",	{.data.integer = &kts_ifc_vector.u.kts_ifc_init_validation.validation_success, WRITER_BOOL},
			         FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult kts_ifc_init_val_testresult = SET_ARRAY(kts_ifc_init_val_testresult_entries, &kts_ifc_callbacks);

	const struct json_entry kts_ifc_init_val_test_entries[] = {
		{"serverN",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.n, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
		{"serverE",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.e, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
		{"serverP",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.p, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OPTIONAL},
		{"serverQ",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.q, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OPTIONAL},
		{"dkm",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init_validation.dkm, PARSER_BIN},	FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_array kts_ifc_init_val_tests = SET_ARRAY(kts_ifc_init_val_test_entries, &kts_ifc_init_val_testresult);

	/*******************************************************************
	 * KTS IFC Responder test
	 *******************************************************************/
	const struct json_entry kts_ifc_resp_testresult_entries[] = {
		{"dkm",		{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.dkm, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tag",		{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.tag, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult kts_ifc_resp_testresult = SET_ARRAY(kts_ifc_resp_testresult_entries, &kts_ifc_callbacks);

	const struct json_entry kts_ifc_resp_test_entries[] = {
		{"iutN",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.n, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutE",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.e, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutP",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.p, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutQ",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.q, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutD",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.d, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
		{"serverC",	{.data.buf = &kts_ifc_vector.u.kts_ifc_resp.c, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array kts_ifc_resp_tests = SET_ARRAY(kts_ifc_resp_test_entries, &kts_ifc_resp_testresult);

	/*******************************************************************
	 * KTS IFC Initiator test
	 *******************************************************************/
	const struct json_entry kts_ifc_init_testresult_entries[] = {
		{"iutC",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init.iut_c, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
		{"dkm",		{.data.buf = &kts_ifc_vector.u.kts_ifc_init.dkm, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
		{"tag",		{.data.buf = &kts_ifc_vector.u.kts_ifc_init.tag, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult kts_ifc_init_testresult = SET_ARRAY(kts_ifc_init_testresult_entries, &kts_ifc_callbacks);

	const struct json_entry kts_ifc_init_test_entries[] = {
		{"serverN",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init.n, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
		{"serverE",	{.data.buf = &kts_ifc_vector.u.kts_ifc_init.e, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_array kts_ifc_init_tests = SET_ARRAY(kts_ifc_init_test_entries, &kts_ifc_init_testresult);

	/*******************************************************************
	 * KTS IFC Common
	 *******************************************************************/
	const struct json_entry kts_configuration_entries[] = {
		{"hashAlg",			{.data.largeint = &kts_ifc_vector.kts_hash, PARSER_CIPHER}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"associatedDataPattern",	{.data.buf = &kts_ifc_vector.kts_assoc_data_pattern, PARSER_STRING}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"encoding",			{.data.largeint = &kts_ifc_vector.kts_encoding, PARSER_CIPHER}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array kts_configuration = SET_ARRAY(kts_configuration_entries, NULL);

	const struct json_entry kts_mac_configuration_entries[] = {
		{"macType",			{.data.largeint = &kts_ifc_vector.mac, PARSER_CIPHER}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"keyLen",			{.data.integer = &kts_ifc_vector.mac_keylen, PARSER_UINT}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"macLen",			{.data.integer = &kts_ifc_vector.mac_maclen, PARSER_UINT}, FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array kts_mac_configuration = SET_ARRAY(kts_mac_configuration_entries, NULL);

	const struct json_entry kts_ifc_testgroup_entries[] = {
		{"scheme",		{.data.largeint = &kts_ifc_vector.schema, PARSER_CIPHER}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"keyGenerationMethod",	{.data.largeint = &kts_ifc_vector.key_generation_method, PARSER_CIPHER}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"modulo",		{.data.integer = &kts_ifc_vector.modulus, PARSER_UINT}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"l",			{.data.integer = &kts_ifc_vector.keylen, PARSER_UINT}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"iutId",		{.data.buf = &kts_ifc_vector.iut_id, PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"serverId",		{.data.buf = &kts_ifc_vector.server_id, PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"ktsConfiguration",	{.data.array = &kts_configuration, PARSER_OBJECT},	FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"macConfiguration",	{.data.array = &kts_mac_configuration, PARSER_OBJECT},	FLAG_OP_AFT | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER | FLAG_OPTIONAL},

		/* Generation tests */
		{"tests",	{.data.array = &kts_ifc_init_tests, PARSER_ARRAY},
				FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR},
		{"tests",	{.data.array = &kts_ifc_resp_tests, PARSER_ARRAY},
				FLAG_OP_AFT | FLAG_OP_KAS_ROLE_RESPONDER},

		/* Validation tests */
		{"tests",	{.data.array = &kts_ifc_init_val_tests, PARSER_ARRAY},
				FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR},
		{"tests",	{.data.array = &kts_ifc_resp_val_tests, PARSER_ARRAY},
				FLAG_OP_VAL | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array kts_ifc_testgroup = SET_ARRAY(kts_ifc_testgroup_entries, NULL);

	const struct json_entry kts_ifc_testanchor_entries[] = {
		{"testGroups",	{.data.array = &kts_ifc_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array kts_ifc_testanchor = SET_ARRAY(kts_ifc_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&kts_ifc_testanchor, "1.0", in, out);
}

static struct cavs_tester kts_ifc =
{
	ACVP_KTS_IFC,
	0,
	kts_ifc_tester,	/* process_req */
	NULL
};

static struct cavs_tester kas_ifc_ssc =
{
	ACVP_KAS_IFC_SSC,
	0,
	kas_ifc_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_kts_ifc)
static void register_kts_ifc(void)
{
	register_tester(&kts_ifc, "KTS IFC");
	register_tester(&kas_ifc_ssc, "KAS IFC SSC");
}

void register_kts_ifc_impl(struct kts_ifc_backend *implementation)
{
	register_backend(kts_ifc_backend, implementation, "KTS IFC");
}
