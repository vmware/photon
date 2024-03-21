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

#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "read_json.h"
#include "parser.h"
#include "logger.h"
#include "stringhelper.h"

void json_logger(enum logger_verbosity severity,
		 struct json_object *jobj, const char *str)
{
	if (!jobj) {
		logger(severity, "%s: (no JSON data)\n", str);
		return;
	}
	
	// JSON_C_TO_STRING_PLAIN
	// JSON_C_TO_STRING_SPACED
	// JSON_C_TO_STRING_PRETTY
	logger(severity, "%s: %s\n", str,
	       json_object_to_json_string_ext(jobj, JSON_C_TO_STRING_PRETTY));
}

int json_find_key(const struct json_object *inobj, const char *name,
		  struct json_object **out, enum json_type type)
{
	if (!json_object_object_get_ex(inobj, name, out)) {
		/*
		 * Use debug level only as optional fields may be searched
		 * for.
		 */
		logger(LOGGER_DEBUG, "JSON field %s does not exist\n", name);
		return -EINVAL;
	}

	if (!json_object_is_type(*out, type)) {
		logger(LOGGER_ERR,
		       "JSON data type %s does not match expected type %s for field %s\n",
		       json_type_to_name(json_object_get_type(*out)),
		       json_type_to_name(type), name);
		return -EINVAL;
	}

	return 0;
}

int json_get_uint_random(const struct json_object *obj, const char *name,
			 uint32_t *integer)
{
	struct json_object *o = NULL;
	const char *string;
	int ret = json_find_key(obj, name, &o, json_type_int);

	if (ret)
		return ret;

	string = json_object_get_string(o);
	if (string && strlen(string)) {
		if (strncmp(string, "random", 6)) {
			unsigned long int tmp = strtoul(string, NULL, 10);
			if (tmp > UINT_MAX) {
				logger(LOGGER_ERR,
				       "String to integer conversion failed for string %s referenced with key %s\n",
				       string, name);
				return 1;
			}
			*integer = (uint32_t)tmp;
		} else {
			/* string of zero means, random value */
			*integer = 0;
		}
	} else {
		logger(LOGGER_ERR,
		       "Integer expected, but empty string returned\n");
		return 1;
	}

	logger(LOGGER_DEBUG, "Found integer %s with value %u", name, *integer);

	return 0;
}

int json_get_uint(const struct json_object *obj, const char *name,
		  uint32_t *integer)
{
	struct json_object *o = NULL;
	int32_t tmp;
	int ret = json_find_key(obj, name, &o, json_type_int);

	if (ret)
		return ret;

	tmp = json_object_get_int(o);
	if (tmp == INT_MAX || tmp < 0)
		return -EINVAL;

	*integer = (uint32_t)tmp;

	logger(LOGGER_DEBUG, "Found integer %s with value %u\n", name, *integer);

	return 0;
}

int json_get_uint64(const struct json_object *obj, const char *name,
		    uint64_t *integer)
{
	struct json_object *o = NULL;
	int64_t tmp;
	int ret = json_find_key(obj, name, &o, json_type_int);

	if (ret)
		return ret;

	tmp = json_object_get_int64(o);
	if (tmp == LONG_MAX || tmp < 0)
		return -EINVAL;

	*integer = (uint64_t)tmp;

	logger(LOGGER_DEBUG, "Found integer %s with value %" PRIu64 "\n", name, *integer);

	return 0;
}

int json_get_bin(const struct json_object *obj, const char *name,
		 struct buffer *buf)
{
	struct json_object *o = NULL;
	const char *hex;
	int ret;

	if (!buf)
		return -EINVAL;

	/* We are not re-filling an already filled buffer */
	if (buf->buf || buf->len)
		return 0;

	ret = json_find_key(obj, name, &o, json_type_string);
	if (ret)
		return ret;

	hex = json_object_get_string(o);

	if (hex) {
		uint32_t hexlen = (uint32_t)strlen(hex);

		if (!hexlen) {
			logger(LOGGER_DEBUG,
			       "Found empty binary data for key %s\n", name);
			return 0;
		} else {
			ret = hex2bin_alloc(hex, hexlen, &buf->buf, &buf->len);

			logger(LOGGER_DEBUG,
			       "Found binary data for key %s with value %s\n",
			       name, hex);
		}
	} else {
		logger(LOGGER_WARN, "Fetching entry for key %s failed\n", name);
		return -EFAULT;
	}

	return ret;
}

