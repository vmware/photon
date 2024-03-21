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

#ifndef TERM_COLORS_H
#define TERM_COLORS_H

#include <stdarg.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef NO_COLORS
#define TERM_COLOR_NORMAL   ""
#define TERM_COLOR_RED      ""
#define TERM_COLOR_GREEN    ""
#define TERM_COLOR_YELLOW   ""
#define TERM_COLOR_BLUE     ""
#define TERM_COLOR_MAGENTA  ""
#define TERM_COLOR_CYAN     ""
#define TERM_COLOR_WHITE    ""
#else
#define TERM_COLOR_NORMAL	"\x1B[0m"
#define TERM_COLOR_RED		"\x1B[31m"
#define TERM_COLOR_GREEN	"\x1B[32m"
#define TERM_COLOR_YELLOW	"\x1B[33m"
#define TERM_COLOR_BLUE		"\x1B[34m"
#define TERM_COLOR_MAGENTA	"\x1B[35m"
#define TERM_COLOR_CYAN		"\x1B[36m"
#define TERM_COLOR_WHITE	"\x1B[37m"
#endif

#define TERM_COLOR_PRINT(color_name, color)				\
	static inline int fprintf_##color_name(FILE *stream,		\
					       const char *format, ...)	\
	{								\
		va_list args;						\
		int ret;						\
									\
		fprintf(stream, "%s", color);				\
		va_start(args, format);					\
		ret = vfprintf(stream, format, args);			\
		va_end(args);						\
		fprintf(stream, "%s", TERM_COLOR_NORMAL);		\
									\
		return ret;						\
}

/*
 * Create functions fprintf_red, fprintf_green, etc.
 * The are API and functional identical to fprintf(3) except that the
 * string is printed with the respective color.
 */
TERM_COLOR_PRINT(red, TERM_COLOR_RED)
TERM_COLOR_PRINT(green, TERM_COLOR_GREEN)
TERM_COLOR_PRINT(yellow, TERM_COLOR_YELLOW)
TERM_COLOR_PRINT(blue, TERM_COLOR_BLUE)
TERM_COLOR_PRINT(magenta, TERM_COLOR_MAGENTA)
TERM_COLOR_PRINT(cyan, TERM_COLOR_CYAN)
TERM_COLOR_PRINT(white, TERM_COLOR_WHITE)

#ifdef __cplusplus
}
#endif

#endif /* TERM_COLORS_H */
