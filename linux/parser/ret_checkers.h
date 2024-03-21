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

#ifndef RET_CHECKERS_H
#define RET_CHECKERS_H

#ifdef __cplusplus
extern "C"
{
#endif

#define CKINT(x) {							\
	ret = x;							\
	if (ret < 0) {							\
		logger(LOGGER_DEBUG,					\
		       "Failure with return code %d\n", ret);		\
		goto out;						\
	}								\
}

#define CKINT_LOG(x, ...) {						\
	ret = x;							\
	if (ret < 0) {							\
		logger(LOGGER_ERR,  __VA_ARGS__);			\
		goto out;						\
	}								\
}

#define CKNULL(v, r) {							\
	if (!v) {							\
		ret = r;						\
		logger(LOGGER_DEBUG,					\
		       "Failure with return code %d\n", ret);		\
		goto out;						\
	}								\
}

#define CKNULL_LOG(v, r, ...) {						\
	if (!v) {							\
		logger(LOGGER_ERR, __VA_ARGS__);			\
		ret = r;						\
		goto out;						\
	}								\
}

#ifdef __cplusplus
}
#endif

#endif /* RET_CHECKERS_H */
