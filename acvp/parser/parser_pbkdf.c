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

#include "bool.h"
#include "stringhelper.h"
#include "binhexbin.h"
#include "logger.h"
#include "read_json.h"

#include "parser_common.h"

/******************************************************************************
 * PBKDF callback definitions
 ******************************************************************************/
static struct pbkdf_backend *pbkdf_backend = NULL;

static int kdf_tester_pbkdf(struct json_object *in, struct json_object *out,
			    uint64_t cipher)
{
	(void)cipher;

	if (!pbkdf_backend) {
		logger(LOGGER_WARN, "No PBKDF backend set\n");
		return -EOPNOTSUPP;
	}

	/**********************************************************************
	 * PBKDF operation
	 **********************************************************************/
	DEF_CALLBACK(pbkdf, pbkdf, FLAG_OP_AFT);

	const struct json_entry pbkdf_testresult_entries[] = {
		{"derivedKey",		{.data.buf = &pbkdf_vector.derived_key, WRITER_BIN},		FLAG_OP_AFT},
	};
	const struct json_testresult pbkdf_testresult =
		SET_ARRAY(pbkdf_testresult_entries, &pbkdf_callbacks);

	const struct json_entry pbkdf_test_entries[] = {
		{"keyLen",		{.data.integer = &pbkdf_vector.derived_key_length, PARSER_UINT}, FLAG_OP_AFT},
		{"salt",		{.data.buf = &pbkdf_vector.salt, PARSER_BIN},			FLAG_OP_AFT},
		{"password",		{.data.buf = &pbkdf_vector.password, PARSER_STRING},		FLAG_OP_AFT},
		{"iterationCount",	{.data.integer = &pbkdf_vector.iteration_count, PARSER_UINT},	FLAG_OP_AFT},
	};

	/* search for empty arrays */
	const struct json_array pbkdf_test = SET_ARRAY(pbkdf_test_entries, &pbkdf_testresult);

	const struct json_entry pbkdf_testgroup_entries[] = {
		{"hmacAlg",		{.data.largeint = &pbkdf_vector.hash, PARSER_CIPHER},	FLAG_OP_AFT},
		{"tests",		{.data.array = &pbkdf_test, PARSER_ARRAY},			FLAG_OP_AFT},
	};
	const struct json_array pbkdf_testgroup = SET_ARRAY(pbkdf_testgroup_entries, NULL);

	/**********************************************************************
	 * KDF common test group
	 **********************************************************************/
	const struct json_entry pbkdf_testanchor_entries[] = {
		{"testGroups",			{.data.array = &pbkdf_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array pbkdf_testanchor = SET_ARRAY(pbkdf_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&pbkdf_testanchor, "1.0", in, out);
}

static struct cavs_tester pbkdf =
{
	ACVP_PBKDF,
	0,
	kdf_tester_pbkdf,
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_pbkdf)
static void register_pbkdf(void)
{
	register_tester(&pbkdf, "PBKDF");
}

void register_pbkdf_impl(struct pbkdf_backend *implementation)
{
	register_backend(pbkdf_backend, implementation, "PBKDF");
}
