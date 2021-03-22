# Find structure symbols in fips_canister.o
gdb crypto/fips_canister.o -q -ex="set pagination off" -ex="info variables -q -t struct" -ex q | tail -n +2 > fips_canister_structure_symbols

# Loop through the symbols and extract structure name
while read line; do
      if [[ $line =~ ^[0-9]*: ]]; then
         echo $line | sed -n -e 's/.*struct //p' | awk '{print $1}' >> structure-symbols
      fi
done <fips_canister_structure_symbols

awk '!seen[$0]++' structure-symbols > fips-structure-symbols

# Loop through the symbols and compare with vmlinux
while read symbol; do
         if [[ $symbol == "simd_aead_alg" || $symbol == "simd_skcipher_alg" ]]; then
            continue
         fi
         symbol_name="struct ${symbol}"
         if [[ $symbol_name =~ ^[a-zA-Z] ]]; then
            gdb crypto/fips_canister.o -q -ex="set pagination off" -ex="ptype $symbol_name" -ex q | tail -n +2 > symbol-canister
            gdb vmlinux -q -ex="set pagination off" -ex="ptype $symbol_name" -ex q | tail -n +2 > symbol-vmlinux
            diff symbol-canister symbol-vmlinux
            if [[ $? == 1 ]];then
               echo "$symbol_name does not match in vmlinux"
               exit 1
            fi
         fi
done <fips-structure-symbols
rm fips_canister_structure_symbols structure-symbols fips-structure-symbols symbol-canister symbol-vmlinux
