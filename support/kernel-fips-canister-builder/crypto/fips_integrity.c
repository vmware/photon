/*
 * FIPS Integrity check for Crypto API
 *
 * Copyright (C) 2020, 2021, VMware, Inc.
 * Authors: Alexey Makhalov <amakhalov@vmware.com>
 *          Keerthana Kalyanasundaram <keerthanak@vmware.com>
 */

#include <linux/crypto.h>
#include <linux/kallsyms.h>
#include <linux/err.h>
#include <linux/fips.h>
#include <linux/memblock.h>
#include <crypto/hash.h>
#include <asm/elf.h>
#include "fips_integrity.h"
#include "fips_canister_wrapper.h"

#ifndef FIPS_DEBUG
#define FIPS_DEBUG 0
#endif

#define FIPS_CANISTER_VERSION "LKCM 4.0.1"
#define FIPS_KERNEL_VERSION "5.10.4-4"

static unsigned char *canister;
/* Set at canister creation time by final linking */
extern const int canister_size;
/* Set at canister creation time by 'dd' injection after final linking */
extern const unsigned char canister_hmac[];

struct section_info {
	/* Original address (in the loaded kernel) of the section */
	unsigned long saddr;
	/*
	 * Destination address (in the canister image) of the section.
	 * This is the one which will be restored to its original state.
	 */
	char *daddr;
	unsigned long size;
};

static void * __init mem_alloc(size_t size)
{
	/* Can be called before mm_init(). */
	if (!slab_is_available())
		return memblock_alloc(size, 8);

	return fcw_kmalloc(size, GFP_KERNEL);
}

static void __init mem_free(void *p)
{
	if (p && slab_is_available() && PageSlab(virt_to_head_page(p)))
		kfree(p);
}

/*
 * First stage of FIPS integrity:
 *     To restore original canister image for measurement.
 * Must be invoked before any changes, except relocations, in measured sections.
 */
int __init fips_integrity_init(void)
{
	int i, err = 0;
	int sections_size = canister_sections_size;
	const char *ptr = canister_sections;
	unsigned char *c;
	unsigned long *symbols_addr = 0;
	unsigned int offset;
	int prev_section = -1;
	struct section_info *si = 0;
	char *d;
	int bytes_remaining;

	if (!fips_enabled &&
	    /* This function can be called before jump_label_init,
	     * so, kernel parameters are not parsed yet. */
	    !strstr(boot_command_line, "fips=1"))
		return 0;

	/* Canister image to measure */
	c = (unsigned char *)mem_alloc(canister_size);
	if (!c) {
		err = -ENOMEM;
		goto quit;
	}

	/* Description of section regions to put in the canister */
	si = (struct section_info *)mem_alloc(sizeof(struct section_info) * sections_size);
	if (!si) {
		err = -ENOMEM;
		goto quit;
	}

	printk(KERN_INFO "FIPS(%s): canister %s found (based on %s)\n", __FUNCTION__,
		FIPS_CANISTER_VERSION, FIPS_KERNEL_VERSION);
	printk(KERN_INFO "FIPS(%s): processing %d sections, %d bytes\n",
		__FUNCTION__, sections_size, canister_size);
	d = c;
	bytes_remaining = canister_size;
	for (i = 0; i < sections_size; i++) {
		unsigned long s, e, size;
		const char *begin_marker, *end_marker;
		begin_marker = ptr;
		ptr += strlen(ptr) + 1;
		end_marker = ptr;
		ptr += strlen(ptr) + 1;
		s = kallsyms_lookup_name(begin_marker);
		if (!s) {
			printk(KERN_ERR "FIPS(%s): unable to lookup: %s\n", __FUNCTION__, begin_marker);
			err = -ENOENT;
			goto quit;
		}
		e = kallsyms_lookup_name(end_marker);
		if (!e) {
			printk(KERN_ERR "FIPS(%s): unable to lookup: %s\n", __FUNCTION__, end_marker);
			err = -ENOENT;
			goto quit;
		}
		size = e - s;
#if FIPS_DEBUG
		printk("Processing %s: [%lx-%lx], size %ld\n", begin_marker, s, e, size);
#endif
		bytes_remaining -= size;
		if (bytes_remaining < 0)
			break;
		/* Copy content of relocated section to the canister */
		memcpy(d, (char *)s, size);

		si[i].saddr = s;
		si[i].daddr = d;
		si[i].size = size;
		d += size;
	}
	if (bytes_remaining) {
		printk(KERN_ERR "FIPS(%s): invalid canister size or markers\n", __FUNCTION__);
		err = -EINVAL;
		goto quit;
	}

	symbols_addr = (unsigned long *)mem_alloc(sizeof(unsigned long) * canister_strtab_size);
	if (!symbols_addr) {
		err = -ENOMEM;
		goto quit;
	}
	/* Look up strtab once. Convert canister_strtab[i] -> symbols_addr[i]. */
	ptr = canister_strtab;
	for (i = 0; i < canister_strtab_size; i++) {
		symbols_addr[i] = kallsyms_lookup_name(ptr);
		if (!symbols_addr[i]) {
			printk(KERN_ERR "FIPS(%s): unable to lookup: %s\n", __FUNCTION__, ptr);
			err = -ENOENT;
			goto quit;
		}
		ptr += strlen(ptr) + 1;
	}
#if FIPS_DEBUG
	printk("Processed %d symbols\n", canister_strtab_size);
#endif

	/*
	 * Main interpreter work: perform reverse relocation to resotre
	 * canister image to its original state.
	 */
	for (i = 0; i < canister_relocations_size; i++) {
		const struct relocation *r = &canister_relocations[i];
		unsigned long target, pc;
		char *mem;
		/* Relocation target */
		target = symbols_addr[r->symbol];
		target += (int64_t)r->addend;
		/*
		 * Every new section starts with absolute offset.
		 * All consecutive offsets within the section are relative.
		 */
		if (prev_section != r->section) {
			prev_section = r->section;
			offset = 0;
		}
		/* Relocation offset from the section start */
		offset += r->offset;
		/* Relocation actual addess */
		pc = si[r->section].saddr + offset;
		/* Where the reverse relocation will happen, inside canister image */
		mem = si[r->section].daddr + offset;
#if FIPS_DEBUG
		printk("section %d, rel %d, offset %x(%x), target %lx, pc %lx\n",
		       r->section, r->type, offset, r->offset, target, pc);
#endif
		/* Absolute unsigned 64bit relocation: value = target */
		if (r->type == 0 /* R_X86_64_64 */) {
			uint64_t value = *(uint64_t *)mem;
			value -= target;
			*(uint64_t *)mem = value;
#if FIPS_DEBUG
			if (value) {
				printk("%d failed for %d with value %llx\n", i, r->type, value);
				err = -ENOENT;
				goto quit;
			}
#endif
		/* Relative signed 32bit relocation: value = target - pc */
		} else if (r->type == 1 /* R_X86_64_PC32 */) {
			int32_t value = *(int32_t *)mem;
			value -= (long)target - pc;
			*(int32_t *)mem = value;
#if FIPS_DEBUG
			if (value) {
				printk("%d failed for %d with value %x\n", i, r->type, value);
				err = -ENOENT;
				goto quit;
			}
#endif
		/* Absolute signed 32bit relocation: value = target */
		} else if (r->type == 2 /* R_X86_64_32S */) {
			int32_t value = *(int32_t *)mem;
			value -= target;
			*(int32_t *)mem = value;
#if FIPS_DEBUG
			if (value) {
				printk("%d failed for %d with value %x\n", i, r->type, value);
				err = -ENOENT;
				goto quit;
			}
#endif
		} else {
			printk(KERN_ERR "FIPS(%s): unknown relocation type: %d\n", __FUNCTION__, r->type);
			err = -ENOENT;
			goto quit;
		}
	}
#if FIPS_DEBUG
	printk("Processed %d relocations\n", canister_relocations_size);
#endif
quit:
	mem_free(symbols_addr);
	mem_free(si);
	if (err) {
		mem_free(c);
		panic("FIPS(%s) canister initialization failed.", __FUNCTION__);
	} else {
		/* It is save to set 'canister' pointer now. */
		canister = c;
	}

	return err;
}

