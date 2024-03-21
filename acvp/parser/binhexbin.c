/*
 * Convert hex string into binary representation and vice versa
 *
 * Copyright (C) 2014 - 2022, Stephan Mueller <smueller@chronox.de>
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

#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

#include "binhexbin.h"

static uint8_t bin_char(char hex)
{
	if (48 <= hex && 57 >= hex)
		return (uint8_t)(hex - 48);
	if (65 <= hex && 70 >= hex)
		return (uint8_t)(hex - 55);
	if (97 <= hex && 102 >= hex)
		return (uint8_t)(hex - 87);
	return 0;
}

/*
 * Convert hex representation into binary string
 * @hex input buffer with hex representation
 * @hexlen length of hex
 * @bin output buffer with binary data
 * @binlen length of already allocated bin buffer (should be at least
 *	   half of hexlen -- if not, only a fraction of hexlen is converted)
 */
void hex2bin(const char *hex, size_t hexlen,
	     uint8_t *bin, size_t binlen)
{
	size_t i;
	size_t chars = (binlen > (hexlen / 2)) ? (hexlen / 2) : binlen;

	/*
	 * handle odd-length of strings where the first digit is the least
	 * significant nibble
	 */
	if (hexlen & 1) {
		bin[0] = bin_char(hex[0]);
		bin++;
		hex++;
	}

	for (i = 0; i < chars; i++) {
		bin[i] = (uint8_t)(bin_char(hex[(i*2)]) << 4);
		bin[i] |= bin_char(hex[((i*2)+1)]);
	}
}

/*
 * Allocate sufficient space for binary representation of hex
 * and convert hex into bin
 *
 * Caller must free bin
 * @hex input buffer with hex representation
 * @hexlen length of hex
 * @bin return value holding the pointer to the newly allocated buffer
 * @binlen return value holding the allocated size of bin
 *
 * return: 0 on success, !0 otherwise
 */
int hex2bin_alloc(const char *hex, size_t hexlen,
		  uint8_t **bin, size_t *binlen)
{
	uint8_t *out = NULL;
	size_t outlen = 0;

	if (!hexlen)
		return -EINVAL;

	outlen = (hexlen + 1) / 2;

	out = calloc(1, outlen + 1);
	if (!out)
		return -errno;

	hex2bin(hex, hexlen, out, outlen);
	*bin = out;
	*binlen = outlen;
	return 0;
}

static const char hex_char_map_l[] = { '0', '1', '2', '3', '4', '5', '6', '7',
				       '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };
static const char hex_char_map_u[] = { '0', '1', '2', '3', '4', '5', '6', '7',
				       '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };
static char hex_char(unsigned int bin, int u)
{
	if (bin < sizeof(hex_char_map_l))
		return (u) ? hex_char_map_u[bin] : hex_char_map_l[bin];
	return 'X';
}

/*
 * Convert binary string into hex representation
 * @bin input buffer with binary data
 * @binlen length of bin
 * @hex output buffer to store hex data
 * @hexlen length of already allocated hex buffer (should be at least
 *	   twice binlen -- if not, only a fraction of binlen is converted)
 * @u case of hex characters (0=>lower case, 1=>upper case)
 */
void bin2hex(const uint8_t *bin, size_t binlen,
	     char *hex, size_t hexlen, int u)
{
	size_t i = 0;
	size_t chars = (binlen > (hexlen / 2)) ? (hexlen / 2) : binlen;

	for (i = 0; i < chars; i++) {
		hex[(i*2)] = hex_char((bin[i] >> 4), u);
		hex[((i*2)+1)] = hex_char((bin[i] & 0x0f), u);
	}
}

/*
 * Allocate sufficient space for hex representation of bin
 * and convert bin into hex
 *
 * Caller must free hex
 * @bin input buffer with bin representation
 * @binlen length of bin
 * @hex return value holding the pointer to the newly allocated buffer
 * @hexlen return value holding the allocated size of hex
 *
 * return: 0 on success, !0 otherwise
 */
int bin2hex_alloc(const uint8_t *bin, size_t binlen,
		  char **hex, size_t *hexlen)
{
	char *out = NULL;
	size_t outlen = 0;

	if (!binlen)
		return -EINVAL;

	outlen = (binlen) * 2;

	out = calloc(1, outlen + 1);
	if (!out)
		return -errno;

	bin2hex(bin, binlen, out, outlen, 0);
	*hex = out;
	*hexlen = outlen;
	return 0;
}

void bin2print(const unsigned char *bin, size_t binlen,
	       FILE *out, const char *explanation)
{
	char *hex = NULL;
	size_t hexlen = binlen * 2 + 1;

	if (binlen) {
		hex = calloc(1, hexlen);
		if (!hex)
			return;
		bin2hex(bin, binlen, hex, hexlen - 1 , 0);
	}
	fprintf(out, "%s = %s\n", explanation, (hex) ? hex : "");
	free(hex);
}
