/*
 * Copyright (C) 2019 - 2022, Stephan Mueller <smueller@chronox.de>
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

#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

#define ARRAY_SIZE(a) (sizeof(a)/sizeof(a[0]))

uint64_t convert_algo_cipher(const char *algo, uint64_t cipher);
int convert_cipher_algo(uint64_t cipher, uint64_t cipher_type_mask,
			const char **algo);
int convert_cipher_match(uint64_t cipher1, uint64_t cipher2,
			 uint64_t cipher_type_mask);
int convert_cipher_contain(uint64_t cipher1, uint64_t cipher2,
			   uint64_t cipher_type_mask);

#ifdef __cplusplus
}
#endif

#endif /* ALGORITHMS_H */
