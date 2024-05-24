/*
 * Kernel assembly wrapper for jitterentropy v3.4.1
 *
 * Copyright (C) 2023 VMware, Inc.
 * Authors: Keerthana K <keerthanak@vmware.com>
 *
 */

#include <linux/linkage.h>
#include <linux/version.h>
#include <asm/export.h>

SYM_FUNC_START(jcw_printk)
#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
	jmp printk
#else
        jmp _printk
#endif
SYM_FUNC_END(jcw_printk)
