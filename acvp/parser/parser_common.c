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
#define _GNU_SOURCE
#include "bool.h"
#include "read_json.h"
#include "stringhelper.h"
#include "parser.h"
#include "logger.h"

#include "parser_common.h"

/*
 * Match parsed entry with a search criteria
 * return 0 if match not found, 1 match found
 */
static int match_entry(flags_t parsed_flags, flags_t search, const char *log)
{
	/*
	 * We allow callback->flags to be a mask.
	 * WARNING: Ensure that all entries that are ORed together have a
	 * value that can form a mask!
	 */
	flags_t not_matched = parsed_flags &~ (search & FLAG_OP_MASK);

	/* Exact match */
	/*
	 * unsigned int not_matched = (parsed_flags != (search & FLAG_OP_MASK));
	 */

	if (not_matched) {
		logger(LOGGER_DEBUG,
			"Not matching %s (parsed_flags %" PRIu64 ", entry flags %llu, result %" PRIu64 ")\n",
			log, parsed_flags, (search & FLAG_OP_MASK),
			not_matched);
		return 0;
	}

	logger(LOGGER_DEBUG,
	       "Matching %s (parsed_flags %" PRIu64 ", entry flags %llu)\n",
	       log ? log : "(unnamed)", parsed_flags, (search & FLAG_OP_MASK));

	return 1;
}

static void vector_free_all_array(const struct json_array *processdata);
static void vector_free_entry(const struct json_entry *entry)
{
	const struct json_data *data = &entry->data;
	const struct json_array *processdata;
	struct buffer_array *array;
	struct cipher_array *cipher_array;
	unsigned int i;

	if (!entry) {
		logger(LOGGER_ERR,
		       "Missing definitions in function vector_free_entry\n");
		return;
	}

	/* Free each data type. */
	switch (data->datatype) {
	case PARSER_BIN:
	case PARSER_MPINT:
	case PARSER_STRING:
	case WRITER_BIN:
	case WRITER_BIN_ALWAYS:
		logger(LOGGER_DEBUG, "Freeing entry %s with data type %d\n",
		       entry->name, data->datatype);
		/* free struct buffer */
		free_buf(data->data.buf);
		break;
	case PARSER_BIN_BUFFERARRAY:
		array = data->data.buffer_array;
		for (i = 0; i < array->arraysize; i++) {
			logger(LOGGER_DEBUG,
			       "Freeing entry %s with data type %d\n",
			       entry->name, data->datatype);
			/* free struct buffer */
			free_buf(&array->buffers[i]);
		}
		array->arraysize = 0;
		break;
	case PARSER_UINT:
	case WRITER_UINT:
	case PARSER_UINT_RANDOM:
	case PARSER_BOOL:
	case WRITER_BOOL:
	case WRITER_BOOL_TRUE_TO_FALSE:
	case WRITER_ECC:
	case WRITER_HASH:
		logger(LOGGER_DEBUG, "Freeing entry %s with data type %d\n",
		       entry->name, data->datatype);
		*data->data.integer = 0;
		break;

	case PARSER_UINT64:
	case PARSER_CIPHER:
		logger(LOGGER_DEBUG, "Freeing entry %s with data type %d\n",
		       entry->name, data->datatype);
		*data->data.largeint = 0;
		break;
	case PARSER_CIPHER_ARRAY:
		cipher_array = data->data.cipher_array;
		for (i = 0; i < cipher_array->arraysize; i++) {
			logger(LOGGER_DEBUG,
			       "Freeing entry %s with data type %d\n",
			       entry->name, data->datatype);
			cipher_array->cipher[i] = 0;
		}
		cipher_array->arraysize = 0;
		break;
	case PARSER_ARRAY:
	case WRITER_STRING_NOFREE:
		/* PARSER_ARRAY should be freed in subordinate levels */
		break;
	case PARSER_OBJECT:
	case PARSER_ARRAY_BUFFERARRAY:
		/* Do the freeing found in parse_array */
		processdata = entry->data.data.array;
		vector_free_all_array(processdata);
		break;
	default:
		logger(LOGGER_ERR, "Unknown data type %u to be released\n",
		       data->datatype);
		break;
	}
}

static void vector_free_all_array(const struct json_array *processdata)
{
	const struct json_entry *entry;
	uint32_t i;

	for_each_arraymember(processdata, entry, i)
		vector_free_entry(entry);

	if (processdata->testresult) {
		for_each_testresult(processdata->testresult, entry, i)
			vector_free_entry(entry);
	}
}

static int write_bin(const struct json_entry *entry,
		     struct json_object *testresult, const struct buffer *buf,
		     int write_always)
{
	int ret = 0;

	logger_binary(LOGGER_DEBUG, buf->buf, buf->len, "Add to test results");
	if (buf->len == CIPHER_DECRYPTION_FAILED_LEN &&
	    !memcmp(buf->buf, CIPHER_DECRYPTION_FAILED,
		    CIPHER_DECRYPTION_FAILED_LEN)) {
		CKINT(json_object_object_add(testresult, "testPassed",
					     json_object_new_boolean(0)));
	} else {
		/* A JSON entry if data is available */
		if (write_always) {
			CKINT(json_add_bin2hex(testresult, entry->name, buf));
		} else {
			if (buf->buf && buf->len)
				CKINT(json_add_bin2hex(testresult, entry->name,
						       buf));
		}
	}

out:
	return ret;
}

