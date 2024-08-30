/*
 * FIPS Integrity canister relocations generator.
 *
 * Copyright (C) 2020 - 2022 VMware, Inc.
 * Authors: Alexey Makhalov <amakhalov@vmware.com>
 *          Keerthana Kalyanasundaram <keerthanak@vmware.com>
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <libelf.h>
#include <gelf.h>
#include <string.h>
#include <stdarg.h>
#include "fips_integrity.h"

#define MARK_PREFIX_BEGIN "__canister_s"
#define MARK_PREFIX_E_POSITION 11

#define INT_MAX		((int)(~0U>>1))
#define INT_MIN		(-INT_MAX - 1)
#define UINT_MAX        (~0U)

/*
* Canister bytecode instruction set
*
* LJMP - Long Jump
* SRPR - Short RPR (Repeat Previous Relocation. Use same reloc type, section and symbol as previous instruction)
* LRPR - Long RPR (Repeat Previous Relocation. Use same reloc type, section and symbol as previous instruction)
* SREL - Short Relocation
* LREL - Long Relocation
*
*-------------------------------------------------------------------------------------------------------------------------------*
| Name	|Bytes	|	Opcode		|	Param bits	|	Param			|	Notes	   		|
|_______|_______|_______________________|_______________________|_______________________________|_______________________________|
|SECTION|   1	|     1101 {N:4}	|	4		| 4 bits of section increment	|   Section increment from prev	|
|-------|-------------------------------|-----------------------|-------------------------------|-------------------------------|
| JMP	|   1	|     00   {P:6}   	|	6		| 6 bits of unsigned offset	|   Offset range [0;63]		|
|-------|-------------------------------|-----------------------|-------------------------------|-------------------------------|
| LJMP	|   2	|     01   {P:14}	|	14		| 14 bits of unsigned offset	|   Offset range [0;16383]	|
|-------|-------------------------------|-----------------------|-------------------------------|-------------------------------|
| SRPR	|   1	|     101  {A:5}	|	5		| 5 bits of signed addend delta	|   Addend range [-16 ; 15] 	|
|-------|-------------------------------|-----------------------|-------------------------------|-------------------------------|
| LRPR	|   2	|     100  {A:13}	|	13		| 13 bits of signed addend delta|   Addend range [-4096;4095]	|
|-------|-------------------------------|-----------------------|-------------------------------|-------------------------------|
|	|   	|   			|			| S - 8 bits of unsigned symbol	|   Symbol range [0;255]	|
| SREL	|   2	|   1100 {S:8}{C:4}	|	12		| C - 4 bits of rel type and	|				|
|	|	|			|			|     addend combination	|				|
|-------|-------------------------------|-----------------------|-------------------------------|-------------------------------|
|	|	|			|			|R - 2 bits of rel type		|   Rel type range [0;3]	|
| LREL	|   4	|  111 {R:2}{S:8}{A:19}	|			|S - 8 bits of unsigned symbol	|   Symbol range [0;255]	|
|	|	|			|	29		|A - 19 bits of unsigned addend	|   Addend range[0;524287]	|
|	|   	|  			|			|				|				|
*-------------------------------------------------------------------------------------------------------------------------------*

*
* SREL - Rel type Addend combination
*
*---------------------------------------*
| {Type, Addend} |	Substitute	|
|________________|______________________|
|  {0, 0}	 |	0000		|
|----------------|----------------------|
|  {1, -1}	 |	0001		|
|----------------|----------------------|
|  {1, -2}	 |	0010		|
|----------------|----------------------|
|  {1, -3}	 |	0011		|
|----------------|----------------------|
|  {1, -4}	 |	0110		|
|----------------|----------------------|
|  {1, -5}	 |	0101		|
|----------------|----------------------|
|  {1, 0}	 |	0100		|
|----------------|----------------------|
|  {1, 5}	 |	0111		|
|----------------|----------------------|
|  {1, 7}	 |	1101		|
|----------------|----------------------|
|  {2, 0}	 |	1100		|
|----------------|----------------------|
|  {2, 4}	 |	1110		|
*---------------------------------------*
*
*
*/

#define ONE_BYTE_UNSIGNED_MAX_VALUE				(1 << 8) - 1
#define TWO_BYTE_UNSIGNED_MAX_VALUE				(1 << 16) -1
#define THREE_BYTE_UNSIGNED_MAX_VALUE				(1 << 24) - 1
#define FOUR_BYTE_UNSIGNED_MAX_VALUE				(~0U)

