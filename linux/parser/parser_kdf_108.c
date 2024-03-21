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

static struct kdf_108_backend *kdf_108_backend = NULL;

static int kdf_108_tester(struct json_object *in, struct json_object *out,
			  uint64_t cipher)
{
	(void)cipher;

	if (!kdf_108_backend) {
		logger(LOGGER_WARN, "No SP800-108 KDF backend set\n");
		return -EOPNOTSUPP;
	}

	DEF_CALLBACK(kdf_108, kdf_108, FLAG_OP_AFT);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry kdf_108_testresult_entries[] = {
		{"breakLocation",{.data.integer = &kdf_108_vector.break_location, WRITER_UINT}, FLAG_OP_AFT},
		{"fixedData",	{.data.buf = &kdf_108_vector.fixed_data, WRITER_BIN}, FLAG_OP_AFT},
		{"keyOut",	{.data.buf = &kdf_108_vector.derived_key, WRITER_BIN}, FLAG_OP_AFT},
	};
	const struct json_testresult kdf_108_testresult = SET_ARRAY(kdf_108_testresult_entries, &kdf_108_callbacks);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file.
	 */
	const struct json_entry kdf_108_test_entries[] = {
		{"keyIn",	{.data.buf = &kdf_108_vector.key, PARSER_BIN}, FLAG_OP_AFT},
		{"iv",		{.data.buf = &kdf_108_vector.iv, PARSER_BIN}, FLAG_OP_AFT | FLAG_OPTIONAL},

		/* Support for regression test */
		{"breakLocation",{.data.integer = &kdf_108_vector.break_location, PARSER_UINT}, FLAG_OP_AFT | FLAG_OPTIONAL},
		{"fixedData",	{.data.buf = &kdf_108_vector.fixed_data, PARSER_BIN}, FLAG_OP_AFT | FLAG_OPTIONAL},
	};
	const struct json_array kdf_108_test =
		SET_ARRAY(kdf_108_test_entries, &kdf_108_testresult);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors.
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry kdf_108_testgroup_entries[] = {
		{"macMode",		{.data.largeint = &kdf_108_vector.mac, PARSER_CIPHER}, FLAG_OP_AFT},
		{"kdfMode",		{.data.largeint = &kdf_108_vector.kdfmode, PARSER_CIPHER}, FLAG_OP_AFT},
		{"counterLocation",	{.data.largeint = &kdf_108_vector.counter_location, PARSER_CIPHER}, FLAG_OP_AFT},

		{"keyOutLength",	{.data.integer = &kdf_108_vector.derived_key_length, PARSER_UINT}, FLAG_OP_AFT},
		{"counterLength",	{.data.integer = &kdf_108_vector.counter_length, PARSER_UINT}, FLAG_OP_AFT},

		{"tests",		{.data.array = &kdf_108_test, PARSER_ARRAY}, FLAG_OP_AFT},
	};
	const struct json_array kdf_108_testgroup = SET_ARRAY(kdf_108_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry kdf_108_testanchor_entries[] = {
		{"testGroups",	{.data.array = &kdf_108_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array kdf_108_testanchor = SET_ARRAY(kdf_108_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&kdf_108_testanchor, "1.0", in, out);
}

static struct cavs_tester kdf_108 =
{
	ACVP_KDF_800_108,
	0,
	kdf_108_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_kdf_108)
static void register_kdf_108(void)
{
	register_tester(&kdf_108, "SP800-108 KDF");
}

void register_kdf_108_impl(struct kdf_108_backend *implementation)
{
	register_backend(kdf_108_backend, implementation, "SP800-108 KDF");
}
