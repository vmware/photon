/* vim: set ts=2 sw=2 sts=2 et: */

/* Copyright (C) 2024, Broadcom, Inc. */

/*
 * How to build:
 * tdnf install -y build-essential dwarves-devel elfutils-devel
 * gcc -Wall -Werror -o struct_comparator struct-comparator.c -ldwarves
 */

#include <argp.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#include <dwarves/dwarves.h>
#include <dwarves/dutil.h>
#include <dwarves/list.h>

#define LINE_SZ 1024

#define pr_err(fmt, ...)   fprintf(stderr, "ERROR: " fmt, ##__VA_ARGS__)
#define pr_info(fmt, ...)  printf("INFO: " fmt, ##__VA_ARGS__)
#define pr_crit(fmt, ...)  printf("CRITICAL: " fmt, ##__VA_ARGS__)

int rc;
LIST_HEAD(fips_head);
char knwn_vmlinux_def_dir[1024];

struct struct_def {
  char name[1024];
  char *def;
  struct list_head list_entry;
};

struct conf_fprintf conf = {
  .emit_stats = 1,
};

static void free_struct_def(struct struct_def *s_def)
{
  free(s_def->def);
  free(s_def);
}

/* Check if this definition matches one that we know we are safe to ignore */
static int matches_knwn_vmlinux_def(const struct struct_def *s_def)
{
  bool ret = false;
  FILE *knwn_fp;
  char *tmp = NULL;
  char *known_def = NULL;
  int new_size = 0;
  char filename[PATH_MAX] = {};
  char line[LINE_SZ] = {};

  /* Definitions should be stored in files in the form: <name>.txt */
  snprintf(filename, sizeof(filename), "%s/%s.txt", knwn_vmlinux_def_dir,
     s_def->name);
  knwn_fp = fopen(filename, "r");
  if (!knwn_fp) {
    pr_err("fopen: '%s' (%s)\n", filename, strerror(errno));
    return ret;
  }

  while (fgets(line, sizeof(line), knwn_fp) != NULL) {
    int line_sz = strlen(line);
    new_size += line_sz;

    tmp = realloc(known_def, new_size + 1);
    if (!tmp) {
      free(known_def);
      fclose(knwn_fp);
      return ret;
    }

    known_def = tmp;

    strncpy(known_def + (new_size - line_sz), line, line_sz);
    known_def[new_size] = '\0';
  }

  fclose(knwn_fp);

  ret = strcmp(known_def, s_def->def) == 0;
  free(known_def);
  return ret;
}

/* Compare the vmlinux definition against the FIPS list */
static int fips_vmlinux_comp(const struct struct_def *vmlinux_def)
{
  struct struct_def *entry, *n;

  list_for_each_entry_safe(entry, n, &fips_head, list_entry) {
    /* If name matches, compare the definitions */
    if (strcmp(entry->name, vmlinux_def->name) != 0)
      continue;
    if (strcmp(entry->def, vmlinux_def->def) == 0)
      continue;

    if (matches_knwn_vmlinux_def(vmlinux_def))
      return 0;

    pr_err("struct %s doesn't match between vmlinux and fips canister\n"
       "************************************************************\n"
       "FIPS Definition:\n%s\n"
       "vmlinux definition:\n%s\n"
       "***********************************************************\n\n",
       entry->name, entry->def, vmlinux_def->def);

    /* Remove from FIPS list, so we don't check/print again */
    list_del(&entry->list_entry);
    free_struct_def(entry);
    return -1;
  }

  return 0;
}

/* Add a struct_def to the list of FIPS definitions */
static void add_to_fips_list(struct struct_def *s_def)
{
  /*
   * Check if this definition is either brand new, or is
   * different from any existing definitions for this struct.
   * FIPS canister will likely have the same struct defined
   * multiple places in the debuginfo, but we should only keep
   * unique definitions... Probably there should be only 1 unique
   * but in vmlinux at least, there can be multiple different definitions.
   */
  struct struct_def *entry;
  bool is_unique = true;

  list_for_each_entry(entry, &fips_head, list_entry) {
    if (strcmp(entry->name, s_def->name) != 0)
      continue;

    if (strcmp(entry->def, s_def->def) == 0) {
      /* Matched an existing def in the list, not unique */
      is_unique = false;
      break;
    }
  }

  if (is_unique)
    list_add(&s_def->list_entry, &fips_head);
  else
    free_struct_def(s_def);
}

static void free_struct_def_list(struct list_head *list_head)
{
  struct struct_def *n = NULL;
  struct struct_def *pos = NULL;

  list_for_each_entry_safe(pos, n, list_head, list_entry) {
    list_del(&pos->list_entry);
    free_struct_def(pos);
  }
}