/* SEC Instruction */
#define SEC_INSN_OPCODE					0xD0		/*1101 0000 */

/* JMP Insturctions */
#define JMP_INSN_OPCODE					0x0		/* 0000 0000 */
#define LJMP_INSN_OPCODE				0x4000		/* 0100 0000 0000 0000 */
#define LJMP_INSN_MAX_OFFSET				0x3FFF		/* 11 1111 1111 1111 */

/* Short Rel Instructions */
#define SREL_INSN_OPCODE				0xC000		/* 1100 0000 0000 0000 */
#define SREL_INSN_TYPE_ADD_1				0x0		/* "0000" = Rel type 1, Addend -4 */
#define SREL_INSN_TYPE_ADD_2				0x1		/* "0001" = Rel type 1, Addend -5 */
#define SREL_INSN_TYPE_ADD_3				0x2		/* "0010" = Rel type 1, Addend 0 */
#define SREL_INSN_TYPE_ADD_4				0x3		/* "0011" = Rel type 2, Addend 0 */
#define SREL_INSN_TYPE_ADD_5				0x6		/* "0110" = Rel type 1, Addend 4 */
#define SREL_INSN_TYPE_ADD_6				0x5		/* "0101" = Rel type 0, Addend 5 */


/* Long Rel Instructions */
#define LREL_INSN_OPCODE				0xE0000000	/* 1110 0000 0000 0000 0000 0000 0000 0000 */

/* Short RPR Instructions */
#define SRPR_INSN_OPCODE_SIGN_BIT_SET			0xB0		/* 1011 0000 */
#define SRPR_INSN_OPCODE_SIGN_BIT_UNSET			0xA0		/* 1010 0000 */

/* Long RPR Instructions */
#define LRPR_INSN_OPCODE_SIGN_BIT_SET			0x9000		/* 1001 0000 0000 0000 */
#define LRPR_INSN_OPCODE_SIGN_BIT_UNSET			0x8000		/* 1000 0000 0000 0000 */

#define MIN_VALUE_3_BITS_SIGN				(-8)		/* 1 000 */
#define MIN_VALUE_4_BITS_SIGN				0xFFFFFFF0	/* 1 0000 */
#define MIN_VALUE_12_BITS_SIGN				0xFFFFF000	/* 1 0000 0000 0000 */

#define MAX_VALUE_3_BITS				0x7		/* 111 */
#define MAX_VALUE_4_BITS				0xF		/* 1111 */
#define MAX_VALUE_6_BITS				0x3F		/* 11 1111 */
#define MAX_VALUE_12_BITS				0xFFF		/* 1111 1111 1111 */
#define MAX_VALUE_14_BITS				0x3FFF		/* 11 1111 1111 1111 */
#define MAX_VALUE_19_BITS				0x7FFFF		/* 111 1111 1111 1111 1111 */

struct symbol_entry {
	char *name;
	char *based_on;
	unsigned int index;
	unsigned int addend;
};

/* Local, not packed version of relocation structure */
struct _relocation {
	/* Output section index in generated sections table */
	unsigned char section;
	/* Relocation type (ours 2 bits value) */
	unsigned char type;
	/* Output symbol index in generated symbols table */
	unsigned int symbol;
	/* Original relocation addend */
	unsigned int addend;
	/*
	 * Offseti (relative) in output section. Relative means: it contains
	 * offset from previous relocation location to the current one.
	 */
	unsigned int offset;
};

struct section_marker {
	char *name;
	char *begin;
	char *end;
	int ondx;
	int symbol_index;
};

/* Array of section markers pointers. It is as big as number of sections in input file. */
static struct section_marker **section_symbols = NULL;
static struct _relocation *canister_relocs = NULL;
/* Number of relocations in canister image */
static int n_relocs = 0;
/* Number of sections in input file. */
static size_t n_sections = 0;
static bool initrodata_present = false;
static Elf64_Sym *symtab = 0;


static struct relocation *canister_relocations;
static unsigned int bytecode_size = 0;

static struct section_marker *marker(char *in);
static int error(const char *format, ...);
static void process_section(Elf *elf, Elf_Scn *s, int sndx, struct symbol_entry *symbols, size_t strndx);
static void parse_sections(Elf *elf, size_t shstrndx, int *n_syms, size_t *strndx);
static void dump_header(int ofd, char *prog);
static void dump_sections(int ofd, int sfd);
static void dump_symbols(int ofd, int sfd, struct symbol_entry *symbols, int n_syms);
static void dump_relocations(int ofd, struct symbol_entry *symbols);
static void generate_ldscript(char *filename);