int mpint2bin(const char *mpi, uint32_t mpilen, struct buffer *buf)
{
	int ret = 0;

	if (mpilen < 8) {
		logger(LOGGER_WARN, "Incomplete MPINT value\n");
		return -EINVAL;
	} else if (mpilen == 8) {
		logger(LOGGER_DEBUG, "Found empty MPINT value\n");
		return 0;
	} else {
		const struct mpint *mpint = (const struct mpint *)mpi;
		const char *ptr = mpint->value;

		/* Reduce the length of the string by the header */
		mpilen -= (uint32_t)sizeof(mpint->len);

		/* Remove leading zero byte */
		if (mpilen > 2 && mpint->value[0] == 60 &&
			mpint->value[1] == 60) {
			ptr += 2;
			mpilen -= 2;
		}

		ret = hex2bin_alloc(ptr, mpilen, &buf->buf, &buf->len);

		logger(LOGGER_DEBUG,
			"Found binary data with length %u with value %s\n",
			mpilen, mpint->value);
	}

	return ret;
}

int json_get_mpint(const struct json_object *obj, const char *name,
		   struct buffer *buf)
{
	const char *raw;
	struct json_object *o = NULL;
	int ret;

	if (!buf)
		return -EINVAL;

	/* We are not re-filling an already filled buffer */
	if (buf->buf || buf->len)
		return 0;

	ret = json_find_key(obj, name, &o, json_type_string);
	if (ret)
		return ret;

	raw = json_object_get_string(o);

	if (raw) {
		uint32_t hexlen = (uint32_t)strlen(raw);

		CKINT(mpint2bin(raw, hexlen, buf));
	} else {
		ret = -EFAULT;
		logger(LOGGER_WARN, "Fetching entry for key %s failed\n", name);
	}

out:
	return ret;
}

int json_get_bool(const struct json_object *obj, const char *name,
		  uint32_t *integer)
{
	struct json_object *o = NULL;
	int ret = json_find_key(obj, name, &o, json_type_boolean);

	if (ret)
		return ret;

	*integer = (uint32_t)json_object_get_boolean(o);

	return 0;
}

int json_get_string(const struct json_object *obj, const char *name,
		    const char **outbuf)
{
	struct json_object *o = NULL;
	const char *string;
	int ret = json_find_key(obj, name, &o, json_type_string);

	if (ret)
		return ret;

	string = json_object_get_string(o);

	logger(LOGGER_DEBUG, "Found string data %s with value %s\n", name,
	       string);

	*outbuf = string;

	return 0;
}

int json_get_string_buf(const struct json_object *obj, const char *name,
		    	struct buffer *buf)
{
	struct json_object *o = NULL;
	size_t len;
	const char *string;
	int ret = json_find_key(obj, name, &o, json_type_string);

	if (ret)
		return ret;

	string = json_object_get_string(o);

	logger(LOGGER_DEBUG, "Found string data %s with value %s\n", name,
	       string);

	len = strlen(string);
	if (len > INT_MAX)
		return -EINVAL;

	ret = alloc_buf(len + 1, buf);
	if (ret)
		return ret;

	buf->len--;

#ifdef __APPLE__
	/* strlcpy adds the trailing NULL terminator into last character */
	strlcpy((char *)buf->buf, string, buf->len + 1);
#else
	/* strncpy does not add the trailing NULL terminator */
	strncpy((char *)buf->buf, string, buf->len);
#endif

	return 0;
}

int json_add_response_data(const struct json_object *in,
			   struct json_object *out)
{
	struct json_object *vsid;
	int ret = json_find_key(in, "vsId", &vsid, json_type_int);
	if (ret)
		return ret;

	json_object_get(vsid);

	ret = json_object_object_add(out, "vsId", vsid);
	if (ret)
		goto out;

	json_logger(LOGGER_DEBUG, vsid, "Processed vsID");

out:
	return ret;
}

int json_add_test_data(const struct json_object *in, struct json_object *out)
{
	struct json_object *tcid;
	int ret = json_find_key(in, "tcId", &tcid, json_type_int);

	if (ret)
		return 0;

	json_object_get(tcid);

	ret = json_object_object_add(out, "tcId", tcid);
	if (ret)
		goto out;

	json_logger(LOGGER_DEBUG, tcid, "Processed tcID");

out:
	return ret;
}

int json_add_bin2hex(struct json_object *dst, const char *key,
		     const struct buffer *buf)
{
	char *hex;
	size_t hexlen;
	int ret;

	if (buf->len == 0) {
		json_object_object_add(dst, key, json_object_new_string(""));
		return 0;
	}

	ret = bin2hex_alloc(buf->buf, buf->len, &hex, &hexlen);
	if (ret)
		return ret;

	ret = json_object_object_add(dst, key, json_object_new_string(hex));
	free(hex);

	return ret;
}

