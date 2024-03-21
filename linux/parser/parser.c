/*
 * Copyright (C) 2017 - 2022, Stephan Mueller <smueller@chronox.de>
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

#define _DEFAULT_SOURCE
#include <errno.h>
#include <getopt.h>
#include <string.h>
#include <stdarg.h>

#include "parser.h"
#include "parser_common.h"
#include "logger.h"
#include "read_json.h"
#include "stringhelper.h"
#include "term_colors.h"

/* no locking -> single threaded */
struct cavs_tester *tester = NULL;

int generate_testvector = 0;

static struct main_extension *main_extension = NULL;

#if !defined(NO_MAIN)
void register_main_extension(struct main_extension* extension)
{
	register_backend(main_extension, extension, "main backend");
}
#endif

void register_tester(struct cavs_tester *curr_tester, const char *log)
{
	struct cavs_tester *tmp_tester;

	if (!tester) {
		logger(LOGGER_DEBUG, "Register first executor (%s)\n", log);
		tester = curr_tester;
		return;
	}
	for (tmp_tester = tester;
	     tmp_tester != NULL;
	     tmp_tester = tmp_tester->next) {
		if (!tmp_tester->next) {
			logger(LOGGER_DEBUG, "Register next executor (%s)\n",
			       log);
			tmp_tester->next = curr_tester;
			return;
		}
	}
}

static int test_algo(struct json_object *in, struct json_object *out,
		     const char *algo)
{
	struct cavs_tester *curr_tester;
	uint64_t cipher;
	int ret;

	CKNULL_LOG(tester, -EINVAL, "No text executor registered\n");

	cipher = convert_algo_cipher(algo, 0);
	if (cipher == ACVP_UNKNOWN) {
		logger(LOGGER_ERR, "Unknown cipher %s\n", algo);
		return -EINVAL;
	}

	/* loop through the testers to find a test handler */
	for (curr_tester = tester;
		curr_tester != NULL;
		curr_tester = curr_tester->next) {
		if ((curr_tester->testid && (cipher == curr_tester->testid)) ||
		    (curr_tester->mask && (convert_cipher_contain(cipher,
						curr_tester->mask, 0)))) {
			logger(LOGGER_DEBUG, "Found test executor for %s\n",
			       algo);
			return curr_tester->process_req(in, out, cipher);
		}
	}

	ret = -ENOMSG;

out:
	return ret;
}

static int get_algorithm(struct json_object *obj, const char **algo)
{
	struct json_object *acvpdata, *versiondata;
	int ret;

	*algo = NULL;

	CKINT(json_split_version(obj, &acvpdata, &versiondata));

	CKINT(json_get_string(acvpdata, "algorithm", algo));

out:
	return ret;
}

#if !defined(NO_MAIN)
static int versionstring(char *buf, size_t buflen)
{
	return snprintf(buf, buflen, "ACVPParser/%d.%d.%d",
			MAJVERSION, MINVERSION, PATCHLEVEL);
}
#else
static int versionstring(char *buf, size_t buflen)
{
	(void)buf;
	(void)buflen;
	return 0;
}
#endif

int match_expected_vector(const char *actualfile, const char *expectedfile)
{
	int ret = 0;

	if (json_validate_result(actualfile, expectedfile) ==
	    JSON_VAL_RES_PASS_EXPECTED) {
		if (logger_get_verbosity() >= LOGGER_WARN) {
			fprintf_green(stdout, "[PASSED] ");
			fprintf(stdout,"compare %s with %s\n", actualfile,
			        expectedfile);
		}
		ret = 0;
	} else {
		if (logger_get_verbosity() >= LOGGER_WARN) {
			fprintf_red(stdout, "[FAILED] ");
			fprintf(stdout, "compare %s with %s\n", actualfile,
			        expectedfile);
		}
		ret = -EIO;
	}

	return ret;
}