/*
 * Section markers name generator.
 * The rules are:
 *  1) dots (.) are removed from section name.
 *  2) begin marker is prefixed by __canister_s.
 *  3) end marker is prefixed by __canister_e.
 *  Example: markers for '.init.rodata' will be
 *  '__canister_sinitrodata' and '__canister_einitrodata'
 */
static struct section_marker *marker(char *in)
{
	int i = 0, l = 0;
	struct section_marker *m = (struct section_marker *)malloc(sizeof(struct section_marker));
	if (m == NULL)
		error("Unable to allocate memory for section marker");
	m->name = strdup(in);
	while (in[i]) {
		if (in[i] != '.')
			l++;
		i++;
	}
	m->begin = calloc(l + 1 + strlen(MARK_PREFIX_BEGIN), 1);
	if (m->begin == NULL)
		error("Unable to allocate memory for section marker");
	strcpy(m->begin, MARK_PREFIX_BEGIN);
	i = 0;
	l = strlen(MARK_PREFIX_BEGIN);
	while (in[i]) {
		if (in[i] != '.')
			m->begin[l++] = in[i];
		i++;
	}
	if (strcmp(in, ".bss") == 0) {
		/*
		 * BSS section will not be measured, but it can be referenced
		 * by other sections relocations. So create start label only
		 * for proper symbol lookup for reverse relocation.
		 */
		m->end = NULL;
	} else {
		m->end = strdup(m->begin);
		m->end[MARK_PREFIX_E_POSITION] = 'e';
	}
	if (!strcmp(in, ".init.rodata"))
		initrodata_present = true;
	return m;
}

static int error(const char *format, ...)
{
	va_list args;
	va_start(args, format);
	vfprintf(stderr, format, args);
	fprintf(stderr, "\n");
	va_end(args);
	exit(1);
}

/*
 * Populates canister_relocs table by _relocation entries
 */
static void process_section(Elf *elf, Elf_Scn *s, int sndx, struct symbol_entry *symbols, size_t strndx)
{
	Elf_Data *data;
	int n, n_entries;
	unsigned int offset = 0;
	Elf64_Rela *rels;
	struct _relocation *r;
	data = elf_getdata(s, NULL);
	rels = (Elf64_Rela *)data->d_buf;
	n_entries = data->d_size / sizeof (Elf64_Rela);

	/* Extend output canister_relocs table by n_entries */
	canister_relocs = (struct _relocation *)realloc(canister_relocs, (n_relocs + n_entries) * sizeof (struct _relocation));
	r = &canister_relocs[n_relocs];
	n_relocs += n_entries;

	for (n = 0; n < n_entries; n++) {
		uint32_t r_sym = rels[n].r_info >> 32; /* symbol index */
		uint32_t r_type; /* relocation type */
		/* Shrink 32 bits relocation type to 2 bits */
		switch (rels[n].r_info & 0xffffffff) {
			case R_X86_64_64:
				r_type = 0;
				break;
			case R_X86_64_PC32:
			case R_X86_64_PLT32:
				/*
				 * arch/x86/tools/relocs.c:
				 * NB: R_X86_64_PLT32 can be treated as R_X86_64_PC32.
				 */
				r_type = 1;
				break;
			case R_X86_64_32S:
				r_type = 2;
				break;
			default:
				error("Unsupported relocation type");
		}

		/* First time we've seen this r_sym? look up needed. */
		if (!symbols[r_sym].name) {
			if (ELF64_ST_TYPE(symtab[r_sym].st_info) == STT_SECTION) {
				/* Symbol type is section name. */
				struct section_marker *m = section_symbols[symtab[r_sym].st_shndx];
				/*
				 * It should point to local section and this section must be
				 * measured (present in section_symbols).
				 */
				if (!m)
					error("Cannot find marker for section index: %d", symtab[r_sym].st_shndx);
				/*
				 * Do not use section name as a target as in
				 * vmlinux it will point to aggregated section.
				 * Use begin marker instead which will survive
				 * final vmlinux linking and will point to
				 * actual start of the canister section.
				 */
				symbols[r_sym].name = m->begin;
			} else {
				/* Get symbol name */
				symbols[r_sym].name = strdup(elf_strptr(elf, strndx, symtab[r_sym].st_name));
			}
		}
		if (rels[n].r_addend > INT_MAX || rels[n].r_addend < INT_MIN)
			error("r_addend overflow");
		if (rels[n].r_offset - offset > UINT_MAX)
			error("r_offset overflow");
		r->section = section_symbols[sndx]->ondx;
		r->type = r_type;
		r->symbol = r_sym;
		r->addend = rels[n].r_addend;
		/* Use relative offset to shrink u64 to u32 field. */
		r->offset = rels[n].r_offset - offset;
		offset = rels[n].r_offset;
		r++;
	}
}

