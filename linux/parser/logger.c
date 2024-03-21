/* Logging support
 *
 * Copyright (C) 2018 - 2022, Stephan Mueller <smueller@chronox.de>
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

#define _DEFAULT_SOURCE
#include <time.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

#include "binhexbin.h"
#include "logger.h"
#include "term_colors.h"

static enum logger_verbosity logger_verbosity_level = LOGGER_NONE;

static void logger_severity(enum logger_verbosity severity, char *sev,
			    unsigned int sevlen)
{
	switch (severity) {
	case LOGGER_DEBUG2:
		snprintf(sev, sevlen, "Debug2");
		break;
	case LOGGER_DEBUG:
		snprintf(sev, sevlen, "Debug");
		break;
	case LOGGER_VERBOSE:
		snprintf(sev, sevlen, "Verbose");
		break;
	case LOGGER_WARN:
		snprintf(sev, sevlen, "Warning");
		break;
	case LOGGER_ERR:
		snprintf(sev, sevlen, "Error");
		break;
	case LOGGER_STATUS:
		snprintf(sev, sevlen, "Status");
		break;
	case LOGGER_NONE:
		break;
	case LOGGER_MAX_LEVEL:
	default:
		snprintf(sev, sevlen, "Unknown");
	}
}

void _logger(enum logger_verbosity severity,
	     const char *file, const char *func,
	     const size_t line, const char *fmt, ...)
{
	time_t now;
	struct tm now_detail;
	va_list args;
	int(* fprintf_color)(FILE *stream, const char *format, ...) = &fprintf;
	char msg[4096];
	char sev[10];

	if (severity > logger_verbosity_level)
		return;

	va_start(args, fmt);
	vsnprintf(msg, sizeof(msg), fmt, args);
	va_end(args);

	logger_severity(severity, sev, sizeof(sev));

	now = time(NULL);
	localtime_r(&now, &now_detail);

	switch (severity) {
	case LOGGER_DEBUG2:
		fprintf_color = &fprintf_cyan;
		break;
	case LOGGER_DEBUG:
		fprintf_color = &fprintf_blue;
		break;
	case LOGGER_VERBOSE:
		fprintf_color = &fprintf_green;
		break;
	case LOGGER_WARN:
		fprintf_color = &fprintf_yellow;
		break;
	case LOGGER_ERR:
		fprintf_color = &fprintf_red;
		break;
	case LOGGER_STATUS:
		fprintf_color = &fprintf_magenta;
		break;
	case LOGGER_NONE:
		break;
	case LOGGER_MAX_LEVEL:
	default:
		fprintf_color = &fprintf;
	}

	switch (logger_verbosity_level) {
	case LOGGER_DEBUG2:
	case LOGGER_DEBUG:
		fprintf_color(stderr,
			      "ACVPParser (%.2d:%.2d:%.2d) %s [%s:%s:%u]: ",
			      now_detail.tm_hour, now_detail.tm_min,
			      now_detail.tm_sec, sev, file, func, line);
		break;
	case LOGGER_VERBOSE:
	case LOGGER_WARN:
	case LOGGER_ERR:
	case LOGGER_STATUS:
	case LOGGER_NONE:
	case LOGGER_MAX_LEVEL:
	default:
		fprintf_color(stderr,
			      "ACVPParser (%.2d:%.2d:%.2d) %s: ",
			      now_detail.tm_hour, now_detail.tm_min,
			      now_detail.tm_sec, sev);
		break;
	}

	fprintf(stderr, "%s", msg);
}

void _logger_binary(const enum logger_verbosity severity,
		    const unsigned char *bin, const size_t binlen,
		    const char *str, const char *file,
		    const char *func, const size_t line)
{
	time_t now;
	struct tm now_detail;
	char sev[10];
	char msg[4096];

	if (severity > logger_verbosity_level)
		return;

	logger_severity(severity, sev, sizeof(sev));

	now = time(NULL);
	localtime_r(&now, &now_detail);

	switch (logger_verbosity_level) {
	case LOGGER_DEBUG2:
	case LOGGER_DEBUG:
		snprintf(msg, sizeof(msg),
			 "ACVPParser (%.2d:%.2d:%.2d) %s [%s:%s:%zu]: %s",
			 now_detail.tm_hour, now_detail.tm_min,
			 now_detail.tm_sec, sev, file, func, line, str);
		break;
	case LOGGER_VERBOSE:
	case LOGGER_WARN:
	case LOGGER_ERR:
	case LOGGER_STATUS:
	case LOGGER_NONE:
	case LOGGER_MAX_LEVEL:
	default:
		snprintf(msg, sizeof(msg), "ACVPParser (%.2d:%.2d:%.2d) %s: %s",
			 now_detail.tm_hour, now_detail.tm_min,
			 now_detail.tm_sec, sev, str);
		break;
	}


	bin2print(bin, binlen, stderr, msg);
}

void logger_set_verbosity(enum logger_verbosity level)
{
	logger_verbosity_level = level;
}

enum logger_verbosity logger_get_verbosity(void)
{
	return logger_verbosity_level;
}

void logger_inc_verbosity(void)
{
	if (logger_verbosity_level >= LOGGER_MAX_LEVEL - 1)
		return;

	logger_verbosity_level++;
}