int write_one_entry(const struct json_entry *entry,
		    struct json_object *testresult,
		    flags_t parsed_flags)
{
	const struct json_data *data = &entry->data;
	const char *algo;
	int ret = 0;

	CKNULL_LOG(entry, -EINVAL,
		   "Missing write definitions in function write_one_entry\n");

	/* Apply entry only if it matches the condition. */
	if (!match_entry(parsed_flags, entry->flags, entry->name))
		return 0;

	/* Process each type of write definition. */
	switch (data->datatype) {
	case WRITER_BIN:
		CKINT(write_bin(entry, testresult, data->data.buf, 0));
		break;
	case WRITER_BIN_ALWAYS:
		CKINT(write_bin(entry, testresult, data->data.buf, 1));
		break;
	case WRITER_BOOL:
		logger(LOGGER_DEBUG, "Add boolean to test result %u\n",
		       *data->data.integer);
		json_object_object_add(testresult, entry->name,
			json_object_new_boolean(!!(*data->data.integer)));
		break;
	case WRITER_BOOL_TRUE_TO_FALSE:
		/* Only write false values */
		if (!*data->data.integer)
			goto out;

		logger(LOGGER_DEBUG, "Add boolean to test result %u\n",
		       !*data->data.integer);
		json_object_object_add(testresult, entry->name,
				       json_object_new_boolean(0));
		break;
	case WRITER_UINT:
		logger(LOGGER_DEBUG, "Add integer to test result %u\n",
		       *data->data.integer);
		json_object_object_add(testresult, entry->name,
				json_object_new_int((int32_t)(*data->data.integer)));
		break;
	case WRITER_STRING_NOFREE:
		logger(LOGGER_DEBUG, "Add string %s to test result\n",
		       data->data.buf->buf);
		json_object_object_add(testresult, entry->name,
			json_object_new_string(
				(const char *)data->data.buf->buf));
		break;
	case WRITER_ECC:
		CKINT(convert_cipher_algo(*data->data.largeint & ACVP_CURVEMASK,
					  ACVP_CIPHERTYPE_ECC, &algo));
		logger(LOGGER_DEBUG, "Add ECC curve %s to test result\n",
		       algo);
		json_object_object_add(testresult, entry->name,
				       json_object_new_string(algo));
		break;
	case WRITER_HASH:
		CKINT(convert_cipher_algo(*data->data.largeint & ACVP_HASHMASK,
					  ACVP_CIPHERTYPE_HASH, &algo));
		logger(LOGGER_DEBUG, "Add hash %s to test result\n",
		       algo);
		json_object_object_add(testresult, entry->name,
				       json_object_new_string(algo));
		break;

	case PARSER_ARRAY:
	case PARSER_ARRAY_BUFFERARRAY:
	case PARSER_BIN:
	case PARSER_BIN_BUFFERARRAY:
	case PARSER_BOOL:
	case PARSER_CIPHER:
	case PARSER_CIPHER_ARRAY:
	case PARSER_MPINT:
	case PARSER_OBJECT:
	case PARSER_STRING:
	case PARSER_UINT:
	case PARSER_UINT64:
	case PARSER_UINT_RANDOM:
	default:
		logger(LOGGER_ERR, "Unknown data type %u to be written\n",
		       data->datatype);
		break;
	}

out:
	return ret;
}

/**
 * @brief Unparse the generated test results into JSON using the write
 *	  definitions of the parsing information.
 *
 * @param writedef Write definition of parser specification
 * @param testvector Input JSON data to process
 * @param testresults Output JSON data to fill with the unparsing.
 * @param parsed_flags All previously parsed flags
 *
 * @return 0 on success, < 0 on error
 */
static int write_all_results(const struct json_testresult *writedef,
			     struct json_object *testvector,
			     struct json_object *testresults,
			     flags_t parsed_flags)
{
	const struct json_entry *entry;
	struct json_object *testresult;
	uint32_t i;
	int ret = 0;

	/* If no test results are defined to be written, skip processing. */
	if (!writedef->count)
		return 0;

	/* Create output stream. */
	testresult = json_object_new_object();
	CKNULL(testresult, ENOMEM);
	CKINT(json_add_test_data(testvector, testresult));

	/* Iterate over each write definition and invoke it. */
	for_each_testresult(writedef, entry, i)
		CKINT(write_one_entry(entry, testresult, parsed_flags));

	CKINT(json_object_array_add(testresults, testresult));

out:
	return ret;
}

#define CB_HANDLER(name)						       \
	case CB_TYPE_##name :						       \
	{								       \
		const struct name ## _callback *cb = &callback->callback.name ;\
		if (cb && cb->helper) {					       \
			CKINT(cb->helper(processdata, parsed_flags, testvector,\
					 testresults, cb->fn, cb->vector));    \
		} else if (cb && cb->fn) {				       \
			CKINT(cb->fn(cb->vector, parsed_flags));	       \
		} else {						       \
			logger(LOGGER_VERBOSE, "No callback defined\n");       \
			ret = -EOPNOTSUPP;				       \
			goto out;					       \
		}							       \
		break;							       \
	}

/**
 * @brief Execute one test as defined by the JSON parser information
 *
 * @param processdata JSON parser specification.
 * @param parsed_flags Accumulated flags that have been identified so far
 * @param testvector Input JSON data
 * @param testresults Output JSON data
 *
 * @return 0 on success, < 0 on error
 */
static int exec_test(const struct json_array *processdata,
		     flags_t parsed_flags,
		     struct json_object *testvector,
		     struct json_object *testresults)
{
	const struct json_testresult *testresult = processdata->testresult;
	const struct json_callback *callback;
	uint32_t i;
	int ret = 0;

	CKNULL_LOG(processdata, -EINVAL,
		   "Missing execution definitions in function exec_test\n");

	/* If no testresult data set defined, do not apply testing. */
	if (!testresult)
		return 0;

	if (!testresult->callbacks)
		return 0;