int json_add_array_bin2hex(struct json_object *dst, const struct buffer *buf)
{
	char *hex;
	size_t hexlen;
	int ret;

	if (buf->len == 0) {
		json_object_array_add(dst, json_object_new_string(""));
		return 0;
	}

	ret = bin2hex_alloc(buf->buf, buf->len, &hex, &hexlen);
	if (ret)
		return ret;

	ret = json_object_array_add(dst, json_object_new_string(hex));
	free(hex);

	return ret;
}

int json_add_uint2hex(struct json_object *dst, const char *key, uint32_t val)
{
	char hex[20] = { 0 };

	snprintf(hex, sizeof(hex), "%x", val);

	return json_object_object_add(dst, key, json_object_new_string(hex));
}

void json_print_data(struct json_object *jobj, FILE *stream)
{
	// JSON_C_TO_STRING_PLAIN
	// JSON_C_TO_STRING_SPACED
	// JSON_C_TO_STRING_PRETTY
	const char *string = json_object_to_json_string_ext(jobj,
						JSON_C_TO_STRING_PRETTY);

	fprintf(stream, "%s\n", string ? string : "(null)");
}

int json_write_data(struct json_object *jobj, const char *filename)
{
	FILE *outfile;

	if (!jobj)
		return 0;

	outfile = fopen(filename, "w");

	if (!outfile) {
		int errsv = -errno;

		logger(LOGGER_ERR,
		       "Cannot open output file %s for writing: %d\n",
		       filename, errsv);
		return errsv;
	}
	json_print_data(jobj, outfile);

	fclose(outfile);

	return 0;
}

int json_read_data(const char *filename, struct json_object **inobj)
{
	struct json_object *o =  json_object_from_file(filename);
	int ret;

	if (!o) {
		logger(LOGGER_ERR, "Cannot parse input file %s\n", filename);
		return -EFAULT;
	}

	if (!json_object_is_type(o, json_type_array)) {
		logger(LOGGER_ERR,
		       "JSON input data is not expected ACVP array\n");
		ret = -EINVAL;
		goto out;
	}

	*inobj = o;

	return 0;

out:
	json_object_put(o);
	return ret;
}

int json_split_version(struct json_object *full_json,
		       struct json_object **inobj,
		       struct json_object **versionobj)
{
	int ret = 0;
	uint32_t i;

	*inobj = NULL;
	*versionobj = NULL;

	/* Parse response */
	if (json_object_get_type(full_json) == json_type_array) {
		for (i = 0; i < (uint32_t)json_object_array_length(full_json);
		     i++) {
			struct json_object *found =
					json_object_array_get_idx(full_json, i);

			/* discard version information */
			if (json_object_object_get_ex(found, "acvVersion",
						      NULL)) {
				*versionobj = found;
			} else {
				*inobj = found;
			}
		}
		if (!*inobj || !*versionobj) {
			json_logger(LOGGER_WARN, full_json,
				    "No data found in ACVP server response");
			ret = -EINVAL;
			goto out;
		}
	} else {
		*inobj = full_json;
	}

	json_logger(LOGGER_DEBUG, *inobj, "ACVP vector");
	json_logger(LOGGER_DEBUG, *versionobj, "ACVP version");

	if (!json_object_is_type(*inobj, json_type_object) ||
	    !json_object_is_type(*versionobj, json_type_object)) {
		logger(LOGGER_ERR,
		       "JSON data is are not expected ACVP objects\n");
		ret = EINVAL;
		goto out;
	}

out:
	return ret;
}

/*
 * Prune any auxiliary data in the first level of the test results - this is
 * needed to match with the ACVP-server-provided expected files which contain
 * additional data not produced by the ACVP Parser.
 */
static void json_prune_data(struct json_object *in)
{
	json_object_object_foreach(in, key, child) {
		(void)child;
		if (strncmp(key, "vsId", 4) &&
		    strncmp(key, "testGroups", 10))
			json_object_object_del(in, key);
	}
}

static int json_strncasecmp(const void *s1, const void *s2, size_t n)
{
	return strncasecmp(s1, s2, n);
}

enum json_validate_res json_validate_result_json(struct json_object *actual,
						 struct json_object *expected)
{
	struct json_object *expecteddata, *expectedversion,
			   *actualdata, *actualversion;
	enum json_validate_res rc = JSON_VAL_RES_FAIL_EXPECTED;
	int ret;

	/* Open and parse expected test result */
	CKINT(json_split_version(expected, &expecteddata, &expectedversion));
	json_prune_data(expecteddata);