int perform_testing(const char *infile, const char *outfile)
{
	struct json_object *inobj = NULL, *outobj = NULL;
	int ret;
	const char *algo;

	CKINT(json_read_data(infile, &inobj));
	logger(LOGGER_DEBUG, "Request file %s read successfully\n", infile);

	CKINT(get_algorithm(inobj, &algo))
	logger(LOGGER_DEBUG, "Algorithm %s found in request file %s\n",
	       algo, infile);

	outobj = json_object_new_array();
	CKNULL_LOG(outobj, -ENOMEM,
		   "Cannot create toplevel output JSON object\n");

	ret = test_algo(inobj, outobj, algo);
	if (ret) {
		char filename[FILENAME_MAX];

		snprintf(filename, sizeof(filename), "%s.partial", outfile);
		json_write_data(outobj, filename);
	} else {
		ret = json_write_data(outobj, outfile);
	}

out:
	if (outobj)
		json_object_put(outobj);
	if (inobj)
		json_object_put(inobj);

	return ret;
}

static int validate_result(struct json_object *outobj,
			   struct json_object *expected)
{
	if (json_validate_result_json(outobj, expected) ==
	    JSON_VAL_RES_PASS_EXPECTED) {
		if (logger_get_verbosity() >= LOGGER_WARN) {
			fprintf_green(stdout, "[PASSED] ");
			fprintf(stdout, "regression test match\n");
		}
		return 0;
	} else {
		if (logger_get_verbosity() >= LOGGER_WARN) {
			fprintf_red(stdout, "[FAILED] ");
			fprintf(stdout, "regression test failure\n");
		}
		return -EIO;
	}
}

int perform_testing_regression(const char *infile, const char *expectedfile)
{
	struct json_object *inobj = NULL, *outobj = NULL, *expected = NULL;
	int ret;
	const char *algo;

	CKINT(json_read_data(infile, &inobj));
	logger(LOGGER_DEBUG, "Request file %s read successfully\n", infile);

	CKINT(json_read_data(expectedfile, &expected));
	logger(LOGGER_DEBUG, "Expected data file %s read successfully\n",
	       expectedfile);

	CKINT(get_algorithm(inobj, &algo))
	logger(LOGGER_DEBUG, "Algorithm %s found in request file %s\n",
	       algo, infile);

	outobj = json_object_new_array();
	CKNULL_LOG(outobj, -ENOMEM,
		   "Cannot create toplevel output JSON object\n");

	ret = test_algo(inobj, outobj, algo);
	if (ret) {
		if (logger_get_verbosity() >= LOGGER_WARN) {
			fprintf_red(stdout, "[FAILED] ");
			fprintf(stdout, "Generation of test results failed\n");
		}
		ret = -EIO;
		goto out;
	}

	CKINT(validate_result(outobj, expected));

out:
	if (outobj)
		json_object_put(outobj);
	if (inobj)
		json_object_put(inobj);
	if (expected)
		json_object_put(expected);

	return ret;
}

static int merge_acvp_tests(struct json_object *dst, struct json_object *src,
			    struct json_object *qx, struct json_object *qy,
			    struct json_object *p, struct json_object *q,
			    struct json_object *g, struct json_object *y)
{
	struct json_object_iter src_iter;
	int ret = 0;

	json_object_object_foreachC(src, src_iter) {
		switch (json_object_get_type(src_iter.val)) {
		case json_type_boolean:
		case json_type_double:
		case json_type_int:
		case json_type_null:
		case json_type_string:
			json_object_get(src_iter.val);
			CKINT(json_object_object_add(dst, src_iter.key,
						     src_iter.val));
			break;
		case json_type_object:
		case json_type_array:
		default:
			logger(LOGGER_ERR,
			       "Tests: unknown data type %s for key %s\n",
			       json_type_to_name(json_object_get_type(src_iter.val)),
			       src_iter.key);
		}
	}

