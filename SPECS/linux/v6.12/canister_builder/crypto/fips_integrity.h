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

#define SREL_INSN_TYPE_ADD_1				0x0		/* "0000" = Rel type 1, Addend -4 */
#define SREL_INSN_TYPE_ADD_2				0x1		/* "0001" = Rel type 1, Addend -5 */
#define SREL_INSN_TYPE_ADD_3				0x2		/* "0010" = Rel type 1, Addend 0 */
#define SREL_INSN_TYPE_ADD_4				0x3		/* "0011" = Rel type 2, Addend 0 */
#define SREL_INSN_TYPE_ADD_5				0x6		/* "0110" = Rel type 1, Addend 4 */
#define SREL_INSN_TYPE_ADD_6				0x5		/* "0101" = Rel type 0, Addend 5 */
#define SREL_INSN_TYPE_ADD_7				0x7		/* "0111" = Rel type 3, Addend 0 */

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

