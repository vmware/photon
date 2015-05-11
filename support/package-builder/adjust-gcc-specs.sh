#! /bin/bash

if [ $# -eq 1 -a $1 = "clean" ]; then
    rm -f `dirname $(/usr/bin/gcc --print-libgcc-file-name)`/specs
    exit 0
fi

cat <<EOF > `dirname $(/usr/bin/gcc --print-libgcc-file-name)`/specs
*cc1:
+ %{!fno-stack-protector:-fstack-protector} %{fno-pie|fno-PIE|fpic|fPIC|shared:;:-fPIE} 

*cc1plus:
+ %{!fno-stack-protector:-fstack-protector} %{fno-pie|fno-PIE|fpic|fPIC|shared:;:-fPIE} 

*cpp:
+ %{O1|O2|O3|Os|Ofast:-D_FORTIFY_SOURCE=2}

*link:
+ %{!norelro:-z relro} %{!nonow:-z now}

*libgcc:
+ -lgcc_s
EOF