	if (qx) {
		CKINT(json_object_object_add(dst, "qx",
			json_object_new_string(json_object_get_string(qx))));
	}
	if (qy) {
		CKINT(json_object_object_add(dst, "qy",
			json_object_new_string(json_object_get_string(qy))));
	}
	if (p) {
		CKINT(json_object_object_add(dst, "p",
			json_object_new_string(json_object_get_string(p))));
	}
	if (q) {
		CKINT(json_object_object_add(dst, "q",
			json_object_new_string(json_object_get_string(q))));
	}
	if (g) {
		CKINT(json_object_object_add(dst, "g",
			json_object_new_string(json_object_get_string(g))));
	}
	if (y) {
		CKINT(json_object_object_add(dst, "y",
			json_object_new_string(json_object_get_string(y))));
	}

out:
	return ret;
}

static int merge_acvp_testgroups(struct json_object *dst,
				 struct json_object *src,
				 char *key, char *val)
{
	struct json_object *src_tstarray, *dst_tstarray, *qx = NULL, *qy = NULL,
			   *p = NULL, *q = NULL, *g = NULL, *y = NULL;
	struct json_object_iter src_iter;
	size_t i;
	int ret;

	if (key && val) {
		struct json_object *json_replace;

		CKINT_LOG(json_find_key(dst, key, &json_replace,
					json_type_string),
			  "Cannot find replacement key %s\n", key);
		CKINT(json_object_set_string(json_replace, val));
	}

	json_object_object_foreachC(src, src_iter) {
		switch (json_object_get_type(src_iter.val)) {
		case json_type_boolean:
		case json_type_double:
		case json_type_int:
		case json_type_null:
		case json_type_string:
			json_object_get(src_iter.val);
			CKINT(json_object_object_add(dst, src_iter.key,
						     src_iter.val));

			/* Exception for ECDSA */
			if (strlen(src_iter.key) == 2) {
				if (!strncmp(src_iter.key, "qx", 2))
					qx = src_iter.val;
				if (!strncmp(src_iter.key, "qy", 2))
					qy = src_iter.val;
			}

			/* Exception for DSA */
			if (strlen(src_iter.key) == 1) {
				if (!strncmp(src_iter.key, "p", 1))
					p = src_iter.val;
				if (!strncmp(src_iter.key, "q", 1))
					q = src_iter.val;
				if (!strncmp(src_iter.key, "g", 1))
					g = src_iter.val;
				if (!strncmp(src_iter.key, "y", 1))
					y = src_iter.val;
			}
			break;
		case json_type_array:
			if (!strncmp(src_iter.key, "tests", 5))
				continue;
			/* FALLTHROUGH */
		case json_type_object:
		default:
			logger(LOGGER_ERR,
			       "Groups: unknown data type %s for key %s\n",
			       json_type_to_name(json_object_get_type(src_iter.val)),
			       src_iter.key);
			ret = -EINVAL;
			goto out;
		}
	}

	CKINT(json_find_key(src, "tests", &src_tstarray, json_type_array));
	CKINT(json_find_key(dst, "tests", &dst_tstarray, json_type_array));

	if (json_object_array_length(src_tstarray) !=
	    json_object_array_length(dst_tstarray)) {
		logger(LOGGER_ERR, "Arrays do not match\n");
		ret = -EINVAL;
		goto out;
	}

	for (i = 0; i < json_object_array_length(src_tstarray); i++) {
		struct json_object *src_entry =
				json_object_array_get_idx(src_tstarray, i);
		struct json_object *dst_entry =
				json_object_array_get_idx(dst_tstarray, i);

		CKNULL(src_entry, -EFAULT);
		CKNULL(dst_entry, -EFAULT);

		CKINT(merge_acvp_tests(dst_entry, src_entry, qx, qy, p, q, g,
				       y));
	}

out:
	return ret;
}

