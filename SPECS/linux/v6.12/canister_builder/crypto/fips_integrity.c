/*
 * FIPS Integrity check for Crypto API
 *
 * Copyright (C) 2020 - 2022 VMware, Inc.
 * Authors: Alexey Makhalov <amakhalov@vmware.com>
 *          Keerthana Kalyanasundaram <keerthanak@vmware.com>
 */

#include <linux/crypto.h>
#include <linux/kallsyms.h>
#include <linux/err.h>
#include <linux/fips.h>
#include <crypto/hash.h>
#include <asm/elf.h>
#include "fips_integrity.h"
#include "fips_canister_wrapper.h"

#ifndef FIPS_DEBUG
#define FIPS_DEBUG 0
#endif

#define FIPS_CANISTER_VERSION "6.0.0"
#define FIPS_KERNEL_VERSION "6.12.1-1.ph5"

#define RUNTIME_HMAC_SIZE	32

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

static int canister_perform_reverse_relocation(int i, struct relocation *r, char *mem, unsigned long target, unsigned long pc)
{
	int err = 0;

	/* Absolute unsigned 64bit relocation: value = target */
	if (r->type == 0 /* R_X86_64_64 */) {
		uint64_t value = *(uint64_t *)mem;
		value -= target;
		*(uint64_t *)mem = value;
#if FIPS_DEBUG
		if (value) {
			fcw_printk("%d failed for %d with value %llx\n", i, r->type, value);
			err = -ENOENT;
			return err;
		}
#endif
	/* Relative signed 32bit relocation: value = target - pc */
	} else if (r->type == 1 /* R_X86_64_PC32 */) {
		int32_t value = *(int32_t *)mem;
		value -= (long)target - pc;
		*(int32_t *)mem = value;
#if FIPS_DEBUG
		if (value) {
			fcw_printk("%d failed for %d with value %x\n", i, r->type, value);
			err = -ENOENT;
			return err;
		}
#endif
	/* Absolute signed 32bit relocation: value = target */
	} else if (r->type == 2  || r->type == 3 /* R_X86_64_32S || R_X86_64_32 */) {
		int32_t value = *(int32_t *)mem;
		value -= target;
		*(int32_t *)mem = value;
#if FIPS_DEBUG
		if (value) {
			fcw_printk("%d failed for %d with value %x\n", i, r->type, value);
			err = -ENOENT;
			return err;
		}
#endif
	} else {
		fcw_printk(KERN_ERR "FIPS(%s): unknown relocation type: %d\n", __FUNCTION__, r->type);
		err = -ENOENT;
		return err;
	}

	return err;
}

