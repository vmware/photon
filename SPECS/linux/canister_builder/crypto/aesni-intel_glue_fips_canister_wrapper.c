/*
 * Kernel APIs wrapper for the aesni_intel_glue.c
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */
#include <crypto/scatterwalk.h>
#include <linux/scatterlist.h>

struct scatterlist *fcw_scatterwalk_ffwd(struct scatterlist dst[2],
				     struct scatterlist *src,
				     unsigned int len)
{
	return scatterwalk_ffwd(dst, src, len);
}

void fcw_scatterwalk_unmap(void *vaddr)
{
	return scatterwalk_unmap(vaddr);
}

