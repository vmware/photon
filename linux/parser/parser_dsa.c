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

#define DSA_DEF_CALLBACK(name, flags)		DEF_CALLBACK(dsa, name, flags)
#define DSA_DEF_CALLBACK_HELPER(name, flags, helper)			       \
				DEF_CALLBACK_HELPER(dsa, name, flags, helper)

static struct dsa_backend *dsa_backend = NULL;

static int dsa_pqggen_helper(struct dsa_pqggen_data *pqg, flags_t parsed_flags)
{
	if (pqg->safeprime)
		return 0;

	if (!dsa_backend->dsa_pqggen) {
		logger(LOGGER_ERR, "dsa_pqggen backend missing!\n");
		return -EOPNOTSUPP;
	}

	if (pqg->P.len != pqg->L / 8 ||
	    pqg->Q.len != pqg->N / 8 ||
	    pqg->G.len != pqg->L / 8) {
		int ret;

		switch (pqg->N) {
		case 160:
			pqg->cipher = ACVP_SHA1;
			break;
		case 224:
			pqg->cipher = ACVP_SHA224;
			break;
		case 256:
			pqg->cipher = ACVP_SHA256;
			break;
		default:
			logger(LOGGER_ERR, "Unknown N value %u\n", pqg->N);
			return -EINVAL;
		}

		free_buf(&pqg->P);
		free_buf(&pqg->Q);
		free_buf(&pqg->G);

		ret = dsa_backend->dsa_pqggen(pqg, parsed_flags);

		left_pad_buf(&pqg->P, pqg->L / 8);
		left_pad_buf(&pqg->Q, pqg->N / 8);
		left_pad_buf(&pqg->G, pqg->L / 8);

		return ret;
	}

	return 0;
}

static int dsa_keygen_helper(const struct json_array *processdata,
			     flags_t parsed_flags,
			     struct json_object *testvector,
			     struct json_object *testresults,
	int (*callback)(struct dsa_keygen_data *vector, flags_t parsed_flags),
			struct dsa_keygen_data *vector)
{
	int ret;

	(void)processdata;
	(void)testvector;
	(void)testresults;

	CKINT(dsa_pqggen_helper(&vector->pqg, parsed_flags));

	CKINT(callback(vector, parsed_flags));

out:
	return ret;
}

struct dsa_static_key {
	void *key;
	struct buffer Y;
	struct dsa_pqggen_data pqg;
};
static struct dsa_static_key dsa_key = { NULL, { NULL, 0 },
					 { 0, 0, 0, 0, { NULL, 0 }, { NULL, 0 },
					  { NULL, 0 }} };

static void dsa_key_free(struct dsa_static_key *key)
{
	if (key->key)
		dsa_backend->dsa_free_key(key->key);
	key->key = NULL;
	key->pqg.L = 0;
	key->pqg.N = 0;
	key->pqg.cipher = 0;

	free_buf(&key->Y);
	free_buf(&key->pqg.P);
	free_buf(&key->pqg.Q);
	free_buf(&key->pqg.G);
}

static void dsa_key_free_static(void)
{
	dsa_key_free(&dsa_key);
}

static int dsa_duplicate_buf(const struct buffer *src, struct buffer *dst)
{
	int ret;

	CKINT(alloc_buf(src->len, dst));
	memcpy(dst->buf, src->buf, dst->len);

out:
	return ret;
}

static int dsa_siggen_keygen(struct dsa_siggen_data *data, void **dsa_privkey,
			     flags_t parsed_flags)
{
	struct dsa_pqggen_data *pqg = &data->pqg;
	struct dsa_pqggen_data *preserved_pqg = &dsa_key.pqg;
	int ret = 0;

	if ((preserved_pqg->N != pqg->N) || (preserved_pqg->L != pqg->L) ||
	    (preserved_pqg->cipher != (data->cipher & ACVP_HASHMASK)) ||
	    !dsa_key.key) {
		dsa_key_free_static();

		CKINT(dsa_pqggen_helper(&data->pqg, parsed_flags));

		CKINT(dsa_backend->dsa_keygen_en(pqg, &data->Y, &dsa_key.key));

		logger_binary(LOGGER_DEBUG, data->Y.buf, data->Y.len,
			      "DSA generated Y");

		/* Free the global variable at exit */
		atexit(dsa_key_free_static);

		CKINT(dsa_duplicate_buf(&data->Y, &dsa_key.Y));
		CKINT(dsa_duplicate_buf(&pqg->P, &preserved_pqg->P));
		CKINT(dsa_duplicate_buf(&pqg->Q, &preserved_pqg->Q));
		CKINT(dsa_duplicate_buf(&pqg->G, &preserved_pqg->G));
		preserved_pqg->L = pqg->L;
		preserved_pqg->N = pqg->N;
		preserved_pqg->cipher = (data->cipher & ACVP_HASHMASK);
	}

	if (!data->Y.len)
		CKINT(dsa_duplicate_buf(&dsa_key.Y, &data->Y));
	if (!pqg->P.len)
		CKINT(dsa_duplicate_buf(&preserved_pqg->P, &pqg->P));
	if (!pqg->Q.len)
		CKINT(dsa_duplicate_buf(&preserved_pqg->Q, &pqg->Q));
	if (!pqg->G.len)
		CKINT(dsa_duplicate_buf(&preserved_pqg->G, &pqg->G));

	*dsa_privkey = dsa_key.key;

out:
	return ret;
}

