#! /bin/bash

echo "Using options:" $@

if [ $# -eq 1 -a "x$1" = "xnone" ]; then
    rm -f `dirname $(gcc --print-libgcc-file-name)`/../specs
    exit 0
fi

cat <<EOF > `dirname $(gcc --print-libgcc-file-name)`/../specs
# add sec hardening flags for cc1.
*cc1:
+ %{!fno-stack-protector-strong:-fstack-protector-strong} %{fno-pie|fno-PIE|fpic|fPIC|shared:;:-fPIE -fpie}

# add sec hardening flags for cc1.
*cc1plus:
+ %{!fno-stack-protector-strong:-fstack-protector-strong} %{fno-pie|fno-PIE|fpic|fPIC|shared:;:-fPIE -fpie}

# add -D_FORTIFY_SOURCE=2 for preprocessor.
*cpp:
+ %{O1|O2|O3|Os|Ofast:-D_FORTIFY_SOURCE=2}

# sec hardening flags require shared libgcc_s during linking.
*libgcc:
+ %{!static:--as-needed -lgcc_s --no-as-needed}

# replace default startfile rules to use crt that PIE code requires.
*startfile:
%{!shared: %{pg|p|profile:gcrt1.o%s;:Scrt1.o%s}}    crti.o%s %{static:crtbeginT.o%s;:crtbeginS.o%s}

EOF

if [ $# -eq 1 -a "x$1" = "xnonow" ]; then
cat <<EOF >> `dirname $(gcc --print-libgcc-file-name)`/../specs
# add sec hardening flags for linker.
*link:
+ %{r|nostdlib|fno-pie|fno-PIE|fno-pic|fno-PIC|shared:;:-pie} %{!norelro:-z relro}

EOF
else
cat <<EOF >> `dirname $(gcc --print-libgcc-file-name)`/../specs
# add sec hardening flags for linker.
*link:
+ %{r|nostdlib|fno-pie|fno-PIE|fno-pic|fno-PIC|shared|static:;:-pie} %{!norelro:-z relro} %{!nonow:-z now}

EOF
fi