	/* Iterate over all callbacks and invoke them. */
	for_each_callback(testresult, callback, i) {
		/* Apply entry only if it matches the condition. */
		if (!match_entry(parsed_flags, callback->flags, "callback"))
			continue;

		/* Invoke the callbacks type-specific. */
		switch(callback->cb_type) {
			CB_HANDLER(aead)
			CB_HANDLER(sym)
			CB_HANDLER(sha)
			CB_HANDLER(rsa_keygen_prime)
			CB_HANDLER(rsa_keygen_prov_prime)
			CB_HANDLER(rsa_keygen)
			CB_HANDLER(rsa_siggen)
			CB_HANDLER(rsa_sigver)
			CB_HANDLER(rsa_signature_primitive)
			CB_HANDLER(rsa_decryption_primitive)
			CB_HANDLER(dh_ss)
			CB_HANDLER(dh_ss_ver)
			CB_HANDLER(dh_keygen)
			CB_HANDLER(dh_keyver)
			CB_HANDLER(drbg)
			CB_HANDLER(dsa_pqg)
			CB_HANDLER(dsa_keygen)
			CB_HANDLER(dsa_keyver)
			CB_HANDLER(dsa_siggen)
			CB_HANDLER(dsa_sigver)
			CB_HANDLER(ecdh_ss)
			CB_HANDLER(ecdh_ss_ver)
			CB_HANDLER(ecdh_ed_ss)
			CB_HANDLER(ecdh_ed_ss_ver)
			CB_HANDLER(ecdsa_keygen)
			CB_HANDLER(ecdsa_keygen_extra)
			CB_HANDLER(ecdsa_pkvver)
			CB_HANDLER(ecdsa_siggen)
			CB_HANDLER(ecdsa_sigver)
			CB_HANDLER(eddsa_keygen)
			CB_HANDLER(eddsa_keyver)
			CB_HANDLER(eddsa_siggen)
			CB_HANDLER(eddsa_sigver)
			CB_HANDLER(hmac)
			CB_HANDLER(kdf_tls)
			CB_HANDLER(kdf_ssh)
			CB_HANDLER(kdf_ikev1)
			CB_HANDLER(kdf_ikev2)
			CB_HANDLER(kdf_108)
			CB_HANDLER(pbkdf)
			CB_HANDLER(hkdf)
			CB_HANDLER(kts_ifc)
			CB_HANDLER(tls12)
			CB_HANDLER(tls13)
			CB_HANDLER(kmac)
			CB_HANDLER(ansi_x963)
			CB_HANDLER(kdf_srtp)
			CB_HANDLER(cshake)
		default:
			logger(LOGGER_ERR,
			       "Unknown function callback type %u\n",
			       callback->cb_type);
			ret = 1;
			break;
		}
	}

	/*
	 * Write out all test results that are defined to be written unless
	 * called function already did that.
	 */
	if (!(ret & FLAG_RES_DATA_WRITTEN))
		CKINT(write_all_results(testresult, testvector,
					testresults, parsed_flags));
	ret = 0;

out:
	if (ret)
		logger(LOGGER_WARN, "Test execution failed with error %d\n",
		       ret);
	return ret;
}

/* Flags conversion */
struct parser_flagsconv {
	flags_t flag;		/* C flag */
	union {
		const char *string;	/* JSON string */
		bool boolean;
	} val;
	const char *log;	/* logger string information */
};

/**
 * @brief parse_flagblock - convert JSON flag into a C flag
 *
 * Iterate over the flags definition of a given block and detect which flag
 * is set in the test case entry.
 *
 * @param obj test case entry
 * @param parsed_flags flags field that should contain the C flags
 * @param jsonkey JSON key of the test vector holding the flag to be converted.
 * @param flagsconv block of flags conversion definition to be applied. Only
 *		    one flag out of the flags definition array is allowed at
 *		    any given time.
 */
static void parse_flagblock(const struct json_object *obj,
			    flags_t *parsed_flags,
			    const char *jsonkey, enum json_type type,
			    const struct parser_flagsconv *flagsconv)
{
	const struct parser_flagsconv *conv = flagsconv;
	struct json_object *o = NULL;
	flags_t remove_flags = 0;
	const char *string = NULL;
	int ret = json_find_key(obj, jsonkey, &o, type);
	bool found = false;

	/* keyword not found, so no conversion necessary */
	if (ret)
		return;

	while (conv->flag) {
		remove_flags |= conv->flag;
		conv++;
	}

	/* Clear out existing flags that will be set in this block. */
	*parsed_flags &= ~remove_flags;

	if (type == json_type_string)
		string = json_object_get_string(o);

	conv = flagsconv;
	while (conv->flag) {
		switch (type) {
		case json_type_string:
			if ((strlen(conv->val.string) == strlen(string)) &&
			    (strcasestr(conv->val.string, string))) {
				*parsed_flags |= conv->flag;
				logger(LOGGER_VERBOSE,
				       "Found JSON flag: %" PRIu64 " (%s)\n",
				       *parsed_flags, conv->log);

				found = true;
			}
			break;
		case json_type_boolean:
			if (conv->val.boolean == json_object_get_boolean(o)) {
				*parsed_flags |= conv->flag;
				logger(LOGGER_VERBOSE,
				       "Found JSON flag: %" PRIu64 " (%s)\n",
				       *parsed_flags, conv->log);

				found = true;
			}
			break;

		case json_type_array:
		case json_type_double:
		case json_type_int:
		case json_type_null:
		case json_type_object:
		default:
			logger(LOGGER_WARN, "Unhandled data type %s\n",
			       json_type_to_name(type));
			break;
		}

		conv++;
	}

	//TODO: some keywords are reused (e.g. "mode" in RSA and DRBGs) with
	// totally different meanings - shall we add a search restriction to
	// the parser_flagsconv structure to limit the applicability of the
	// structure?
	if (!found) {
		logger(LOGGER_VERBOSE,
		       "Found JSON key %s but value is unhandled\n", jsonkey);
	}

	return;
}