static int merge_acvp_base(struct json_object *dst, struct json_object *src,
			   char *replace)
{
	struct json_object *dstdata, *dstversiondata, *srcdata, *srcversiondata,
			   *src_tstarray, *dst_tstarray, *json_replace;
	struct json_object_iter src_iter;
	size_t i;
	int ret;
	char *saveptr = NULL, *key, *val, *set_key = NULL, *set_val = NULL;

	key = strtok_r(replace, ":", &saveptr);
	CKNULL_LOG(key, -EINVAL, "Search keyword definition wrong: %s\n",
		   replace);
	val = strtok_r(NULL, ":", &saveptr);
	CKNULL_LOG(val, -EINVAL, "Search value definition wrong: %s\n",
		   replace);

	CKINT(json_split_version(dst, &dstdata, &dstversiondata));
	CKINT(json_split_version(src, &srcdata, &srcversiondata));

	ret = json_find_key(dstdata, key, &json_replace, json_type_string);
	if (ret == -EINVAL) {
		set_key = key;
		set_val = val;
	} else if (ret) {
		goto out;
	} else {
		CKINT(json_object_set_string(json_replace, val));
	}

	json_object_object_foreachC(srcdata, src_iter) {
		switch (json_object_get_type(src_iter.val)) {
		case json_type_string:
		case json_type_boolean:
		case json_type_double:
		case json_type_int:
		case json_type_null:
			json_object_get(src_iter.val);
			CKINT(json_object_object_add(dstdata, src_iter.key,
						     src_iter.val));
			break;
		case json_type_array:
			if (!strncmp(src_iter.key, "testGroups", 10))
				continue;
		/* FALLTHROUGH */
		case json_type_object:
		default:
			logger(LOGGER_ERR,
			       "Base: unknown data type %s for key %s\n",
			       json_type_to_name(json_object_get_type(src_iter.val)),
			       src_iter.key);
			ret = -EINVAL;
			goto out;
		}
	}

	CKINT(json_find_key(srcdata, "testGroups", &src_tstarray,
			    json_type_array));
	CKINT(json_find_key(dstdata, "testGroups", &dst_tstarray,
			    json_type_array));

	if (json_object_array_length(src_tstarray) !=
	    json_object_array_length(dst_tstarray)) {
		logger(LOGGER_ERR, "Arrays do not match\n");
		ret = -EINVAL;
		goto out;
	}

	for (i = 0; i < json_object_array_length(src_tstarray); i++) {
		struct json_object *src_entry =
				json_object_array_get_idx(src_tstarray, i);
		struct json_object *dst_entry =
				json_object_array_get_idx(dst_tstarray, i);

		CKNULL(src_entry, -EFAULT);
		CKNULL(dst_entry, -EFAULT);

		CKINT(merge_acvp_testgroups(dst_entry, src_entry, set_key,
					    set_val));
	}

out:
	return ret;
}

static int check_sig(struct json_object *out)
{
	struct json_object *data, *versiondata, *testgroups;
	size_t i;
	int ret;

	CKINT(json_split_version(out, &data, &versiondata));

	CKINT(json_find_key(data, "testGroups", &testgroups, json_type_array));

	ret = -EINVAL;
	for (i = 0; i < json_object_array_length(testgroups); i++) {
		size_t j;
		struct json_object *tests, *testsobj =
				json_object_array_get_idx(testgroups, i);

		CKNULL_LOG(testsobj, -EFAULT, "testGroups not found\n");

		CKINT(json_find_key(testsobj, "tests", &tests, json_type_array));

		ret = -EINVAL;
		for (j = 0; j < json_object_array_length(tests); j++) {
			uint32_t res;
			struct json_object *testobj =
				json_object_array_get_idx(tests, j);

			CKNULL_LOG(testobj, -EFAULT, "tests object not found\n");

			CKINT(json_get_bool(testobj, "testPassed", &res));
			if (!res) {
				logger(LOGGER_ERR, "Signature check: signature verification falure\n");
				ret = -EINVAL;
				goto out;
			} else {
				ret = 0;
			}
		}
	}

out:
	return ret;
}

static int check_kas(struct json_object *out, struct json_object *request,
		     struct json_object *expected)
{
	struct json_object *data, *versiondata, *testgroups;
	struct json_object *r_data, *r_versiondata, *r_testgroups;
	struct json_object *e_data, *e_versiondata, *e_testgroups;
	size_t i;
	int ret = 0;

