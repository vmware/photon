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

#include "stringhelper.h"
#include "binhexbin.h"
#include "logger.h"

#include "parser_common.h"
#include "parser_ecdsa.h"

#define ECDSA_DEF_CALLBACK(name, flags)		DEF_CALLBACK(ecdsa, name, flags)
#define ECDSA_DEF_CALLBACK_HELPER(name, flags, helper)			       \
				DEF_CALLBACK_HELPER(ecdsa, name, flags, helper)

static struct ecdsa_backend *ecdsa_backend = NULL;

struct ecdsa_static_key {
	void *key;
	uint64_t curve;
	struct buffer Qx;
	struct buffer Qy;
};
static struct ecdsa_static_key ecdsa_key = { NULL, 0, {NULL, 0}, {NULL, 0} };

static void ecdsa_key_free(struct ecdsa_static_key *key)
{
	if (key->key)
		ecdsa_backend->ecdsa_free_key(key->key);
	key->key = NULL;
	key->curve = 0;

	free_buf(&key->Qx);
	free_buf(&key->Qy);
}

static void ecdsa_key_free_static(void)
{
	ecdsa_key_free(&ecdsa_key);
}

static int ecdsa_duplicate_buf(const struct buffer *src, struct buffer *dst)
{
	int ret;

	CKINT(alloc_buf(src->len, dst));
	memcpy(dst->buf, src->buf, dst->len);

out:
	return ret;
}

static int ecdsa_siggen_keygen(struct ecdsa_siggen_data *data,
			       void **ecdsa_privkey)
{
	int ret = 0;

	if ((ecdsa_key.curve != (data->cipher & ACVP_CURVEMASK)) ||
	    !ecdsa_key.key) {
		ecdsa_key_free_static();
		CKINT(ecdsa_backend->ecdsa_keygen_en(data->cipher, &data->Qx,
						     &data->Qy,
						     &ecdsa_key.key));

		logger_binary(LOGGER_DEBUG, data->Qx.buf, data->Qx.len,
			      "ECDSA generated Qx");
		logger_binary(LOGGER_DEBUG, data->Qy.buf, data->Qy.len,
			      "ECDSA generated Qy");

		/* Free the global variable at exit */
		atexit(ecdsa_key_free_static);

		CKINT(ecdsa_duplicate_buf(&data->Qx, &ecdsa_key.Qx));
		CKINT(ecdsa_duplicate_buf(&data->Qy, &ecdsa_key.Qy));
		ecdsa_key.curve = data->cipher & ACVP_CURVEMASK;
	}

	if (!data->Qx.len)
		CKINT(ecdsa_duplicate_buf(&ecdsa_key.Qx, &data->Qx));
	if (!data->Qy.len)
		CKINT(ecdsa_duplicate_buf(&ecdsa_key.Qy, &data->Qy));

	*ecdsa_privkey = ecdsa_key.key;

out:
	return ret;
}

static int ecdsa_siggen_helper(const struct json_array *processdata,
			     flags_t parsed_flags,
			     struct json_object *testvector,
			     struct json_object *testresults,
	int (*callback)(struct ecdsa_siggen_data *vector, flags_t parsed_flags),
			struct ecdsa_siggen_data *vector)
{
	int ret;
	void *ecdsa_privkey = NULL;

	(void)processdata;
	(void)testvector;
	(void)testresults;

	if (ecdsa_backend->ecdsa_keygen_en && ecdsa_backend->ecdsa_free_key) {
		CKINT(ecdsa_siggen_keygen(vector, &ecdsa_privkey));
	}

	vector->privkey = ecdsa_privkey;

	CKINT(callback(vector, parsed_flags));

out:
	return ret;
}

void ecdsa_get_bufferlen(uint64_t curve, size_t *dlen,
			 size_t *xlen, size_t *ylen)
{
	switch (curve & ACVP_CURVEMASK) {
		case ACVP_NISTB163:
		case ACVP_NISTK163:
			*xlen = 163 / 8 + 1;
			*dlen = *xlen;
			*ylen = *xlen;
			break;
		case ACVP_NISTB233:
		case ACVP_NISTK233:
			*xlen = 233 / 8 + 1;
			*dlen = *xlen;
			*ylen = *xlen;
			break;
		case ACVP_NISTB283:
		case ACVP_NISTK283:
			*xlen = 283 / 8 + 1;
			*dlen = *xlen;
			*ylen = *xlen;
			break;
		case ACVP_NISTB409:
		case ACVP_NISTK409:
			*xlen = 409 / 8 + 1;
			*dlen = *xlen;
			*ylen = *xlen;
			break;
		case ACVP_NISTB571:
		case ACVP_NISTK571:
			*xlen = 571 / 8 + 1;
			*dlen = *xlen;
			*ylen = *xlen;
			break;
		case ACVP_NISTP192:
			*xlen = 192 / 8;
			*dlen = *xlen;
			*ylen = *xlen;
			break;
		case ACVP_NISTP224:
			*xlen = 224 / 8;
			*dlen = *xlen;
			*ylen = *xlen;
			break;
		case ACVP_NISTP256:
			*xlen = 256 / 8;
			*dlen = *xlen;
			*ylen = *xlen;
			break;
		case ACVP_NISTP384:
			*xlen = 384 / 8;
			*dlen = *xlen;
			*ylen = *xlen;
			break;
		case ACVP_NISTP521:
			*dlen = 66;
			*xlen = 66;
			*ylen = 66;
			break;
		default:
			logger(LOGGER_WARN,
			       "ECDSA: Unknown curve to determine bufferlen\n");
			break;
	}
}

