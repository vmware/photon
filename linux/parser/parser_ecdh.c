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

#define ECDH_DEF_CALLBACK(name, flags)	DEF_CALLBACK(ecdh, name, flags)
#define ECDH_DEF_CALLBACK_HELPER(name, flags, helper)			       \
				DEF_CALLBACK_HELPER(ecdh, name, flags, helper)

static struct ecdh_backend *ecdh_backend = NULL;

static int ecdh_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	(void)cipher;

	if (!ecdh_backend) {
		logger(LOGGER_WARN, "No ECDH backend set\n");
		return -EOPNOTSUPP;
	}

	/**********************************************************************
	 * ECDH shared secret verification
	 **********************************************************************/
	ECDH_DEF_CALLBACK(ecdh_ss_ver, FLAG_OP_VAL | FLAG_OP_MASK_ECDH | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER);

	/*
	 * Ephemeral Unified
	 * TODO: No KDF/KC support
	 */
	const struct json_entry ecdh_eu_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdh_ss_ver_vector.validity_success, WRITER_BOOL},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_eu_ver_testresult =
		SET_ARRAY(ecdh_eu_ver_testresult_entries, &ecdh_ss_ver_callbacks);

	const struct json_entry ecdh_eu_ver_test_entries[] = {
		{"ephemeralPublicServerX",	{.data.buf = &ecdh_ss_ver_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicServerY",	{.data.buf = &ecdh_ss_ver_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicIutX",		{.data.buf = &ecdh_ss_ver_vector.Qxloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicIutY",		{.data.buf = &ecdh_ss_ver_vector.Qyloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPrivateIut",		{.data.buf = &ecdh_ss_ver_vector.privloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",			{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_eu_ver_test =
			SET_ARRAY(ecdh_eu_ver_test_entries, &ecdh_eu_ver_testresult);

	/*
	 * One Pass DH
	 * TODO: No KDF/KC support
	 */
	const struct json_entry ecdh_opdh_i_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdh_ss_ver_vector.validity_success, WRITER_BOOL},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
	};
	const struct json_testresult ecdh_opdh_i_ver_testresult =
		SET_ARRAY(ecdh_opdh_i_ver_testresult_entries, &ecdh_ss_ver_callbacks);

	const struct json_entry ecdh_opdh_i_ver_test_entries[] = {
		{"staticPublicServerX",	{.data.buf = &ecdh_ss_ver_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"staticPublicServerY",	{.data.buf = &ecdh_ss_ver_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"ephemeralPublicIutX",		{.data.buf = &ecdh_ss_ver_vector.Qxloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"ephemeralPublicIutY",		{.data.buf = &ecdh_ss_ver_vector.Qyloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"ephemeralPrivateIut",		{.data.buf = &ecdh_ss_ver_vector.privloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"hashZIut",			{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
	};
	const struct json_array ecdh_opdh_i_ver_test =
			SET_ARRAY(ecdh_opdh_i_ver_test_entries, &ecdh_opdh_i_ver_testresult);

	const struct json_entry ecdh_opdh_r_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdh_ss_ver_vector.validity_success, WRITER_BOOL},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_opdh_r_ver_testresult =
		SET_ARRAY(ecdh_opdh_r_ver_testresult_entries, &ecdh_ss_ver_callbacks);

	const struct json_entry ecdh_opdh_r_ver_test_entries[] = {
		{"ephemeralPublicServerX",	{.data.buf = &ecdh_ss_ver_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicServerY",	{.data.buf = &ecdh_ss_ver_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutX",		{.data.buf = &ecdh_ss_ver_vector.Qxloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutY",		{.data.buf = &ecdh_ss_ver_vector.Qyloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",		{.data.buf = &ecdh_ss_ver_vector.privloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",			{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_opdh_r_ver_test =
			SET_ARRAY(ecdh_opdh_r_ver_test_entries, &ecdh_opdh_r_ver_testresult);

	/*
	 * Static Unified
	 * TODO: No KDF/KC support
	 */
	const struct json_entry ecdh_su_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdh_ss_ver_vector.validity_success, WRITER_BOOL},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_su_ver_testresult =
		SET_ARRAY(ecdh_su_ver_testresult_entries, &ecdh_ss_ver_callbacks);

	const struct json_entry ecdh_su_ver_test_entries[] = {
		{"staticPublicServerX",	{.data.buf = &ecdh_ss_ver_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicServerY",	{.data.buf = &ecdh_ss_ver_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutX",		{.data.buf = &ecdh_ss_ver_vector.Qxloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutY",		{.data.buf = &ecdh_ss_ver_vector.Qyloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",		{.data.buf = &ecdh_ss_ver_vector.privloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",			{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_su_ver_test =
			SET_ARRAY(ecdh_su_ver_test_entries, &ecdh_su_ver_testresult);

	/**********************************************************************
	 * ECDH shared secret generation
	 **********************************************************************/
	ECDH_DEF_CALLBACK(ecdh_ss, FLAG_OP_AFT | FLAG_OP_MASK_ECDH | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER);

	/*
	 * Component testing.
	 */
	const struct json_entry ecdh_cdh_testresult_entries[] = {
		{"publicIutX",	{.data.buf = &ecdh_ss_vector.Qxloc, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST},
		{"publicIutY",	{.data.buf = &ecdh_ss_vector.Qyloc, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST},
		{"z",		{.data.buf = &ecdh_ss_vector.hashzz, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST},
	};
	const struct json_testresult ecdh_cdh_testresult =
			SET_ARRAY(ecdh_cdh_testresult_entries, &ecdh_ss_callbacks);

	const struct json_entry ecdh_cdh_test_entries[] = {
		{"publicServerX",	{.data.buf = &ecdh_ss_vector.Qxrem, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST},
		{"publicServerY",	{.data.buf = &ecdh_ss_vector.Qyrem, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST},
	};
	const struct json_array ecdh_cdh_test =
			SET_ARRAY(ecdh_cdh_test_entries, &ecdh_cdh_testresult);

	/*
	 * Ephemeral Unified
	 * TODO: No KDF/KC support
	 */
	const struct json_entry ecdh_eu_testresult_entries[] = {
		{"ephemeralPublicIutX",	{.data.buf = &ecdh_ss_vector.Qxloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicIutY",	{.data.buf = &ecdh_ss_vector.Qyloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPrivateIut",	{.data.buf = &ecdh_ss_vector.privloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",		{.data.buf = &ecdh_ss_vector.hashzz, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_eu_testresult =
			SET_ARRAY(ecdh_eu_testresult_entries, &ecdh_ss_callbacks);

	const struct json_entry ecdh_eu_test_entries[] = {
		{"ephemeralPublicServerX",	{.data.buf = &ecdh_ss_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicServerY",	{.data.buf = &ecdh_ss_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_eu_test =
			SET_ARRAY(ecdh_eu_test_entries, &ecdh_eu_testresult);

	/*
	 * One Pass DH
	 * TODO: No KDF/KC support
	 */
	const struct json_entry ecdh_opdh_i_testresult_entries[] = {
		{"ephemeralPublicIutX",	{.data.buf = &ecdh_ss_vector.Qxloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR},
		{"ephemeralPublicIutY",	{.data.buf = &ecdh_ss_vector.Qyloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR},
		{"ephemeralPrivateIut",	{.data.buf = &ecdh_ss_vector.privloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR},
		{"hashZIut",		{.data.buf = &ecdh_ss_vector.hashzz, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult ecdh_opdh_i_testresult =
			SET_ARRAY(ecdh_opdh_i_testresult_entries, &ecdh_ss_callbacks);

	const struct json_entry ecdh_opdh_i_test_entries[] = {
		{"staticPublicServerX",	{.data.buf = &ecdh_ss_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"staticPublicServerY",	{.data.buf = &ecdh_ss_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
	};
	const struct json_array ecdh_opdh_i_test =
			SET_ARRAY(ecdh_opdh_i_test_entries, &ecdh_opdh_i_testresult);

	const struct json_entry ecdh_opdh_r_testresult_entries[] = {
		{"staticPublicIutX",	{.data.buf = &ecdh_ss_vector.Qxloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutY",	{.data.buf = &ecdh_ss_vector.Qyloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",	{.data.buf = &ecdh_ss_vector.privloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",		{.data.buf = &ecdh_ss_vector.hashzz, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_opdh_r_testresult =
			SET_ARRAY(ecdh_opdh_r_testresult_entries, &ecdh_ss_callbacks);

	const struct json_entry ecdh_opdh_r_test_entries[] = {
		{"ephemeralPublicServerX",	{.data.buf = &ecdh_ss_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER },
		{"ephemeralPublicServerY",	{.data.buf = &ecdh_ss_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER },
	};
	const struct json_array ecdh_opdh_r_test =
			SET_ARRAY(ecdh_opdh_r_test_entries, &ecdh_opdh_r_testresult);

	/*
	 * Static Unified
	 * TODO: No KDF/KC support
	 */
	const struct json_entry ecdh_su_testresult_entries[] = {
		{"staticPublicIutX",	{.data.buf = &ecdh_ss_vector.Qxloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutY",	{.data.buf = &ecdh_ss_vector.Qyloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",	{.data.buf = &ecdh_ss_vector.privloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZIut",		{.data.buf = &ecdh_ss_vector.hashzz, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_su_testresult =
			SET_ARRAY(ecdh_su_testresult_entries, &ecdh_ss_callbacks);

	const struct json_entry ecdh_su_test_entries[] = {
		{"staticPublicServerX",	{.data.buf = &ecdh_ss_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicServerY",	{.data.buf = &ecdh_ss_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_su_test =
			SET_ARRAY(ecdh_su_test_entries, &ecdh_su_testresult);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test ss_vectors.
	 *
	 * As this definition does not mark specific individual test ss_vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry ecdh_testgroup_entries[] = {
		/* Common entries */
		{"curve",	{.data.largeint = &ecdh_ss_vector.cipher, PARSER_CIPHER}, 	FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashAlg",	{.data.largeint = &ecdh_ss_vector.cipher, PARSER_CIPHER},	FLAG_OPTIONAL | FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"macType",	{.data.largeint = &ecdh_ss_vector.cipher, PARSER_CIPHER},	FLAG_OPTIONAL | FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"curve",	{.data.largeint = &ecdh_ss_ver_vector.cipher, PARSER_CIPHER},	FLAG_OP_MASK_ECDH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashAlg",	{.data.largeint = &ecdh_ss_ver_vector.cipher, PARSER_CIPHER},	FLAG_OPTIONAL | FLAG_OP_MASK_ECDH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"macType",	{.data.largeint = &ecdh_ss_ver_vector.cipher, PARSER_CIPHER},	FLAG_OPTIONAL | FLAG_OP_MASK_ECDH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &ecdh_cdh_test, PARSER_ARRAY},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &ecdh_eu_test, PARSER_ARRAY},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &ecdh_eu_ver_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &ecdh_opdh_i_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"tests",	{.data.array = &ecdh_opdh_r_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER },
		{"tests",	{.data.array = &ecdh_opdh_i_ver_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR},
		{"tests",	{.data.array = &ecdh_opdh_r_ver_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &ecdh_su_test, PARSER_ARRAY},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &ecdh_su_ver_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &ecdh_cdh_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST},
	};
	const struct json_array ecdh_testgroup = SET_ARRAY(ecdh_testgroup_entries, NULL);

	const struct json_entry ecdh_component_testgroup_entries[] = {
		/* Common entries */
		{"curve",	{.data.largeint = &ecdh_ss_vector.cipher, PARSER_CIPHER}, 	FLAG_OP_MASK_ECDH | FLAG_OP_AFT },

		{"tests",	{.data.array = &ecdh_cdh_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST},
	};
	const struct json_array ecdh_component_testgroup = SET_ARRAY(ecdh_component_testgroup_entries, NULL);
	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry ecdh_testanchor_entries[] = {
		{"testGroups",	{.data.array = &ecdh_testgroup, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST},
		{"testGroups",	{.data.array = &ecdh_component_testgroup, PARSER_ARRAY},	FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST}
	};
	const struct json_array ecdh_testanchor = SET_ARRAY(ecdh_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&ecdh_testanchor, "1.0", in, out);
}

static struct cavs_tester ecdh =
{
	ACVP_ECDH,
	0,
	ecdh_tester,	/* process_req */
	NULL
};

static int kas_ecc_r3_ssc_helper(const struct json_array *processdata,
				 flags_t parsed_flags,
				 struct json_object *testvector,
				 struct json_object *testresults,
	int (*callback)(struct ecdh_ss_data *vector, flags_t parsed_flags),
			struct ecdh_ss_data *vector)
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
	CKINT(json_add_bin2hex(testresult, (vector->cipher & ACVP_HASHMASK) ?
					   "hashZ" : "z",
			       &vector->hashzz));
	free_buf(&vector->hashzz);

	ret = FLAG_RES_DATA_WRITTEN;

out:
	return ret;
}

static int kas_ecc_r3_ssc_tester(struct json_object *in,
				 struct json_object *out,
				 uint64_t cipher)
{
	(void)cipher;

	if (!ecdh_backend) {
		logger(LOGGER_WARN, "No ECDH backend set\n");
		return -EOPNOTSUPP;
	}

	/**********************************************************************
	 * ECDH shared secret verification
	 **********************************************************************/
	ECDH_DEF_CALLBACK(ecdh_ss_ver, FLAG_OP_VAL | FLAG_OP_MASK_ECDH | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER);

	/*
	 * Ephemeral Unified
	 * TODO: No KDF/KC support
	 */
	const struct json_entry ecdh_eu_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdh_ss_ver_vector.validity_success, WRITER_BOOL},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_eu_ver_testresult =
		SET_ARRAY(ecdh_eu_ver_testresult_entries, &ecdh_ss_ver_callbacks);

	const struct json_entry ecdh_eu_ver_test_entries[] = {
		{"ephemeralPublicServerX",	{.data.buf = &ecdh_ss_ver_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicServerY",	{.data.buf = &ecdh_ss_ver_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicIutX",		{.data.buf = &ecdh_ss_ver_vector.Qxloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicIutY",		{.data.buf = &ecdh_ss_ver_vector.Qyloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPrivateIut",		{.data.buf = &ecdh_ss_ver_vector.privloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZ",			{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"z",				{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_eu_ver_test =
			SET_ARRAY(ecdh_eu_ver_test_entries, &ecdh_eu_ver_testresult);

	/*
	 * One Pass DH
	 * TODO: No KDF/KC support
	 */
	const struct json_entry ecdh_opdh_i_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdh_ss_ver_vector.validity_success, WRITER_BOOL},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
	};
	const struct json_testresult ecdh_opdh_i_ver_testresult =
		SET_ARRAY(ecdh_opdh_i_ver_testresult_entries, &ecdh_ss_ver_callbacks);

	const struct json_entry ecdh_opdh_i_ver_test_entries[] = {
		{"staticPublicServerX",	{.data.buf = &ecdh_ss_ver_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"staticPublicServerY",	{.data.buf = &ecdh_ss_ver_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"ephemeralPublicIutX",		{.data.buf = &ecdh_ss_ver_vector.Qxloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"ephemeralPublicIutY",		{.data.buf = &ecdh_ss_ver_vector.Qyloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"ephemeralPrivateIut",		{.data.buf = &ecdh_ss_ver_vector.privloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"hashZ",			{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"z",				{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
	};
	const struct json_array ecdh_opdh_i_ver_test =
			SET_ARRAY(ecdh_opdh_i_ver_test_entries, &ecdh_opdh_i_ver_testresult);

	const struct json_entry ecdh_opdh_r_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdh_ss_ver_vector.validity_success, WRITER_BOOL},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_opdh_r_ver_testresult =
		SET_ARRAY(ecdh_opdh_r_ver_testresult_entries, &ecdh_ss_ver_callbacks);

	const struct json_entry ecdh_opdh_r_ver_test_entries[] = {
		{"ephemeralPublicServerX",	{.data.buf = &ecdh_ss_ver_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicServerY",	{.data.buf = &ecdh_ss_ver_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutX",		{.data.buf = &ecdh_ss_ver_vector.Qxloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutY",		{.data.buf = &ecdh_ss_ver_vector.Qyloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",		{.data.buf = &ecdh_ss_ver_vector.privloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZ",			{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"z",				{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_opdh_r_ver_test =
			SET_ARRAY(ecdh_opdh_r_ver_test_entries, &ecdh_opdh_r_ver_testresult);

	/*
	 * Static Unified
	 * TODO: No KDF/KC support
	 */
	const struct json_entry ecdh_su_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdh_ss_ver_vector.validity_success, WRITER_BOOL},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_su_ver_testresult =
		SET_ARRAY(ecdh_su_ver_testresult_entries, &ecdh_ss_ver_callbacks);

	const struct json_entry ecdh_su_ver_test_entries[] = {
		{"staticPublicServerX",	{.data.buf = &ecdh_ss_ver_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicServerY",	{.data.buf = &ecdh_ss_ver_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutX",		{.data.buf = &ecdh_ss_ver_vector.Qxloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutY",		{.data.buf = &ecdh_ss_ver_vector.Qyloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",		{.data.buf = &ecdh_ss_ver_vector.privloc, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashZ",			{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"z",				{.data.buf = &ecdh_ss_ver_vector.hashzz, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OPTIONAL | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_su_ver_test =
			SET_ARRAY(ecdh_su_ver_test_entries, &ecdh_su_ver_testresult);

	/**********************************************************************
	 * ECDH shared secret generation
	 **********************************************************************/
	ECDH_DEF_CALLBACK_HELPER(ecdh_ss, FLAG_OP_AFT | FLAG_OP_MASK_ECDH | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER, kas_ecc_r3_ssc_helper);

	/*
	 * Ephemeral Unified
	 */
	const struct json_entry ecdh_eu_testresult_entries[] = {
		{"ephemeralPublicIutX",	{.data.buf = &ecdh_ss_vector.Qxloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicIutY",	{.data.buf = &ecdh_ss_vector.Qyloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPrivateIut",	{.data.buf = &ecdh_ss_vector.privloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_eu_testresult =
			SET_ARRAY(ecdh_eu_testresult_entries, &ecdh_ss_callbacks);

	const struct json_entry ecdh_eu_test_entries[] = {
		{"ephemeralPublicServerX",	{.data.buf = &ecdh_ss_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"ephemeralPublicServerY",	{.data.buf = &ecdh_ss_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_eu_test =
			SET_ARRAY(ecdh_eu_test_entries, &ecdh_eu_testresult);

	/*
	 * One Pass DH
	 */
	const struct json_entry ecdh_opdh_i_testresult_entries[] = {
		{"ephemeralPublicIutX",	{.data.buf = &ecdh_ss_vector.Qxloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR},
		{"ephemeralPublicIutY",	{.data.buf = &ecdh_ss_vector.Qyloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR},
		{"ephemeralPrivateIut",	{.data.buf = &ecdh_ss_vector.privloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR},
	};
	const struct json_testresult ecdh_opdh_i_testresult =
			SET_ARRAY(ecdh_opdh_i_testresult_entries, &ecdh_ss_callbacks);

	const struct json_entry ecdh_opdh_i_test_entries[] = {
		{"staticPublicServerX",	{.data.buf = &ecdh_ss_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"staticPublicServerY",	{.data.buf = &ecdh_ss_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
	};
	const struct json_array ecdh_opdh_i_test =
			SET_ARRAY(ecdh_opdh_i_test_entries, &ecdh_opdh_i_testresult);

	const struct json_entry ecdh_opdh_r_testresult_entries[] = {
		{"staticPublicIutX",	{.data.buf = &ecdh_ss_vector.Qxloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutY",	{.data.buf = &ecdh_ss_vector.Qyloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",	{.data.buf = &ecdh_ss_vector.privloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_opdh_r_testresult =
			SET_ARRAY(ecdh_opdh_r_testresult_entries, &ecdh_ss_callbacks);

	const struct json_entry ecdh_opdh_r_test_entries[] = {
		{"ephemeralPublicServerX",	{.data.buf = &ecdh_ss_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER },
		{"ephemeralPublicServerY",	{.data.buf = &ecdh_ss_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER },
	};
	const struct json_array ecdh_opdh_r_test =
			SET_ARRAY(ecdh_opdh_r_test_entries, &ecdh_opdh_r_testresult);

	/*
	 * Static Unified
	 */
	const struct json_entry ecdh_su_testresult_entries[] = {
		{"staticPublicIutX",	{.data.buf = &ecdh_ss_vector.Qxloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicIutY",	{.data.buf = &ecdh_ss_vector.Qyloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPrivateIut",	{.data.buf = &ecdh_ss_vector.privloc, WRITER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_testresult ecdh_su_testresult =
			SET_ARRAY(ecdh_su_testresult_entries, &ecdh_ss_callbacks);

	const struct json_entry ecdh_su_test_entries[] = {
		{"staticPublicServerX",	{.data.buf = &ecdh_ss_vector.Qxrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"staticPublicServerY",	{.data.buf = &ecdh_ss_vector.Qyrem, PARSER_BIN},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_su_test =
			SET_ARRAY(ecdh_su_test_entries, &ecdh_su_testresult);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test ss_vectors.
	 *
	 * As this definition does not mark specific individual test ss_vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry ecdh_testgroup_entries[] = {
		/* Common entries */
		{"domainParameterGenerationMode",	{.data.largeint = &ecdh_ss_vector.cipher, PARSER_CIPHER}, 	FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashFunctionZ",	{.data.largeint = &ecdh_ss_vector.cipher, PARSER_CIPHER},	FLAG_OPTIONAL | FLAG_OP_MASK_ECDH | FLAG_OP_AFT | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"domainParameterGenerationMode",	{.data.largeint = &ecdh_ss_ver_vector.cipher, PARSER_CIPHER},	FLAG_OP_MASK_ECDH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"hashFunctionZ",	{.data.largeint = &ecdh_ss_ver_vector.cipher, PARSER_CIPHER},	FLAG_OPTIONAL | FLAG_OP_MASK_ECDH | FLAG_OP_VAL | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &ecdh_eu_test, PARSER_ARRAY},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &ecdh_eu_ver_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &ecdh_opdh_i_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR },
		{"tests",	{.data.array = &ecdh_opdh_r_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER },
		{"tests",	{.data.array = &ecdh_opdh_i_ver_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_INITIATOR},
		{"tests",	{.data.array = &ecdh_opdh_r_ver_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_ONE_PASS_DH | FLAG_OP_KAS_ROLE_RESPONDER},

		{"tests",	{.data.array = &ecdh_su_test, PARSER_ARRAY},		FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_AFT | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
		{"tests",	{.data.array = &ecdh_su_ver_test, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST | FLAG_OP_VAL | FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED | FLAG_OP_KAS_ROLE_INITIATOR | FLAG_OP_KAS_ROLE_RESPONDER},
	};
	const struct json_array ecdh_testgroup = SET_ARRAY(ecdh_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry ecdh_testanchor_entries[] = {
		{"testGroups",	{.data.array = &ecdh_testgroup, PARSER_ARRAY},	FLAG_OP_KAS_SCHEME_TEST},
	};
	const struct json_array ecdh_testanchor = SET_ARRAY(ecdh_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&ecdh_testanchor, "1.0", in, out);
}

static struct cavs_tester kas_ecc_r3_ssc =
{
	ACVP_KAS_ECC_R3_SSC,
	0,
	kas_ecc_r3_ssc_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_ecdh)
static void register_ecdh(void)
{
	register_tester(&ecdh, "ECDH");
	register_tester(&kas_ecc_r3_ssc, "KAS ECC R3 SSC");
}

void register_ecdh_impl(struct ecdh_backend *implementation)
{
	register_backend(ecdh_backend, implementation, "ECDH");
}