/* Flags conversion definition for the encryption/decryption indicator */
static const struct parser_flagsconv flagsconv_direction[] = {
	{FLAG_OP_ENC, {.string = "encrypt"}, "encryption"},
	{FLAG_OP_DEC, {.string = "decrypt"}, "decryption"},
	{FLAG_OP_CMAC_GEN_TEST, {.string = "gen"}, "CMAC generation"},
	{FLAG_OP_CMAC_VER_TEST, {.string = "ver"}, "CMAC verification"},
	{0, {NULL}, NULL}
};

/* Flags conversion definition for test type */
static const struct parser_flagsconv flagsconv_testtype[]= {
	{FLAG_OP_AFT, {.string = "AFT"}, "AFT test type"},
	{FLAG_OP_MCT, {.string = "MCT"}, "MCT test type"},
	{FLAG_OP_KAT, {.string = "KAT"}, "KAT test type"},
	{FLAG_OP_GDT, {.string = "GDT"}, "GDT test type"},
	{FLAG_OP_VAL, {.string = "VAL"}, "VAL test type"},
	{FLAG_OP_AFT, {.string = "CTR"}, "CTR test type"},
	{FLAG_OP_VOT, {.string = "VOT"}, "VOT test type"},
	{FLAG_OP_LDT, {.string = "LDT"}, "LDT test type"},
	{FLAG_OP_MVT, {.string = "MVT"}, "MVT test type"},
	{0, {NULL}, NULL}
};

/* Flags conversion for mode */
static const struct parser_flagsconv flagsconv_mode[] = {
	{FLAG_OP_ASYM_TYPE_SIGGEN, {.string = "sigGen"}, "Asymmetric signature generation"},
	{FLAG_OP_ASYM_TYPE_SIGVER, {.string = "sigVer"}, "Asymmetric signature verification"},
	{FLAG_OP_ASYM_TYPE_KEYGEN, {.string = "keyGen"}, "Asymmetric key generation"},
	{FLAG_OP_ASYM_TYPE_KEYVER, {.string = "keyVer"}, "Asymmetric key verification"},
	{FLAG_OP_RSA_TYPE_LEGACY_SIGVER, {.string = "legacySigVer"},
					"RSA legacy signature verification"},
	{FLAG_OP_RSA_TYPE_COMPONENT_SIG_PRIMITIVE, {.string = "signaturePrimitive"},
					"RSA signature component primitive"},
	{FLAG_OP_RSA_TYPE_COMPONENT_DEC_PRIMITIVE, {.string = "decryptionPrimitive"},
					"RSA decryption component primitive"},
	{FLAG_OP_DSA_TYPE_PQGGEN, {.string = "pqgGen"}, "DSA PQG generation"},
	{FLAG_OP_DSA_TYPE_PQGVER, {.string = "pqgVer"}, "DSA PQG verification"},

	{FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST,
		{.string = "CDH-Component"}, "ECCDH component test"},
	{FLAG_OP_KAS_SCHEME_TEST,
		{.string = "Component"}, "KAS test"},

	{FLAG_OP_KDF_TYPE_TLS, {.string = "tls"}, "TLS KDF"},
	{FLAG_OP_KDF_TYPE_IKEV2, {.string = "ikev2"}, "IKEv2 KDF"},
	{FLAG_OP_KDF_TYPE_IKEV1, {.string = "ikev1"}, "IKEv1 KDF"},
	{FLAG_OP_KDF_TYPE_SSH, {.string = "ssh"}, "SSHv2 KDF"},
	{FLAG_OP_KDF_TYPE_ANSI_X963, {.string = "ansix9.63"}, "ANSI X9.63 KDF"},
	{FLAG_OP_KDF_TYPE_SRTP, {.string = "srtp"}, "SRTP KDF"},

	{0, {NULL}, NULL}
};

/* Flags conversion for RSA randPQ */
static const struct parser_flagsconv flagsconv_rsarandpq[] = {
	{FLAG_OP_RSA_PQ_B32_PRIMES, {.string = "B.3.2"}, "RSA rand PQ primes Appendix B.3.2"},
	{FLAG_OP_RSA_PQ_B33_PRIMES, {.string = "B.3.3"}, "RSA rand PQ primes Appendix B.3.3"},
	{FLAG_OP_RSA_PQ_B34_PRIMES, {.string = "B.3.4"}, "RSA rand PQ primes Appendix B.3.4"},
	{FLAG_OP_RSA_PQ_B35_PRIMES, {.string = "B.3.5"}, "RSA rand PQ primes Appendix B.3.5"},
	{FLAG_OP_RSA_PQ_B36_PRIMES, {.string = "B.3.6"}, "RSA rand PQ primes Appendix B.3.6"},
	{0, {NULL}, NULL}
};

/* Flags conversion for RSA keyFormat */
static const struct parser_flagsconv flagsconv_rsakeyformat[] = {
	{FLAG_OP_RSA_CRT, {.string = "crt"}, "RSA CRT key format"},
	{0, {NULL}, NULL}
};

/* Flags conversion for RSA signature type */
static const struct parser_flagsconv flagsconv_rsasigtype[] = {
	{FLAG_OP_RSA_SIG_PKCS15, {.string = "pkcs1v1.5"}, "RSA signature PKCS15"},
	{FLAG_OP_RSA_SIG_X931, {.string = "ansx9.31"}, "RSA signature X9.31"},
	{FLAG_OP_RSA_SIG_PKCS1PSS, {.string = "pss"}, "RSA signature PKCS1 PSS"},
	{0, {NULL}, NULL}
};