/*
 * Second stage of FIPS integrity:
 *     To perform canister image measurement and compare with golden value.
 * Can be invoked at any time after crypto algorithms initialization and
 * self-tests completed.
 */
static int __init fips_integrity_check (void)
{
	int err;
	unsigned char runtime_hmac[32];
	struct crypto_shash *tfm = NULL;
	struct shash_desc *shash;
	/* HMAC key. Same key as we used at canister build time. */
	const unsigned char *key = "FIPS-PH4-VMW2020";

	if (!fips_enabled)
		return 0;

	if (!canister) {
		printk (KERN_ERR "FIPS(%s): canister image not found\n", __FUNCTION__);
		return -EINVAL;
	}

	tfm = crypto_alloc_shash ("hmac(sha256)", 0, 0);
	if (IS_ERR(tfm)) {
		printk(KERN_ERR "FIPS(%s): crypto_alloc_shash failed (%d)\n", __FUNCTION__, (int)PTR_ERR(tfm));
		return PTR_ERR(tfm);
	}

	err = crypto_shash_setkey (tfm, key, strlen(key));
	if (err) {
		printk(KERN_ERR "FIPS(%s): crypto_hash_setkey failed (%d)\n", __FUNCTION__, err);
		goto free_tfm;
	}

	shash = fcw_kzalloc(sizeof(*shash) + crypto_shash_descsize(tfm),
			GFP_KERNEL);
	if (!shash) {
		err = -ENOMEM;
		goto free_tfm;
	}

	shash->tfm = tfm;
	err = crypto_shash_digest(shash, canister, canister_size, runtime_hmac);
	if (err)
		printk(KERN_ERR "FIPS(%s): crypto_shash_digest failed (%d)\n", __FUNCTION__, err);

	kfree(shash);
free_tfm:
	crypto_free_shash (tfm);
	mem_free(canister);
#if FIPS_DEBUG
	printk("canister: %lx %d\n", (unsigned long)canister, canister_size);
#endif
	if (err)
		return err;

	{
		int i;
		unsigned char linebuf[32 * 2 + 1];
		for (i = 0; i < 32; i++)
			snprintf(&linebuf[i * 2], 3, "%02x", runtime_hmac[i]);
		linebuf[sizeof(linebuf)] = 0;
		printk("FIPS canister HMAC: %s\n", linebuf);
	}

	err = memcmp (canister_hmac, runtime_hmac, sizeof(runtime_hmac)) ? -EACCES: 0;
	if (!err)
		printk("FIPS canister verification passed!");
	else
		panic("FIPS canister verification failed!");
	return err;
}
module_init(fips_integrity_check);
