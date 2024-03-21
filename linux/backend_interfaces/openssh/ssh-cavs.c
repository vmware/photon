/*
 * Copyright (C) 2015 - 2022, Stephan Mueller <smueller@chronox.de>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * ALTERNATIVELY, this product may be distributed under the terms of
 * the GNU General Public License, in which case the provisions of the GPL2
 * are required INSTEAD OF the above restrictions.  (This clause is
 * necessary due to a potential bad interaction between the GPL and
 * the restrictions contained in a BSD-style copyright.)
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

#include "includes.h"

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <string.h>

#include <openssl/bn.h>

#include "xmalloc.h"
#include "sshbuf.h"
#include "sshkey.h"
#include "cipher.h"
#include "kex.h"
#include "packet.h"

static int bin_char(unsigned char hex)
{
	if (48 <= hex && 57 >= hex)
		return (hex - 48);
	if (65 <= hex && 70 >= hex)
		return (hex - 55);
	if (97 <= hex && 102 >= hex)
		return (hex - 87);
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
static void hex2bin(const char *hex, size_t hexlen,
		    unsigned char *bin, size_t binlen)
{
	size_t i = 0;
	size_t chars = (binlen > (hexlen / 2)) ? (hexlen / 2) : binlen;

	for (i = 0; i < chars; i++) {
		bin[i] = bin_char(hex[(i*2)]) << 4;
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
static int hex2bin_alloc(const char *hex, size_t hexlen,
			 unsigned char **bin, size_t *binlen)
{
	unsigned char *out = NULL;
	size_t outlen = 0;

	if (!hexlen)
		return -EINVAL;

	outlen = (hexlen + 1) / 2;

	out = calloc(1, outlen);
	if (!out)
		return -errno;

	hex2bin(hex, hexlen, out, outlen);
	*bin = out;
	*binlen = outlen;
	return 0;
}

static char hex_char_map_l[] = { '0', '1', '2', '3', '4', '5', '6', '7',
				 '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };
static char hex_char_map_u[] = { '0', '1', '2', '3', '4', '5', '6', '7',
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
static void bin2hex(const unsigned char *bin, size_t binlen,
		    char *hex, size_t hexlen, int u)
{
	size_t i = 0;
	size_t chars = (binlen > (hexlen / 2)) ? (hexlen / 2) : binlen;

	for (i = 0; i < chars; i++) {
		hex[(i*2)] = hex_char((bin[i] >> 4), u);
		hex[((i*2)+1)] = hex_char((bin[i] & 0x0f), u);
	}
}

struct kdf_cavs {
	unsigned char *K;
	size_t Klen;
	unsigned char *H;
	size_t Hlen;
	unsigned char *session_id;
	size_t session_id_len;

	unsigned int iv_len;
	unsigned int ek_len;
	unsigned int ik_len;
};

static int sshkdf_cavs(struct kdf_cavs *test)
{
	int ret = 0;
	struct kex kex;
	BIGNUM *Kbn = NULL;
	int mode = 0;
	struct newkeys *ctoskeys;
	struct newkeys *stockeys;
	struct ssh *ssh = NULL;

#define HEXOUTLEN 500
	char hex[HEXOUTLEN];

	memset(&kex, 0, sizeof(struct kex));

	Kbn = BN_new();
	BN_bin2bn(test->K, test->Klen, Kbn);
	if (!Kbn) {
		printf("cannot convert K into BIGNUM\n");
		ret = 1;
		goto out;
	}

	kex.session_id = test->session_id;
	kex.session_id_len = test->session_id_len;

	/* setup kex */

	/* select the right hash based on struct ssh_digest digests */
	switch (test->ik_len) {
		case 20:
			kex.hash_alg = 1;
			break;
		case 32:
			kex.hash_alg = 2;
			break;
		case 48:
			kex.hash_alg = 3;
			break;
		case 64:
			kex.hash_alg = 4;
			break;
		default:
			printf("Wrong hash type %u\n", test->ik_len);
			ret = 1;
			goto out;
	}

	/* implement choose_enc */
	for (mode = 0; mode < 2; mode++) {
		kex.newkeys[mode] = calloc(1, sizeof(struct newkeys));
		if (!kex.newkeys[mode]) {
			printf("allocation of newkeys failed\n");
			ret = 1;
			goto out;
		}
		kex.newkeys[mode]->enc.iv_len = test->iv_len;
		kex.newkeys[mode]->enc.key_len = test->ek_len;
		kex.newkeys[mode]->enc.block_size = (test->iv_len == 64) ? 8 : 16;
		kex.newkeys[mode]->mac.key_len = test->ik_len;
	}

	/* implement kex_choose_conf */
	kex.we_need = kex.newkeys[0]->enc.key_len;
	if (kex.we_need < kex.newkeys[0]->enc.block_size)
		kex.we_need = kex.newkeys[0]->enc.block_size;
	if (kex.we_need < kex.newkeys[0]->enc.iv_len)
		kex.we_need = kex.newkeys[0]->enc.iv_len;
	if (kex.we_need < kex.newkeys[0]->mac.key_len)
		kex.we_need = kex.newkeys[0]->mac.key_len;

	/* MODE_OUT (1) -> server to client
	 * MODE_IN (0) -> client to server */
	kex.server = 1;

	/* do it */
	if ((ssh = ssh_packet_set_connection(NULL, -1, -1)) == NULL){
		printf("Allocation error\n");
		goto out;
	}
	ssh->kex = &kex;
	kex_derive_keys_bn(ssh, test->H, test->Hlen, Kbn);

	ctoskeys = kex.newkeys[0];
	stockeys = kex.newkeys[1];

	/* get data */
	memset(hex, 0, HEXOUTLEN);
	bin2hex(ctoskeys->enc.iv, (size_t)ctoskeys->enc.iv_len,
		hex, HEXOUTLEN, 0);
	printf("Initial IV (client to server) = %s\n", hex);
	memset(hex, 0, HEXOUTLEN);
	bin2hex(stockeys->enc.iv, (size_t)stockeys->enc.iv_len,
		hex, HEXOUTLEN, 0);
	printf("Initial IV (server to client) = %s\n", hex);

	memset(hex, 0, HEXOUTLEN);
	bin2hex(ctoskeys->enc.key, (size_t)ctoskeys->enc.key_len,
		hex, HEXOUTLEN, 0);
	printf("Encryption key (client to server) = %s\n", hex);
	memset(hex, 0, HEXOUTLEN);
	bin2hex(stockeys->enc.key, (size_t)stockeys->enc.key_len,
		hex, HEXOUTLEN, 0);
	printf("Encryption key (server to client) = %s\n", hex);

	memset(hex, 0, HEXOUTLEN);
	bin2hex(ctoskeys->mac.key, (size_t)ctoskeys->mac.key_len,
		hex, HEXOUTLEN, 0);
	printf("Integrity key (client to server) = %s\n", hex);
	memset(hex, 0, HEXOUTLEN);
	bin2hex(stockeys->mac.key, (size_t)stockeys->mac.key_len,
		hex, HEXOUTLEN, 0);
	printf("Integrity key (server to client) = %s\n", hex);