	/* Open and parse actual test result */
	CKINT(json_split_version(actual, &actualdata, &actualversion));
	json_prune_data(actualdata);

	ret = json_object_equal(expecteddata, actualdata, &json_strncasecmp);
	if (ret)
		rc = JSON_VAL_RES_PASS_EXPECTED;
	else
		rc = JSON_VAL_RES_FAIL_EXPECTED;

out:
	return (ret < 0) ? JSON_VAL_RES_FAIL_EXPECTED : rc;
}

enum json_validate_res json_validate_result(const char *actualfile,
					    const char *expectedfile)
{
	struct json_object *expected = NULL, *actual = NULL;
	struct stat statbuf;
	enum json_validate_res rc = JSON_VAL_RES_FAIL_EXPECTED;
	int ret;

    
	/*
	 * If file not found, do not return an error, user does not
	 * want to have result validated.
	 */
	ret = stat(expectedfile, &statbuf);
	if (ret) {
		if (errno == ENOENT) {
			ret = JSON_VAL_RES_PASS;
			goto out;
		}
		ret = -errno;
		goto out;
	}

	/* Open and parse expected test result */
	CKINT(json_read_data(expectedfile, &expected));

	/* Open and parse actual test result */
	CKINT(json_read_data(actualfile, &actual));

	rc = json_validate_result_json(actual, expected);

out:
	if (expected)
		json_object_put(expected);
	if (actual)
		json_object_put(actual);
	return (ret < 0) ? JSON_VAL_RES_FAIL_EXPECTED : rc;
}

int json_check_acvversion(struct json_object *in, const char *exp_version,
			  struct json_object *out)
{
	struct json_object *o = NULL;
	const char *ver;
	int ret = json_find_key(in, "acvVersion", &o, json_type_string);

	if (ret) {
		json_logger(LOGGER_DEBUG, in, "Used JSON object");
		return ret;
	}

	ver = json_object_to_json_string(o);
	if (strstr(ver, exp_version)) {
		logger(LOGGER_DEBUG, "Expected JSON file version %s found\n",
		       ver);
		if (out)
			json_object_object_add(out, "acvVersion",
					json_object_new_string(exp_version));
		return 0;
	} else {
		logger(LOGGER_ERR,
		       "Unexpected JSON file version %s (expected %s)\n",
		       ver, exp_version);
		return -EOPNOTSUPP;
	}
}

int json_acvp_generate(struct json_object **full_json,
		       struct json_object **testdef,
		       struct json_object **testgroup,
		       struct json_object **test,
		       struct json_object **vectors,
		       const char *version,
		       const char *algorithm,
		       bool issample)
{
	struct json_object *json = NULL, *td, *tmp, *testgroups, *v;
	int ret;

	if (!*test) {
		if (!*testgroup) {
			json = json_object_new_array();
			CKNULL(json, -ENOMEM);

			/* Version array member */
			tmp = json_object_new_object();
			CKNULL(tmp, -ENOMEM);
			CKINT(json_object_array_add(json, tmp));
			CKINT(json_object_object_add(tmp, "acvVersion",
					json_object_new_string(version)));

			/* Actual data - first level */
			td = json_object_new_object();
			CKNULL(td, -ENOMEM);
			CKINT(json_object_array_add(json, td));
			CKINT(json_object_object_add(td, "vsId",
					json_object_new_int(INT_MAX)));
			CKINT(json_object_object_add(td, "algorithm",
					json_object_new_string(algorithm)));
			CKINT(json_object_object_add(td, "revision",
					json_object_new_string("1.0")));
			CKINT(json_object_object_add(td, "isSample",
					json_object_new_boolean(issample)));

			/* Test groups */
			testgroups = json_object_new_array();
			CKNULL(tmp, -ENOMEM);
			CKINT(json_object_object_add(td, "testGroups", testgroups));
		} else {
			json = *full_json;
			td = *testdef;
			testgroups = *testgroup;
		}

		/* One test group */
		tmp = json_object_new_object();
		CKNULL(tmp, -ENOMEM);
		CKINT(json_object_array_add(testgroups, tmp));
	} else {
		json = *full_json;
		td = *testdef;
		testgroups = *testgroup;
		tmp = *test;
	}

	v = json_object_new_array();
	CKNULL(v, -ENOMEM);
	CKINT(json_object_object_add(tmp, "tests", v));

	if (full_json)
		*full_json = json;
	if (testdef)
		*testdef = td;
	if (testgroup)
		*testgroup = testgroups;
	if (test)
		*test = tmp;
	if (vectors)
		*vectors = v;

	return 0;

out:
	if (!*testgroup)
		json_object_put(json);
	return ret;
}

