/* Jitter RNG ACVP Test Tool for SHA-3 256 conditioner
 *
 * Copyright (C) 2020 - 2022, Stephan Mueller <smueller@chronox.de>
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

#define _DEFAULT_SOURCE
#include <stdlib.h>
#include "backend_common.h"

#undef MAJVERSION
#undef MINVERSION
#undef PATCHLEVEL
#undef ARRAY_SIZE

/* This is for Jitter RNG >= 3.1.0 */
#include "jitterentropy-sha3.c"

/* This is for Jitter RNG < 3.1.0 */
//#include "jitterentropy-base.c"

/************************************************
 * SHA cipher interface functions
 ************************************************/
static int jent_sha_generate(struct sha_data *data, flags_t parsed_flags)
{
	HASH_CTX_ON_STACK(ctx);
	int ret;

	(void)parsed_flags;

	if (data->cipher != ACVP_SHA3_256)
		return -EOPNOTSUPP;

	CKINT(alloc_buf(SHA3_256_SIZE_DIGEST, &data->mac));

	sha3_256_init(&ctx);
	sha3_update(&ctx, data->msg.buf, data->msg.len);
	sha3_final(&ctx, data->mac.buf);

out:
	return ret;
}

static struct sha_backend jent_sha =
{
	jent_sha_generate,   /* hash_generate */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(jent_sha_backend)
static void jent_sha_backend(void)
{
	register_sha_impl(&jent_sha);
}