/*
 * Walk through all sections:
 *  - if it is .symtab - save its content and remember number of symbols (*n_syms).
 *  - if it is .strtab - remember its index (*strndx).
 *  - create section markers for every SHF_ALLOC section, it it is not in exception list.
 */
static void parse_sections(Elf *elf, size_t shstrndx, int *n_syms, size_t *strndx)
{
	Elf_Scn *section = NULL;
	GElf_Shdr section_header;
	char *name;
	size_t ndx;
	int ondx = 0;

	*strndx = 0;
	if (elf_getshdrnum (elf, &n_sections) < 0)
		error("Unable to get sections number");

	section_symbols = (struct section_marker **)calloc(n_sections, sizeof(struct section_marker *));
	if (section_symbols == NULL)
		error("Unable to allocate memory for section_symbols");

	for (ndx = 0; ndx < n_sections; ++ndx)
	{
		section = elf_getscn (elf, ndx);
		if (section == NULL)
			error("Error getting section");

		if (gelf_getshdr(section , &section_header) != &section_header)
			error("getshdr() failed");

		if ((name = elf_strptr(elf, shstrndx , section_header.sh_name )) == NULL)
			error("elf_strptr () failed");

		if (!strcmp(name, ".symtab")) {
			*n_syms = section_header.sh_size / sizeof (Elf64_Sym);
			symtab = (Elf64_Sym *)malloc(sizeof(Elf64_Sym) * (*n_syms));
			if (!symtab)
				error("symtab allocation failed");
			memcpy(symtab, elf_getdata(section, NULL)->d_buf, sizeof(Elf64_Sym) * (*n_syms));
			continue;
		}
		if (!strcmp(name, ".strtab")) {
			*strndx = ndx;
			continue;
		}

		if ((section_header.sh_flags & SHF_ALLOC) == 0)
			continue;

		if (!strncmp(name, "__jump_table", 12) ||
		    !strncmp(name, ".retpoline_sites", 16) ||
		    !strncmp(name, ".return_sites", 13) ||
		    !strncmp(name, ".printk_index", 13) ||
		    !strncmp(name, "__bug_table", 13)) {
			error("ERROR: Forbidden %s section found in canister!! Please fix it.");
		}
		/*
		 * .discard, .exitcall.exit and .modinfo sections will be
		 * dropped at vmlinux linking time (see vmlinux linker
		 * script: arch/x86/kernel/vmlinux.lds)
		 *
		 * Ignore symbol table sections as there are no needs to
		 * measure them.
		 *
		 * Ignore __ex_table as it will be sorted ("corrupted") by
		 * sort_main_extable() code before fips integrity code. If
		 * we really want to measure __ex_table, we must run
		 * fips_integrity_init() before sort_main_extable()
		 * The same situation is with __jump_table which got sorted
		 * by jump_label_init().
		 *
		 * Skip ".note.gnu.property" section from canister measurement
		 * as this section is stripped off from vmlinux.
		 *
		 * Skip __mcount_loc section for canister measurement as it will be
		 * discarded during initial bootup process before canister measurement.
		 *
		 * Skip __patchable_function_entries section for canister measurement,
		 * as it will be discarded in final vmlinux
		 */
		if (!strncmp(name, ".discard.", 9) ||
		    !strcmp(name, ".exitcall.exit") ||
		    !strcmp(name, ".modinfo") ||
		    !strncmp(name, "__ksymtab_", 10) ||
		    !strncmp(name, "___ksymtab", 10) ||
		    !strncmp(name, "___kcrctab", 10) ||
		    !strcmp(name, "__ex_table") ||
		    !strcmp(name, "__jump_table") ||
		    !strcmp(name, "__mcount_loc") ||
		    !strcmp(name, ".note.gnu.property") ||
		    !strcmp(name, "__patchable_function_entries"))
			continue;

		/*
		 * Allocate section_marker structure,
		 * initialize .name, .begin, .end fields.
		 */
		section_symbols[ndx] = marker(name);
		/*
		 * ndx - section index in inout file.
		 * ondx - section index in generated .c file
		 */
		section_symbols[ndx]->ondx = ondx++;
	}
	if (!symtab)
		error("Unable to find .symtab section");
	if (!*strndx)
		error("Unable to find .strtab section");
}