	CKINT(json_split_version(out, &data, &versiondata));
	CKINT(json_split_version(request, &r_data, &r_versiondata));
	CKINT(json_split_version(expected, &e_data, &e_versiondata));

	CKINT(json_find_key(data, "testGroups", &testgroups, json_type_array));
	CKINT(json_find_key(r_data, "testGroups", &r_testgroups,
			    json_type_array));
	CKINT(json_find_key(e_data, "testGroups", &e_testgroups,
			    json_type_array));

	if (json_object_array_length(testgroups) !=
	    json_object_array_length(r_testgroups) ||
	    json_object_array_length(testgroups) !=
	    json_object_array_length(e_testgroups)) {
		logger(LOGGER_ERR, "Array size mismatch\n");
		ret = -EINVAL;
		goto out;
	}

	ret = -EINVAL;
	for (i = 0; i < json_object_array_length(testgroups); i++) {
		size_t j;
		struct json_object *tests, *testsobj =
				json_object_array_get_idx(testgroups, i);
		struct json_object *r_tests, *r_testsobj =
				json_object_array_get_idx(r_testgroups, i);
		struct json_object *e_tests, *e_testsobj =
				json_object_array_get_idx(e_testgroups, i);
		const char *testtype;

		CKNULL_LOG(testsobj, -EFAULT, "testGroups not found\n");
		CKNULL_LOG(r_testsobj, -EFAULT, "testGroups not found\n");
		CKNULL_LOG(e_testsobj, -EFAULT, "testGroups not found\n");

		CKINT(json_get_string(r_testsobj, "testType", &testtype));

		CKINT(json_find_key(testsobj, "tests", &tests,
				    json_type_array));
		CKINT(json_find_key(r_testsobj, "tests", &r_tests,
				    json_type_array));
		CKINT(json_find_key(e_testsobj, "tests", &e_tests,
				    json_type_array));

		if (json_object_array_length(tests) !=
		    json_object_array_length(r_tests) ||
		    json_object_array_length(tests) !=
		    json_object_array_length(e_tests)) {
			logger(LOGGER_ERR, "Array size mismatch\n");
			ret = -EINVAL;
			goto out;
		}

		ret = -EINVAL;
		for (j = 0; j < json_object_array_length(tests); j++) {
			uint32_t res, e_res;
			struct json_object *testobj =
				json_object_array_get_idx(tests, j);
			struct json_object *e_testobj =
				json_object_array_get_idx(e_tests, j);

			CKNULL_LOG(testobj, -EFAULT,
				   "tests object not found\n");
			CKNULL_LOG(e_testobj, -EFAULT,
				   "tests object not found\n");

			if (!strncmp(testtype, "VAL", 3)) {
				CKINT(json_get_bool(testobj, "testPassed",
						    &res));
				CKINT(json_get_bool(e_testobj, "testPassed",
						    &e_res));

				if (res != e_res) {
					ret = -EINVAL;
					goto out;
				} else {
					ret = 0;
				}
			} else {
				CKINT(json_get_bool(testobj, "testPassed",
						    &res));
				if (!res) {
					ret = -EINVAL;
					goto out;
				} else {
					ret = 0;
				}
			}
		}
	}

out:
	return ret;
}

/*
 * Regression test for non-known-answer tests
 *
 * Approach: Merge test responses into test vector to have a consolidated
 * JSON structure of both files assuming that the response data contains
 * all input to perform a known-answer test for the respective counterpart
 * crypto operation (e.g. sigGen -> sigVer).
 *
 * After the merger and replacing the keyword (e.g. sigGen -> sigVer), the
 * merged file is processed with the parser and the resulting data is
 * now compared to the expected output or validated (sigVer, pqgVer, keyVer
 * should always contain passing verdicts).
 */