static void emit_tag(struct tag *tag, uint32_t tag_id, struct cu *cu,
    bool do_compare)
{
  bool name_in_fips_list = false;
  FILE *tmp_fp = NULL;
  struct struct_def *s_def = NULL;
  const char *type_name = NULL;
  struct struct_def *pos = NULL;
  size_t buf_size;
  struct type *type = &tag__class(tag)->type;

  if (tag__is_struct(tag)) {
    /* Can't do comparison without a struct name! */
    type_name = type__name(type);
    if (!type_name)
      return;

    /* Skip comparison if size is 0 */
    if (!tag__size(tag, cu))
      return;

    /* Skip out if not in fips canister list */
    if (do_compare) {
      list_for_each_entry(pos, &fips_head, list_entry) {
        if (strcmp(pos->name, type_name) == 0) {
          name_in_fips_list = true;
          break;
        }
      }

      if (!name_in_fips_list)
        return;
    }

    s_def = calloc(sizeof(struct struct_def), 1);
    if (!s_def) {
      pr_err("Failed to allocate memory: %s", strerror(errno));
      free_struct_def_list(&fips_head);
      exit(1);
    }

    tmp_fp = open_memstream(&s_def->def, &buf_size);
    if (!tmp_fp) {
      pr_err("Can't open tmp file for writing!: %s\n", strerror(errno));
      free_struct_def_list(&fips_head);
      exit(1);
    }

    tag__fprintf(tag, cu, &conf, tmp_fp);
    fprintf(tmp_fp, " /* size: %zd */\n\n", tag__size(tag, cu));

    /* Save the definition */
    strncpy(s_def->name, type_name, sizeof(s_def->name));

    fclose(tmp_fp);

    if (do_compare) {
      if (fips_vmlinux_comp(s_def) < 0)
        rc = -1;
      free_struct_def(s_def);
    } else {
      add_to_fips_list(s_def);
    }
  }
}

static int cu__emit_tags_fips(struct cu *cu)
{
  uint32_t i;
  struct tag *tag;

  cu__for_each_type(cu, i, tag) {
    emit_tag(tag, i, cu, false);
  }

  return 0;
}

static enum load_steal_kind fips_stealer(struct cu *cu,
          struct conf_load *conf_load __maybe_unused,
          void *thr_data __maybe_unused)
{
  cu__emit_tags_fips(cu);
  return LSK__DELETE;
}

struct conf_load fips_conf_load = {
  .steal = fips_stealer,
  .conf_fprintf = &conf,
};

static int cu__emit_tags_vmlinux(struct cu *cu)
{
  uint32_t i;
  struct tag *tag;

  cu__for_each_type(cu, i, tag) {
    emit_tag(tag, i, cu, true);
  }

  return 0;
}

static enum load_steal_kind vmlinux_stealer(struct cu *cu,
             struct conf_load *conf_load __maybe_unused,
             void *thr_data __maybe_unused)
{
  cu__emit_tags_vmlinux(cu);
  return LSK__DELETE;
}

struct conf_load vmlinux_conf_load = {
  .steal = vmlinux_stealer,
  .conf_fprintf = &conf,
};

int main(int argc, char **argv)
{
  struct cus *cus = NULL;
  const char *fips_obj_path;
  const char *vmlinux_path;
  const char *vmlinux_dir;

  if (argc < 4) {
    pr_err("Usage: Please provide all 3 arguments:\n"
      "1. fips_canister.o path\n"
      "2. vmlinux path\n"
      "3. Path to dir holding known vmlinux definitions\n"
    );
    return -1;
  }

  fips_obj_path = argv[1];
  vmlinux_path = argv[2];
  vmlinux_dir = argv[3];

  strncpy(knwn_vmlinux_def_dir, vmlinux_dir, sizeof(knwn_vmlinux_def_dir));

  cus = cus__new();

  /* Read canister first */
  if (dwarves__init() || cus == NULL) {
    fputs("insufficient memory\n", stderr);
    goto finish;
  }

  dwarves__resolve_cacheline_size(&fips_conf_load, 0);

  if (cus__load_file(cus, &fips_conf_load, fips_obj_path) != 0) {
    rc = -1;
    goto finish;
  }

  /* To be safe, start fresh when processing vmlinux */
  cus__delete(cus);
  dwarves__exit();

  /* Compare vmlinux structs to saved canister definitions */
  cus = cus__new();
  if (dwarves__init() || cus == NULL) {
    fputs("insufficient memory\n", stderr);
    goto finish;
  }

  dwarves__resolve_cacheline_size(&vmlinux_conf_load, 0);

  if (cus__load_file(cus, &vmlinux_conf_load, vmlinux_path) != 0)
    rc = -1;

finish:
  /* Free fips list */
  free_struct_def_list(&fips_head);

  cus__delete(cus);
  dwarves__exit();

  if (!rc) {
    pr_info("PASS: Struct comparison done\n");
  } else {
    pr_err("FAIL: Struct comparison did not go as expected\n");
  }

  return rc;
}