static void dump_header(int ofd, char *prog)
{
	dprintf(ofd,
		"/*\n"
		" * Generated by %s\n"
		" */\n"
		"#include \"fips_integrity.h\"\n\n", prog);
}

static void dump_sections(int ofd, int sfd)
{
	int i, n = 0;
	/*
	 * Put all strings in '\0' separated array of chars.
	 * Do not use array of string (char * canister_sections[]) as
	 * it introduces new relocations in canister.
	 */
	dprintf(ofd, "const __section(\".init.rodata\") char canister_sections[] = {\n");
	for (i = 0; i < n_sections; i++)
		if (section_symbols[i] && section_symbols[i]->end) {
			dprintf(ofd, "\t\"%s\\0\"\n\t\"%s\\0\"\n",
				section_symbols[i]->begin,
				section_symbols[i]->end);
			dprintf(sfd, "%s\n%s\n", section_symbols[i]->begin,
				section_symbols[i]->end);
			n++;
		}
	/* We've just introduced/generated fresh .init.rodata section, add its section markers. */
	if (!initrodata_present) {
		dprintf(ofd, "\t\"__canister_sinitrodata\\0\"\n\t\"__canister_einitrodata\\0\"\n");
		dprintf(sfd, "__canister_sinitrodata\n__canister_einitrodata\n");
		n++;
	}
	dprintf(ofd, "};\n");
	dprintf(ofd, "const __section(\".init.rodata\") int canister_sections_size = %d;\n\n", n);
};

/*
 * Not only dump the symbols table, but post process (optimize) it
 * to be used by dump_relocations() later.
 */
static void dump_symbols(int ofd, int sfd, struct symbol_entry *symbols, int n_syms)
{
	int i;
	/* Index in output symbol table. */
	uint32_t index = 0;

	/* Use same format as for canister_sections. */
	dprintf(ofd, "const __section(\".init.rodata\") char canister_strtab[] = {\n");
	for (i = 0; i < n_syms; i++) {
		int stype, ssection;
		if (!symbols[i].name)
			continue;
		stype = ELF64_ST_TYPE(symtab[i].st_info);
		ssection = symtab[i].st_shndx;
		if (stype == STT_SECTION) {
			/*
			* Section symbols always come first. So, symbol_index'es
			* will be always initialized before use.
			*/
			section_symbols[symtab[i].st_shndx]->symbol_index = index;
		} else if (ssection != SHN_UNDEF && ssection != SHN_ABS) {
			/*
			 * Optimization. Do not print local symbols, and do not
			 * look up them at runtime.
			 * For local relocations, instead of using local symbol,
			 * use its section begin marker as a symbol, and
			 * its offset in the section as addend.
			 * Example:
			 *    target = (address of function A in section .text)
			 * will be transformed to
			 *    target = (address of __canister_stext) + (offset to A)
			 */
			symbols[i].based_on = section_symbols[ssection]->begin;
			symbols[i].addend = symtab[i].st_value;
			symbols[i].index = section_symbols[ssection]->symbol_index;
			continue;
		}
		symbols[i].index = index;
		dprintf(ofd, "\t\"%s\\0\" /* %d: %x %d %lx */\n", symbols[i].name, i, symtab[i].st_info, symtab[i].st_shndx, symtab[i].st_value);
		dprintf(sfd, "%s\n", symbols[i].name);
		index++;
	}
	dprintf(ofd, "};\n");
	dprintf(ofd, "const __section(\".init.rodata\") int canister_strtab_size = %d;\n\n", index);
}

