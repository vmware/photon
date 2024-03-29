/*
 * Kernel APIs wrapper for the testmgr.c
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */
#include <linux/scatterlist.h>
#include <linux/uio.h>
#include "fips_canister_wrapper_internal.h"

extern void fcw_sg_set_buf(struct scatterlist *sg, const void *buf, unsigned int buflen);
extern int fcw_warn_on(int cond);
extern size_t fcw_copy_from_iter(void *addr, size_t bytes, struct iov_iter *i);
extern void *fcw_memcpy(void *dst, const void *src, size_t len);

void *fcw_sg_page_address(struct scatterlist *sg)
{
	struct page *page = sg_page(sg);
	return page_address(page);
}

static unsigned int count_test_sg_divisions(const struct test_sg_division *divs)
{
	unsigned int remaining = TEST_SG_TOTAL;
	unsigned int ndivs = 0;

	do {
		remaining -= divs[ndivs++].proportion_of_total;
	} while (remaining);

	return ndivs;
}

static void testmgr_poison(void *addr, size_t len)
{
	memset(addr, TESTMGR_POISON_BYTE, len);
}

/**
 * build_test_sglist() - build a scatterlist for a crypto test
 *
 * @tsgl: the scatterlist to build.  @tsgl->bufs[] contains an array of 2-page
 *       buffers which the scatterlist @tsgl->sgl[] will be made to point into.
 * @divs: the layout specification on which the scatterlist will be based
 * @alignmask: the algorithm's alignmask
 * @total_len: the total length of the scatterlist to build in bytes
 * @data: if non-NULL, the buffers will be filled with this data until it ends.
 *       Otherwise the buffers will be poisoned.  In both cases, some bytes
 *       past the end of each buffer will be poisoned to help detect overruns.
 * @out_divs: if non-NULL, the test_sg_division to which each scatterlist entry
 *           corresponds will be returned here.  This will match @divs except
 *           that divisions resolving to a length of 0 are omitted as they are
 *           not included in the scatterlist.
 *
 * Return: 0 or a -errno value
 */
static int build_test_sglist(struct test_sglist *tsgl,
			     const struct test_sg_division *divs,
			     const unsigned int alignmask,
			     const unsigned int total_len,
			     struct iov_iter *data,
			     const struct test_sg_division *out_divs[XBUFSIZE])
{
	struct {
		const struct test_sg_division *div;
		size_t length;
	} partitions[XBUFSIZE];
	const unsigned int ndivs = count_test_sg_divisions(divs);
	unsigned int len_remaining = total_len;
	unsigned int i;

	BUILD_BUG_ON(ARRAY_SIZE(partitions) != ARRAY_SIZE(tsgl->sgl));
	if (fcw_warn_on(ndivs > ARRAY_SIZE(partitions)))
		return -EINVAL;

	/* Calculate the (div, length) pairs */
	tsgl->nents = 0;
	for (i = 0; i < ndivs; i++) {
		unsigned int len_this_sg =
			     min(len_remaining,
			     (total_len * divs[i].proportion_of_total +
			     TEST_SG_TOTAL / 2) / TEST_SG_TOTAL);

		if (len_this_sg != 0) {
			partitions[tsgl->nents].div = &divs[i];
			partitions[tsgl->nents].length = len_this_sg;
			tsgl->nents++;
			len_remaining -= len_this_sg;
		}
	}
	if (tsgl->nents == 0) {
		partitions[tsgl->nents].div = &divs[0];
		partitions[tsgl->nents].length = 0;
		tsgl->nents++;
	}
	partitions[tsgl->nents - 1].length += len_remaining;

	/* Set up the sgl entries and fill the data or poison */
	sg_init_table(tsgl->sgl, tsgl->nents);
	for (i = 0; i < tsgl->nents; i++) {
		unsigned int offset = partitions[i].div->offset;
		void *addr;
		if (partitions[i].div->offset_relative_to_alignmask)
			offset += alignmask;
		while (offset + partitions[i].length + TESTMGR_POISON_LEN > 2 * PAGE_SIZE) {
			if (fcw_warn_on(offset <= 0))
				return -EINVAL;
			offset /= 2;
		}

		addr = &tsgl->bufs[i][offset];
		fcw_sg_set_buf(&tsgl->sgl[i], addr, partitions[i].length);
		if (out_divs)
			out_divs[i] = partitions[i].div;

		if (data) {
			size_t copy_len, copied;

			copy_len = min(partitions[i].length, data->count);
			copied = fcw_copy_from_iter(addr, copy_len, data);
			if (fcw_warn_on(copied != copy_len))
				return -EINVAL;
			testmgr_poison(addr + copy_len, partitions[i].length +
				       TESTMGR_POISON_LEN - copy_len);
		} else {
			testmgr_poison(addr, partitions[i].length +
				       TESTMGR_POISON_LEN);
		}
	}

	sg_mark_end(&tsgl->sgl[tsgl->nents - 1]);
	tsgl->sgl_ptr = tsgl->sgl;
	fcw_memcpy(tsgl->sgl_saved, tsgl->sgl, tsgl->nents * sizeof(tsgl->sgl[0]));
	return 0;
}

