/*
 * Kernel assembly wrapper for canister
 *
 * Copyright (C) 2023 VMware, Inc.
 * Authors: Keerthana K <keerthanak@vmware.com>
 *	    Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com>
 *
 */

#include <linux/linkage.h>
#include <linux/version.h>
#include <asm/export.h>

SYM_FUNC_START(fcw_printk)
#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
	jmp printk
#else
        jmp _printk
#endif
SYM_FUNC_END(fcw_printk)

SYM_FUNC_START(fcw_warn_printk)
	jmp __warn_printk
SYM_FUNC_END(fcw_warn_printk)
