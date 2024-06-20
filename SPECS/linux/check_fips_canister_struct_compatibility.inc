vmlinux="vmlinux"
GDB="/usr/bin/gdb"
gdb_cmds="gdb_commands.gdb"
tmp_fn="/tmp/structure-symbols"
canister_obj="crypto/fips_canister.o"
sym_vmlinux_fn="/tmp/symbol-vmlinux"
sym_canister_fn="/tmp/symbol-canister"
canister_syms_fn="/tmp/fips_canister_structure_symbols"

# Find structure symbols in fips_canister.o
echo "Extracting symbols from ${canister_obj} ..."
${GDB} ${canister_obj} -q -ex="set pagination off" \
  -ex="info types" -ex q | \
  tail -n +2 > ${canister_syms_fn}

echo "Filtering structure and union symbols ..."
# get lines starting with number, having struct|union keyword followed by valid C variable name
sed -n 's/^[0-9]\+:.*\(\bstruct\b\|\bunion\b\)[[:space:]]\+\([a-zA-Z0-9_]\+\)\b.*/\1 \2/p' ${canister_syms_fn} > ${tmp_fn}

# remove dups and preserve order
# prepend 'ptype struct' to each line
awk '!seen[$0]++ {print "ptype " $0}' ${tmp_fn} > ${gdb_cmds}

# gdb doesn't exit with non zero error status if the script is wrong
# so ensure that stderr file is empty
err_fn="/tmp/gdb.err.log"

${GDB} ${canister_obj} -q -ex="set pagination off" -x ${gdb_cmds} -ex q 2>${err_fn} | tail -n +2 \
  >${sym_canister_fn}

[ -s ${err_fn} ] && exit 1

${GDB} ${vmlinux} -q -ex="set pagination off" -x ${gdb_cmds} -ex q 2>${err_fn} | tail -n +2 \
  >${sym_vmlinux_fn}

[ -s ${err_fn} ] && exit 1

ignore_list='void \*module;\|struct module \*module;\|raw_spinlock_t lock;\|void \*lock;\|void \*drbg_mutex;\|struct mutex drbg_mutex;\|void \*cra_type;\|const struct crypto_type \*cra_type;\|void \*cra_module;\|struct module \*cra_module;'

echo "Comparing the symbols between canister and vmlinux ..."
if ! diff ${sym_canister_fn} ${sym_vmlinux_fn} -I "${ignore_list}"; then
  echo "ERROR: Mismatch between ${vmlinux} and ${canister_obj} symbols ..." 1>&2
  echo "Inspect diff between ${sym_canister_fn} and ${sym_vmlinux_fn} file ..." 1>&2
  exit 1
fi

rm ${canister_syms_fn} \
   ${tmp_fn} ${gdb_cmds} \
   ${sym_canister_fn} \
   ${sym_vmlinux_fn} \
   ${err_fn}
