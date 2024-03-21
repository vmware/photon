/*
 * Copyright (C) 2019 - 2022, Stephan Mueller <smueller@chronox.de>
 *
 * License: see LICENSE file
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT KDF_108LL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 */

#ifndef _PARSER_TLS13_H
#define _PARSER_TLS13_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief TLS v1.3 data structure
 *
 * @var hash [in] hash to be used for the KDF - note, the backend must
 *		  use the hash to initialize the HMAC cipher as required by
 *		  the TLS 1.3 specification.
 * @var psk [in] Random pre-shared key, included for PSK and PSK-DHE running
 *		 modes.
 * @var dhe [in] Random Diffie-Hellman shared secret, included for DHE and
 *		 PSK-DHE running modes.
 * @var server_hello_random [in] Server hello random value
 * @var client_hello_random [in] Client hello random value
 * @var server_finished_random [in] Server finished random value
 * @var client_finished_random [in] Client finished random value
 *
 * @var client_early_traffic_secret [out] The client early traffic secret.
 *	`Derive-Secret(., "c e traffic", ClientHello)`
 * @var early_exporter_master_secret [out] The early exporter master secret.
 *	`Derive-Secret(., "e exp master", ClientHello)`
 * @var client_handshake_traffic_secret [out] The client handshake traffic
 *					      secret.
 *	`Derive-Secret(., "c hs traffic", ClientHello...ServerHello)`
 * @var server_handshake_traffic_secret [out] The server handshake traffic
 *					      secret.
 *	`Derive-Secret(., "s hs traffic", ClientHello...ServerHello)`
 * @var client_application_traffic_secret [out] The client application traffic
 * 						secret.
 *	`Derive-Secret(., "c ap traffic", ClientHello...server Finished)`
 * @var server_application_traffic_secret [out] The server application traffic
 *						secret.
 *	`Derive-Secret(., "s ap traffic", ClientHello...server Finished)`
 * @var exporter_master_secret [out] The exporter master secret.
 *	`Derive-Secret(., "exp master", ClientHello...server Finished)`
 * @var resumption_master_secret [out] The resumption master secret.
 * 	`Derive-Secret(., "res master", ClientHello...client Finished)`
 */
struct tls13_data {
	uint64_t hash;
	struct buffer psk;
	struct buffer dhe;
	struct buffer server_hello_random;
	struct buffer client_hello_random;
	struct buffer server_finished_random;
	struct buffer client_finished_random;

	struct buffer client_early_traffic_secret;
	struct buffer early_exporter_master_secret;
	struct buffer client_handshake_traffic_secret;
	struct buffer server_handshake_traffic_secret;
	struct buffer client_application_traffic_secret;
	struct buffer server_application_traffic_secret;
	struct buffer exporter_master_secret;
	struct buffer resumption_master_secret;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 * @var tls13 Perform a TLS 1.3 PRF operation
 */
struct tls13_backend {
	int (*tls13)(struct tls13_data *data, flags_t parsed_flags);
};

void register_tls13_impl(struct tls13_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_TLS13_H */
