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

#ifndef _PARSER_COMMON_H
#define _PARSER_COMMON_H

#include <stdint.h>

#include "ret_checkers.h"

#include "parser_flags.h"
#include "parser_aead.h"
#include "parser_sym.h"
#include "parser_sha.h"
#include "parser_rsa.h"
#include "parser_dh.h"
#include "parser_drbg.h"
#include "parser_dsa.h"
#include "parser_ecdh.h"
#include "parser_ecdh_ed.h"
#include "parser_ecdsa.h"
#include "parser_eddsa.h"
#include "parser_hmac.h"
#include "parser_kdf_tls.h"
#include "parser_kdf_ssh.h"
#include "parser_kdf_ikev1.h"
#include "parser_kdf_ikev2.h"
#include "parser_kdf_108.h"
#include "parser_pbkdf.h"
#include "parser_hkdf.h"
#include "parser_ifc.h"
#include "parser_tls12.h"
#include "parser_tls13.h"
#include "parser_kmac.h"
#include "parser_ansi_x963.h"
#include "parser_kdf_srtp.h"
#include "parser_cshake.h"

#ifdef __cplusplus
extern "C"
{
#endif

struct json_array;

/*
 * The parser header file contains all definitions to specify how a JSON
 * file should be parsed for a given test definition. The core concept of the
 * JSON parser is a data driven model. That means that for defining a
 * particular expected JSON structure with all fields expected to be found,
 * only the JSON data model should be expressed. For defining a test
 * structure, no JSON parsing code should ever be needed.
 *
 * The following data structures must be used to define the expected JSON
 * structure the JSON parser should find and read into local variables.
 */

/******************************************************************************
 * JSON data entry
 ******************************************************************************/

/**
 * json_data holds a reference to the data part of one JSON entry. Each data
 * will have exactly one type of data that is denominated with the
 * @datatype variable. For each datatype, variable of the corresponding
 * referenced datatype is to be provided.
 *
 * PARSER_BIN parses a hex string from JSON into data.buf but
 * PARSER_BIN_BUFFERARRAY parses a hex string into a struct buffer_array
 * PARSER_UINT parses a unsigned int from JSON into data.integer
 * PARSER_UINT64 parses a unsigned long long from JSON into data.integer
 * PARSER_UINT_RANDOM parses a unsigned int from JSON into data.integer (if
 *		      the JSON value contains "random" instead of integer,
 *		      the parser function returns 0)
 * PARSER_BOOL parses a string representation of a boolean value into an integer
 *	       (1 == true, 0 == false)
 * PARSER_CIPHER parses a cipher algo string from JSON into data.largeint by
 *		 ORing the the parsed value with the existing value
 * PARSER_CIPHER_ARRAY parses an array of cipher algo strings from JSON into
 *		       data.cipherarray by ORing the the parsed value with the
 *		       existing value
 * PARSER_ARRAY parses a JSON array as defined by data.array
 * PARSER_ARRAY_BUFFERARRAY parses a JSON array that will contain BUFFERARRAYs
 * PARSER_MPINT parses an MPINT such that the MPINT header is stripped (see
 *		RFC4251 chapter 5)
 * WRITER_BIN will write data.buf in hex format to JSON, buffer is not created
 *	      empty hex value is provided
 * WRITER_BIN_ALWAYS will write data.buf in hex format to JSON unconditionally
 *		     (i.e. the JSON entry is written even when the buffer is
 *		     empty)
 * WRITER_UINT will write a data.integer to JSON
 * WRITER_BOOL_TRUE_TO_FALSE will write "false" if data.integer is true - i.e.
 *			     the parser with flip the value (if value is false,
 *			     it is a noop)
 */
enum json_data_type {
	PARSER_BIN,
	PARSER_BIN_BUFFERARRAY,
	PARSER_UINT,
	PARSER_UINT64,
	PARSER_UINT_RANDOM,
	PARSER_BOOL,
	PARSER_CIPHER,
	PARSER_CIPHER_ARRAY,
	PARSER_ARRAY,
	PARSER_ARRAY_BUFFERARRAY,
	PARSER_OBJECT,
	PARSER_MPINT,
	PARSER_STRING,
	WRITER_BIN,
	WRITER_BIN_ALWAYS,
	WRITER_UINT,
	WRITER_BOOL,
	WRITER_BOOL_TRUE_TO_FALSE,
	WRITER_STRING_NOFREE,

	WRITER_ECC,
	WRITER_HASH,
};

struct json_data {
	union {
		struct buffer *buf;
		struct buffer_array *buffer_array;
		uint32_t *integer;
		uint64_t *largeint;
		struct cipher_array *cipher_array;
		const struct json_array *array;
	} data;
	enum json_data_type datatype;
};

/**
 * @brief json_entry specifies precisely one JSON element in the JSON tree. Each
 * element is defined with the following information.
 *
 * @var name The name of of the JSON entry
 * @var data The data value of the JSON entry
 * @var flags Flags defined in parser_flags.h.
 */

struct json_entry {
	const char *name;
	const struct json_data data;
	flags_t flags;
};

/******************************************************************************
 * Callback definitions per data type
 ******************************************************************************/

/**
 * @brief The ##name_callback structure references one callback to the backends
 *	  for an the respective cipher operation.
 * @var fn Function pointer from the registered backend to be invoked.
 * @var vector Reference to data structure holding the input data to the
 *		 backend.
 * @var helper Specify a helper function that can pre-process data before
 *		 invoking the backend. This can be used to implement MCT as part
 *		 of the parser. Note, @var fn always must be set. If
 *		 @var helper is non-NULL, it is invoked instead of @var fn,
 *		 but obtains the reference to @var fn with the idea that the
 *		 helper will invoke @var fn as needed. The parameters
 *		 of @var helper are identical to exec_test() plus the
 *		 @var fn and @var vector information to allow the callback
 *		 to be invoked.
 */
#define DEF_CALLBACK_TYPE(name)						       \
	struct name ## _callback {					       \
		int (*fn)(struct name ## _data *vector, flags_t parsed_flags); \
		struct name ## _data *vector;				       \
		int (*helper)(const struct json_array *processdata,	       \
			      flags_t parsed_flags,			       \
			      struct json_object *testvector,		       \
			      struct json_object *testresults,		       \
			      int (*fn)(struct name ## _data *vector,	       \
					flags_t parsed_flags),		       \
			      struct name ## _data *vector);		       \
	};

DEF_CALLBACK_TYPE(aead)
DEF_CALLBACK_TYPE(sym)
DEF_CALLBACK_TYPE(sha)
DEF_CALLBACK_TYPE(rsa_keygen_prime)
DEF_CALLBACK_TYPE(rsa_keygen_prov_prime)
DEF_CALLBACK_TYPE(rsa_keygen)
DEF_CALLBACK_TYPE(rsa_siggen)
DEF_CALLBACK_TYPE(rsa_sigver)
DEF_CALLBACK_TYPE(rsa_signature_primitive)
DEF_CALLBACK_TYPE(rsa_decryption_primitive)
DEF_CALLBACK_TYPE(dh_ss)
DEF_CALLBACK_TYPE(dh_ss_ver)
DEF_CALLBACK_TYPE(dh_keygen)
DEF_CALLBACK_TYPE(dh_keyver)
DEF_CALLBACK_TYPE(drbg)
DEF_CALLBACK_TYPE(dsa_pqg)
DEF_CALLBACK_TYPE(dsa_keygen)
DEF_CALLBACK_TYPE(dsa_keyver)
DEF_CALLBACK_TYPE(dsa_siggen)
DEF_CALLBACK_TYPE(dsa_sigver)
DEF_CALLBACK_TYPE(ecdh_ss)
DEF_CALLBACK_TYPE(ecdh_ss_ver)
DEF_CALLBACK_TYPE(ecdh_ed_ss)
DEF_CALLBACK_TYPE(ecdh_ed_ss_ver)
DEF_CALLBACK_TYPE(ecdsa_keygen)
DEF_CALLBACK_TYPE(ecdsa_keygen_extra)
DEF_CALLBACK_TYPE(ecdsa_pkvver)
DEF_CALLBACK_TYPE(ecdsa_siggen)
DEF_CALLBACK_TYPE(ecdsa_sigver)
DEF_CALLBACK_TYPE(eddsa_keygen)
DEF_CALLBACK_TYPE(eddsa_keyver)
DEF_CALLBACK_TYPE(eddsa_siggen)
DEF_CALLBACK_TYPE(eddsa_sigver)
DEF_CALLBACK_TYPE(hmac)
DEF_CALLBACK_TYPE(kdf_tls)
DEF_CALLBACK_TYPE(kdf_ssh)
DEF_CALLBACK_TYPE(kdf_ikev1)
DEF_CALLBACK_TYPE(kdf_ikev2)
DEF_CALLBACK_TYPE(kdf_108)
DEF_CALLBACK_TYPE(pbkdf)
DEF_CALLBACK_TYPE(hkdf)
DEF_CALLBACK_TYPE(kts_ifc)
DEF_CALLBACK_TYPE(tls12)
DEF_CALLBACK_TYPE(tls13)
DEF_CALLBACK_TYPE(kmac)
DEF_CALLBACK_TYPE(ansi_x963)
DEF_CALLBACK_TYPE(kdf_srtp)
DEF_CALLBACK_TYPE(cshake)

/**
 * @brief json_callback specifies one generic callback. It therefore wraps the
 * data type of a particular callback.
 *
 * @var callback This union refers to exactly one particular callback.
 * @var cb_type The type field specifies the particular data type of the
 *		  callback.
 * @var flags This field specifies one of the flags documented for
 *		@var json_entry.
 */
enum {
	CB_TYPE_aead,
	CB_TYPE_sym,
	CB_TYPE_sha,
	CB_TYPE_rsa_keygen_prime,
	CB_TYPE_rsa_keygen_prov_prime,
	CB_TYPE_rsa_keygen,
	CB_TYPE_rsa_siggen,
	CB_TYPE_rsa_sigver,
	CB_TYPE_rsa_signature_primitive,
	CB_TYPE_rsa_decryption_primitive,
	CB_TYPE_dh_ss,
	CB_TYPE_dh_ss_ver,
	CB_TYPE_dh_keygen,
	CB_TYPE_dh_keyver,
	CB_TYPE_drbg,
	CB_TYPE_dsa_pqg,
	CB_TYPE_dsa_keygen,
	CB_TYPE_dsa_keyver,
	CB_TYPE_dsa_siggen,
	CB_TYPE_dsa_sigver,
	CB_TYPE_ecdh_ss,
	CB_TYPE_ecdh_ss_ver,
	CB_TYPE_ecdh_ed_ss,
	CB_TYPE_ecdh_ed_ss_ver,
	CB_TYPE_ecdsa_keygen,
	CB_TYPE_ecdsa_keygen_extra,
	CB_TYPE_ecdsa_pkvver,
	CB_TYPE_ecdsa_siggen,
	CB_TYPE_ecdsa_sigver,
	CB_TYPE_eddsa_keygen,
	CB_TYPE_eddsa_keyver,
	CB_TYPE_eddsa_siggen,
	CB_TYPE_eddsa_sigver,
	CB_TYPE_dsa_pqggen,
	CB_TYPE_dsa_pqgver,
	CB_TYPE_hmac,
	CB_TYPE_kdf_tls,
	CB_TYPE_kdf_ssh,
	CB_TYPE_kdf_ikev1,
	CB_TYPE_kdf_ikev2,
	CB_TYPE_kdf_108,
	CB_TYPE_pbkdf,
	CB_TYPE_hkdf,
	CB_TYPE_kts_ifc,
	CB_TYPE_tls12,
	CB_TYPE_tls13,
	CB_TYPE_kmac,
	CB_TYPE_ansi_x963,
	CB_TYPE_kdf_srtp,
	CB_TYPE_cshake,
};
struct json_callback {
	union {
		struct aead_callback aead;
		struct sym_callback sym;
		struct sha_callback sha;
		struct rsa_keygen_prime_callback rsa_keygen_prime;
		struct rsa_keygen_prov_prime_callback rsa_keygen_prov_prime;
		struct rsa_keygen_callback rsa_keygen;
		struct rsa_siggen_callback rsa_siggen;
		struct rsa_sigver_callback rsa_sigver;
		struct rsa_signature_primitive_callback rsa_signature_primitive;
		struct rsa_decryption_primitive_callback rsa_decryption_primitive;
		struct dh_ss_callback dh_ss;
		struct dh_ss_ver_callback dh_ss_ver;
		struct dh_keygen_callback dh_keygen;
		struct dh_keyver_callback dh_keyver;
		struct drbg_callback drbg;
		struct dsa_pqg_callback dsa_pqg;
		struct dsa_keygen_callback dsa_keygen;
		struct dsa_keyver_callback dsa_keyver;
		struct dsa_siggen_callback dsa_siggen;
		struct dsa_sigver_callback dsa_sigver;
		struct ecdh_ss_callback ecdh_ss;
		struct ecdh_ss_ver_callback ecdh_ss_ver;
		struct ecdh_ed_ss_callback ecdh_ed_ss;
		struct ecdh_ed_ss_ver_callback ecdh_ed_ss_ver;
		struct ecdsa_keygen_callback ecdsa_keygen;
		struct ecdsa_keygen_extra_callback ecdsa_keygen_extra;
		struct ecdsa_pkvver_callback ecdsa_pkvver;
		struct ecdsa_siggen_callback ecdsa_siggen;
		struct ecdsa_sigver_callback ecdsa_sigver;
		struct eddsa_keygen_callback eddsa_keygen;
		struct eddsa_keyver_callback eddsa_keyver;
		struct eddsa_siggen_callback eddsa_siggen;
		struct eddsa_sigver_callback eddsa_sigver;
		struct hmac_callback hmac;
		struct kdf_tls_callback kdf_tls;
		struct kdf_ssh_callback kdf_ssh;
		struct kdf_ikev1_callback kdf_ikev1;
		struct kdf_ikev2_callback kdf_ikev2;
		struct kdf_108_callback kdf_108;
		struct pbkdf_callback pbkdf;
		struct hkdf_callback hkdf;
		struct kts_ifc_callback kts_ifc;
		struct tls12_callback tls12;
		struct tls13_callback tls13;
		struct kmac_callback kmac;
		struct ansi_x963_callback ansi_x963;
		struct kdf_srtp_callback kdf_srtp;
		struct cshake_callback cshake;
	} callback;
	uint32_t cb_type;
	flags_t flags;
};

/**
 * @brief The json_callbacks wraps one or more @var json_callback instances.
 *
 * @var callback This variable is the head of an array of @var json_callback
 *		   instances.
 * @var count This variable specifies the number of callbacks.
 */
struct json_callbacks {
	const struct json_callback *callback;
	uint32_t count;
};

/**
 * @brief With the @var json_testresult data structure, a set of entries can
 * be specified. These entries will point to C variables which should be turned
 * into a JSON structure.
 *
 * @var entry This variable is the head of an array of @json_entry values. All
 *		these pointers should ultimately refer to a @json_data value of
 *		type WRITE_*.
 * @var count This variable specifies the number of entries.
 * @var callbacks Before any variable pointed to by one of the @entry values
 *		    is written to the JSON file, all callbacks are executed.
 *		    The idea is that precisely when a @var json_testresult is
 *		    hit, one test is executed by the backend cipher
 *		    implementation to fill the variables pointed to by
 *		    @var entry before they are written to JSON.
 */
struct json_testresult {
	const struct json_entry *entry;
	uint32_t count;
	const struct json_callbacks *callbacks;
};

/**
 * @brief The @var json_array is considered to hold the basic test definition
 * of one hierarchy level of the JSON input data. If @var testresult is
 * non-NULL, at the end of the parsing of all @var entry members, the logic
 * described for @var testresult is invoked to invoke one test with the given
 * data. If @var testresult is NULL, no test is executed for the respective
 * JSON hierarchy level.
 *
 * @var entry This variable is the head of an array of @json_entry values.
 *		All these pointers should ultimately refer to a @json_data value
 *		of type PARSER_*.
 * @var count This variable specifies the number of entries.
 * @var testresult This is a reference to one @var json_testresult
 *		     definition. It may be NULL which would imply that no
 *		     testing is invoked after parsing all members of
 *		     @var entry.
 */
struct json_array {
	const struct json_entry *entry;
	uint32_t count;
	const struct json_testresult *testresult;
};

#define ARRAY_SIZE(a) (sizeof(a)/sizeof(a[0]))
#define SET_CALLBACKS(entry) { entry, ARRAY_SIZE(entry) }
#define SET_ARRAY(entry, addtl) { entry, ARRAY_SIZE(entry), addtl }

#define for_each_arraymember(__array, __entry, __i)			\
	for (__i = 0, __entry = __array->entry;				\
	     __i < __array->count;					\
	     __i++, __entry = __array->entry + __i )

#define for_each_callback(__testresult, __callback, __i)		\
	for (__i = 0, __callback = __testresult->callbacks->callback;	\
	     __i < __testresult->callbacks->count;			\
	     __i++, __callback = __testresult->callbacks->callback + __i )

#define for_each_testresult(__testresult, __entry, __i)			\
	for (__i = 0, __entry = __testresult->entry;			\
	     __i < __testresult->count;					\
	     __i++, __entry = __testresult->entry + __i )

/**
 * @brief Entry function to start evaluating a test definition
 *
 * This function is to be invoked by the different test definitions in
 * parser_*.c with the layout definition of the JSON data to be parsed.
 *
 * @var processdata Parser definition to process
 * @var exp_version Version number to search for in the JSON data (if version
 *		      does not match, the parser definition is not executed).
 * @var in Input JSON data to analyze.
 * @var out Any data to be generated based on the application of the parser
 *	      definition is written to this value.
 *
 * @return 0 on success, < 0 on error
 */
int process_json(const struct json_array *processdata, const char *exp_version,
		 struct json_object *in, struct json_object *out);

/**
 * @brief write_one_entry writes the test result data to the testresults
 *	  structure based on the test definition given in @var entry.
 *
 * @var entry Test definition with the C data to be added to testresult
 * @var testresult JSON data that shall receive the data from the C structure
 * @var parsed_flags Flags that have been obtained from the input JSON data.
 *
 * @return 0 on success, < 0 on error
 */
int write_one_entry(const struct json_entry *entry,
		    struct json_object *testresult,
		    flags_t parsed_flags);

#define register_backend(backend, definition, log)			\
	if (backend) {							\
		logger(LOGGER_ERR,					\
		       "Backend %s already registered\n", log);		\
		exit(-EFAULT);						\
	}								\
	backend = definition;						\
	logger(LOGGER_VERBOSE, "Backend %s registered\n", log);

#define DEF_CALLBACK_HELPER(type, name, flags, helper)			\
	struct name ## _data name ## _vector ;				\
	const struct name ## _callback name = {type ## _backend->name,	\
					       &name ## _vector, helper};\
	const struct json_callback name ## _callback[] = {		\
		{ .callback.name = name, CB_TYPE_##name, flags },	\
	};								\
	const struct json_callbacks name ## _callbacks =		\
				SET_CALLBACKS(name ## _callback); 	\
	memset(&name ## _vector, 0, sizeof(name ## _vector));

#define DEF_CALLBACK(type, name, flags)					\
	DEF_CALLBACK_HELPER(type, name, flags, NULL)

int match_expected_vector(const char *actualfile, const char *expectedfile);
int perform_testing(const char *infile, const char *outfile);
int perform_testing_regression(const char *infile, const char *expectedfile);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_COMMON_H */
