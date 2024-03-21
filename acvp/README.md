# Generic ACVP JSON Parser

This parser implements the ACVP protocol used by NIST for the automated
CAVS testing (Automated Cryptographic Validation Program - ACVP).

This parser processes JSON files that are already downloaded from the
ACVP server. It invokes the cryptographic implementation and generates
the test response JSON data as defined by the ACVP protocol.

The entire ACVP server interaction including download of test vectors
and upload of test responses must be handled with a separate tool, like the
ACVP Proxy.

The ACVP Proxy is proudly supported by [atsec information security corp](https://www.atsec.com).

## Usage

The ACVP Parser operates on one file at a time. Simply invoke

`acvp-parser <testvector-request.json> <testvector-response.json>`

NOTE: If you want to use the ACVP Parser in unison with the ACVP Proxy, you
MUST use the file name `testvector-response.json` to hold the test responses!

If you want to compare two test responses with each other, simply use

`acvp-parser -e <expected-response.json> <testvector-response.json>`

To increase verbosity, use `-v` one or more times.

## Concept of Parser

The parser is implemented as a data-driven engine. The JSON parsing code
is separated from the definitions of which parts of the JSON input stream
to parse and which format the JSON input stream is expected to have.

This implies that an implementation for a specific test definition, such as
the AEAD or symmetric cipher algorithm, the test definitions do not
contain any code, but only the data specifying the expected JSON format
and pointing to the local variables where the data is to be stored into.

In addition to the parsing of the input data, the data-driven model allows
specifying the test execution convention and which local variables shall be
exported to the JSON stream holding the test results.

The data model is defined with the different data structures found in
parser_common.h.

As a rule of thumb: if there is any parsing related code except the
invocation of process_json in the test definition specification of the different
parser_*.c files (except parser_common.c), there is a programming error and
a violation of the basic concept.

## Architecture

The parser consists of 3 layers:

1. parser.c implements a linked list where all parsers with usable
   callbacks are registered. Each parser must register with a particular cipher
   identifier. When a JSON file is parsed, the cipher identifier is searched for
   and the respective parser handler is called if a match is found.

2. parser_*.c implement the register functions registering with parser.c
   In addition, they implement the handler function that is triggered when
   parser.c is finished. The idea now is that the respective parser is invoked
   with the JSON file it can handle. The parser now implements all logic to:

	* parse the JSON file

	* obtain all relevant data from the JSON file and store it in a parser
	  specific data structure

	* invoke the backend implementation that interfaces with the cipher
	  mechanism implementation

	* create the JSON response file with the correct format.

3. backend_*.c implement the backend that uses the parser data structure to
   invoke a specific crypto library. The backend is not needed to implement all
   backend functions of all parsers. If a callback from a parser is not
   supported, it must be marked as NULL. If a parser identifies a NULL handler,
   it returns with an error such that the JSON file cannot be processed.

## Backend Selection

To select the appropriate backend, invoke make with the right option.

When invoking `make` the implemented compile options are given.


# Building

## Prerequisite

The ACVP parser requires the presence of the POSIX APIs.

## Compiling

As discussed above, the backend must be chosen out of the list given with
`make`.

NOTE: If the backend <NAME> is chosen, the file backend_<NAME>.c must
exist.

Example: To compile the OpenSSL support, invoke: `make openssl`.

## Building on Cygwin

The following steps are required to build the ACVP Proxy on Cygwin:

- Verify that the required cygwin packages are installed:

	* gcc

	* make

- Build acvp-parser.exe using with a build target as outlined above.

## Backend-specific Hints: Linux Kernel

The ACVP test for the Linux kernel requires a kernel module that is provided
with the directory `backend_interfaces/kcapi/`. You need to compile it and load
it into the kernel.

The ACVP Parser tool must now be executed as root to access the kernel module's
interface files at `/sys/kernel/debug/kcapi-cavs`.

## Backend-specific Hints: Libreswan

To execute the Libreswan ACVP test, you need to compile an application
that will be invoked by the ACVP parser. See
`backend_interfaces/libreswan/README` for details on compiling the
interface application.

Ensure that the inteface application is found via the PATH environment
variable.

## Backend-specific Hints: Strongswan

To execute the Strongswan ACVP test, you need to compile an application
that will be invoked by the ACVP parser. See
`backend_interfaces/strongswan/README` for details on compiling the
interface application.

Ensure that the inteface application is found via the PATH environment
variable.

## Backend-specific Hints: OpenSSH

To execute the OpenSSH ACVP test, you need to compile an application
that will be invoked by the ACVP parser. See
`backend_interfaces/openssh/README` for details on compiling the
interface application.

Ensure that the inteface application is found via the PATH environment
variable.

## Backend-specific Hints: BoringSSL

Please modify the Makefile to point to the static library to compile against.

# Helper Scripts

## Test Execution Scripts

Helper scripts for executing multiple test vectors for a given module are
provided in the `helper/` directory. Note, the script `exec_lib.sh` is not
intended to be executed directly, but provides a library for the other
scripts.

The scripts are all named `exec_<modulename>.sh`.

## Regression Test Scripts

The ACVP Parser can also be used as a regression test system. The regression
tests are executed with a helper script given for each module.

The scripts are named `exec_<modulename>_regression.sh`.

It is permissible to provide one or more vsIDs as command line parameters for
the regression test script. In this case, only the referenced vsIDs regression
tested.

Note, the regression test is deactivated for test vectors that are based on
random numbers to be generated by the module.

# Backend Implementation

A backend is the code that connects the parser with a particular cryptographic
implementation. A backend implements the code that invokes the cryptographic
implementation to be tested using the data provided with various data
structures.

The backend implementation is invoked once for each individual cipher test.
It does not need to carry state information other than what is required
by the particular cryptographic implementation it interfaces with.

The backend is unrelated to any formatting or other CAVS/ACVP logic.

A backend implementation is achieved with the following steps:

1. Include `backend_common.h` from the parser. There are no other header files
   from the parser needed. The `backend_common.h includes the various header
   files of the different parsers for the cipher implementations.

2. Select which cipher implementations the backend shall handle. For each
   cipher implementation, there is a `parser_*.h` header that defines the
   data structure(s) used to exchange data between the parser and the backend
   as well as the interface functions that need to be implemented by the
   backend. For the following example, a SHA hash implementation shall be
   tested. The corresponding header file is `parser_sha.h` which contains
   the `struct sha_data` definition. The documentation explains which member
   variables are provided by the parser and which data is expected to be
   returned by the backend. Furthermore, the `parser_sha.h` header defines
   the `struct sha_backend` function pointer data structure that must be
   filled by the backend.

3. The backend implements the functions defined by the function pointer data
   structure. In case of SHA, the `hash_generate` function must be implemented
   following the definition of the function in `parser_sha.h`.

4. The backend must now register its implementation by defining the function
   pointer data structure and registering it with the register call found
   in `parser_sha.h`. The function pointer data structure instance must
   be marked with the `ACVP_DEFINE_CONSTRUCTOR` macro to ensure that it is
   invoked by the operating system loader during load time of the executable.
   The following example illustrates this registering:

   ```
   static int backend_sha_generate(struct sha_data *data, flags_t parsed_flags)
   {
   ...
           <invoke the backend's SHA function>;
   ....
   }

   static struct sha_backend backend_sha =
   {
           backend_sha_generate,
   };

   ACVP_DEFINE_CONSTRUCTOR(backend_sha_backend)
   static void backend_sha_backend(void)
   {
            register_sha_impl(&backend_sha);
   }
   ```

5. Ensure that the C file(s) implementing the backend is compiled when compiling
   the parser.

The example outlines that apart from including the `backend_common.h`, no
further change is needed to link the backend implementation with the parser.

Note, the parser will guarantee that only one backend can register its callback
function pointer data structure for a given cipher. I.e. the function
`register_sha_impl` used in the example above MUST ONLY be used once in the
entire code base of the parser that is compiled. Subsequent register operations
for a particular cipher type will fail.

# Author

Stephan Mueller  <smueller@chronox.de>
Copyright (C) 2018 - 2021
