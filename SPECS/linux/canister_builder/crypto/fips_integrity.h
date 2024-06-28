/*
 * FIPS Integrity check for Crypto API
 *
 * Copyright (C) 2020 - 2022 VMware, Inc.
 * Author: Alexey Makhalov <amakhalov@vmware.com>
 *
 */

/*
 * Bits can be moved around to satisfy current core canister.
 * TYPE_BITS can easily be 2 and 1 released bit can be added
 * to one of the other twos.
 */
#include <linux/types.h>

struct __attribute__((packed)) relocation {
	unsigned char section;
	unsigned char type;
	unsigned short symbol;
	unsigned int offset;
	int addend;
	bool insn_read_complete;
};

/* Generated data. */
extern const char canister_sections[];
extern const int canister_sections_size;
extern const char canister_strtab[];
extern const int canister_strtab_size;
extern const unsigned char canister_relocations_bytecode[];
extern const unsigned int canister_relocations_bytecode_size;