static int canister_bytecode_interpreter(struct relocation *r, int *pos)
{
	int err = 0;
	unsigned char c = 0, n_1 = 0, n_2 = 0, n_3 = 0;
	unsigned char rel_add = 0;

	if (!r) {
		fcw_printk(KERN_ERR "FIPS(%s): Relocation is NULL\n", __FUNCTION__);
		return -ENOENT;
	}
	c = canister_relocations_bytecode[*pos];

	if ((c & 0xC0) == 0x0) { /* JMP */
		/* Jmp Offset (6 bits) = 3, 4, 5, 6, 7, 8 bits of first byte */
		r->offset += (c & 0x3F);
		r->insn_read_complete = false;

	} else if ((c & 0xC0) == 0x40) { /* LJMP */
		(*pos)++;
		n_1 = canister_relocations_bytecode[*pos];
		/* Long Jmp Offset (14 bits) = 3, 4, 5, 6, 7, 8 bits of first byte + next byte */
		r->offset += (((c & 0x3F) << 8) + n_1);
		r->insn_read_complete = false;

	} else if ((c & 0xE0) == 0x80) { /* LRPR */
		(*pos)++;
		n_1 = canister_relocations_bytecode[*pos];
		/* LRPR signed addend (1 sign bit + 12 bits) = 4th bit + 5, 6, 7, 8 bits of first byte + next byte */
		if ((c & 0x10) >> 4 == 0) { /* Sign bit is 0 */
			r->addend += (((c & 0xF) << 8) + n_1);
		} else { /* Sign bit is 1 */
			/* Addend value of 1000000000000 = -4096 */
			if ((((c & 0xF) << 8) + n_1) == 0x0)
				r->addend += (-4096);
			else
				r->addend += (-(((c & 0xF) << 8) + n_1));
		}
		r->insn_read_complete = true;

	} else if ((c & 0xE0) == 0xA0) { /* SRPR */
		/* SRPR signed addend (1 sign bit + 4 bits) = 4th bit + 5, 6, 7, 8 bits of first byte */
		if ((c & 0x10) >> 4 == 0) /* Sign bit is 0 */
			r->addend += (c & 0xF);
		else { /*Sign bit is 1 */
			/* Addend value of 10000 = -16 */
			if ((c & 0xF) == 0x0)
				r->addend += (-16);
			else
				r->addend += (-(c & 0xF));
		}
		r->insn_read_complete = true;

	} else if ((c & 0xE0) == 0xE0) { /* LREL */
		(*pos)++;
		n_1 = canister_relocations_bytecode[*pos];
		(*pos)++;
		n_2 = canister_relocations_bytecode[*pos];
		(*pos)++;
		n_3 = canister_relocations_bytecode[*pos];
		/* Rel Type (2 bits) = 4th and 5th bit from first byte */
		r->type = (c & 0x18) >> 3;
		/* Symbol (8 bits) = 6, 7, 8th bit from first byte + first 5 bits from next byte*/
		r->symbol = ((c & 0x7) << 5) + ((n_1 & 0xF8) >> 3);
		/* Addend (19 bits) = 6, 7, 8th bit from n_1 + n2 + n3 */
		r->addend = ((n_1 & 0x7) << 16) + (n_2 << 8) + n_3;
		r->insn_read_complete = true;

	} else if ((c & 0xF0) == 0xC0) { /* SREL */
		(*pos)++;
		n_1 = canister_relocations_bytecode[*pos];
		/* Symbol (8 bits) = 4 bits from first byte + 4 bits from next byte */
		r->symbol = ((c & 0x0F) << 4) + (n_1 >> 4);
		/* Rel Type, Addend combination (4 bits) = 5, 6, 7, 8 bits from next byte */
		rel_add = n_1 & 0x0F;
		if (rel_add == SREL_INSN_TYPE_ADD_1) {
			r->type = 1;
			r->addend = -4;
		} else if (rel_add == SREL_INSN_TYPE_ADD_2) {
			r->type = 1;
			r->addend = -5;
		} else if (rel_add == SREL_INSN_TYPE_ADD_3) {
			r->type = 1;
			r->addend = 0;
		} else if (rel_add == SREL_INSN_TYPE_ADD_4) {
			r->type = 2;
			r->addend = 0;
		} else if (rel_add == SREL_INSN_TYPE_ADD_5) {
			r->type = 1;
			r->addend = 4;
		} else if (rel_add == SREL_INSN_TYPE_ADD_6) {
			r->type = 0;
			r->addend = 5;
		} else if (rel_add == SREL_INSN_TYPE_ADD_7) {
			r->type = 3;
			r->addend = 0;
		} else {
			err = -ENOENT;
			return err;
		}
		r->insn_read_complete = true;

	} else if ((c & 0xF0) == 0xD0) { /* SEC */
		/* Section increment (4 bits) = 5, 6, 7, 8 bits of first byte */
		r->section += (c & 0x0F);
		r->insn_read_complete = false;

	} else {
		fcw_printk(KERN_ERR "FIPS(%s): Unknown Instruction\n", __FUNCTION__);
		err = -ENOENT;
		return err;
	}
	return err;
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
	struct relocation *r = NULL;
	int canister_relocations_size;

	if (!fips_enabled &&
	    /* This function can be called before jump_label_init,
	     * so, kernel parameters are not parsed yet. */
	    !strstr(boot_command_line, "fips=1"))
		return 0;

	/* Canister image to measure */
	c = (unsigned char *)fcw_mem_alloc(canister_size);
	if (!c) {
		err = -ENOMEM;
		goto quit;
	}

	/* Description of section regions to put in the canister */
	si = (struct section_info *)fcw_mem_alloc(sizeof(struct section_info) * sections_size);
	if (!si) {
		err = -ENOMEM;
		goto quit;
	}

	fcw_printk(KERN_INFO "FIPS(%s): canister %s found (based on %s)\n", __FUNCTION__,
		FIPS_CANISTER_VERSION, FIPS_KERNEL_VERSION);
	fcw_printk(KERN_INFO "FIPS(%s): processing %d sections, %d bytes\n",
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
			fcw_printk(KERN_ERR "FIPS(%s): unable to lookup: %s\n", __FUNCTION__, begin_marker);
			err = -ENOENT;
			goto quit;
		}
		e = kallsyms_lookup_name(end_marker);
		if (!e) {
			fcw_printk(KERN_ERR "FIPS(%s): unable to lookup: %s\n", __FUNCTION__, end_marker);
			err = -ENOENT;
			goto quit;
		}
		size = e - s;
#if FIPS_DEBUG
		fcw_printk("Processing %s: [%lx-%lx], size %ld\n", begin_marker, s, e, size);
#endif
		bytes_remaining -= size;
		if (bytes_remaining < 0)
			break;
		/* Copy content of relocated section to the canister */
		fcw_memcpy(d, (char *)s, size);

		si[i].saddr = s;
		si[i].daddr = d;
		si[i].size = size;
		d += size;
	}
	if (bytes_remaining) {
		fcw_printk(KERN_ERR "FIPS(%s): invalid canister size or markers\n", __FUNCTION__);
		err = -EINVAL;
		goto quit;
	}

	symbols_addr = (unsigned long *)fcw_mem_alloc(sizeof(unsigned long) * canister_strtab_size);
	if (!symbols_addr) {
		err = -ENOMEM;
		goto quit;
	}
	/* Look up strtab once. Convert canister_strtab[i] -> symbols_addr[i]. */
	ptr = canister_strtab;
	for (i = 0; i < canister_strtab_size; i++) {
		symbols_addr[i] = kallsyms_lookup_name(ptr);
		if (!symbols_addr[i] && !strncmp(ptr, "__kcfi_typeid_", 14)) {
			const char *name = ptr + strlen("__kcfi_typeid_");
			unsigned long addr = kallsyms_lookup_name(name);
			if (addr) {
				//kcfi hash will be present at addr(func-16) bytes
				addr -= 0xF;
				int *addrp = (int *)addr;
				symbols_addr[i] = *addrp;
			}
		}
		if (!symbols_addr[i]) {
			fcw_printk(KERN_ERR "FIPS(%s): unable to lookup: %s\n", __FUNCTION__, ptr);
			err = -ENOENT;
			goto quit;
		}
		ptr += strlen(ptr) + 1;
	}
