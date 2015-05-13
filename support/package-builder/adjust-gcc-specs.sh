#! /bin/bash

if [ $# -eq 1 -a "x$1" = "xclean" ]; then
    rm -f `dirname $(gcc --print-libgcc-file-name)`/../specs
    exit 0
fi

cat <<EOF > `dirname $(gcc --print-libgcc-file-name)`/../specs
*cc1:
+ %{!fno-stack-protector:-fstack-protector} %{fno-pie|fno-PIE|fpic|fPIC|shared:;:-fPIE -fpie}

*cc1plus:
+ %{!fno-stack-protector:-fstack-protector} %{fno-pie|fno-PIE|fpic|fPIC|shared:;:-fPIE -fpie}

*cpp:
+ %{O1|O2|O3|Os|Ofast:-D_FORTIFY_SOURCE=2}

*link:
+ %{r|fno-pie|fno-PIE|fpic|fPIC|fno-pic|fno-PIC|shared:;:-pie} %{!norelro:-z relro} %{!nonow:-z now}

*libgcc:
+ -lgcc_s

*startfile:
%{!mandroid|tno-android-ld:%{!shared: %{pg|p|profile:gcrt1.o%s;:Scrt1.o%s}}    crti.o%s %{static:crtbeginT.o%s;:crtbeginS.o%s};:%{shared: crtbegin_so%O%s;:  %{static: crtbegin_static%O%s;: crtbegin_dynamic%O%s}}}

EOF