int fcw_build_hash_sglist(struct test_sglist *tsgl,
			     const struct hash_testvec *vec,
			     const struct testvec_config *cfg,
			     unsigned int alignmask,
			     const struct test_sg_division *divs[XBUFSIZE])
{
	struct kvec kv;
	struct iov_iter input;

	kv.iov_base = (void *)vec->plaintext;
	kv.iov_len = vec->psize;
	iov_iter_kvec(&input, WRITE, &kv, 1, vec->psize);
	return build_test_sglist(tsgl, cfg->src_divs, alignmask, vec->psize,
				 &input, divs);
}

/* Build the src and dst scatterlists for an skcipher or AEAD test */
int fcw_build_cipher_test_sglists(struct cipher_test_sglists *tsgls,
				  const struct testvec_config *cfg,
				  unsigned int alignmask,
				  unsigned int src_total_len,
				  unsigned int dst_total_len,
				  const struct kvec *inputs,
				  unsigned int nr_inputs)
{
	struct iov_iter input;
	int err;

	iov_iter_kvec(&input, WRITE, inputs, nr_inputs, src_total_len);
	err = build_test_sglist(&tsgls->src, cfg->src_divs, alignmask,
				cfg->inplace_mode != OUT_OF_PLACE ?
					max(dst_total_len, src_total_len) :
					src_total_len,
				&input, NULL);
	if (err)
		return err;

	/*
	 * In-place crypto operations can use the same scatterlist for both the
	 * source and destination (req->src == req->dst), or can use separate
	 * scatterlists (req->src != req->dst) which point to the same
	 * underlying memory.  Make sure to test both cases.
	 */
	if (cfg->inplace_mode == INPLACE_ONE_SGLIST) {
		tsgls->dst.sgl_ptr = tsgls->src.sgl;
		tsgls->dst.nents = tsgls->src.nents;
		return 0;
	}
	if (cfg->inplace_mode == INPLACE_TWO_SGLISTS) {
		/*
		 * For now we keep it simple and only test the case where the
		 * two scatterlists have identical entries, rather than
		 * different entries that split up the same memory differently.
		 */
		fcw_memcpy(tsgls->dst.sgl, tsgls->src.sgl,
		       tsgls->src.nents * sizeof(tsgls->src.sgl[0]));
		fcw_memcpy(tsgls->dst.sgl_saved, tsgls->src.sgl,
		       tsgls->src.nents * sizeof(tsgls->src.sgl[0]));
		tsgls->dst.sgl_ptr = tsgls->dst.sgl;
		tsgls->dst.nents = tsgls->src.nents;
		return 0;
	}
	/* Out of place */
	return build_test_sglist(&tsgls->dst,
				 cfg->dst_divs[0].proportion_of_total ?
					cfg->dst_divs : cfg->src_divs,
				 alignmask, dst_total_len, NULL, NULL);
}