static void dump_relocations(int ofd, struct symbol_entry *symbols)
{
	int i;
	/*
	 * Array of structures is OK, it does not introduce new relocations.
	 *
	 * Packed (runtime) version of 'struct relocation' is defined in fips_integrity.h
	 */
	canister_relocations = (struct relocation *)malloc(sizeof(struct relocation) * n_relocs);
	for (i = 0; i < n_relocs; i++) {
		struct symbol_entry *s = &symbols[canister_relocs[i].symbol];
		if (s->based_on) {
			/* Relocation to collapsed local symbol, print nice comment. */
				canister_relocations[i].section = canister_relocs[i].section;
				canister_relocations[i].type = canister_relocs[i].type;
				canister_relocations[i].symbol = s->index;
				canister_relocations[i].offset = canister_relocs[i].offset;
				canister_relocations[i].addend = canister_relocs[i].addend + s->addend;
		} else {
			/* Relocation to local section or to external (from vmlinux) symbol. */
				canister_relocations[i].section = canister_relocs[i].section;
				canister_relocations[i].type = canister_relocs[i].type;
				canister_relocations[i].symbol = s->index;
				canister_relocations[i].offset = canister_relocs[i].offset;
				canister_relocations[i].addend = canister_relocs[i].addend;
		}
	}
}

static void generate_ldscript(char *filename)
{
	int i, n = 0;
	/* Open output file.  */
	int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
	if (fd == -1)
		error("Cannot open output file");

	dprintf(fd, "SECTIONS\n{\n");
	for (i = 0; i < n_sections; i++)
		if (section_symbols[i]) {
			if (section_symbols[i]->end) {
				n++;
				dprintf(fd,
					"  %s : {\n"
					"    %s = .;\n"
					"    *(%s)\n"
					"    %s = .;\n"
					"  }\n",
					section_symbols[i]->name,
					section_symbols[i]->begin,
					section_symbols[i]->name,
					section_symbols[i]->end);
			} else {
				dprintf(fd,
					"  %s :  {\n"
					"    %s = .;\n"
					"    *(%s)\n"
					"  }\n",
					section_symbols[i]->name,
					section_symbols[i]->begin,
					section_symbols[i]->name);
			}
		}
	/* Section from generated .c file. */
	if (!initrodata_present)
		dprintf(fd,
			"  .init.rodata : {\n"
			"    __canister_sinitrodata = .;\n"
			"    *(.init.rodata)\n"
			"    __canister_einitrodata = .;\n"
			"  }\n");
	/*
	 * Some ldscript tricks here:
	 *  - Allocate placeholder for golden canister HMAC value
	 *  - Provide canister_size symbol
	 */
	dprintf(fd,
		"  .init.rodata.canister_info :  {\n"
		"    canister_hmac = .;\n"
		"    . = . + 32;\n"
		"    canister_size = .;\n"
		"    LONG(");
	for (i = 0; i < n_sections; i++)
		if (section_symbols[i]) {
			if (section_symbols[i]->end) {
				n--;
				dprintf(fd, "SIZEOF(%s)", section_symbols[i]->name);
				if (n)
					dprintf(fd, " + ");
			}
		}
	if (!initrodata_present)
		dprintf(fd, " + SIZEOF(.init.rodata)");
	dprintf(fd, ")\n  }\n");
	dprintf(fd, "}\n");

	close(fd);
}

static void print_insn_byte_wise(unsigned int insn, int nfd)
{
	if (insn <= ONE_BYTE_UNSIGNED_MAX_VALUE) {
		dprintf(nfd, "0x%02x, ", insn & 0xff);
		bytecode_size++;
	} else if (insn <= TWO_BYTE_UNSIGNED_MAX_VALUE) {
		dprintf(nfd, "0x%02x, 0x%02x, ",
			(insn >> 8) & 0xff, insn & 0xff);
		bytecode_size += 2;
	} else if (insn <= THREE_BYTE_UNSIGNED_MAX_VALUE) {
		dprintf(nfd, "0x%02x, 0x%02x, 0x%02x, ",
			(insn >> 16) & 0xff,
			(insn >> 8) & 0xff,
			insn & 0xff);
		bytecode_size += 3;
	} else if (insn <= FOUR_BYTE_UNSIGNED_MAX_VALUE) {
		dprintf(nfd, "0x%02x, 0x%02x, 0x%02x, 0x%02x, ",
			(insn >> 24) & 0xff,
			(insn >> 16) & 0xff,
			(insn >> 8) & 0xff,
			insn & 0xff);
		bytecode_size += 4;
	}
	else {
		error("Unsupported canister bytecode instruction size!!");
	}
}

