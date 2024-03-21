/* OpenSSH backend
 *
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

#define _DEFAULT_SOURCE
#include <ctype.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#include "binhexbin.h"
#include "logger.h"
#include "read_json.h"
#include "stringhelper.h"

#include "backend_common.h"

/*
 * This backend uses the ssh-cavs helper tool. This tool must be compiled
 * as outlined in its readme and must be found in PATH.
 */

static int openssh_handle_child_process_output(char *buffer,
					       struct kdf_ssh_data *data)
{
	int ret;
	char *res = NULL;
	char *saveptr = NULL;

	logger(LOGGER_DEBUG, "Parsing buffer %s\n", buffer);

	res = strtok_r(buffer, "\n", &saveptr);

	while (res) {
		if (strstr(res, "Initial IV (client to server)")) {
			CKINT(get_binval(res, "=", &data->initial_iv_client));
		} else if (strstr(res, "Initial IV (server to client)")) {
			CKINT(get_binval(res, "=", &data->initial_iv_server));
		} else if (strstr(res, "Encryption key (client to server)")) {
			CKINT(get_binval(res, "=",
					 &data->encryption_key_client));
		} else if (strstr(res, "Encryption key (server to client)")) {
			CKINT(get_binval(res, "=",
					 &data->encryption_key_server));
		} else if (strstr(res, "Integrity key (client to server)")) {
			CKINT(get_binval(res, "=",
					 &data->integrity_key_client));
		} else if (strstr(res, "Integrity key (server to client)")) {
			CKINT(get_binval(res, "=",
					 &data->integrity_key_server));
		}

		res = strtok_r(NULL, "\n", &saveptr);
	}

	if (!data->initial_iv_client.len || !data->initial_iv_server.len ||
	    !data->encryption_key_client.len ||
	    !data->encryption_key_server.len ||
	    !data->integrity_key_client.len ||
	    !data->integrity_key_server.len) {
		logger(LOGGER_WARN, "Data not found in buffer:\n%s\n", buffer);
		ret = -EINVAL;
	} else {
		logger(LOGGER_DEBUG, "Parsing successful\n");
		ret = 0;
	}

out:
	return ret;
}

static int openssh_kdf_ssh(struct kdf_ssh_data *data, flags_t parsed_flags)
{
	BUFFER_INIT(K);
	char *k_hex = NULL, *h_hex = NULL, *session_id_hex = NULL, *buffer_p,
	     *k_mpint_hex = NULL;
	char ivlen_buf[11], enclen_buf[11], maclen_buf[11];
	char buffer[4096];
	size_t k_hex_len, h_hex_len, session_id_hex_len, k_mpint_hex_len;
	unsigned int ivlen, enclen, maclen, buflen;
	pid_t pid;
	int ret;
	int filedes[2];

	(void)parsed_flags;

	filedes[0] = -1;
	filedes[1] = -1;

	CKINT(bin2hex_alloc(data->k.buf, data->k.len, &k_mpint_hex,
			    &k_mpint_hex_len));
	CKINT(mpint2bin(k_mpint_hex, (uint32_t)k_mpint_hex_len, &K));

	CKINT(bin2hex_alloc(K.buf, K.len, &k_hex, &k_hex_len));
	CKINT(bin2hex_alloc(data->h.buf, data->h.len, &h_hex, &h_hex_len));
	CKINT(bin2hex_alloc(data->session_id.buf, data->session_id.len,
			    &session_id_hex, &session_id_hex_len));

	switch (data->cipher & ACVP_SYMMASK) {
	case ACVP_AES128:
		enclen = 16;
		ivlen = 16;
		break;
	case ACVP_AES192:
		enclen = 24;
		ivlen = 16;
		break;
	case ACVP_AES256:
		enclen = 32;
		ivlen = 16;
		break;
	case ACVP_TDESECB:
		enclen = 24;
		ivlen = 8;
		break;
	default:
		logger(LOGGER_WARN, "Cipher not identified\n");
		ret = -EINVAL;
		goto out;
	}

	switch (data->cipher & ACVP_HASHMASK) {
	case ACVP_SHA1:
		maclen = 20;
		break;
	case ACVP_SHA256:
		maclen = 32;
		break;
	case ACVP_SHA384:
		maclen = 48;
		break;
	case ACVP_SHA512:
		maclen = 64;
		break;
	default:
		logger(LOGGER_WARN, "Mac not identified\n");
		ret = -EINVAL;
		goto out;
	}

	snprintf(enclen_buf, sizeof(enclen_buf), "%u", enclen);
	snprintf(ivlen_buf, sizeof(ivlen_buf), "%u", ivlen);
	snprintf(maclen_buf, sizeof(maclen_buf), "%u", maclen);

	if (pipe(filedes) == -1) {
		ret = -errno;
		logger(LOGGER_WARN, "Cannot create pipe\n");
		goto out;
	}

	pid = fork();
	if (pid == -1) {
		ret = -errno;
		logger(LOGGER_WARN, "Fork failed\n");
		goto out;
	}

	if (pid == 0) {
		while ((dup2(filedes[1], STDOUT_FILENO) == -1) &&
			(errno == EINTR)) {}
		close(filedes[1]);
		close(filedes[0]);
		logger(LOGGER_DEBUG,
		       "Execute: ssh-cavs -K %s -H %s -s %s -i %s -e %s -m %s\n",
			k_hex, h_hex, session_id_hex, ivlen_buf, enclen_buf,
			maclen_buf);
		execlp("ssh-cavs", "ssh-cavs",
		       "-K", k_hex,
		       "-H", h_hex,
		       "-s", session_id_hex,
		       "-i", ivlen_buf,
		       "-e", enclen_buf,
		       "-m", maclen_buf,
		       (char*)NULL);
		printf("Execl failed\n");
		logger(LOGGER_ERR, "Execl failed\n");
		ret = -EFAULT;
		goto out;
	}

	buffer_p = buffer;
	buflen = sizeof(buffer) - 1;
	close(filedes[1]);
	while (1) {
		ssize_t count = read(filedes[0], buffer_p, buflen);

		if (count == -1) {
			if (errno == EINTR) {
				continue;
			} else {
				ret = -errno;
				logger(LOGGER_WARN, "Read error");
				goto out;
			}
		} else if (count == 0) {
			*buffer_p = 0;
			CKINT(openssh_handle_child_process_output(buffer,
								  data));
			break;
		} else {
			buffer_p += count;
			buflen -= count;
		}
	}
	wait(NULL);


out:
	if (filedes[0] >= 0)
		close(filedes[0]);
	if (k_hex)
		free(k_hex);
	if (h_hex)
		free(h_hex);
	if (session_id_hex)
		free(session_id_hex);
	if (k_mpint_hex)
		free(k_mpint_hex);
	free_buf(&K);
	return ret;
}

static struct kdf_ssh_backend openssh_kdf =
{
	openssh_kdf_ssh,
};

ACVP_DEFINE_CONSTRUCTOR(openssh_kdf_ssh_backend)
static void openssh_kdf_ssh_backend(void)
{
	register_kdf_ssh_impl(&openssh_kdf);
}