/* Flags conversion for RSA primality test */
#if 0
static const struct parser_flagsconv flagsconv_rsaprimetest[] = {
	{FLAG_OP_RSA_PRIME_TEST_C2, "tblC2", "RSA primality test C.2"},
	{FLAG_OP_RSA_PRIME_TEST_C3, "tblC3", "RSA primality test C.3"},
	{0, {NULL}, NULL}
};
#endif

/* Flags conversion for SHA bitwise definition */
static const struct parser_flagsconv flagsconv_shabitwise[] = {
	{FLAG_OP_SHA_BITWISE, {.boolean = true}, "SHA bitwise"},
	{FLAG_OP_SHA_BYTEWISE, {.boolean = false}, "SHA bytewise"},
	{0, {NULL}, NULL}
};

/* Flags conversion for SHA empty string support */
static const struct parser_flagsconv flagsconv_shaempty[] = {
	{FLAG_OP_SHA_EMPTY_MSG, {.boolean = true}, "SHA empty message included"},
	{0, {NULL}, NULL}
};

static const struct parser_flagsconv flagsconv_ecdsa_secretgenerationmode[] = {
	{FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS, {.string = "extra bits"}, "ECDSA key generation B.4.1"},
	{FLAG_OP_ECDSA_SECRETGENTYPE_TESTING, {.string = "testing candidates"}, "ECDSA key generation B.4.2"},
	{0, {NULL}, NULL}
};

static const struct parser_flagsconv flagsconv_dsa_mode[] = {
	{FLAG_OP_DSA_PROBABLE_PQ_GEN, {.string = "probable"}, "DSA probable P/Q generation"},
	{FLAG_OP_DSA_PROVABLE_PQ_GEN, {.string = "provable"}, "DSA provable P/Q generation"},
	{FLAG_OP_DSA_UNVERIFIABLE_G_GEN, {.string = "unverifiable"}, "DSA unverifiable G generation"},
	{FLAG_OP_DSA_CANONICAL_G_GEN, {.string = "canonical"}, "DSA canonical G generation"},
	{0, {NULL}, NULL}
};

/* Flags conversion for ECDH and DH schema */
static const struct parser_flagsconv flagsconv_scheme[] = {
	{FLAG_OP_ECDH_SCHEME_FULL_UNIFIED, {.string = "fullUnified"}, "Full Unified"},
	{FLAG_OP_ECDH_SCHEME_FULL_MQV, {.string = "fullMqv"}, "ECDH full MQV"},
	{FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED, {.string = "ephemeralUnified"},
						"ECDH ephemeral unified"},
	{FLAG_OP_ECDH_SCHEME_ONE_PASS_UNIFIED, {.string = "onePassUnified"},
						"ECDH one pass unified"},
	{FLAG_OP_ECDH_SCHEME_ONE_PASS_MQV, {.string = "onePassMqv"}, "ECDH one pass MQV"},
	{FLAG_OP_ECDH_SCHEME_ONE_PASS_DH, {.string = "onePassDh"}, "ECDH one pass DH"},
	{FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED, {.string = "staticUnified"},
						"ECDH static unified"},

	{FLAG_OP_DH_SCHEME_DH_HYBRID1, {.string = "dhHybrid1"}, "DH Hybrid 1"},
	{FLAG_OP_DH_SCHEME_MQV2, {.string = "MQV2"}, "MQV2"},
	{FLAG_OP_DH_SCHEME_EPHEMERAL, {.string = "dhEphem"}, "DH ephemeral"},
	{FLAG_OP_DH_SCHEME_HYBRID_ONE_FLOW, {.string = "dhHybridOneFlow"},
							"DH hybrid one flow"},
	{FLAG_OP_DH_SCHEME_MQV1, {.string = "MQV1"}, "MQV1"},
	{FLAG_OP_DH_SCHEME_ONE_FLOW, {.string = "dhOneFlow"}, "DH one flow"},
	{FLAG_OP_DH_SCHEME_STATIC, {.string = "dhStatic"}, "DH static"},

	{0, {NULL}, NULL}
};

static const struct parser_flagsconv flagsconv_kasrole[] = {
	{FLAG_OP_KAS_ROLE_INITIATOR, {.string = "initiator"}, "KAS initiator"},
	{FLAG_OP_KAS_ROLE_RESPONDER, {.string = "responder"}, "KAS responder"},
	{0, {NULL}, NULL}
};

static const struct parser_flagsconv flagsconv_authmethod[] = {
	{FLAG_OP_KDF_TYPE_IKEV1_PSK, {.string = "psk"}, "IKEv1 PSK authentication method"},
	{FLAG_OP_KDF_TYPE_IKEV1_DSA, {.string = "dsa"}, "IKEv1 DSA authentication method"},
	{FLAG_OP_KDF_TYPE_IKEV1_PKE, {.string = "pke"}, "IKEv1 PKE authentication method"},
	{0, {NULL}, NULL}
};

static const struct parser_flagsconv flagsconv_drbg_otherinput[] = {
	{FLAG_OP_DRBG_RESEED, {.string = "reSeed"}, "DRBG reseed data"},
	{FLAG_OP_DRBG_GENERATE, {.string = "generate"}, "DRBG reseed data for prediction resistance"},
	{0, {NULL}, NULL}
};

