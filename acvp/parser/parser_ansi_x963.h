/*
 * Copyright (C) 2021 - 2022, Stephan Mueller <smueller@chronox.de>
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

#ifndef _PARSER_ANSI_X963_H
#define _PARSER_ANSI_X963_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief ANSI X9.63 KDF testing
 *
 * @var hashalg [in] Hash algorithm to be used for KDF.
 * @var field_size [in] The field length used in bits
 * @var key_data_len [in] The encryption key length used in bits
 * @var z [in] Shared secret buffer
 * @var shared_info [in] Buffer with shared information
 *			 (NOTE buffer may be NULL if shared information length
 *			  is zero)
 * @var key_data [out] Buffer with the generated key - backend must allocate
 *		       buffer, the parser takes care of disposing of it.
 */
struct ansi_x963_data {
	uint64_t hashalg;
	uint32_t field_size;
	uint32_t key_data_len;
	struct buffer z;
	struct buffer shared_info;

	struct buffer key_data;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 * @var ansi_x963 Perform a ANSI X9.63 key derivation
 */
struct ansi_x963_backend {
	int (*ansi_x963)(struct ansi_x963_data *data, flags_t parsed_flags);
};

void register_ansi_x963_impl(struct ansi_x963_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_ANSI_X963_H */
