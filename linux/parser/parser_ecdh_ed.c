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

#include "parser_common.h"

#define ECDH_ED_DEF_CALLBACK(name, flags) DEF_CALLBACK(ecdh_ed, name, flags)

static struct ecdh_ed_backend *ecdh_ed_backend = NULL;

static int ecdh_ed_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	(void)cipher;

	if (!ecdh_ed_backend) {
		logger(LOGGER_WARN, "No ECDH_ED backend set\n");
		return -EOPNOTSUPP;
	}

	/**********************************************************************
	 * ECDH_ED shared secret verification
	 **********************************************************************/
	ECDH_ED_DEF_CALLBACK(ecdh_ed_ss_ver, FLAG_OP_VAL);

	const struct json_entry ecdh_ed_ver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdh_ed_ss_ver_vector.validity_success, WRITER_BOOL}, FLAG_OP_VAL},
	};
	const struct json_testresult ecdh_ed_ver_testresult =
		SET_ARRAY(ecdh_ed_ver_testresult_entries, &ecdh_ed_ss_ver_callbacks);

	const struct json_entry ecdh_ed_ver_test_entries[] = {
		{"staticPublicServer",	{.data.buf = &ecdh_ed_ss_ver_vector.pub_rem, PARSER_BIN},	FLAG_OP_VAL},
		{"staticPrivateServer",	{.data.buf = &ecdh_ed_ss_ver_vector.priv_rem, PARSER_BIN},	FLAG_OP_VAL},
		{"ephemeralPublicIut",	{.data.buf = &ecdh_ed_ss_ver_vector.pub_loc, PARSER_BIN},	FLAG_OP_VAL},
		{"ephemeralPrivateIut",	{.data.buf = &ecdh_ed_ss_ver_vector.priv_loc, PARSER_BIN},	FLAG_OP_VAL},
		{"kdfZIut",		{.data.buf = &ecdh_ed_ss_ver_vector.kdfz, PARSER_BIN},	FLAG_OP_VAL},
	};
	const struct json_array ecdh_ed_ver_test =
			SET_ARRAY(ecdh_ed_ver_test_entries, &ecdh_ed_ver_testresult);

	/**********************************************************************
	 * ECDH_ED shared secret generation
	 **********************************************************************/
	ECDH_ED_DEF_CALLBACK(ecdh_ed_ss, FLAG_OP_AFT);

	/*
	 * Component testing.
	 */
	const struct json_entry ecdh_ed_ss_testresult_entries[] = {
		{"publicIut",	{.data.buf = &ecdh_ed_ss_vector.pub_loc, WRITER_BIN},	FLAG_OP_AFT},
		{"kdfZIut",	{.data.buf = &ecdh_ed_ss_vector.kdfz, WRITER_BIN},	FLAG_OP_AFT},
	};
	const struct json_testresult ecdh_ed_ss_testresult =
			SET_ARRAY(ecdh_ed_ss_testresult_entries, &ecdh_ed_ss_callbacks);

	const struct json_entry ecdh_ed_ss_test_entries[] = {
		{"staticPublicServer",	{.data.buf = &ecdh_ed_ss_vector.pub_rem, PARSER_BIN},	FLAG_OP_AFT},
		{"staticPrivateServer",	{.data.buf = &ecdh_ed_ss_vector.priv_rem, PARSER_BIN},	FLAG_OP_AFT},
	};
	const struct json_array ecdh_ed_ss_test =
			SET_ARRAY(ecdh_ed_ss_test_entries, &ecdh_ed_ss_testresult);


	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test ss_vectors.
	 *
	 * As this definition does not mark specific individual test ss_vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry ecdh_ed_testgroup_entries[] = {
		/* Common entries */
		{"curve",	{.data.largeint = &ecdh_ed_ss_vector.cipher, PARSER_CIPHER}, 	FLAG_OP_AFT},
		{"curve",	{.data.largeint = &ecdh_ed_ss_ver_vector.cipher, PARSER_CIPHER}, 	FLAG_OP_VAL},

		{"tests",	{.data.array = &ecdh_ed_ss_test, PARSER_ARRAY},		FLAG_OP_AFT},
		{"tests",	{.data.array = &ecdh_ed_ver_test, PARSER_ARRAY},		FLAG_OP_VAL},
	};
	const struct json_array ecdh_ed_testgroup = SET_ARRAY(ecdh_ed_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry ecdh_ed_testanchor_entries[] = {
		{"testGroups",	{.data.array = &ecdh_ed_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array ecdh_ed_testanchor = SET_ARRAY(ecdh_ed_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&ecdh_ed_testanchor, "1.0", in, out);
}

static struct cavs_tester ecdh_ed =
{
	ACVP_ECDH_ED,
	0,
	ecdh_ed_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_ecdh_ed)
static void register_ecdh_ed(void)
{
	register_tester(&ecdh_ed, "ECDH_ED");
}

void register_ecdh_ed_impl(struct ecdh_ed_backend *implementation)
{
	register_backend(ecdh_ed_backend, implementation, "ECDH_ED");
}
