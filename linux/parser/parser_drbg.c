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
#include "logger.h"

#include "parser_common.h"
#include "parser_drbg.h"

static struct drbg_backend *drbg_backend = NULL;

static int drbg_tester(struct json_object *in, struct json_object *out,
		       uint64_t cipher)
{
	if (!drbg_backend) {
		logger(LOGGER_WARN, "No DRBG backend set\n");
		return -EOPNOTSUPP;
	}

	DEF_CALLBACK(drbg, drbg, FLAG_OP_AFT);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry drbg_testresult_entries[] = {
		{"returnedBits",	{.data.buf = &drbg_vector.random, WRITER_BIN},	FLAG_OP_AFT},
	};
	const struct json_testresult drbg_testresult = SET_ARRAY(drbg_testresult_entries, &drbg_callbacks);

	/* Optional: prediction resistance */
	const struct json_entry drbg_otherinput_entries[] = {
		{"additionalInput",	{.data.buffer_array = &drbg_vector.addtl_generate, PARSER_BIN_BUFFERARRAY},	FLAG_OP_AFT | FLAG_OP_DRBG_GENERATE | FLAG_OPTIONAL},
		{"entropyInput",	{.data.buffer_array = &drbg_vector.entropy_generate, PARSER_BIN_BUFFERARRAY},	FLAG_OP_AFT | FLAG_OP_DRBG_GENERATE | FLAG_OPTIONAL},
		{"additionalInput",	{.data.buffer_array = &drbg_vector.addtl_reseed, PARSER_BIN_BUFFERARRAY},	FLAG_OP_AFT | FLAG_OP_DRBG_RESEED | FLAG_OPTIONAL},
		{"entropyInput",	{.data.buffer_array = &drbg_vector.entropy_reseed, PARSER_BIN_BUFFERARRAY},	FLAG_OP_AFT | FLAG_OP_DRBG_RESEED | FLAG_OPTIONAL},
	};
	const struct json_array drbg_otherinput = SET_ARRAY(drbg_otherinput_entries, NULL);

	const struct json_entry drbg_otherinput_object_entries[] = {
		{NULL,	{.data.array = &drbg_otherinput, PARSER_ARRAY_BUFFERARRAY},	FLAG_OP_AFT | FLAG_OP_DRBG_GENERATE | FLAG_OP_DRBG_RESEED},
	};
	const struct json_array drbg_otherinput_object = SET_ARRAY(drbg_otherinput_object_entries, NULL);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file.
	 */
	const struct json_entry drbg_test_entries[] = {
		{"entropyInput",	{.data.buf = &drbg_vector.entropy, PARSER_BIN},	FLAG_OP_AFT},
		{"nonce",		{.data.buf = &drbg_vector.nonce, PARSER_BIN},	FLAG_OP_AFT},
		{"persoString",		{.data.buf = &drbg_vector.pers, PARSER_BIN},		FLAG_OP_AFT},

		{"otherInput",		{.data.array = &drbg_otherinput_object, PARSER_ARRAY_BUFFERARRAY},	FLAG_OPTIONAL | FLAG_OP_AFT},
	};
	const struct json_array drbg_test = SET_ARRAY(drbg_test_entries, &drbg_testresult);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors.
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry drbg_testgroup_entries[] = {
		{"predResistance",	{.data.integer = &drbg_vector.pr, PARSER_BOOL},			FLAG_OP_AFT},
		{"derFunc",		{.data.integer = &drbg_vector.df, PARSER_BOOL},			FLAG_OP_AFT | FLAG_OPTIONAL},
		{"returnedBitsLen",	{.data.integer = &drbg_vector.rnd_data_bits_len, PARSER_UINT},	FLAG_OP_AFT},
		{"mode",		{.data.largeint = &drbg_vector.cipher, PARSER_CIPHER},		FLAG_OP_AFT},
		{"tests",		{.data.array = &drbg_test, PARSER_ARRAY},			FLAG_OP_AFT},
	};
	const struct json_array drbg_testgroup = SET_ARRAY(drbg_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data.
	 */
	const struct json_entry drbg_testanchor_entries[] = {
		{"testGroups",	{.data.array = &drbg_testgroup, PARSER_ARRAY},		0}
	};
	const struct json_array drbg_testanchor = SET_ARRAY(drbg_testanchor_entries, NULL);

	/* Set the DRBG type */
	drbg_vector.type = cipher;

	/* Process all. */
	return process_json(&drbg_testanchor, "1.0", in, out);
}

static struct cavs_tester drbg =
{
	0,
	ACVP_DRBGMASK,
	drbg_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_drbg)
static void register_drbg()
{
	register_tester(&drbg, "DRBG");
}

void register_drbg_impl(struct drbg_backend *implementation)
{
	register_backend(drbg_backend, implementation, "DRBG");
}
