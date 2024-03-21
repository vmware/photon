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

#ifndef _READ_JSON_H
#define _READ_JSON_H

#include "bool.h"
#include "parser.h"
#include "logger.h"

#ifdef __cplusplus
extern "C"
{
#endif

/*
 * Log the JSON object.
 */
void json_logger(enum logger_verbosity severity,
		 struct json_object *jobj, const char *str);

/*
 * Find arbitrary key in toplevel hierarchy and check that value is of
 * given type. If key is found and of expected type, return reference to
 * object.
 */
int json_find_key(const struct json_object *inobj, const char *name,
		  struct json_object **out, enum json_type type);

/*
 * Get the uint32_t representation of an integer referenced with the given key.
 */
int json_get_uint(const struct json_object *obj, const char *name,
		  uint32_t *integer);
int json_get_uint64(const struct json_object *obj, const char *name,
		    uint64_t *integer);

/*
 * Get the uint32_t representation of an integer referenced with the given key.
 * If the value of the key contains "random", return 0 which shall be the
 * hint to the caller that a random number shall be used.
 */
int json_get_uint_random(const struct json_object *obj, const char *name,
			 uint32_t *integer);

/*
 * Get the binary representation of the hex value found at the given key
 */
int json_get_bin(const struct json_object *obj, const char *name,
		 struct buffer *buf);

/*
 * Convert MPINT to binary
 */
int mpint2bin(const char *mpi, uint32_t mpilen, struct buffer *buf);
/*
 * Get the binary representation of the hex value of an MPINT at the given key
 */
int json_get_mpint(const struct json_object *obj, const char *name,
		   struct buffer *buf);

/*
 * Get a string that represents a boolean value and turn it into an integer
 * (1 == true, 0 == false)
 */
int json_get_bool(const struct json_object *obj, const char *name,
		  uint32_t *integer);

/*
 * Get the string representation of the value found at the given key
 */
int json_get_string(const struct json_object *obj, const char *name,
		    const char **outbuf);
int json_get_string_buf(const struct json_object *obj, const char *name,
		    	struct buffer *buf);

/*
 * Copy the toplevel identifier data from request to response object
 */
int json_add_response_data(const struct json_object *in,
			   struct json_object *out);

/*
 * Copy the reference identifier for each particular test from test request
 * to test response.
 */
int json_add_test_data(const struct json_object *in, struct json_object *out);

/*
 * Add a JSON string entry with the given key by converting the binary data
 * given with buf
 */
int json_add_bin2hex(struct json_object *dst, const char *key,
		     const struct buffer *buf);

/*
 * Add a JSON string entry to an array converting the binary data
 * given with buf
 */
int json_add_array_bin2hex(struct json_object *dst, const struct buffer *buf);

/*
 * Add a JSON string entry with the given key by converting the integer data
 * given with val into a hex representation.
 */
int json_add_uint2hex(struct json_object *dst, const char *key, uint32_t val);

/*
 * Dump the JSON object.
 */
void json_print_data(struct json_object *jobj, FILE *stream);

/*
 * Write the JSON object to a file
 */
int json_write_data(struct json_object *jobj, const char *filename);

/*
 * Read the JSON data from file and parse it.
 */
int json_read_data(const char *filename, struct json_object **inobj);

/**
 * Parse ACVP server response and retrieve array entry that contains the
 * real data and version number
 *
 * Typical server response:
 *
 * [
 *   { "acvVersion": "0.3" },
 *   { "vsId": 1437,
 *     ....
 *   }
 * ]
 *
 * @param full_json [in] JSON object containing fully parsed ACVP response
 * @param inobj [out] JSON object that contains the real data
 * @param versionobj [out] JSON object that contains the version part
 */
int json_split_version(struct json_object *full_json,
		       struct json_object **inobj,
		       struct json_object **versionobj);

/**
 * Check that the ACVP server version matches an expected version.
 *
 * @param in [in] JSON object containing the version information (e.g. the
 *		  @var versionobj variable from json_split_version)
 * @param exp_version [in] Expected version
 * @param out [in] JSON object that the version information should be written
 *		   to in case a match is found - it may be NULL
 */
int json_check_acvversion(struct json_object *in, const char *exp_version,
			  struct json_object *out);

enum json_validate_res {
	JSON_VAL_RES_FAIL,
	JSON_VAL_RES_PASS,
	JSON_VAL_RES_FAIL_EXPECTED,
	JSON_VAL_RES_PASS_EXPECTED,
	JSON_VAL_RES_NOT_IMPLEMENTED,
	JSON_VAL_RES_UNKNOWN
};

/**
 * Validate the actual test result provided with @param actualfile with an
 * expected result found in @param expectedfile .
 *
 * It is permissible that the expected file is not present.
 */
enum json_validate_res json_validate_result(const char *actualfile,
					    const char *expectedfile);

/**
 * Validate the actual test result provided with @param actual with an
 * expected result found in @param expected .
 */
enum json_validate_res json_validate_result_json(struct json_object *actual,
						 struct json_object *expected);

/**
 * Generate a JSON structure compliant to the ACVP request test vectors. This
 * function can be invoked multiple times:
 * (1) It will always generate the vector structure.
 * (2) If @param test is NULL, it will generate the test structure for the
 *     tests array.
 * (3) If @param testgroup is null, it will generate the full_json
 *     and testgroup structure.
 */
int json_acvp_generate(struct json_object **full_json,
		       struct json_object **testdef,
		       struct json_object **testgroup,
		       struct json_object **test,
		       struct json_object **vectors,
		       const char *version,
		       const char *algorithm,
		       bool issample);

/*
 * The return value is treated as a flags array:
 *	up to 4095 are error codes and are treated as such.
 *	all return codes above it convey information to the caller
 */
/* Result data is already written, do not write it again. */
#define FLAG_RES_DATA_WRITTEN	(1<<12UL)

#ifdef __cplusplus
}
#endif

#endif /* _READ_JSON_H */
