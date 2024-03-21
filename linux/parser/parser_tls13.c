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
 * TLS13 callback definitions
 ******************************************************************************/
static struct tls13_backend *tls13_backend = NULL;

static int kdf_tester_tls13(struct json_object *in, struct json_object *out,
			    uint64_t cipher)
{
	(void)cipher;

	/**********************************************************************
	 * TLS13 operation
	 **********************************************************************/
	DEF_CALLBACK(tls13, tls13, FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE);

	const struct json_entry tls13_testresult_entries[] = {
		{"clientEarlyTrafficSecret",		{.data.buf = &tls13_vector.client_early_traffic_secret, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"earlyExporterMasterSecret",		{.data.buf = &tls13_vector.early_exporter_master_secret, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},

		{"clientHandshakeTrafficSecret",	{.data.buf = &tls13_vector.client_handshake_traffic_secret, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"serverHandshakeTrafficSecret",	{.data.buf = &tls13_vector.server_handshake_traffic_secret, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},

		{"clientApplicationTrafficSecret",	{.data.buf = &tls13_vector.client_application_traffic_secret, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"serverApplicationTrafficSecret",	{.data.buf = &tls13_vector.server_application_traffic_secret, WRITER_BIN},	FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},

		{"exporterMasterSecret",		{.data.buf = &tls13_vector.exporter_master_secret, WRITER_BIN},			FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"resumptionMasterSecret",		{.data.buf = &tls13_vector.resumption_master_secret, WRITER_BIN},		FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
	};
	const struct json_testresult tls13_testresult =
		SET_ARRAY(tls13_testresult_entries, &tls13_callbacks);

	const struct json_entry tls13_test_entries[] = {
		{"dhe",			{.data.buf = &tls13_vector.dhe, PARSER_BIN},			FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"psk",			{.data.buf = &tls13_vector.psk, PARSER_BIN},			FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"helloClientRandom",	{.data.buf = &tls13_vector.client_hello_random, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"helloServerRandom",	{.data.buf = &tls13_vector.server_hello_random, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"finishedClientRandom",{.data.buf = &tls13_vector.client_finished_random, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"finishedServerRandom",{.data.buf = &tls13_vector.server_finished_random, PARSER_BIN},	FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
	};

	/* search for empty arrays */
	const struct json_array tls13_test = SET_ARRAY(tls13_test_entries, &tls13_testresult);

	const struct json_entry tls13_testgroup_entries[] = {
		{"hmacAlg",		{.data.largeint = &tls13_vector.hash, PARSER_CIPHER},	FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
		{"tests",		{.data.array = &tls13_test, PARSER_ARRAY},		FLAG_OP_AFT | FLAG_OP_TLS13_RUNNING_MODE_DHE | FLAG_OP_TLS13_RUNNING_MODE_PSK | FLAG_OP_TLS13_RUNNING_MODE_PSKDHE},
	};
	const struct json_array tls13_testgroup = SET_ARRAY(tls13_testgroup_entries, NULL);

	/**********************************************************************
	 * KDF common test group
	 **********************************************************************/
	const struct json_entry tls13_testanchor_entries[] = {
		{"testGroups",			{.data.array = &tls13_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array tls13_testanchor = SET_ARRAY(tls13_testanchor_entries, NULL);

	/* Process all. */
	return process_json(&tls13_testanchor, "1.0", in, out);
}

static struct cavs_tester tls13 =
{
	ACVP_KDF_TLS13,
	0,
	kdf_tester_tls13,
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_tls13)
static void register_tls13(void)
{
	register_tester(&tls13, "TLS13");
}

void register_tls13_impl(struct tls13_backend *implementation)
{
	register_backend(tls13_backend, implementation, "TLS13");
}