static int merge_acvp(const char *dstfile, const char *srcfile, char *replace)
{
	struct json_object *dst = NULL, *src = NULL, *outobj = NULL;
	int ret;
	const char *algo, *str;

	CKINT(json_read_data(dstfile, &dst));
	logger(LOGGER_DEBUG, "Source file %s read successfully\n", dstfile);

	CKINT(json_read_data(srcfile, &src));
	logger(LOGGER_DEBUG, "Destination data file %s read successfully\n",
	       srcfile);

	CKINT(merge_acvp_base(dst, src, replace));

#if 0
	str = json_object_to_json_string_ext(
		dst, JSON_C_TO_STRING_PRETTY | JSON_C_TO_STRING_NOSLASHESCAPE);
	CKNULL_LOG(str, -EFAULT, "JSON object conversion into string failed\n");
	printf("%s\n", str);
#endif

	CKINT(get_algorithm(dst, &algo))
	logger(LOGGER_DEBUG, "Algorithm %s found in request file %s\n",
	       algo, dstfile);

	outobj = json_object_new_array();
	CKNULL_LOG(outobj, -ENOMEM,
		   "Cannot create toplevel output JSON object\n");

	ret = test_algo(dst, outobj, algo);
	if (ret == -EOPNOTSUPP) {
		logger(LOGGER_ERR,
		       "Generation of test results failed: validation algorithm not implemented\n");
		goto out;
	} else if (ret < 0) {
		logger(LOGGER_ERR, "Generation of test results failed\n");
		goto out;
	}

	/*
	 * Covering:
	 *
	 * --replace "mode:keyVer"
	 *	mode:keyGen -> mode:keyVer
	 *
	 * --replace "mode:sigVer"
	 *	mode:sigGen -> mode:sigVer
	 *
	 * --replace "mode:pgqVer"
	 *	mode:pqgGen -> mode:pqgVer
	 */
	if (!strncmp(algo, "RSA", 3) ||
	    !strncmp(algo, "DSA", 3) ||
	    !strncmp(algo, "ECDSA", 5) ||
	    !strncmp(algo, "EDDSA", 5)) {
		CKINT(check_sig(outobj));

	/*
	 * Covering:
	 *
	 * --replace "ivGen:external"
	 *	ivGen:internal -> ivGen:external
	 */
	} else if (!strncmp(algo, "ACVP-AES-GCM", 12)) {
		ret = validate_result(outobj, src);
		goto out;

	/*
	 * Covering:
	 *
	 * Applicable for KAS-*
	 * --replace testType:VAL
	 *	testType:AFT -> testType:VAL
	 */
	} else if (!strncmp(algo, "KAS-", 4)) {
		struct json_object *request;

		CKINT_LOG(json_read_data(dstfile, &request),
			  "Cannot read file %s\n", dstfile);
		ret = check_kas(outobj, request, src);
		goto out;

	/*
	 * Covering:
	 *
	 * Applicable for SP800-108 - note, the replace would be a noop:
	 * --replace algorithm:KDF
	 */
	} else if (!strncmp(algo, "KDF", 3)) {
		ret = validate_result(outobj, src);
		goto out;

	} else {
		logger(LOGGER_ERR,
		       "Automatic check for algorithm %s not implemented - check manually\n",
		       algo);
		str = json_object_to_json_string_ext(
			outobj,
			JSON_C_TO_STRING_PRETTY | JSON_C_TO_STRING_NOSLASHESCAPE);
		CKNULL_LOG(str, -EFAULT,
			   "JSON object conversion into string failed\n");
		printf("%s\n", str);
	}

out:
	if (dst)
		json_object_put(dst);
	if (src)
		json_object_put(src);
	if (outobj)
		json_object_put(outobj);
	return ret;
}

#ifdef ACVP_PARSER_IUT
#define _ACVP_PARSER_IUT ACVP_PARSER_IUT
#else
#define _ACVP_PARSER_IUT NULL
#endif

