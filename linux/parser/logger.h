/*
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

#ifndef LOGGER_H
#define LOGGER_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C"
{
#endif

enum logger_verbosity {
	LOGGER_NONE,
	LOGGER_STATUS,
	LOGGER_ERR,
	LOGGER_WARN,
	LOGGER_VERBOSE,
	LOGGER_DEBUG,
	LOGGER_DEBUG2,

	LOGGER_MAX_LEVEL	/* This must be last entry */
};


/* Helper that is not intended to be called directly */
void _logger(const enum logger_verbosity severity,
	     const char *file, const char *func,
	     const size_t line, const char *fmt, ...)
	__attribute__((format(printf, 5, 6)));
void _logger_binary(const enum logger_verbosity severity,
		    const unsigned char *bin, const size_t binlen,
		    const char *str, const char *file,
		    const char *func, const size_t line);

/**
 * logger - log string with given severity
 * @severity: maximum severity level that causes the log entry to be logged
 * @fmt: format string as defined by fprintf(3)
 */
#define logger(severity, fmt...)                                 	       \
	do {                                                                   \
		_Pragma("GCC diagnostic push")                                 \
		_Pragma("GCC diagnostic ignored \"-Wpedantic\"") 	       \
		_logger(severity, __FILE__, __FUNCTION__, __LINE__, ##fmt);    \
		_Pragma("GCC diagnostic pop")                                  \
	} while (0);

/**
 * logger - log status if LOGGER_WARN or LOGGER_ERR is found
 * @fmt: format string as defined by fprintf(3)
 */
#define logger_status(fmt...) logger(LOGGER_STATUS, ##fmt)

/**
 * logger_binary - log binary string as hex
 * @severity: maximum severity level that causes the log entry to be logged
 * @bin: binary string
 * @binlen: length of binary string
 * @str: string that is prepended to hex-converted binary string
 */
#define logger_binary(severity, bin, binlen, str) 			       \
	do {                                                                   \
		_Pragma("GCC diagnostic push")                                 \
		_Pragma("GCC diagnostic ignored \"-Wpedantic\"")	       \
		_logger_binary(severity, bin, binlen,			       \
			       str, __FILE__, __FUNCTION__, __LINE__);	       \
		_Pragma("GCC diagnostic pop")				       \
	} while (0);

/**
 * logger_set_verbosity - set verbosity level
 */
void logger_set_verbosity(enum logger_verbosity level);

/**
 * logger_get_verbosity - get verbosity level
 */
enum logger_verbosity logger_get_verbosity(void);

/**
 * logger_inc_verbosity - increase verbosity level by one
 */
void logger_inc_verbosity(void);

#ifdef __cplusplus
}
#endif

#endif /* LOGGER_H */