static int ecdsa_tester(struct json_object *in, struct json_object *out,
			uint64_t cipher)
{
	(void)cipher;

	if (!ecdsa_backend) {
		logger(LOGGER_WARN, "No ECDSA backend set\n");
		return -EOPNOTSUPP;
	}

	/**********************************************************************
	 * ECDSA key generation with extra entropy (FIPS 186-4 B.4.1)
	 **********************************************************************/
	struct ecdsa_keygen_extra_data ecdsa_keygen_extra_vector;
	const struct ecdsa_keygen_extra_callback ecdsa_keygen_extra =
		{ecdsa_backend->ecdsa_keygen_extra, &ecdsa_keygen_extra_vector, NULL};

	/**********************************************************************
	 * ECDSA key generation by testing candidates (FIPS 186-4 B.4.2)
	 **********************************************************************/
	struct ecdsa_keygen_data ecdsa_keygen_vector;

	const struct ecdsa_keygen_callback ecdsa_keygen =
		{ecdsa_backend->ecdsa_keygen, &ecdsa_keygen_vector, NULL};

	const struct json_callback ecdsa_keygen_callback[] = {
		{ .callback.ecdsa_keygen = ecdsa_keygen, CB_TYPE_ecdsa_keygen, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING },
		{ .callback.ecdsa_keygen_extra = ecdsa_keygen_extra, CB_TYPE_ecdsa_keygen_extra, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS },
	};
	const struct json_callbacks ecdsa_keygen_callbacks =
				SET_CALLBACKS(ecdsa_keygen_callback);
	memset(&ecdsa_keygen_vector, 0, sizeof(ecdsa_keygen_vector));
	memset(&ecdsa_keygen_extra_vector, 0, sizeof(ecdsa_keygen_extra_vector));

	const struct json_entry ecdsa_keygen_testresult_entries[] = {
		{"qx",		{.data.buf = &ecdsa_keygen_vector.Qx, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING},
		{"qy",		{.data.buf = &ecdsa_keygen_vector.Qy, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING},
		{"d",		{.data.buf = &ecdsa_keygen_vector.d, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING},

		{"qx",		{.data.buf = &ecdsa_keygen_extra_vector.Qx, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS},
		{"qy",		{.data.buf = &ecdsa_keygen_extra_vector.Qy, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS},
		{"d",		{.data.buf = &ecdsa_keygen_extra_vector.d, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS},
	};
	const struct json_testresult ecdsa_keygen_testresult =
	SET_ARRAY(ecdsa_keygen_testresult_entries, &ecdsa_keygen_callbacks);

	/* search for empty arrays */
	const struct json_array ecdsa_keygen_test = {NULL, 0, &ecdsa_keygen_testresult};

	const struct json_entry ecdsa_keygen_testgroup_entries[] = {
		{"curve",	{.data.largeint = &ecdsa_keygen_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING },
		{"curve",	{.data.largeint = &ecdsa_keygen_extra_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS},
		{"tests",	{.data.array = &ecdsa_keygen_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS},
	};
	const struct json_array ecdsa_keygen_testgroup = SET_ARRAY(ecdsa_keygen_testgroup_entries, NULL);

	/**********************************************************************
	 * ECDSA PKV verification
	 **********************************************************************/
	ECDSA_DEF_CALLBACK(ecdsa_pkvver, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS);

	const struct json_entry ecdsa_pkvver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdsa_pkvver_vector.keyver_success, WRITER_BOOL},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS},
	};
	const struct json_testresult ecdsa_pkvver_testresult = SET_ARRAY(ecdsa_pkvver_testresult_entries, &ecdsa_pkvver_callbacks);

	const struct json_entry ecdsa_pkvver_test_entries[] = {
		{"qx",		{.data.buf = &ecdsa_pkvver_vector.Qx, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS},
		{"qy",		{.data.buf = &ecdsa_pkvver_vector.Qy, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS},
	};

	/* search for empty arrays */
	const struct json_array ecdsa_pkvver_test = SET_ARRAY(ecdsa_pkvver_test_entries, &ecdsa_pkvver_testresult);

	const struct json_entry ecdsa_pkvver_testgroup_entries[] = {
		{"curve",	{.data.largeint = &ecdsa_pkvver_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS },
		{"tests",	{.data.array = &ecdsa_pkvver_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING | FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS },
	};
	const struct json_array ecdsa_pkvver_testgroup = SET_ARRAY(ecdsa_pkvver_testgroup_entries, NULL);

	/**********************************************************************
	 * ECDSA signature generation
	 **********************************************************************/
	ECDSA_DEF_CALLBACK_HELPER(ecdsa_siggen,
				  FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN,
				  ecdsa_siggen_helper);

	const struct json_entry ecdsa_siggen_testresult_entries[] = {
		{"r",		{.data.buf = &ecdsa_siggen_vector.R, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"s",		{.data.buf = &ecdsa_siggen_vector.S, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	const struct json_testresult ecdsa_siggen_testresult = SET_ARRAY(ecdsa_siggen_testresult_entries, &ecdsa_siggen_callbacks);

	const struct json_entry ecdsa_siggen_test_entries[] = {
		{"message",		{.data.buf = &ecdsa_siggen_vector.msg, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
	};

	const struct json_entry ecdsa_siggen_testgroup_result_entries[] = {
		{"qx",		{.data.buf = &ecdsa_siggen_vector.Qx, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"qy",		{.data.buf = &ecdsa_siggen_vector.Qy, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	/*
	 * The NULL for the function callbacks implies that the qx and qy
	 * are printed at the same hierarchy level as tgID
	 */
	const struct json_testresult ecdsa_siggen_testgroup_result = SET_ARRAY(ecdsa_siggen_testgroup_result_entries, NULL);

	/* search for empty arrays */
	const struct json_array ecdsa_siggen_test = SET_ARRAY(ecdsa_siggen_test_entries, &ecdsa_siggen_testresult);

	const struct json_entry ecdsa_siggen_testgroup_entries[] = {
		{"curve",	{.data.largeint = &ecdsa_siggen_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"hashAlg",	{.data.largeint = &ecdsa_siggen_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"componentTest",	{.data.integer = &ecdsa_siggen_vector.component, PARSER_BOOL},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN | FLAG_OPTIONAL},
		{"tests",	{.data.array = &ecdsa_siggen_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	const struct json_array ecdsa_siggen_testgroup = SET_ARRAY(ecdsa_siggen_testgroup_entries,
		  &ecdsa_siggen_testgroup_result);

	/**********************************************************************
	 * ECDSA signature verification
	 **********************************************************************/
	ECDSA_DEF_CALLBACK(ecdsa_sigver, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER);

	const struct json_entry ecdsa_sigver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &ecdsa_sigver_vector.sigver_success, WRITER_BOOL},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
	};
	const struct json_testresult ecdsa_sigver_testresult = SET_ARRAY(ecdsa_sigver_testresult_entries, &ecdsa_sigver_callbacks);

	const struct json_entry ecdsa_sigver_test_entries[] = {
		{"message",	{.data.buf = &ecdsa_sigver_vector.msg, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
		{"qx",		{.data.buf = &ecdsa_sigver_vector.Qx, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
		{"qy",		{.data.buf = &ecdsa_sigver_vector.Qy, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
		{"r",		{.data.buf = &ecdsa_sigver_vector.R, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
		{"s",		{.data.buf = &ecdsa_sigver_vector.S, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
	};

	/* search for empty arrays */
	const struct json_array ecdsa_sigver_test = SET_ARRAY(ecdsa_sigver_test_entries, &ecdsa_sigver_testresult);

	const struct json_entry ecdsa_sigver_testgroup_entries[] = {
		{"curve",	{.data.largeint = &ecdsa_sigver_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
		{"hashAlg",	{.data.largeint = &ecdsa_sigver_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
		{"componentTest",	{.data.integer = &ecdsa_sigver_vector.component, PARSER_BOOL},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER | FLAG_OPTIONAL},
		{"tests",	{.data.array = &ecdsa_sigver_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
	};
	const struct json_array ecdsa_sigver_testgroup = SET_ARRAY(ecdsa_sigver_testgroup_entries, NULL);

	/**********************************************************************
	 * ECDSA common test group
	 **********************************************************************/
	const struct json_entry ecdsa_testanchor_entries[] = {
		{"testGroups",	{.data.array = &ecdsa_keygen_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OP_ECDSA_SECRETGENTYPE_TESTING},
		{"testGroups",	{.data.array = &ecdsa_pkvver_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_KEYVER},
		{"testGroups",	{.data.array = &ecdsa_siggen_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_SIGGEN},
		{"testGroups",	{.data.array = &ecdsa_sigver_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_SIGVER},
	};
	const struct json_array ecdsa_testanchor = SET_ARRAY(ecdsa_testanchor_entries, NULL);


	/**********************************************************************
	 * ECDSA signature generation for test vector generation
	 **********************************************************************/
	const struct json_entry gen_ecdsa_siggen_testresult_entries[] = {
		{"r",		{.data.buf = &ecdsa_siggen_vector.R, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"s",		{.data.buf = &ecdsa_siggen_vector.S, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"qx",		{.data.buf = &ecdsa_siggen_vector.Qx, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
		{"qy",		{.data.buf = &ecdsa_siggen_vector.Qy, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
		{"message",	{.data.buf = &ecdsa_siggen_vector.msg, WRITER_BIN },
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
	};
	const struct json_testresult gen_ecdsa_siggen_testresult = SET_ARRAY(gen_ecdsa_siggen_testresult_entries, &ecdsa_siggen_callbacks);

	const struct json_entry gen_ecdsa_siggen_test_entries[] = {
		{"message",		{.data.buf = &ecdsa_siggen_vector.msg, PARSER_BIN},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
	};

	const struct json_entry gen_ecdsa_siggen_testgroup_result_entries[] = {
		{"qx",		{.data.buf = &ecdsa_siggen_vector.Qx, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"qy",		{.data.buf = &ecdsa_siggen_vector.Qy, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"curve",	{.data.largeint = &ecdsa_siggen_vector.cipher, WRITER_ECC},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
		{"hashAlg",	{.data.largeint = &ecdsa_siggen_vector.cipher, WRITER_HASH},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
	};
	/*
	 * The NULL for the function callbacks implies that the qx and qy
	 * are printed at the same hierarchy level as tgID
	 */
	const struct json_testresult gen_ecdsa_siggen_testgroup_result = SET_ARRAY(gen_ecdsa_siggen_testgroup_result_entries, NULL);

	/* search for empty arrays */
	const struct json_array gen_ecdsa_siggen_test = SET_ARRAY(gen_ecdsa_siggen_test_entries, &gen_ecdsa_siggen_testresult);

	const struct json_entry gen_ecdsa_siggen_testgroup_entries[] = {
		{"curve",	{.data.largeint = &ecdsa_siggen_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"hashAlg",	{.data.largeint = &ecdsa_siggen_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"componentTest",	{.data.integer = &ecdsa_siggen_vector.component, PARSER_BOOL},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN | FLAG_OPTIONAL},
		{"tests",	{.data.array = &gen_ecdsa_siggen_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	const struct json_array gen_ecdsa_siggen_testgroup = SET_ARRAY(gen_ecdsa_siggen_testgroup_entries, 		  &gen_ecdsa_siggen_testgroup_result);

	/**********************************************************************
	 * ECDSA common test group
	 **********************************************************************/
	struct buffer ecdsa_algo = { .buf = (unsigned char *)"ECDSA",
				     .len = 5 };
	struct buffer ecdsa_sigver_mode = { .buf = (unsigned char *)"sigVer",
					    .len = 6 };
	struct buffer ecdsa_revision = { .buf = (unsigned char *)"1.0",
					 .len = 6 };
	const struct json_entry gen_ecdsa_testgroup_result_entries[] = {
		{"algorithm",	{.data.buf = &ecdsa_algo,  WRITER_STRING_NOFREE},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"mode",	{.data.buf = &ecdsa_sigver_mode, WRITER_STRING_NOFREE},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"revision",	{.data.buf = &ecdsa_revision, WRITER_STRING_NOFREE},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	/*
	 * The NULL for the function callbacks implies that the qx and qy
	 * are printed at the same hierarchy level as tgID
	 */
	const struct json_testresult gen_ecdsa_testgroup_result = SET_ARRAY(gen_ecdsa_testgroup_result_entries, NULL);

	const struct json_entry gen_ecdsa_testanchor_entries[] = {
		{"testGroups",	{.data.array = &gen_ecdsa_siggen_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_SIGGEN},
	};
	const struct json_array gen_ecdsa_testanchor = SET_ARRAY(gen_ecdsa_testanchor_entries, &gen_ecdsa_testgroup_result);

	/* Process all. */
	if (generate_testvector)
		return process_json(&gen_ecdsa_testanchor, "1.0", in, out);
	else
		return process_json(&ecdsa_testanchor, "1.0", in, out);
}

static struct cavs_tester ecdsa =
{
	ACVP_ECDSA,
	0,
	ecdsa_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_ecdsa)
static void register_ecdsa(void)
{
	register_tester(&ecdsa, "ECDSA");
}

void register_ecdsa_impl(struct ecdsa_backend *implementation)
{
	register_backend(ecdsa_backend, implementation, "ECDSA");
}