static int dsa_siggen_helper(const struct json_array *processdata,
			     flags_t parsed_flags,
			     struct json_object *testvector,
			     struct json_object *testresults,
	int (*callback)(struct dsa_siggen_data *vector, flags_t parsed_flags),
			struct dsa_siggen_data *vector)
{
	int ret;
	void *dsa_privkey = NULL;

	(void)processdata;
	(void)testvector;
	(void)testresults;

	if (dsa_backend->dsa_keygen_en && dsa_backend->dsa_free_key) {
		CKINT(dsa_siggen_keygen(vector, &dsa_privkey, parsed_flags));
	}

	vector->privkey = dsa_privkey;

	CKINT(callback(vector, parsed_flags));

out:
	return ret;
}

static int dsa_tester(struct json_object *in, struct json_object *out,
		      uint64_t cipher)
{
	(void)cipher;

	if (!dsa_backend) {
		logger(LOGGER_WARN, "No DSA backend set\n");
		return -EOPNOTSUPP;
	}

	/**********************************************************************
	 * DSA PQG generation and verification
	 **********************************************************************/
	DSA_DEF_CALLBACK(dsa_pqg, FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PQG_TYPES_MASK);

	const struct json_entry dsa_pqg_testresult_entries[] = {
		/* PQ generation with probable and provable primes */
		{"p",		{.data.buf = &dsa_pqg_vector.P, WRITER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROBABLE_PQ_GEN | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"q",		{.data.buf = &dsa_pqg_vector.Q, WRITER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROBABLE_PQ_GEN | FLAG_OP_DSA_PROVABLE_PQ_GEN},

		/* PQ generation with probable primes */
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.pq_prob_domain_param_seed, WRITER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROBABLE_PQ_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.domainseed, WRITER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROBABLE_PQ_GEN},
		{"counter",	{.data.integer = &dsa_pqg_vector.pq_prob_counter, WRITER_UINT},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROBABLE_PQ_GEN},

		/* PQ generation with provable primes */
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.pq_prov_firstseed, WRITER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.domainseed, WRITER_BIN},		FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"pSeed",	{.data.buf = &dsa_pqg_vector.pq_prov_pseed, WRITER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"qSeed",	{.data.buf = &dsa_pqg_vector.pq_prov_qseed, WRITER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"pCounter",	{.data.integer = &dsa_pqg_vector.pq_prov_pcounter, WRITER_UINT},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"qCounter",	{.data.integer = &dsa_pqg_vector.pq_prov_qcounter, WRITER_UINT},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROVABLE_PQ_GEN},

		/* canonical and unverifiable G generation */
		{"g",		{.data.buf = &dsa_pqg_vector.G, WRITER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_UNVERIFIABLE_G_GEN | FLAG_OP_DSA_CANONICAL_G_GEN},

		/* PQG verification */
		{"testPassed",	{.data.integer = &dsa_pqg_vector.pqgver_success, WRITER_BOOL},
			         FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER |FLAG_OP_DSA_PQG_TYPES_MASK},
	};

	const struct json_testresult dsa_pqg_testresult =
	SET_ARRAY(dsa_pqg_testresult_entries, &dsa_pqg_callbacks);

	const struct json_entry dsa_pqg_test_entries[] = {
		/* canonical and unverifiable G generation */
		{"p",		{.data.buf = &dsa_pqg_vector.P, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_UNVERIFIABLE_G_GEN | FLAG_OP_DSA_CANONICAL_G_GEN},
		{"q",		{.data.buf = &dsa_pqg_vector.Q, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_UNVERIFIABLE_G_GEN | FLAG_OP_DSA_CANONICAL_G_GEN},

		/* canonical G generation */
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.g_canon_domain_param_seed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_CANONICAL_G_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.domainseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_CANONICAL_G_GEN},
		{"index",	{.data.buf = &dsa_pqg_vector.g_canon_index, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_CANONICAL_G_GEN},

		/* PQ verification for probable and provable primes */
		/* canonical and unverifiable G verification */
		{"p",		{.data.buf = &dsa_pqg_vector.P, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PQG_TYPES_MASK},
		{"q",		{.data.buf = &dsa_pqg_vector.Q, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PQG_TYPES_MASK},

		/* PQ verification with probable primes */
		{"counter",	{.data.integer = &dsa_pqg_vector.pq_prob_counter, PARSER_UINT},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROBABLE_PQ_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.pq_prob_domain_param_seed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROBABLE_PQ_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.domainseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROBABLE_PQ_GEN},

		/* PQ verification with provable primes */
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.pq_prov_firstseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.domainseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"pSeed",	{.data.buf = &dsa_pqg_vector.pq_prov_pseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"qSeed",	{.data.buf = &dsa_pqg_vector.pq_prov_qseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"pCounter",	{.data.integer = &dsa_pqg_vector.pq_prov_pcounter, PARSER_UINT},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROVABLE_PQ_GEN},
		{"qCounter",	{.data.integer = &dsa_pqg_vector.pq_prov_qcounter, PARSER_UINT},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROVABLE_PQ_GEN},

		/* canonical and unverifiable G verification */
		{"g",		{.data.buf = &dsa_pqg_vector.G, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_CANONICAL_G_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.pq_prov_firstseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_CANONICAL_G_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.domainseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_CANONICAL_G_GEN},
		{"index",	{.data.buf = &dsa_pqg_vector.g_canon_index, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_CANONICAL_G_GEN},

		/* unverifiable G verification */
		{"g",		{.data.buf = &dsa_pqg_vector.G, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_UNVERIFIABLE_G_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.g_unver_domain_param_seed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_UNVERIFIABLE_G_GEN | FLAG_OPTIONAL},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.domainseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_UNVERIFIABLE_G_GEN | FLAG_OPTIONAL},
		{"h",		{.data.buf = &dsa_pqg_vector.g_unver_h, PARSER_STRING},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_UNVERIFIABLE_G_GEN | FLAG_OPTIONAL},

		/* canonical G verification */
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.g_canon_domain_param_seed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_CANONICAL_G_GEN},
		{"domainSeed",	{.data.buf = &dsa_pqg_vector.domainseed, PARSER_BIN},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_CANONICAL_G_GEN},
		{"index",	{.data.buf = &dsa_pqg_vector.g_canon_index, PARSER_BIN},	FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_CANONICAL_G_GEN},
	};

	const struct json_array dsa_pqg_test = SET_ARRAY(dsa_pqg_test_entries, &dsa_pqg_testresult);

	const struct json_entry dsa_pqg_testgroup_entries[] = {
		{"l",	{.data.integer = &dsa_pqg_vector.L, PARSER_UINT},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PQG_TYPES_MASK},
		{"n",	{.data.integer = &dsa_pqg_vector.N, PARSER_UINT},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PQG_TYPES_MASK },
		{"hashAlg",	{.data.largeint = &dsa_pqg_vector.cipher, PARSER_CIPHER},	FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PQG_TYPES_MASK },
		{"tests",	{.data.array = &dsa_pqg_test, PARSER_ARRAY},		FLAG_OP_GDT | FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PQG_TYPES_MASK},
	};

	const struct json_array dsa_pqg_testgroup = SET_ARRAY(dsa_pqg_testgroup_entries, NULL);

	/**********************************************************************
	 * DSA key generation
	 **********************************************************************/
	DSA_DEF_CALLBACK_HELPER(dsa_keygen,
				FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN,
				dsa_keygen_helper);

	const struct json_entry dsa_keygen_testresult_entries[] = {
		{"x",		{.data.buf = &dsa_keygen_vector.X, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN},
		{"y",		{.data.buf = &dsa_keygen_vector.Y, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN},
	};
	const struct json_testresult dsa_keygen_testresult =
	SET_ARRAY(dsa_keygen_testresult_entries, &dsa_keygen_callbacks);

	const struct json_array dsa_keygen_test =
					{ NULL, 0, &dsa_keygen_testresult};

	const struct json_entry dsa_keygen_testgroup_entries[] = {
		/* L, N are provided for SP800-56A rev 1 / FIPS 186-4 keygen */
		{"l",	{.data.integer = &dsa_keygen_vector.pqg.L, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OPTIONAL},
		{"n",	{.data.integer = &dsa_keygen_vector.pqg.N, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OPTIONAL},

		/* safeprime cipher is provided for SP800-56A rev 3 keygen */
		{"safePrimeGroup",	{.data.largeint = &dsa_keygen_vector.pqg.safeprime, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OPTIONAL},

		{"tests",	{.data.array = &dsa_keygen_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN},
	};

	const struct json_entry dsa_keygen_testgroup_result_entries[] = {
		/* P, Q, G are provided for SP800-56A rev 1 / FIPS 186-4 */
		{"p",		{.data.buf = &dsa_keygen_vector.pqg.P, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OPTIONAL},
		{"q",		{.data.buf = &dsa_keygen_vector.pqg.Q, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OPTIONAL},
		{"g",		{.data.buf = &dsa_keygen_vector.pqg.G, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYGEN | FLAG_OPTIONAL},
	};
	/*
	 * The NULL for the function callbacks implies that the n and e
	 * are printed at the same hierarchy level as tgID
	 */
	const struct json_testresult dsa_keygen_testgroup_result = SET_ARRAY(dsa_keygen_testgroup_result_entries, NULL);

	const struct json_array dsa_keygen_testgroup = SET_ARRAY(dsa_keygen_testgroup_entries, &dsa_keygen_testgroup_result);

	/**********************************************************************
	 * DSA key verification (SP800-56A rev 3 safe primes)
	 **********************************************************************/
	DSA_DEF_CALLBACK(dsa_keyver, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER);

	const struct json_entry dsa_keyver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dsa_keyver_vector.keyver_success, WRITER_BOOL},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
	};
	const struct json_testresult dsa_keyver_testresult =
	SET_ARRAY(dsa_keyver_testresult_entries, &dsa_keyver_callbacks);

	const struct json_entry dsa_keyver_test_entries[] = {
		{"x",		{.data.buf = &dsa_keyver_vector.X, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
		{"y",		{.data.buf = &dsa_keyver_vector.Y, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},

		/* P, Q, G are provided for SP800-56A rev 1 / FIPS 186-4 */
		{"p",		{.data.buf = &dsa_keyver_vector.pqg.P, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OPTIONAL},
		{"q",		{.data.buf = &dsa_keyver_vector.pqg.Q, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OPTIONAL},
		{"g",		{.data.buf = &dsa_keyver_vector.pqg.G, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OPTIONAL},
	};

	/* search for empty arrays */
	const struct json_array dsa_keyver_test = SET_ARRAY(dsa_keyver_test_entries, &dsa_keyver_testresult);

	const struct json_entry dsa_keyver_testgroup_entries[] = {
		/* safeprime cipher is provided for SP800-56A rev 3 keygen */
		{"safePrimeGroup",	{.data.largeint = &dsa_keyver_vector.pqg.safeprime, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER | FLAG_OPTIONAL},

		{"tests",	{.data.array = &dsa_keyver_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_KEYVER},
	};

	const struct json_array dsa_keyver_testgroup = SET_ARRAY(dsa_keyver_testgroup_entries, NULL);

	/**********************************************************************
	 * DSA signature generation
	 **********************************************************************/
	DSA_DEF_CALLBACK_HELPER(dsa_siggen,
				FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN,
				dsa_siggen_helper);

	const struct json_entry dsa_siggen_testresult_entries[] = {
		{"r",		{.data.buf = &dsa_siggen_vector.R, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"s",		{.data.buf = &dsa_siggen_vector.S, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	const struct json_testresult dsa_siggen_testresult = SET_ARRAY(dsa_siggen_testresult_entries, &dsa_siggen_callbacks);

	const struct json_entry dsa_siggen_test_entries[] = {
		{"message",	{.data.buf = &dsa_siggen_vector.msg, PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
	};

	/* search for empty arrays */
	const struct json_array dsa_siggen_test = SET_ARRAY(dsa_siggen_test_entries, &dsa_siggen_testresult);

	const struct json_entry dsa_siggen_testgroup_result_entries[] = {
		{"p",		{.data.buf = &dsa_siggen_vector.pqg.P, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
		{"q",		{.data.buf = &dsa_siggen_vector.pqg.Q, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
		{"g",		{.data.buf = &dsa_siggen_vector.pqg.G, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
		{"y",		{.data.buf = &dsa_siggen_vector.Y, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN},
	};
	/*
	 * The NULL for the function callbacks implies that the n and e
	 * are printed at the same hierarchy level as tgID
	 */
	const struct json_testresult dsa_siggen_testgroup_result = SET_ARRAY(dsa_siggen_testgroup_result_entries, NULL);

	const struct json_entry dsa_siggen_testgroup_entries[] = {
		{"l",	{.data.integer = &dsa_siggen_vector.pqg.L, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"n",	{.data.integer = &dsa_siggen_vector.pqg.N, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"hashAlg",	{.data.largeint = &dsa_siggen_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"hashAlg",	{.data.largeint = &dsa_siggen_vector.pqg.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
		{"tests",	{.data.array = &dsa_siggen_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGGEN },
	};
	const struct json_array dsa_siggen_testgroup = SET_ARRAY(dsa_siggen_testgroup_entries, &dsa_siggen_testgroup_result);

	/**********************************************************************
	 * DSA signature verification
	 **********************************************************************/
	DSA_DEF_CALLBACK(dsa_sigver, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER);

	const struct json_entry dsa_sigver_testresult_entries[] = {
		{"testPassed",	{.data.integer = &dsa_sigver_vector.sigver_success, WRITER_BOOL},
			         FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
	};
	const struct json_testresult dsa_sigver_testresult = SET_ARRAY(dsa_sigver_testresult_entries, &dsa_sigver_callbacks);

	const struct json_entry dsa_sigver_test_entries[] = {
		{"message",	{.data.buf = &dsa_sigver_vector.msg, PARSER_BIN},
			        FLAG_OP_AFT |  FLAG_OP_ASYM_TYPE_SIGVER},
		{"y",		{.data.buf = &dsa_sigver_vector.Y, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
		{"r",		{.data.buf = &dsa_sigver_vector.R, PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
		{"s",		{.data.buf = &dsa_sigver_vector.S, PARSER_BIN}, FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
	};

	/* search for empty arrays */
	const struct json_array dsa_sigver_test = SET_ARRAY(dsa_sigver_test_entries, &dsa_sigver_testresult);

	const struct json_entry dsa_sigver_testgroup_entries[] = {
		{"l",	{.data.integer = &dsa_sigver_vector.pqg.L, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
		{"n",	{.data.integer = &dsa_sigver_vector.pqg.N, PARSER_UINT},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
		{"hashAlg",	{.data.largeint = &dsa_sigver_vector.cipher, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
		{"p",		{.data.buf = &dsa_sigver_vector.pqg.P, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
		{"q",		{.data.buf = &dsa_sigver_vector.pqg.Q, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},
		{"g",		{.data.buf = &dsa_sigver_vector.pqg.G, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER},

		{"tests",	{.data.array = &dsa_sigver_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_ASYM_TYPE_SIGVER },
	};
	const struct json_array dsa_sigver_testgroup = SET_ARRAY(dsa_sigver_testgroup_entries, NULL);

	/**********************************************************************
	 * DSA common test group
	 **********************************************************************/
	const struct json_entry dsa_testanchor_entries[] = {
		{"testGroups",	{.data.array = &dsa_pqg_testgroup, PARSER_ARRAY},	FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_TYPE_PQGVER},
		{"testGroups",	{.data.array = &dsa_keygen_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_KEYGEN},
		{"testGroups",	{.data.array = &dsa_keyver_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_KEYVER},
		{"testGroups",	{.data.array = &dsa_siggen_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_SIGGEN},
		{"testGroups",	{.data.array = &dsa_sigver_testgroup, PARSER_ARRAY},	FLAG_OP_ASYM_TYPE_SIGVER},
	};
	const struct json_array dsa_testanchor = SET_ARRAY(dsa_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&dsa_testanchor, "1.0", in, out);
}

static struct cavs_tester dsa =
{
	ACVP_DSA,
	0,
	dsa_tester,	/* process_req */
	NULL
};

static struct cavs_tester safeprimes =
{
	ACVP_SAFEPRIMES,
	0,
	dsa_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_dsa)
static void register_dsa(void)
{
	register_tester(&dsa, "DSA");
	register_tester(&safeprimes, "Safe Primes");
}

void register_dsa_impl(struct dsa_backend *implementation)
{
	register_backend(dsa_backend, implementation, "DSA");
}