static const struct parser_flagsconv flagsconv_tls13_runningmode[] = {
	{FLAG_OP_TLS13_RUNNING_MODE_DHE, {.string = "DHE"}, "TLS v1.3 DHE running mode"},
	{FLAG_OP_TLS13_RUNNING_MODE_PSK, {.string = "PSK"}, "TLS v1.3 PSK running mode"},
	{FLAG_OP_TLS13_RUNNING_MODE_PSKDHE, {.string = "PSK-DHE"}, "TLS v1.3 PSK-DHE running mode"},
	{0, {NULL}, NULL}
};

/**
 * @brief For each JSON hierarchy level, the flags are parsed and accumulated
 *	  in the parsed_flags variable.
 *
 * @param obj [in] Input JSON hierarchy level to read.
 * @param parsed_flags [out] The flags found in the JSON hiararchy level.
 *
 * @return 0 on success, < 0 on error
 */
static int parse_flags(const struct json_object *obj, flags_t *parsed_flags)
{
	/* Symmetric ciphers */
	parse_flagblock(obj, parsed_flags, "direction", json_type_string,
			flagsconv_direction);

	/* Different ciphers */
	parse_flagblock(obj, parsed_flags, "testType", json_type_string,
			flagsconv_testtype);

	/* RSA */
	parse_flagblock(obj, parsed_flags, "mode", json_type_string,
			flagsconv_mode);
	parse_flagblock(obj, parsed_flags, "randPQ", json_type_string,
			flagsconv_rsarandpq);
	parse_flagblock(obj, parsed_flags, "sigType", json_type_string,
			flagsconv_rsasigtype);
	parse_flagblock(obj, parsed_flags, "keyFormat", json_type_string,
			flagsconv_rsakeyformat);
#if 0
	parse_flagblock(obj, parsed_flags, "primeTest", flagsconv_rsaprimetest);
#endif

	/* SHA */
	parse_flagblock(obj, parsed_flags, "inBit", json_type_boolean,
			flagsconv_shabitwise);
	parse_flagblock(obj, parsed_flags, "inEmpty", json_type_boolean,
			flagsconv_shaempty);

	/* ECDH / DH */
	parse_flagblock(obj, parsed_flags, "scheme", json_type_string,
			flagsconv_scheme);
	parse_flagblock(obj, parsed_flags, "kasRole", json_type_string,
			flagsconv_kasrole);

	/* ECDSA */
	parse_flagblock(obj, parsed_flags, "secretGenerationMode",
			json_type_string, flagsconv_ecdsa_secretgenerationmode);

	/* DSA */
	parse_flagblock(obj, parsed_flags, "gMode", json_type_string,
			flagsconv_dsa_mode);
	parse_flagblock(obj, parsed_flags, "pqMode", json_type_string,
			flagsconv_dsa_mode);

	/* IKEv1 */
	parse_flagblock(obj, parsed_flags, "authenticationMethod",
			json_type_string, flagsconv_authmethod);

	/* DRBG */
	parse_flagblock(obj, parsed_flags, "intendedUse", json_type_string,
			flagsconv_drbg_otherinput);

	/* TLS v1.3 */
	parse_flagblock(obj, parsed_flags, "runningMode", json_type_string,
			flagsconv_tls13_runningmode);

	return 0;
}

static int parse_all_processdata(const struct json_array *processdata,
				 const struct json_object *json_obj,
				 flags_t parsed_flags,
				 struct json_object *testresults);
static int parse_array(const struct json_entry *entry,
		       const struct json_object *readdata,
		       flags_t parsed_flags,
		       struct json_object *testresults)
{
	struct json_object *json_nobj;
	const struct json_array *processdata = entry->data.data.array;
	uint32_t i;
	int ret = 0;

	CKINT_LOG(json_find_key(readdata, entry->name, &json_nobj,
				json_type_array),
		  "Name %s not found\n", entry->name);

	if (!json_nobj) {
		logger(LOGGER_ERR,
		       "Parsing of entry %s with expected array failed\n",
		      entry->name);
		return -EINVAL;
	}

	/* Iterate over all array members and parse each individually. */
	for (i = 0; i < (uint32_t)json_object_array_length(json_nobj); i++) {
		struct json_object *testvector =
			json_object_array_get_idx(json_nobj, i);

		CKNULL_LOG(testvector, -EINVAL, "No vector\n");

		/* Find out about flags and operation types */
		CKINT_LOG(parse_flags(testvector, &parsed_flags),
			  "Parsing flags failed\n");

		/* Parse all members of one array entry. */
		CKINT_LOG(parse_all_processdata(processdata, testvector,
						parsed_flags, testresults),
			  "Parsing processdata failed\n");

		/* Apply test invocation, if there is any defined. */
		CKINT_LOG(exec_test(processdata, parsed_flags, testvector,
				    testresults), "Test execution failed\n");

		/* Free all allocated data. */
		vector_free_all_array(processdata);
	}

out:
	vector_free_all_array(processdata);
	return ret;
}

static int parse_buffer_array(const struct json_entry *entry,
			      const struct json_object *readdata,
			      flags_t parsed_flags,
			      struct json_object *testresults)
{
	struct json_object *json_nobj;
	const struct json_array *processdata = entry->data.data.array;
	uint32_t i;
	int ret = 0;

	if (!entry->name) {
		/* Find out about flags and operation types */
		CKINT(parse_flags(readdata, &parsed_flags));

		/* Parse all members of one array entry. */
		CKINT(parse_all_processdata(processdata, readdata,
					    parsed_flags, testresults));
		goto out;
	}

	CKINT_LOG(json_find_key(readdata, entry->name, &json_nobj,
				json_type_array),
		  "Name %s not found\n", entry->name);

	if (!json_nobj) {
		logger(LOGGER_ERR,
		       "Parsing of entry %s with expected array failed\n",
		      entry->name);
		return -EINVAL;
	}