static void print_jmp_insn(int nfd, unsigned int off)
{
	unsigned short rem_off = 0;
	unsigned int jmp;

	if (off <= MAX_VALUE_6_BITS) {
		jmp = JMP_INSN_OPCODE | off;
		print_insn_byte_wise(jmp, nfd);
	} else if (off <= MAX_VALUE_14_BITS) {
		jmp = LJMP_INSN_OPCODE | off;
		print_insn_byte_wise(jmp, nfd);
	} else {
		jmp = LJMP_INSN_OPCODE | LJMP_INSN_MAX_OFFSET;
		print_insn_byte_wise(jmp, nfd);
		rem_off = off - MAX_VALUE_14_BITS;

		while (rem_off >= MAX_VALUE_14_BITS) {
			rem_off -= MAX_VALUE_14_BITS;
			jmp = LJMP_INSN_OPCODE | LJMP_INSN_MAX_OFFSET;
			print_insn_byte_wise(jmp, nfd);
		}
		if (rem_off) {
			if (rem_off <= MAX_VALUE_6_BITS) {
				jmp = JMP_INSN_OPCODE | rem_off;
				print_insn_byte_wise(jmp, nfd);
			}
			else {
				jmp = LJMP_INSN_OPCODE | rem_off;
				print_insn_byte_wise(jmp, nfd);
			}
		}
	}
}

static void print_sec_insn(int nfd, unsigned short sec_incr)
{
	unsigned int sec;

	sec = SEC_INSN_OPCODE | sec_incr;
	print_insn_byte_wise(sec, nfd);

}

static void print_srel_insn(int nfd, unsigned short type, unsigned short symbol, int addend)
{
	unsigned int srel;

	srel = SREL_INSN_OPCODE | (symbol << 4);
	if (type == 1 && addend == -4) {
		srel = srel | SREL_INSN_TYPE_ADD_1;
	} else if (type == 1 && addend == -5) {
		srel = srel | SREL_INSN_TYPE_ADD_2;
	} else if (type == 1 && addend == 0) {
		srel = srel | SREL_INSN_TYPE_ADD_3;
	} else if (type == 2 && addend == 0) {
		srel = srel | SREL_INSN_TYPE_ADD_4;
	} else if (type == 1 && addend == 4) {
		srel = srel | SREL_INSN_TYPE_ADD_5;
	} else if (type == 0 && addend == 5) {
		srel = srel | SREL_INSN_TYPE_ADD_6;
	} else {
		error("Unknown rel type and addend combination!!! %d %d\n", type, addend);
	}
	print_insn_byte_wise(srel, nfd);
}

static void print_lrel_insn(int nfd, unsigned short type, unsigned short symbol, int addend)
{
	unsigned int lrel;

	// LREL instruction: 111{R:2}{S:8}{A:19}
	lrel = LREL_INSN_OPCODE | (type << 27) | (symbol << 19) | addend;
	print_insn_byte_wise(lrel, nfd);
}

static void print_srpr_insn(int nfd, int add_del)
{
	unsigned int srpr;

	if (add_del < 0) {
		srpr = SRPR_INSN_OPCODE_SIGN_BIT_SET;
		if (add_del != -16) {
			srpr |= abs(add_del);
		}
	} else {
		srpr = SRPR_INSN_OPCODE_SIGN_BIT_UNSET | add_del;
	}
	print_insn_byte_wise(srpr, nfd);
}