static void usage(void)
{
	char version[50];

	versionstring(version, sizeof(version));

	fprintf(stderr, "\nACVP Parser executing the crypto implementation %s\n",
		(_ACVP_PARSER_IUT) ? _ACVP_PARSER_IUT : "(undefined)");
	fprintf(stderr, "\nACVP Parser version: %s\n\n", version);
	fprintf(stderr, "Usage:\n");
	fprintf(stderr, " acvp-parser [OPTIONS] <testvector-request.json> <testvector-response.json>\n");
	fprintf(stderr, " acvp-parser [OPTIONS] -e <expected-response.json> <testvector-response.json>\n\n");
	fprintf(stderr, " acvp-parser [OPTIONS] -r <testvector-request.json> <expected-response.json>\n\n");

	fprintf(stderr, "Options:\n");
	fprintf(stderr, "\t-e --expected\tPerform a JSON matching between the two files\n");
	fprintf(stderr, "\t\t\t\t(return code 0 - both files match)\n");
	fprintf(stderr, "\t\t\t\t(return code 1 - both files mismatch)\n");
	fprintf(stderr, "\t-r --regression\tPerform a JSON regression testing\n");
	fprintf(stderr, "\t-t --testvector\tGenerate testvector\n");

	fprintf(stderr, "\n\t-v --verbose\tVerbose logging, multiple options increase verbosity\n");
	fprintf(stderr, "\t-h --help\tPrint this help information\n");

	if (main_extension && main_extension->usage) {
		fprintf(stderr, "\n");
		main_extension->usage();
	}
}

int main(int argc, char *argv[])
{
	const char *infile, *outfile = NULL;
	char *replace = NULL;
	int ret, expected = 0, regression = 0, c = 0;

#define ACVP_PARSER_WITH_GETOPTLONG

	opterr = 0;

	logger_set_verbosity(LOGGER_ERR);

	while (1) {
		int opt_index = 0;

#ifdef ACVP_PARSER_WITH_GETOPTLONG
		static struct option options[] = {
			{"verbose",		no_argument,		0, 'v'},
			{"expected",		no_argument,		0, 'e'},
			{"regression",		no_argument,		0, 'r'},
			{"testvector",		no_argument,		0, 't'},
			{"help",		no_argument,		0, 'h'},

			{"replace",		required_argument,	0, 0},

			{0, 0, 0, 0}
		};
		c = getopt_long(argc, argv, "verth", options, &opt_index);
#else
		c = getopt(argc, argv, "verth");
#endif
		if (-1 == c)
			break;
		switch (c) {
		case 0:
			switch (opt_index) {
			case 0:
				logger_inc_verbosity();
				break;
			case 1:
				expected = 1;
				break;
			case 2:
				regression = 1;
				break;
			case 3:
				generate_testvector = 1;
				break;
			case 4:
				usage();
				return 0;

			/* replace */
			case 5:
				replace = optarg;
				break;

			default:
				if (main_extension) {
					ret = main_extension->main(argc, argv);
				} else {
					usage();
					ret = -EINVAL;
				}
				goto out;
			}
			break;

		case 'v':
			logger_inc_verbosity();
			break;
		case 'e':
			expected = 1;
			break;
		case 'r':
			regression = 1;
			break;
		case 't':
			generate_testvector = 1;
			break;
		case 'h':
			usage();
			return 0;
		default:
			if (main_extension) {
				ret = main_extension->main(argc, argv);
			} else {
				usage();
				ret = -EINVAL;
			}
			goto out;
		}
	}

	if (expected && regression) {
		logger(LOGGER_ERR, "The options of -r and -e are mutually exclusive\n");
		ret = -EINVAL;
		goto out;
	}

	if (argc != optind + 2) {
		usage();
		ret = -EINVAL;
		goto out;
	}

	infile = argv[optind];
	outfile = argv[optind + 1];

	if (replace) {
		ret = merge_acvp(infile, outfile, replace);
	} else if (expected) {
		ret = match_expected_vector(infile, outfile);
	} else if (regression) {
		ret = perform_testing_regression(infile, outfile);
	} else {
		ret = perform_testing(infile, outfile);
	}

out:
	return -ret;
}