	/* Iterate over all array members and parse each individually. */
	for (i = 0; i < (uint32_t)json_object_array_length(json_nobj); i++) {
		struct json_object *testvector =
			json_object_array_get_idx(json_nobj, i);

		CKNULL(testvector, -EINVAL);

		/* Find out about flags and operation types */
		CKINT(parse_flags(testvector, &parsed_flags));

		/* Parse all members of one array entry. */
		CKINT(parse_all_processdata(processdata, testvector,
					    parsed_flags, testresults));
	}

out:
	/* We do not count here, so do not relay positive integers */
	return (ret < 0) ? ret : 0;
}

static int parse_object(const struct json_entry *entry,
			const struct json_object *readdata,
			flags_t parsed_flags,
			struct json_object *testresults)
{
	struct json_object *json_nobj;
	const struct json_array *processdata = entry->data.data.array;
	int ret = 0;

	CKNULL_LOG(entry->name, -EINVAL, "Entry name missing\n");

	CKINT(json_find_key(readdata, entry->name, &json_nobj,
			    json_type_object));

	if (!json_nobj) {
		logger(LOGGER_ERR,
		       "Parsing of entry %s with expected array failed\n",
		      entry->name);
		return -EINVAL;
	}

	CKINT(parse_all_processdata(processdata, json_nobj, parsed_flags,
				    testresults));

out:
	/* We do not count here, so do not relay positive integers */
	return (ret < 0) ? ret : 0;
}

/**
 * @brief Apply one parser definition to the JSON hierarchy level.
 *
 * Note, the parser works by analyzing one JSON hierarchy level at a time.
 * All keywords in one hierarchy level are in scope and can be searched for.
 * The parser definition must use one of the data types implemented below.
 *
 * @param entry One entry of the parser definition to apply to the input
 *		data.
 * @param readdata Input JSON data to be parsed.
 * @param parsed_flags All flags that have been parsed so far.
 * @param testresults Output JSON data that contains the JSON data that were
 *		      generated to far by applying previous test definitions.
 *
 * @return 0 on success but no entry found, 1 on success and entry found,
 *	   < 0 on error
 */
static int parse_one_entry(const struct json_entry *entry,
			   const struct json_object *readdata,
			   flags_t parsed_flags,
			   struct json_object *testresults)
{
	const struct json_data *data = &entry->data;
	struct buffer_array *barray;
	int ret = 0;

	CKNULL_LOG(entry, -EINVAL,
		   "Empty search entry found in function parse_one_entry\n");

	/* Apply entry only if it matches the condition. */
	if (!match_entry(parsed_flags, entry->flags, entry->name))
		return 0;

	/* Process different types of search entries. */
	switch (data->datatype) {
	case PARSER_BIN:
		logger(LOGGER_DEBUG, "Get binary data for %s\n", entry->name);
		ret = json_get_bin(readdata, entry->name, data->data.buf);
		break;
	case PARSER_BIN_BUFFERARRAY:
		barray = data->data.buffer_array;
		if (barray->arraysize >= MAX_BUFFER_ARRAY) {
			logger(LOGGER_ERR,
			       "Array size %u reached, diregarding entry\n",
			       MAX_BUFFER_ARRAY);
			ret = -EINVAL;
			goto out;
		}

		ret = json_get_bin(readdata, entry->name,
				   &barray->buffers[barray->arraysize]);
		logger(LOGGER_DEBUG, "Parsing buffer array entry %u\n",
		       barray->arraysize);
		barray->arraysize++;
		break;
	case PARSER_UINT:
		ret = json_get_uint(readdata, entry->name, data->data.integer);
		break;
	case PARSER_UINT64:
		ret = json_get_uint64(readdata, entry->name,
				      data->data.largeint);
		break;
	case PARSER_UINT_RANDOM:
		ret = json_get_uint_random(readdata, entry->name,
					   data->data.integer);
		break;
	case PARSER_CIPHER:
		{
			const char *cipher;

			ret = json_get_string(readdata, entry->name, &cipher);
			if (ret)
				break;

			*data->data.largeint = convert_algo_cipher(cipher,
							*data->data.largeint);
			if (*data->data.largeint == ACVP_UNKNOWN) {
				logger(LOGGER_WARN,
				       "Unknown cipher algorithm %s\n", cipher);
				ret = -EINVAL;
				goto out;
			}
			break;
		}
	case PARSER_CIPHER_ARRAY:
		{
			uint32_t i;

			for (i = 0;
			     i < (uint32_t)json_object_array_length(readdata);
			     i++) {
				struct cipher_array *carray =
							data->data.cipher_array;
				const char *cipher;

				if (carray->arraysize >= MAX_BUFFER_ARRAY) {
					logger(LOGGER_ERR,
					"Array size %u reached, diregarding entry\n",
					       MAX_CIPHER_ARRAY);
					ret = -EINVAL;
					goto out;
				}

				CKINT(json_get_string(readdata, entry->name,
						      &cipher));
				carray->cipher[carray->arraysize] =
					convert_algo_cipher(cipher,
						carray->cipher[carray->arraysize]);
				if (carray->cipher[carray->arraysize] ==
				    ACVP_UNKNOWN) {
					logger(LOGGER_WARN,
					       "Unknown cipher algorithm %s\n", cipher);
					ret = -EINVAL;
					goto out;
				}
				carray->arraysize++;
			}
			break;
		}
	case PARSER_BOOL:
		ret = json_get_bool(readdata, entry->name, data->data.integer);
		break;
	case PARSER_ARRAY:
		logger(LOGGER_DEBUG, "Parsing array for JSON key %s\n",
		       entry->name ? entry->name : "(unnamed)");
		ret = parse_array(entry, readdata, parsed_flags, testresults);
		break;
	case PARSER_OBJECT:
		logger(LOGGER_DEBUG, "Parsing object for JSON key %s\n",
		       entry->name ? entry->name : "(unnamed)");
		ret = parse_object(entry, readdata, parsed_flags, testresults);
		break;
	case PARSER_ARRAY_BUFFERARRAY:
		logger(LOGGER_DEBUG, "Parsing array for JSON key %s\n",
		       entry->name ? entry->name : "(unnamed)");
		ret = parse_buffer_array(entry, readdata, parsed_flags,
					 testresults);
		break;
	case PARSER_MPINT:
		ret = json_get_mpint(readdata, entry->name, data->data.buf);
		break;
	case PARSER_STRING:
		ret = json_get_string_buf(readdata, entry->name,
					  data->data.buf);
		break;

	case WRITER_BIN:
	case WRITER_BIN_ALWAYS:
	case WRITER_BOOL:
	case WRITER_BOOL_TRUE_TO_FALSE:
	case WRITER_ECC:
	case WRITER_HASH:
	case WRITER_STRING_NOFREE:
	case WRITER_UINT:
	default:
		logger(LOGGER_ERR, "Unknown data type %u to be parsed\n",
		       data->datatype);
		break;
	}

