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

ignore_list='void \*module;\|struct module \*module;\|raw_spinlock_t lock;\|void \*lock;\|void \*drbg_mutex;\|struct mutex drbg_mutex;\|void \*cra_type;\|const struct crypto_type \*cra_type;\|void \*cra_module;\|struct module \*cra_module;'

#
## Loop through the symbols and compare with vmlinux
echo "Comparing the symbols between canister and vmlinux"
while read symbol; do
     if [[ ${symbol} == *"struct"* ]]; then
        gdb crypto/fips_canister.o -q -ex="set pagination off" -ex="$symbol" -ex q | tail -n +2 > symbol-canister
        gdb vmlinux -q -ex="set pagination off" -ex="$symbol" -ex q | tail -n +2 > symbol-vmlinux
        diff symbol-canister symbol-vmlinux -I "$ignore_list"
        if [[ $? == 1 ]];then
           echo "$symbol does not match in vmlinux"
           exit 1
        fi
     fi
done <fips-canister-symbols-gdbcmds
rm fips_canister_symbols fips-canister-symbols-gdbcmds symbol-canister symbol-vmlinux
