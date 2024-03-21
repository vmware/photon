# Addition of Cipher Parser

To add a new cipher parser, e.g. when NIST announced a new cipher is testable
with ACVP, the following steps must be taken:

1. Create a new parser_<cipher_name>.h that contains:

	a) the data structure definition(s) holding all input and output
	   data the backend will be handed to perform testing for the new
	   cipher. The new parser is intended to fill the input values defined
	   in the data structure(s) and to unparse the output values into JSON
	   The backend is intended it take the input data to invoke the cipher
	   and fill the output values.

	b) the function pointer data structure that allows the callback to
	   register its handler functions that are invoked by the parser.

	c) the register function allowing the backend to register its
	   filled-in function pointer data structure.

   Note: The ACVP Parser uses different macros to help using the parser.
   These macros assume the following conventions:

	a) Data structures holding the test data must be named
	   struct <cipher>_data

	b) The data structure with the function pointers must be named
	   struct <cipher>_backend

2. Add the new parser_<cipher_name>.h to backend_common.h.

3. Create a new parser implementation parser_<cipher_name>.c that contains:

	a) the register function invoked by the constructor to register the
	   new parser with the ACVP Parser framework.

	b) the register function must provide a filled-in struct cavs_tester
	   that specifies the entry-point function of the parser.

	c) implement the entry-point function (see below for guidance)

4. Update the ACVP Parser framework to make the new parser support known:

	a) add DEF_CALLBACK_TYPE in parser_common.h - note, use the <cipher>
	   string here (the same string that you used for the
	   struct <cipher>_data above).

	b) add a new CB_TYPE_<cipher> in parser_common.h

	c) extend the union in struct json_callback with the convention
	   struct <cipher>_callback <cipher>

	d) add a CB_HANDLER(<cipher>) in parser_common.c:exec_test()

## Parser Entry-Point Function

Ultimately the parser can be implemented as you wish, but the ACVP Parser
framework provides utility functions to simplify the parser construction.
Only the use of those helpers are documented here as any other approach should
not be applied.

### Backend Registration

The backend must be offered a function that allows registering a filled-in
function pointer data structure. Usually this is achieved with the following
example:

```
void register_hkdf_impl(struct hkdf_backend *implementation)
{
	register_backend(hkdf_backend, implementation, "HKDF");
}
```

This code implies that there is a global variable holding the backend in the
parser file:

```
static struct hkdf_backend *hkdf_backend = NULL;
```

Note, use the naming convention of <cipher>_backend if you want to use
the helper macros discussed in the following.

The first step of the parser entry-point function is to verify that this
pointer is filled in by the backend:

```
	if (!hkdf_backend) {
		logger(LOGGER_WARN, "No SP800-108 KDF backend set\n");
		return -EOPNOTSUPP;
	}
```

## Flags

Note that the parser framework automatically parses flags from the test vector
which are provided to implement conditionals in the parsing logic.

The test vectors not only contain the test data, but also contain meta
information that tell how the data is to be interpreted. The most common
examples are the flags for "AFT", "VAL", etc. which are referenced by the
JSON keyword "testType".

Flags that are known and parsed are defined in parser_flags.h

## Notify Parser Framework of Backend Function Pointers

The parser framework eventually will execute the individual function pointer
that are present in the function pointer data structure.

Such a specific callback is defined with the
DEF_CALLBACK(<function pointer>, <cipher>, flags). The flags must be a superset of
the flags that are parsed - i.e. this is how you ensure conditionals.

For example if you have a callback for AFT and one for VAL, you

DEF_CALLBACK(<aft_ptr>, <cipher>, FLAG_OP_AFT);

and

DEF_CALLBACK(<val_ptr>, <cipher>, FLAG_OP_VAL);

Note, the <cipher> will be resolved to the <cipher>_callback registered above.

Note, the DEF_CALLBACK also defines a local data structure called
<cipher>_vector that is the instance of struct <cipher>_vector.

## Parsing

The concept of the parser is to define a hierarchy of data structures that
are traversed by the parser framework. This hierarchy must follow the JSON
hierarchy that is to be parsed.

Each hierarchy entry is defined by three data structures:

`struct json_entry` defines a structure parsing the JSON keywords. In addition
this data structure is also used to define the JSON structure to unparse
output data.

`struct json_array` references one `struct json_entry` definition and one
`struct json_testresult` entry: the first is the parsing of the data and
the second is the unparsing of test result data. The unparsing data structure
may be NULL if no JSON keywords shall be create at the given JSON hierarchy
level.

Each entry in a `struct json_array` contains flags that must be a superset
of the parsed flags at the given hierarchy level. It also contains the hint to
parse or unparse data. Also, the definition defines the JSON keyword to be
parsed or unparsed.

The following parsing code is defined.

- PARSER_ARRAY: Provide a new `struct json_array` for the next lower JSON
hierarchy structure. Use it with
`.data.array = &<new_json_array_implementation>`.

- PARSER_CIPHER: Parse a cipher name into the data structure with
`.data.largeint = &<cipher>_vector.<target_variable> - the parser framework
converts the string representation of the cipher into a uint64_t value defined
in cipher_definitions.h

- PARSER_UINT: Parse an integer: `.data.integer = &<cipher>_backend.<integer>`

- PARSER_BIN: Parse a hex string into a struct buffer and convert it to binary
  `.data.buf = &<cipher>_backend.<struct buffer>`

- WRITER_BIN: Unparse a binary into hex string:
  `.data.buf = &<cipher>_backend.<struct buffer>`

For the others, see parser_common.h

Note, the parser framework performs an automated garbage collection, so you
do not need to manually free data.

# Author

Stephan Müller <smueller@chronox.de>
