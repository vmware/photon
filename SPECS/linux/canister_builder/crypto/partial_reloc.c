/*
 * Canister object file relocations reducer.
 *
 * Copyright (c) 2025 Broadcom. All Rights Reserved. The term "Broadcom"
 * refers to Broadcom Inc. and/or its subsidiaries.
 *
 * Author: Alexey Makhalov <alexey.makhalov@broadcom.com>
 *
 *
 * `ld -r` performs linking of multiple .o files into single canister object
 * file (canister.o). Unfortunately, linker does not apply local relocations,
 * but just combines all realocation together in corresponding .rela.*
 * sections for later stages, which is vmlinux linking.
 * It costs us increased canister_relocations_bytecode and canister_strtab
 * tables as well as boot time penalty.
 *
 * There are 2 known cases where relocation can be locally applied:
 * - Relocations for __kcfi_typeid_* ABS symbols produced by .S files. As
 *   their definitions are already in the canister object file. We can get
 *   rid of them completely. It will eliminate special handling logic in
 *   fips_integrity code.
 * - PC-relative 32-bit relocation within the same section where relocation
 *   symbol is defined internally. Example: 2 functions A and B defined in
 *   .text section of the canister.o. And A calls B. B is local object. So,
 *   the distance between addresses of these functions will remain the same
 *   even after the final linking of vmlinux. Apply it now.
 *
 * Input: relocatable 64-bit x86_64 ELF object (ET_REL) to be modified to
 * apply mentioned above local relocations and drop them from relocation
 * sections.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <fcntl.h>
#include <libelf.h>
#include <gelf.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <inttypes.h>
#include <assert.h>

#ifndef DEBUG
#define DEBUG 0
#endif

#if DEBUG
#define dbg(x...) printf(x...)
#else
#define dbg(x...) {}
#endif

static void error(const char *fmt, ...)
{
	va_list ap;
	va_start(ap, fmt);
	vfprintf(stderr, fmt, ap);
	fprintf(stderr, "\n");
	va_end(ap);
	exit(EXIT_FAILURE);
}

int main(int argc, char **argv)
{
	Elf *elf;
	GElf_Ehdr ehdr;
	Elf_Scn *scn = NULL, *symtab_scn = NULL;
	GElf_Shdr symtab_shdr;
	Elf_Data *symdata;
	size_t nsym;
	size_t sec_count;
	Elf_Scn **scn_by_index;

	if (argc != 2) {
		fprintf(stderr, "Usage: %s input.o", argv[0]);
		return 2;
	}

	const char *filename = argv[1];

	if (elf_version(EV_CURRENT) == EV_NONE)
		error("libelf initialization failed: %s", elf_errmsg(-1));

	int fd = open(filename, O_RDWR);
	if (fd < 0)
		error("open(%s): %s", filename, strerror(errno));

	elf = elf_begin(fd, ELF_C_RDWR, NULL);
	if (!elf || (elf_kind(elf) != ELF_K_ELF))
		error("Not an ELF file");

	if (!gelf_getehdr(elf, &ehdr))
		error("gelf_getehdr: %s", elf_errmsg(-1));

	if (ehdr.e_type != ET_REL)
		error("Input must be relocatable object (ET_REL)");

	if ((ehdr.e_ident[EI_CLASS] != ELFCLASS64) || (ehdr.e_machine != EM_X86_64))
		error("Only x86_64 ELFCLASS64 supported");

	/* Get symbol table */
	while ((scn = elf_nextscn(elf, scn)) != NULL) {
		if (!gelf_getshdr(scn, &symtab_shdr)) error("gelf_getshdr: %s", elf_errmsg(-1));
		if (symtab_shdr.sh_type == SHT_SYMTAB) {
			symtab_scn = scn;
			break;
		}
	}
	if (!symtab_scn)
		error("No symbol table (SHT_SYMTAB) found");

	symdata = elf_getdata(symtab_scn, NULL);
	if (!symdata)
		error("elf_getdata(symtab): %s", elf_errmsg(-1));
	nsym = symdata->d_size / symtab_shdr.sh_entsize;

	/* Map section index -> section */
	sec_count = ehdr.e_shnum;
	scn_by_index = calloc(sec_count, sizeof(Elf_Scn*));
	if (!scn_by_index)
		error("calloc() failed: %s", strerror(errno));

	scn = NULL;
	while ((scn = elf_nextscn(elf, scn)) != NULL) {
		size_t idx = elf_ndxscn(scn);
		if (idx < sec_count)
			scn_by_index[idx] = scn;
	}

