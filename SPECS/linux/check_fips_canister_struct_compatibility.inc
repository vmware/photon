# Find structure symbols in fips_canister.o
echo "Extracting symbols from fips_canister.o"
gdb crypto/fips_canister.o -q -ex="set pagination off" -ex="info types" -ex q | tail -n +2 > fips_canister_symbols

echo "Filtering structure and union symbols"
while read line; do
      if [[ $line =~ ^[0-9]*:[[:space:]]*.*struct|union ]]; then
           if [[ $line =~ .*"typedef".* ]]; then
              echo $line | awk '{print "ptype "$NF}' | sed -r 's/;+$//' >> fips-canister-symbols-gdbcmds
          else
             echo $line | awk '{print "ptype "$(NF-1),"\t",$NF}' | sed -r 's/;+$//' >> fips-canister-symbols-gdbcmds
          fi
      fi
done <fips_canister_symbols

awk -i inplace '!seen[$0]++' fips-canister-symbols-gdbcmds

sed -i '/struct/!d' fips-canister-symbols-gdbcmds

ignore_list='void \*module;\|struct module \*module;\|raw_spinlock_t lock;\|void \*lock;\|void \*drbg_mutex;\|struct mutex drbg_mutex;\|void \*cra_type;\|const struct crypto_type \*cra_type;\|void \*cra_module;\|struct module \*cra_module;'

echo "Comparing the symbols between canister and vmlinux"
gdb crypto/fips_canister.o -q -ex="set pagination off" -x fips-canister-symbols-gdbcmds -ex q | tail -n +2 > symbols-canister
gdb vmlinux -q -ex="set pagination off" -x fips-canister-symbols-gdbcmds -ex q | tail -n +2 > symbols-vmlinux
diff symbols-canister symbols-vmlinux -I "$ignore_list"
if [[ $? == 1 ]];then
    echo "symbol mismatch between vmlinux and fips_canister.o"
    echo "Inspect diff between symbols-canister and symbols-vmlinux file"
    exit 1
fi
rm fips_canister_symbols fips-canister-symbols-gdbcmds symbols-canister symbols-vmlinux
