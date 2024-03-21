/*
 * Copyright 2021-2022 VMware, Inc.
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
#include "parser_kmac.h"

static struct kmac_backend *kmac_backend = NULL;

static int kmac_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	logger(LOGGER_DEBUG,"KMAC_tester");
	struct kmac_data vector;

	if (!kmac_backend) {
		logger(LOGGER_WARN, "No KMAC backend set\n");
		return -EOPNOTSUPP;
	}

	/* Referencing the backend functions */
	const struct kmac_callback kmac = { kmac_backend->kmac_generate, &vector, NULL};
	const struct kmac_callback kmac_ver = { kmac_backend->kmac_ver, &vector, NULL};
	const struct json_callback kmac_callback[] = {
		{ .callback.kmac = kmac, CB_TYPE_kmac, FLAG_OP_AFT},
		{ .callback.kmac = kmac_ver, CB_TYPE_kmac, FLAG_OP_MVT},
	};
	const struct json_callbacks kmac_callbacks = SET_CALLBACKS(kmac_callback);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry kmac_testresult_entries[] = {
		{"mac",		{.data.buf = &vector.mac, WRITER_BIN}, FLAG_OP_AFT},
	};
	const struct json_testresult kmac_testresult = SET_ARRAY(kmac_testresult_entries, &kmac_callbacks);
	const struct json_entry kmac_testresult_ver_entries[] = {
		{"testPassed",	{.data.integer = &vector.verify_result, WRITER_BOOL}, FLAG_OP_MVT},
	};
	const struct json_testresult kmac_testresult_ver = SET_ARRAY(kmac_testresult_ver_entries, &kmac_callbacks);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file.
	 */
	const struct json_entry kmac_test_entries[] = {
		{"msg",		{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_AFT},
		{"key",		{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_AFT},
		{"keyLen",	{.data.integer = &vector.keylen, PARSER_UINT},	FLAG_OP_AFT},
		{"macLen",	{.data.integer = &vector.maclen, PARSER_UINT},	FLAG_OP_AFT},
		{"customization",	{.data.buf = &vector.customization, PARSER_STRING},	FLAG_OP_AFT | FLAG_OPTIONAL},
		{"customizationHex",	{.data.buf = &vector.customization, PARSER_BIN},	FLAG_OP_AFT | FLAG_OPTIONAL},
	};
	const struct json_array kmac_test = SET_ARRAY(kmac_test_entries, &kmac_testresult);

	const struct json_entry kmac_test_ver_entries[] = {
		{"msg",		{.data.buf = &vector.msg, PARSER_BIN},	FLAG_OP_MVT},
		{"mac",		{.data.buf = &vector.mac, PARSER_BIN},	FLAG_OP_MVT},
		{"key",		{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_MVT},
		{"keyLen",	{.data.integer = &vector.keylen, PARSER_UINT},	FLAG_OP_MVT},
		{"macLen",	{.data.integer = &vector.maclen, PARSER_UINT},	FLAG_OP_MVT},
		{"customization",	{.data.buf = &vector.customization, PARSER_STRING},	FLAG_OP_MVT | FLAG_OPTIONAL},
		{"customizationHex",	{.data.buf = &vector.customization, PARSER_BIN},	FLAG_OP_MVT | FLAG_OPTIONAL},
	};
	const struct json_array kmac_test_ver = SET_ARRAY(kmac_test_ver_entries, &kmac_testresult_ver);
	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors.
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry mac_testgroup_entries[] = {
		{"xof",	{.data.integer = &vector.xof_enabled, PARSER_BOOL},	FLAG_OP_MVT | FLAG_OP_AFT | FLAG_OPTIONAL},
		{"tests",	{.data.array = &kmac_test, PARSER_ARRAY},	FLAG_OP_AFT },
		{"tests",	{.data.array = &kmac_test_ver, PARSER_ARRAY}, FLAG_OP_MVT},
	};
	const struct json_array mac_testgroup = SET_ARRAY(mac_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry mac_testanchor_entries[] = {
		{"testGroups",	{.data.array = &mac_testgroup, PARSER_ARRAY}, 0},
	};
	const struct json_array mac_testanchor = SET_ARRAY(mac_testanchor_entries, NULL);

	memset(&vector, 0, sizeof(struct kmac_data));
	vector.cipher = cipher;

	/* Process all. */
	return process_json(&mac_testanchor, "1.0", in, out);
}

static struct cavs_tester kmac =
{
	0,
	ACVP_KMACMASK,
	kmac_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_kmac)
static void register_kmac(void)
{
	register_tester(&kmac, "KMAC");
}

void register_kmac_impl(struct kmac_backend *implementation)
{
	register_backend(kmac_backend, implementation, "KMAC");
}