out:
	if (Kbn)
		BN_free(Kbn);
	if (ssh)
		ssh_packet_close(ssh);
	return ret;
}

static void usage(void)
{
	fprintf(stderr, "\nOpenSSH KDF CAVS Test\n\n");
	fprintf(stderr, "Usage:\n");
	fprintf(stderr, "\t-K\tShared secret string\n");
	fprintf(stderr, "\t-H\tHash string\n");
	fprintf(stderr, "\t-s\tSession ID string\n");
	fprintf(stderr, "\t-i\tIV length to be generated\n");
	fprintf(stderr, "\t-e\tEncryption key length to be generated\n");
	fprintf(stderr, "\t-m\tMAC key length to be generated\n");
}

/*
 * Test command example:
 * ./ssh-cavs -K 0055d50f2d163cc07cd8a93cc7c3430c30ce786b572c01ad29fec7597000cf8618d664e2ec3dcbc8bb7a1a7eb7ef67f61cdaf291625da879186ac0a5cb27af571b59612d6a6e0627344d846271959fda61c78354aa498773d59762f8ca2d0215ec590d8633de921f920d41e47b3de6ab9a3d0869e1c826d0e4adebf8e3fb646a15dea20a410b44e969f4b791ed6a67f13f1b74234004d5fa5e87eff7abc32d49bbdf44d7b0107e8f10609233b7e2b7eff74a4daf25641de7553975dac6ac1e5117df6f6dbaa1c263d23a6c3e5a3d7d49ae8a828c1e333ac3f85fbbf57b5c1a45be45e43a7be1a4707eac779b8285522d1f531fe23f890fd38a004339932b93eda4 -H d3ab91a850febb417a25d892ec48ed5952c7a5de -s d3ab91a850febb417a25d892ec48ed5952c7a5de -i 8 -e 24 -m 20
 *
 * Initial IV (client to server) = 4bb320d1679dfd3a
 * Initial IV (server to client) = 43dea6fdf263a308
 * Encryption key (client to server) = 13048cc600b9d3cf9095aa6cf8e2ff9cf1c54ca0520c89ed
 * Encryption key (server to client) = 1e483c5134e901aa11fc4e0a524e7ec7b75556148a222bb0
 * Integrity key (client to server) = ecef63a092b0dcc585bdc757e01b2740af57d640
 * Integrity key (server to client) = 7424b05f3c44a72b4ebd281fb71f9cbe7b64d479
 */
int main(int argc, char *argv[])
{
	struct kdf_cavs test;
	int ret = 1;
	int opt = 0;

	memset(&test, 0, sizeof(struct kdf_cavs));
	while((opt = getopt(argc, argv, "K:H:s:i:e:m:")) != -1)
	{
		size_t len = 0;
		switch(opt)
		{
			/*
			 * CAVS K is MPINT
			 * we want a hex (i.e. the caller must ensure the
			 * following transformations already happened):
			 * 	1. cut off first four bytes
			 * 	2. if most significant bit of value is
			 *	   1, prepend 0 byte
			 */
			case 'K':
				len = strlen(optarg);
				ret = hex2bin_alloc(optarg, len,
						    &test.K, &test.Klen);
				if (ret)
					goto out;
				break;
			case 'H':
				len = strlen(optarg);
				ret = hex2bin_alloc(optarg, len,
						    &test.H, &test.Hlen);
				if (ret)
					goto out;
				break;
			case 's':
				len = strlen(optarg);
				ret = hex2bin_alloc(optarg, len,
						    &test.session_id,
						    &test.session_id_len);
				if (ret)
					goto out;
				break;
			case 'i':
				test.iv_len = strtoul(optarg, NULL, 10);
				break;
			case 'e':
				test.ek_len = strtoul(optarg, NULL, 10);
				break;
			case 'm':
				test.ik_len = strtoul(optarg, NULL, 10);
				break;
			default:
				usage();
				goto out;
		}
	}

	ret = sshkdf_cavs(&test);

out:
	if (test.session_id)
		free(test.session_id);
	if (test.K)
		free(test.K);
	if (test.H)
		free(test.H);
	return ret;

}