#if FIPS_DEBUG
	fcw_printk("Processed %d symbols\n", canister_strtab_size);
#endif

	/*
	 * Main interpreter work: perform reverse relocation to resotre
	 * canister image to its original state.
	 */
	r = (struct relocation *)fcw_mem_alloc(sizeof(struct relocation));
	memset(r, 0, sizeof(struct relocation));
	for (i = 0; i < canister_relocations_bytecode_size; i++) {
		char *mem;
		unsigned long target, pc;

		err = canister_bytecode_interpreter(r, &i);
		if (err)
			goto quit;

		if (!(r->insn_read_complete))
			continue;
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
		fcw_printk("section %d, rel %d, symbol %d, offset %x(%x), addend %d, target %lx, pc %lx\n",
		       r->section, r->type, r->symbol, offset, r->offset, r->addend, target, pc);
#endif
		err = canister_perform_reverse_relocation(i, r, mem, target, pc);
		if (err)
			goto quit;
		r->offset = 0;
		canister_relocations_size++;
	}
#if FIPS_DEBUG
	fcw_printk("Processed %d relocations\n", canister_relocations_size);
#endif
quit:
	fcw_mem_free(symbols_addr);
	fcw_mem_free(si);
	fcw_mem_free(r);
	if (err) {
		fcw_mem_free(c);
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
int __init fips_integrity_check (void)
{
	int err;
	unsigned char runtime_hmac[RUNTIME_HMAC_SIZE];
	struct crypto_shash *tfm = NULL;
	struct shash_desc *shash;
	/* HMAC key. Same key as we used at canister build time. */
	const unsigned char *key = "FIPS-PH4-VMW2020";

	if (!fips_enabled)
		return 0;

	if (!canister) {
		fcw_printk (KERN_ERR "FIPS(%s): canister image not found\n", __FUNCTION__);
		return -EINVAL;
	}

	tfm = crypto_alloc_shash ("hmac(sha256)", 0, 0);
	if (IS_ERR(tfm)) {
		fcw_printk(KERN_ERR "FIPS(%s): crypto_alloc_shash failed (%d)\n", __FUNCTION__, (int)PTR_ERR(tfm));
		return PTR_ERR(tfm);
	}

	err = crypto_shash_setkey (tfm, key, strlen(key));
	if (err) {
		fcw_printk(KERN_ERR "FIPS(%s): crypto_hash_setkey failed (%d)\n", __FUNCTION__, err);
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
		fcw_printk(KERN_ERR "FIPS(%s): crypto_shash_digest failed (%d)\n", __FUNCTION__, err);

	kfree(shash);
free_tfm:
	crypto_free_shash (tfm);
	fcw_mem_free(canister);
#if FIPS_DEBUG
	fcw_printk("canister: %lx %d\n", (unsigned long)canister, canister_size);
#endif
	if (err)
		return err;

	{
		int i;
		unsigned char linebuf[(RUNTIME_HMAC_SIZE * 2) + 1];

		for (i = 0; i < RUNTIME_HMAC_SIZE; i++)
			snprintf(&linebuf[i * 2], 3, "%02x", runtime_hmac[i]);

		linebuf[sizeof(linebuf) - 1] = '\0';

		fcw_printk("FIPS canister HMAC: %s\n", linebuf);
		memzero_explicit(linebuf, sizeof(linebuf));
	}

	err = memcmp (canister_hmac, runtime_hmac, sizeof(runtime_hmac)) ? -EACCES: 0;
	memzero_explicit(runtime_hmac, sizeof(runtime_hmac));
	if (!err)
		fcw_printk("FIPS canister verification passed!");
	else
		panic("FIPS canister verification failed!");
	return err;
}