	/* If marked as optional, we do not care about return code */
	if (entry->flags & FLAG_OPTIONAL)
		ret = 0;

	if (ret) {
		logger(LOGGER_WARN, "Searched object: %s\n",
		       entry->name ? entry->name : "(unnamed)");
	}

out:
	return ret ? ret : 1;
}

/**
 * @brief Iterate over the parser definitions and execute them.
 *
 * @param processdata Parser definition to process
 * @param readdata JSON input data to analyze
 * @param parsed_flags The parsed flags that are already found.
 * @param testresults JSON output data
 *
 * @return 0 on success, < 0 on error
 */
static int parse_all_processdata(const struct json_array *processdata,
				 const struct json_object *readdata,
				 flags_t parsed_flags,
				 struct json_object *testresults)
{
	const struct json_entry *entry;
	struct json_object *tgid = NULL;
	struct json_object *tgid_entry = NULL;
	uint32_t i;
	int ret = 0, processed = 0;

	ret = json_find_key(readdata, "tgId", &tgid, json_type_int);
	if (!ret) {
		/* Create a tgID entry. */
		struct json_object *new_testresults;

		tgid_entry = json_object_new_object();
		CKNULL(tgid_entry, ENOMEM);
		json_object_get(tgid);

		CKINT(json_object_object_add(tgid_entry, "tgId", tgid));
		json_logger(LOGGER_DEBUG, tgid, "Processing tgID");

		new_testresults = json_object_new_array();
		CKNULL(new_testresults, -ENOMEM);
		CKINT(json_object_object_add(tgid_entry, "tests",
					     new_testresults));

		/* Add the tgID entry */
		CKINT(json_object_array_add(testresults, tgid_entry));

		/* The new "sub-"array is to be filled */
		testresults = new_testresults;
	}
	ret = 0;

	/* Iterate over all members of the search criteria and apply them. */
	for_each_arraymember(processdata, entry, i) {
		CKINT(parse_one_entry(entry, readdata, parsed_flags,
				      testresults));
		processed += ret;
	}

	/* Iterate over each write definition and invoke it. */
	if (tgid_entry && processdata->testresult) {
		for_each_testresult(processdata->testresult, entry, i)
			CKINT(write_one_entry(entry, tgid_entry, parsed_flags));

		vector_free_all_array(processdata);
	}

out:
	return ret ? ret : processed;
}

int process_json(const struct json_array *processdata, const char *exp_version,
		 struct json_object *in, struct json_object *out)
{
	const struct json_entry *entry;
	struct json_object *testresults, *acvpdata, *versiondata,
			   *outversion, *outresults;
	flags_t parsed_flags = 0;
	uint32_t i;
	int ret;

	CKNULL_LOG(processdata, -EINVAL,
		   "Usage error of function process_json\n");
	CKNULL_LOG(in, -EINVAL, "Usage error of function process_json\n");
	CKNULL_LOG(out, -EINVAL, "Usage error of function process_json\n");

	/* Get version and ACVP test vector data */
	CKINT(json_split_version(in, &acvpdata, &versiondata));

	/* Check the version of the JSON input with the expected version. */
	outversion = json_object_new_object();
	CKNULL(outversion, -ENOMEM);
	CKINT(json_check_acvversion(versiondata, exp_version, outversion));

	/* Add version information to final output array. */
	CKINT(json_object_array_add(out, outversion));

	/* Add meta data to results */
	outresults = json_object_new_object();
	CKNULL(outresults, -ENOMEM);
	CKINT(json_add_response_data(acvpdata, outresults));

	/* Add test results to final output array. */
	CKINT(json_object_array_add(out, outresults));

	/* Find out about flags and operation types */
	CKINT(parse_flags(acvpdata, &parsed_flags));

	/* Create the output JSON stream holding the test results. */
	testresults = json_object_new_array();
	CKNULL(testresults, -ENOMEM);
	CKINT(json_object_object_add(outresults, "testGroups", testresults));

	/* Process JSON data with the given set of search parameters. */
	ret = parse_all_processdata(processdata, acvpdata, parsed_flags,
				    testresults);
	/* We do not count any more */
	if (ret > 0)
		ret = 0;

	/* Iterate over each write definition and invoke it. */
	if (processdata->testresult) {
		for_each_testresult(processdata->testresult, entry, i)
			CKINT(write_one_entry(entry, outresults,
					      parsed_flags));
	}


out:
	/* Clean all allocated data, if any. */
	vector_free_all_array(processdata);
	return ret;
}