#if DEBUG
	size_t shstrndx;
	if (elf_getshdrstrndx(elf, &shstrndx) != 0)
		error("Unable to find section header string table");
#endif

	scn = NULL;
	while ((scn = elf_nextscn(elf, scn)) != NULL) {
		GElf_Shdr shdr;
		size_t target_sec_idx, nrel;
		Elf_Data *target_sec, *reldat;
		unsigned char *relbuf;
		size_t relbuf_size = 0;

		if (!gelf_getshdr(scn, &shdr))
			error("gelf_getshdr: %s", elf_errmsg(-1));

		/* Canister has only .rela types */
		if (shdr.sh_type != SHT_RELA)
			continue;

		target_sec_idx = shdr.sh_info;
		if (target_sec_idx >= sec_count || scn_by_index[target_sec_idx] == NULL)
			continue;

		target_sec = elf_getdata(scn_by_index[target_sec_idx], NULL);
		if (!target_sec)
			continue;

		reldat = elf_getdata(scn, NULL);
		if (!reldat)
			continue;

		nrel = reldat->d_size / shdr.sh_entsize;
		if (nrel == 0)
			continue;

#if DEBUG
		char *name = elf_strptr(elf, shstrndx, shdr.sh_name );
		if (!name)
			error("elf_strptr() failed");
#endif

		/* New relocation table */
		relbuf = malloc(reldat->d_size);
		if (!relbuf)
			error("malloc() failed: %s", strerror(errno));
		relbuf_size = 0;

		for (size_t i = 0; i < nrel; i++) {
			GElf_Rela rela;
			GElf_Sym sym;
			int applied = 0;

			if (!gelf_getrela(reldat, i, &rela))
				error("gelf_getrela failed");

			if (GELF_R_SYM(rela.r_info) >= nsym)
				error("Relocation symbol index is out of boundary");

			gelf_getsym(symdata, GELF_R_SYM(rela.r_info), &sym);

			switch (GELF_R_TYPE(rela.r_info)) {
				/*
				 * __kcfi_typeid_* absolute symbols defined in accelerator's glue code,
				 * and used in corresponding .S files
				 */
				case R_X86_64_32:
					if ((sym.st_shndx == SHN_ABS) && (rela.r_offset + 4 <= target_sec->d_size)) {
						if (rela.r_addend)
							error("non zero r_addend for ABS symbol");
						*(uint32_t *)((char*)target_sec->d_buf + rela.r_offset) = (uint32_t)sym.st_value;
						applied = 1;
						dbg("ABS32: %s:0x%lx <- %8lx\n", name+5, rela.r_offset, sym.st_value);
					}
					break;
				/*
				 * .text referencing to itself as PC relative offset.
				 * The offset will remain the same after final linking in vmlinux.
				 */
				case R_X86_64_PC32:
				case R_X86_64_PLT32:
					if ((sym.st_shndx == target_sec_idx) && (rela.r_offset + 4 <= target_sec->d_size)) {
						uint64_t value = (sym.st_value + rela.r_addend - rela.r_offset) & 0xffffffffu;
						*(uint32_t *)((char*)target_sec->d_buf + rela.r_offset) = (uint32_t)value;
						applied = 1;
						dbg("PLT32: %s:0x%lx <- %8lx\n", name+5, rela.r_offset, value);
					}
					break;
			}

			if (!applied) {
				unsigned char *raw = (unsigned char*)reldat->d_buf + i * shdr.sh_entsize;
				memcpy(relbuf + relbuf_size, raw, shdr.sh_entsize);
				relbuf_size += shdr.sh_entsize;
			}
		}


		/* No changes in the section, go next */
		if (relbuf_size == reldat->d_size) {
			free(relbuf);
			continue;
		}

		/* Update relocation section, do not free relbuf */
		Elf_Data *first = elf_getdata(scn, NULL);
		first->d_buf = relbuf;
		first->d_size = relbuf_size;
		shdr.sh_size = relbuf_size;
		gelf_update_shdr(scn, &shdr);
	}

	if (elf_update(elf, ELF_C_WRITE) < 0)
		error("elf_update failed: %s", elf_errmsg(-1));

	elf_end(elf);
	close(fd);
	return 0;
}

