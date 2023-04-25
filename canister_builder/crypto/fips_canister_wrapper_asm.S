########################################################################
# Implement asm wrapper for FIPS canister. (x86_64)
#
# Copyright (C) 2023 VMware, Inc.

#include <linux/linkage.h>
#include <linux/version.h>
#include <asm/export.h>

#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
SYM_FUNC_START(_printk)
	jmp printk
SYM_FUNC_END(_printk)
EXPORT_SYMBOL(_printk)
#endif
