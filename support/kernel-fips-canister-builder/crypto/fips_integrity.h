/*
 * FIPS Integrity check for Crypto API
 *
 * Copyright (C) 2020, 2021, VMware, Inc.
 * Author: Alexey Makhalov <amakhalov@vmware.com>
 *
 */

/*
 * Bits can be moved around to satisfy current core canister.
 * TYPE_BITS can easily be 2 and 1 released bit can be added
 * to one of the other twos.
 */
#define SECTION_BITS 5
#define TYPE_BITS 3
#define SYMBOL_BITS 8
#if SECTION_BITS + TYPE_BITS + SYMBOL_BITS != 16
#error Please fix `struct relocation` layout
#endif

/* Keep it packed 8 bytes to consume less kernel memory. */
struct __attribute__((packed)) relocation {
	unsigned char section : SECTION_BITS;
	unsigned char type : TYPE_BITS;
	unsigned short symbol : SYMBOL_BITS;
	unsigned short offset;
	int addend;
};

/* Generated data. */
extern const char canister_sections[];
extern const int canister_sections_size;
extern const char canister_strtab[];
extern const int canister_strtab_size;
extern const struct relocation canister_relocations[];
extern const int canister_relocations_size;

