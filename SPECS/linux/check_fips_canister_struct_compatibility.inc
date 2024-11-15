vmlinux="vmlinux"
GDB="/usr/bin/gdb"
gdb_cmds="gdb_commands.gdb"
tmp_fn="/tmp/structure-symbols"
canister_obj="crypto/fips_canister.o"
sym_vmlinux_fn="/tmp/symbol-vmlinux"
sym_canister_fn="/tmp/symbol-canister"
canister_syms_fn="/tmp/fips_canister_structure_symbols"
knwn_struct_diff="canister_known_struct_diff_list"
knwn_struct_def_vmlinux="canister_known_struct_def_vmlinux"
knwn_struct_gdb_cmds="knwn_struct_gdb_commands.gdb"
sym_vmlinux_fn_knwn="/tmp/symbol-vmlinux-knwn"

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
awk '!seen[$0]++ {print "ptype/o " $0}' ${tmp_fn} > ${gdb_cmds}

echo "Removing known structure differences from gdb command list ..."
# remove list of known structure differences
while read -r LINE
do
   sed -i "/${LINE}/d" ${gdb_cmds}
done < ${knwn_struct_diff}

# prepend ptype to known structure difference list
awk '{print "ptype/o "$0}' ${knwn_struct_diff} > ${knwn_struct_gdb_cmds}

# gdb doesn't exit with non zero error status if the script is wrong
# so ensure that stderr file is empty
err_fn="/tmp/gdb.err.log"

#  List and compare the known structures that are different
${GDB} ${vmlinux} -q -ex="set pagination off" -x "${knwn_struct_gdb_cmds}" -ex q 2>${err_fn} | tail -n +2 \
  >${sym_vmlinux_fn_knwn}

[ -s ${err_fn} ] && exit 1

echo "Comparing list of known structures that are different ..."
if ! diff ${sym_vmlinux_fn_knwn} ${knwn_struct_def_vmlinux}; then
   echo "ERROR: Symbol mismatch for the known structure symbols ..." 1>&2
   echo "Inspect diff between ${sym_vmlinux_fn_knwn} and ${knwn_struct_def_vmlinux} file ..." 1>&2
   exit 1
fi

# List and compare other symbols between vmlinux and canister
${GDB} ${canister_obj} -q -ex="set pagination off" -x ${gdb_cmds} -ex q 2>${err_fn} | tail -n +2 \
  >${sym_canister_fn}

[ -s ${err_fn} ] && exit 1

${GDB} ${vmlinux} -q -ex="set pagination off" -x ${gdb_cmds} -ex q 2>${err_fn} | tail -n +2 \
  >${sym_vmlinux_fn}

[ -s ${err_fn} ] && exit 1

# Structures that are different between canister and vmlinux only by names. Size and offset are same.
ignore_list='void \*module;\|struct module \*module;\|void \*cra_type;\|const struct crypto_type \*cra_type;\|void \*cra_module;\|struct module \*cra_module;'

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
   ${knwn_struct_gdb_cmds} \
   ${sym_vmlinux_fn_knwn} \
   ${err_fn}