static void print_lrpr_insn(int nfd, int add_del)
{
	unsigned int lrpr;

	if (add_del < 0) {
		lrpr = LRPR_INSN_OPCODE_SIGN_BIT_SET;
		if (add_del != -4096)
			lrpr |= abs(add_del);
	} else {
		lrpr = LRPR_INSN_OPCODE_SIGN_BIT_UNSET | add_del;
	}
	print_insn_byte_wise(lrpr, nfd);
}
static void dump_canister_relocations_bytecode(int ofd)
{
	int i;
	struct relocation *r, *p = &canister_relocations[0];
	unsigned short sec_incr = 0;

	dprintf(ofd, "const __section(\".init.rodata\") unsigned char canister_relocations_bytecode[] = { ");

	print_sec_insn(ofd, p->section);
	print_jmp_insn(ofd, p->offset);
	if (p->addend >= MIN_VALUE_3_BITS_SIGN && p->addend <= MAX_VALUE_3_BITS) { /* SREL INSN */
		print_srel_insn(ofd, p->type, p->symbol, p->addend);
	} else if (p->addend > MAX_VALUE_3_BITS && p->addend <= MAX_VALUE_19_BITS) { /* LREL INSN */
		print_lrel_insn(ofd, p->type, p->symbol, p->addend);
	}

	for (i = 1; i < n_relocs; i++) {
		r = &canister_relocations[i];
		if (p->section != r->section) {
			sec_incr = r->section - p->section;
			print_sec_insn(ofd, sec_incr);
		}

		print_jmp_insn(ofd, r->offset);

		if (p->section == r->section && p->type == r->type && p->symbol == r->symbol &&
		   ((r->addend - p->addend) >= MIN_VALUE_12_BITS_SIGN && (r->addend - p->addend) <= MAX_VALUE_12_BITS)) {

			int add_del = r->addend - p->addend;

			/* SRPR instructions */
			if (add_del >= MIN_VALUE_4_BITS_SIGN && add_del <= MAX_VALUE_4_BITS) {
				print_srpr_insn(ofd, add_del);
			} else { /* LRPR instructions */
				print_lrpr_insn(ofd, add_del);
			}

		} else { /* REL instructions */
			if (r->addend >= MIN_VALUE_3_BITS_SIGN && r->addend <= MAX_VALUE_3_BITS) { /* SREL INSN */
				print_srel_insn(ofd, r->type, r->symbol, r->addend);
			} else if (r->addend > MAX_VALUE_3_BITS && r->addend <= MAX_VALUE_19_BITS) { /* LREL INSN */
				print_lrel_insn(ofd, r->type, r->symbol, r->addend);
			}
		}
		p = r;
	}
	dprintf(ofd, "};");
	dprintf(ofd, "\n\nconst unsigned int canister_relocations_bytecode_size = %d;\n", bytecode_size);
}

int main (int argc, char *argv[])
{
	int fd, ofd, sfd;
	Elf *elf;
	GElf_Ehdr ehdr;
	Elf_Scn *section;
	size_t shstrndx, strndx;
	GElf_Shdr section_header;
	char *name;
	int n_syms = 0;
	struct symbol_entry *symbols;

	if (elf_version(EV_CURRENT) ==  EV_NONE)
		error("ELF library initialization failed");

	/* Open input file, core canister */
	fd = open(argv[1], O_RDONLY);
	if (fd == -1)
		error("Cannot open input file");

	elf = elf_begin(fd, ELF_C_READ, NULL);
	if (elf == NULL)
		error("Unable to parse input file");

	if (elf_kind(elf) != ELF_K_ELF)
		error("Input file is not ELF");

	if (gelf_getehdr(elf, &ehdr) == NULL)
		error("Unable to parse ELF file");

	if (gelf_getclass(elf) != ELFCLASS64)
		error("Expecting ELF64");

	if (ehdr.e_type != ET_REL)
		error("Expecting relocatable object file");

	if (elf_getshdrstrndx(elf, &shstrndx) != 0)
		error("Unable to find section header string table");

	parse_sections(elf, shstrndx, &n_syms, &strndx);
	/* n_syms is know, allocate symbols info table */
	symbols = (struct symbol_entry *)calloc(n_syms, sizeof (struct symbol_entry));

	/*
	 * Walk through all sections again to find .rela.* sections we want
	 * to collect relocation from.
	 */
	section = NULL;
	while ((section = elf_nextscn(elf, section)) != NULL) {
		if (gelf_getshdr(section , &section_header) != &section_header)
			error("getshdr() failed");

		if (section_header.sh_type != SHT_RELA)
			continue;

		if (!section_header.sh_info)
			continue;

		if (!section_symbols[section_header.sh_info])
			continue;

		if ((name = elf_strptr(elf, shstrndx, section_header.sh_name )) == NULL)
			error("elf_strptr () failed");

		if (strncmp(name, ".rela", 5))
			continue;

		printf("Processing: %s\n", name);

		process_section(elf, section, section_header.sh_info, symbols, strndx);
	}
	elf_end(elf);
	close(fd);

	/* Open output file, .c file with data for fips_integrity interpreter. */
	ofd = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
	if (ofd == -1)
		error("Cannot open output file");

	sfd = open(argv[4], O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
	if (sfd == -1)
		error("Cannot open output symbols file %s", argv[4]);
	/*
	 * Main rule for generated .c file: do not introduce new relocations
	 * as it won't be accounted (chicken-egg problem).
	 */
	dump_header(ofd, argv[0]);
	dump_sections(ofd, sfd);
	dump_symbols(ofd, sfd, symbols, n_syms);
	dump_relocations(ofd, symbols);

	dump_canister_relocations_bytecode(ofd);

	close(ofd);
	close(sfd);

	/* Linker script for final canister linking. */
	generate_ldscript(argv[3]);
	return 0;
}


