# One spec for every 5.0 subrelease: kernel 6.1 up to photon_subrelease 90,
# kernel 6.12 from 91. The per-kernel preamble and changelog are included
# below; sections that differ carry photon_subrelease conditionals.

# acvp_build and kat_build are x86_64-only: the canister they certify is
# arch/x86 crypto and the only ACVP config is config_x86_64_acvp. Refuse them
# on any other architecture instead of building with x86_64 inputs.
%ifnarch x86_64
%if 0%{?acvp_build} || 0%{?kat_build}
%{error:acvp_build and kat_build are x86_64-only; refusing to build for %{_target_cpu}}
%endif
%endif

Summary:        Kernel
Name:           linux
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%if 0%{?photon_subrelease} <= 90
Version:        6.1.183
%else
Version:        6.12.109
%endif
Source0:        http://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz

Source990:      linux-6.1.inc
Source991:      linux-6.12.inc
Source992:      linux-6.1-changelog.inc
Source993:      linux-6.12-changelog.inc
Source994:      linux-6.1-packages.inc
Source995:      linux-6.12-packages.inc

%if 0%{?photon_subrelease} <= 90
%include %{SOURCE990}
%else
%include %{SOURCE991}
%endif

BuildRequires:  bc
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  elfutils-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  audit-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  binutils-devel
BuildRequires:  xz-devel
BuildRequires:  slang-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  cmake
BuildRequires:  bison
BuildRequires:  dwarves-devel
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
Requires: kmod
Requires: filesystem
Obsoletes:  linux-aws
Obsoletes:  linux-secure
Provides:   linux-secure

%description
The Linux package contains the Linux kernel.
# Enable post FIPS certification
%if 0
This kernel is FIPS certified.
%endif

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%if 0%{?photon_subrelease} <= 90
Requires:       python3
Requires:       gawk
%else
Requires:       python3 gawk dwarves-devel
%endif
%description devel
The Linux package contains the Linux kernel dev files

%package drivers-gpu
Summary:        Kernel GPU Drivers
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package drivers-sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
Requires:       %{name} = %{version}-%{release}
%description docs
The Linux package contains the Linux kernel doc files

%if 0%{?photon_subrelease} <= 90
%include %{SOURCE994}
%else
%include %{SOURCE995}
%endif

%if 0%{?canister_build}
%package fips-canister
Summary:       FIPS canister tarball
Group:         System Environment/Kernel
%if 0%{?photon_subrelease} <= 90
Requires:      python3
Requires:      %{name} = %{version}-%{release}
%endif
%description fips-canister
The kernel fips-canister
%endif

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 3 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 4 -n linux-%{version}

%if 0%{?photon_subrelease} <= 90
%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 32 -n linux-%{version}
%endif

%endif
# Apply CVE patches first
%autopatch -p1 -m3000 -M3999

# common
%autopatch -p1 -m0 -M49
%if 0%{?photon_subrelease} <= 90

# apparmor
%autopatch -p1 -m100 -M100

# seccomp
%autopatch -p1 -m101 -M101
%endif

%ifarch x86_64
# VMW x86
%autopatch -p1 -m50 -M60
%endif

#Secure
%autopatch -p1 -m61 -M63

%if 0%{?photon_subrelease} <= 90
%ifarch aarch64
# aarch64 patches
%autopatch -p1 -m250 -M260
%endif

%ifarch x86_64
# AWS x86
%autopatch -p1 -m300 -M339
%endif

# crypto
%autopatch -p1 -m500 -M504

%ifarch x86_64
%autopatch -p1 -m505 -M507
%endif

%if 0%{?fips}
%autopatch -p1 -m508 -M512
%endif

%if 0%{?acvp_build:1}
#ACVP test harness patches.
#Need to be applied on top of FIPS canister usage patch to avoid HUNK failure
%autopatch -p1 -m513 -M524
%if 0%{?kat_build:1}
%autopatch -p1 -m525 -M525
%endif
%endif

%ifarch x86_64
# SEV on VMware
%autopatch -p1 -m600 -M609
%endif

#HCX-Patches
%autopatch -p1 -m701 -M719

# Report guest crash to vmware hypervisor
%autopatch -p1 -m1000 -M1001

# perf: off-cpu sample
%autopatch -p1 -m221 -M223

# Patches for efa driver
pushd ../amzn-drivers-efa_linux_%{efa_version}
%autopatch -p1 -m1400 -M1409
popd

%if 0%{?canister_build}
%autopatch -p1 -m10000 -M10013

%if 0%{?kat_build}
%autopatch -p1 -m10014 -M10014
%endif
%endif

%ifarch x86_64
cp -r ../jitterentropy-%{jent_major_version}-%{jent_ph_version}/ \
      crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE33} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE34} crypto/jitterentropy-%{jent_major_version}/
cp %{SOURCE35} crypto/jitterentropy-%{jent_major_version}/
%endif

%make_build mrproper
cp %{SOURCE1} .config

cat %{SOURCE20} %{SOURCE21} > photon-cert-bundle.pem
%ifarch x86_64
%if 0%{?fips}
cp %{SOURCE36} \
   %{SOURCE37} \
   %{SOURCE38} \
   %{SOURCE39} \
   %{SOURCE40} \
   %{SOURCE41} \
   %{SOURCE51} \
   crypto/

cp ../fips-canister-%{fips_canister_version}/fips_canister.o \
   ../fips-canister-%{fips_canister_version}/.fips_canister.o.cmd \
   ../fips-canister-%{fips_canister_version}/fips_canister-kallsyms \
   crypto/

mkdir -p %{struct_comp_dir}/%{vmlinux_definition_loc}
cp %{SOURCE9}  %{struct_comp_dir}
cp %{SOURCE75} \
   %{SOURCE76} \
   %{SOURCE77} \
   %{SOURCE78} \
   %{SOURCE79} \
   %{struct_comp_dir}/%{vmlinux_definition_loc}
%endif

%if 0%{?canister_build}
cp %{SOURCE38} \
   %{SOURCE39} \
   %{SOURCE43} \
   %{SOURCE44} \
   %{SOURCE45} \
   %{SOURCE46} \
   %{SOURCE48} \
   %{SOURCE49} \
   crypto/
install -m 755 %{SOURCE47} crypto/
%endif
%endif

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config

%if 0%{?canister_build}
sed -i "0,/FIPS_CANISTER_VERSION.*$/s/FIPS_CANISTER_VERSION.*$/FIPS_CANISTER_VERSION \"%{lkcm_version}\"/" crypto/fips_integrity.c
sed -i "0,/FIPS_KERNEL_VERSION.*$/s/FIPS_KERNEL_VERSION.*$/FIPS_KERNEL_VERSION \"%{version}-%{release}\"/" crypto/fips_integrity.c

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_TAMPER_TEST=y' .config
%endif
%endif

%ifarch x86_64
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@LINUX_PH_GEN@@,%{linux_photon_generation},g" \
    %{SOURCE25} > linux-sbat.csv
%endif

%if 0%{?acvp_build}
cp %{SOURCE53} .config_acvp
%include %{SOURCE54}
%else
%include %{SOURCE7}
%endif

# Set/add CONFIG_CROSS_COMPILE= if needed
if [ %{_host} != %{_build} ]; then
grep -q CONFIG_CROSS_COMPILE= .config && sed -i '/^CONFIG_CROSS_COMPILE=/c\CONFIG_CROSS_COMPILE="%{_host}-"' .config || \
  echo 'CONFIG_CROSS_COMPILE="%{_host}-"' >> .config
fi

%else
# vmxnet3
%autopatch -p1 -m65 -M66

# Backward compatibility
%if "%{dist}" == ".ph5"
%autopatch -p1 -m71 -M71
%endif

%ifarch aarch64
# aarch64 patches
%autopatch -p1 -m200 -M219
%endif

%autopatch -p1 -m221 -M248

%ifarch x86_64
# AWS x86
%autopatch -p1 -m300 -M339
%endif

%autopatch -p1 -m701 -M715

# Patches for efa driver
pushd ../amzn-drivers-efa_linux_%{efa_version}
%autopatch -p1 -m1400 -M1400
popd

# Jitterentropy support and FIPS compliance
%autopatch -p1 -m10000 -M10000

# prep for viomem out-of-tree module
mkdir -p ../viomem
pushd ../viomem
cp %{SOURCE30} Makefile
cp %{SOURCE31} .
popd

%if 0%{?fips}

# Using autosetup is not feasible
%setup -q -T -D -b 10000 -n linux-%{version}

cp -rf ../%{jent_name}/ crypto/
rm crypto/jitterentropy-kcapi.c
mv crypto/%{jent_name}/jitterentropy-kcapi.c crypto/jitterentropy-kcapi.c
cp %{SOURCE10001} crypto/%{jent_name}/
cp %{SOURCE10002} crypto/%{jent_name}/
cp %{SOURCE10003} crypto/%{jent_name}/

install %{SOURCE10101} crypto/
install %{SOURCE10102} crypto/
install %{SOURCE10104} crypto/
install %{SOURCE10105} crypto/
install %{SOURCE10106} crypto/
install %{SOURCE10300} crypto/

%autopatch -p1 -m10001 -M10004
%autopatch -p1 -m10101 -M10118
# FIPS canister plugins
%autopatch -p1 -m10200 -M10204
# Jitterentropy proxy
%autopatch -p1 -m10300 -M10301
%endif

# Clean the build tree. It must be done before copying the canister.
%make_build mrproper

%if 0%{?canister_usage}
tar -xvf /usr/lib/fips-canister/fips-canister-%{fips_canister_version}.tar.bz2
# fips_canister.o is mentioned in obj-y. So, Makefile.modpost expects
# corresponding .cmd file. Empty content is ok, since we are not going
# to rebuild it.
touch crypto/.fips_canister.o.cmd
%endif

%if 0%{?canister_build}
%autopatch -p1 -m11000 -M11017
cp %{SOURCE11000} crypto/
cp %{SOURCE11001} crypto/
cp %{SOURCE11002} crypto/
install -m 755 %{SOURCE11003} crypto/
cp %{SOURCE11004} crypto/
cp %{SOURCE11005} crypto/
sed -i "0,/FIPS_CANISTER_VERSION.*$/s/FIPS_CANISTER_VERSION.*$/FIPS_CANISTER_VERSION \"%{lkcm_version}\"/" crypto/fips_integrity.c
sed -i "0,/FIPS_KERNEL_VERSION.*$/s/FIPS_KERNEL_VERSION.*$/FIPS_KERNEL_VERSION \"%{fips_certified_kernel_version}\"/" crypto/fips_integrity.c
%endif

%if 0%{?acvp_build:1}
# ACVP test harness patches.
%autopatch -p1 -m12000 -M12012
%endif

%if 0%{?kat_build:1}
%autopatch -p1 -m12013 -M12014
%endif

cp %{SOURCE1} .config

cat %{SOURCE20} %{SOURCE21} > photon-cert-bundle.pem

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config

%if 0%{?photon_subrelease} >= 92
# Update toolchain config for gcc 12.5.0 and binutils 2.46.1
sed -i 's/CONFIG_CC_VERSION_TEXT="gcc (GCC) 12.2.0"/CONFIG_CC_VERSION_TEXT="gcc (GCC) 12.5.0"/' .config
sed -i 's/CONFIG_GCC_VERSION=120200/CONFIG_GCC_VERSION=120500/' .config
sed -i 's/CONFIG_AS_VERSION=23900/CONFIG_AS_VERSION=24601/' .config
sed -i 's/CONFIG_LD_VERSION=23900/CONFIG_LD_VERSION=24601/' .config
sed -i 's/CONFIG_GCC_ASM_GOTO_OUTPUT_BROKEN=y/CONFIG_CC_HAS_ASM_GOTO_OUTPUT=y\nCONFIG_CC_HAS_ASM_GOTO_TIED_OUTPUT=y/' .config
%endif

%include %{SOURCE5}

%ifarch x86_64
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@LINUX_PH_GEN@@,%{linux_photon_generation},g" \
    %{SOURCE25} > linux-sbat.csv
%endif

%if 0%{?acvp_build}
cp %{SOURCE12000} .config_acvp
%include %{SOURCE12001}
%else
%include %{SOURCE7}
%endif

# Set/add CONFIG_CROSS_COMPILE= if needed
if [ %{_host} != %{_build} ]; then
grep -q CONFIG_CROSS_COMPILE= .config && sed -i '/^CONFIG_CROSS_COMPILE=/c\CONFIG_CROSS_COMPILE="%{_host}-"' .config || \
  echo 'CONFIG_CROSS_COMPILE="%{_host}-"' >> .config
fi

%endif
%build
%if 0%{?photon_subrelease} <= 90
%make_build \
  KBUILD_BUILD_VERSION="1-photon" \
  KBUILD_BUILD_HOST="photon" \
  ARCH=%{arch}
%else
%make_build KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH=%{arch}
%endif

bldroot="${PWD}"

%if 0%{?photon_subrelease} <= 90
%if 0%{?fips}
# compare struct definitions between fips canister and vmlinux
# fails out if there is a mismatch, and the offending definition
# has not been documented in %{vmlinux_definition_loc}
pushd %{struct_comp_dir}
gcc -Wall -Werror -o %{struct_comparator} %{SOURCE9} -ldwarves
./%{struct_comparator} \
  ${bldroot}/crypto/fips_canister.o ${bldroot}/vmlinux %{vmlinux_definition_loc}
popd

rm -rf %{struct_comp_dir}
%endif

# build ENA module
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
cp configure.sh ena-conf.sh
./ena-conf.sh --kernel-dir "${bldroot}"
%make_build -C ${bldroot} M="${PWD}" V=1 modules
%else
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=deprecated-declarations"

%make_build ARCH=%{arch} -C tools \
        PYTHON=python3 $ARCH_FLAGS \
        perf

ARCH_FLAGS+=" EXTRA_CFLAGS+=-DHAVE_LIBBPF_SUPPORT"
ARCH_FLAGS+=" EXTRA_CFLAGS+=-DBUILD_BPF_SKEL"

%make_build ARCH=%{arch} -C tools \
        PYTHON=python3 $ARCH_FLAGS \
        bpf

# Verify perf has no dependency on libunwind
tools/perf/perf -vv | grep libunwind | grep OFF
tools/perf/perf -vv | grep dwarf | grep on

%ifarch x86_64
# Build turbostat and cpupower
%make_build ARCH=%{arch} -C tools \
    PYTHON=python3 \
    turbostat cpupower
%endif

# build ENA module
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
cp configure.sh ena-conf.sh
./ena-conf.sh --kernel-dir ${bldroot}
%make_build -C ${bldroot} M="${PWD}" modules
%endif
popd

# build EFA module
pushd ../amzn-drivers-efa_linux_%{efa_version}/kernel/linux/efa
%if 0%{?photon_subrelease} <= 90
mkdir -p build
cd build
%cmake -DKERNEL_DIR=${bldroot} ..
%cmake_build
%else
mkdir -p build && cd build
%{cmake} -DKERNEL_DIR=${bldroot} ..
%{cmake_build}
%endif
popd

%if 0%{?photon_subrelease} <= 90
%ifarch x86_64
# build viomem module
mkdir ../viomem
pushd ../viomem
cp %{SOURCE100} Makefile
cp %{SOURCE101} .
cd ../viomem
%make_build -C ${bldroot} M="${PWD}" V=1 modules
popd
%endif

%if 0%{?canister_build}
%include %{SOURCE50}
%endif

%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif
ARCH_FLAGS="${ARCH_FLAGS} EXTRA_CFLAGS=-Wno-error=deprecated-declarations"

%make_build ARCH=%{arch} -C tools perf PYTHON=python3 $ARCH_FLAGS

tools/perf/perf -vv | grep libunwind | grep OFF
tools/perf/perf -vv | grep dwarf | grep on

%ifarch x86_64
%make_build ARCH=%{arch} -C tools turbostat cpupower PYTHON=python3
%endif

%make_build install -C tools/bpf/bpftool prefix=%{_prefix}

%else
# build viomem module
pushd ../viomem
%make_build -C ${bldroot} M="${PWD}" modules
popd

%if 0%{?canister_build}
%include %{SOURCE11500}
%endif

%endif
%if 0%{?photon_subrelease} <= 90
%install
%if 0%{?canister_build}
install -vdm 755 %{buildroot}%{_libdir}/fips-canister/
pushd crypto/
mkdir fips-canister-%{lkcm_version}-%{version}-%{release}
cp fips_canister.o \
   fips_canister-kallsyms \
   .fips_canister.o.cmd \
   fips-canister-%{lkcm_version}-%{version}-%{release}/
tar -cvjf fips-canister-%{lkcm_version}-%{version}-%{release}.tar.bz2 fips-canister-%{lkcm_version}-%{version}-%{release}/
popd
cp crypto/fips-canister-%{lkcm_version}-%{version}-%{release}.tar.bz2 %{buildroot}%{_libdir}/fips-canister/
%endif
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
%make_build ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install

# install ENA module
bldroot="${PWD}"
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
%make_build -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# install EFA module
bldroot="${PWD}"
pushd ../amzn-drivers-efa_linux_%{efa_version}/kernel/linux/efa/build/src
%make_build -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} modules_install
popd

%ifarch x86_64
# install viomem module
pushd ../viomem
%make_build -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} modules_install
popd
%endif

%ifarch x86_64
# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=$(readelf -n vmlinux | grep "Build ID")
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=$(readelf -n extracted-vmlinux | grep "Build ID")
if [ "$ID1" != "$ID2" ] ; then
  echo "Build IDs do not match"
  echo $ID1
  echo $ID2
  exit 1
fi

install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
%if "%{?signing_script}" != ""
%{signing_script} --file_type pe \
      --config_file %{signing_params} \
      --auth_file %{signing_auth} \
      --artifact %{buildroot}/boot/vmlinuz-%{uname_r}
%endif
%endif

%ifarch aarch64
install -vm 644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux
%endif

cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet loadpin.enabled=0 audit=1 slab_nomerge
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}%{_localstatedir}/lib/initramfs/kernel

# Cleanup dangling symlinks
rm -rf %{buildroot}%{_modulesdir}/source \
       %{buildroot}%{_modulesdir}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE19} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif
ARCH_FLAGS="${ARCH_FLAGS} EXTRA_CFLAGS=-Wno-error=deprecated-declarations"

%make_build -C tools ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} perf_install PYTHON=python3 $ARCH_FLAGS

%make_build -C tools/perf ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} PYTHON=python3 install-python_ext

%ifarch x86_64
%make_build -C tools ARCH=%{arch} DESTDIR=%{buildroot} \
      prefix=%{_prefix} mandir=%{_mandir} turbostat_install cpupower_install PYTHON=python3
%endif

%make_build install -C tools/bpf/bpftool \
      prefix=%{_prefix} DESTDIR=%{buildroot}

%include %{SOURCE2}
%include %{SOURCE6}
%include %{SOURCE18}

%else
%install
%if 0%{?canister_build}
install -vdm 755 %{buildroot}%{_libdir}/fips-canister/
tar -cvjf %{buildroot}%{_libdir}/fips-canister/fips-canister-%{version}-%{release}.tar.bz2 \
   crypto/fips_canister.o \
   crypto/fips_canister-kallsyms
%endif

install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}

%make_build ARCH=%{arch} \
    INSTALL_MOD_PATH=%{buildroot} \
    modules_install

# install ENA module
bldroot="${PWD}"
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
%make_build -C ${bldroot} M="${PWD}" \
    INSTALL_MOD_PATH=%{buildroot} \
    modules_install
popd

# install EFA module
bldroot="${PWD}"
pushd ../amzn-drivers-efa_linux_%{efa_version}/kernel/linux/efa/build/src
%make_build -C ${bldroot} M="${PWD}" \
    INSTALL_MOD_PATH=%{buildroot} \
    modules_install
popd

# install viomem module
pushd ../viomem
%make_build -C ${bldroot} M="${PWD}" \
    INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra \
    modules_install
popd

%ifarch x86_64
# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=$(readelf -n vmlinux | grep "Build ID")
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=$(readelf -n extracted-vmlinux | grep "Build ID")
if [ "$ID1" != "$ID2" ] ; then
  echo "ERROR: Build IDs do not match" >&2
  echo "ID1: $ID1"
  echo "ID2: $ID2"
  exit 1
fi
install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
%if "%{?signing_script}" != ""
%{signing_script} --file_type pe \
      --config_file %{signing_params} \
      --auth_file %{signing_auth} \
      --artifact %{buildroot}/boot/vmlinuz-%{uname_r}
%endif
%endif

%ifarch aarch64
install -vm 644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?_enable_debug_packages}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -sv vmlinux-%{uname_r} %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux
%endif

cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet loadpin.enabled=0 audit=1 slab_nomerge
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}%{_sharedstatedir}/initramfs/kernel

# Cleanup dangling symlinks
rm -f %{buildroot}%{_modulesdir}/source \
      %{buildroot}%{_modulesdir}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | \
      xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/%{archdir}/include include scripts -type f | \
      xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | \
      xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/%{archdir}/include Module.symvers include scripts -type f | \
      xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/{objtool,fixdep} \
                 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%endif

# copy .config manually to be where it's expected to be
cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}

ln -sfv "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"

find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%ifarch aarch64
ARCH_FLAGS="EXTRA_CFLAGS=-Wno-error=format-overflow"
%endif

%make_build -C tools ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} $ARCH_FLAGS \
     PYTHON=python3 \
     perf_install

%make_build -C tools/perf ARCH=%{arch} DESTDIR=%{buildroot} \
     prefix=%{_prefix} PYTHON=python3 \
     install-python_ext

%ifarch x86_64
%make_build -C tools ARCH=%{arch} DESTDIR=%{buildroot} \
      prefix=%{_prefix} mandir=%{_mandir} \
      PYTHON=python3 \
      turbostat_install cpupower_install
%endif

%make_install %{?_smp_mflags} -C tools/bpf prefix=%{_prefix}

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE19} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE6}
%include %{SOURCE18}

%endif
%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post drivers-sound
/sbin/depmod -a %{uname_r}

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build
%exclude %{_modulesdir}/kernel/drivers/gpu
%exclude %{_modulesdir}/kernel/sound
%if 0%{?photon_subrelease} >= 91
%exclude %{_includedir}/powercap.h
%endif
%ifarch aarch64
%exclude %{_modulesdir}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_docdir}/linux-%{uname_r}/*
%if 0%{?photon_subrelease} >= 91
%ifarch x86_64
%{_mandir}/*
%endif
%endif

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%{_modulesdir}/kernel/drivers/gpu

%files drivers-sound
%defattr(-,root,root)
%{_modulesdir}/kernel/sound
%ifarch aarch64
%{_modulesdir}/kernel/drivers/staging/vc04_services/bcm2835-audio
%endif

%files tools
%defattr(-,root,root)
%if 0%{?photon_subrelease} <= 90
%ifarch x86_64
%exclude %{_lib64}/traceevent
%endif
%endif
%ifarch aarch64
%exclude %{_libdir}/traceevent
%endif
%{_bindir}/*
%if 0%{?photon_subrelease} >= 91
# exclude bpf_jit_disasm due to binutils-libs dependency
# 91, 92 differ in binutils version
%exclude %{_bindir}/bpf_jit_disasm
%endif
%{_sysconfdir}/bash_completion.d/perf
%{_libexecdir}/perf-core
%{_datadir}/perf-core
%{_docdir}/perf-tip
%if 0%{?photon_subrelease} <= 90
%{_libdir}/perf/examples/bpf/*
%{_libdir}/perf/include/bpf/*
%endif
%{_includedir}/perf/*
%ifarch x86_64
%if 0%{?photon_subrelease} <= 90
%{_mandir}/*
%endif
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%if 0%{?photon_subrelease} <= 90
%{_lib64dir}/libcpupower.so*
%else
%{_libdir}/libcpupower.so*
%endif
%{_docdir}/packages/cpupower
%{_datadir}/bash-completion/completions/cpupower
%config(noreplace) %{_sysconfdir}/cpufreq-bench.conf
%{_sbindir}/cpufreq-bench
%{_datadir}/locale/*/LC_MESSAGES/cpupower.mo
%endif

%files python3-perf
%defattr(-,root,root)
%{python3_sitelib}/*

%files -n bpftool
%defattr(-,root,root)
%{_sbindir}/bpftool
%{_datadir}/bash-completion/completions/bpftool

%if 0%{?canister_build}
%files fips-canister
%defattr(-,root,root)
%{_libdir}/fips-canister/*
%endif

%if 0%{?photon_subrelease} <= 90
%include %{SOURCE992}
%else
%include %{SOURCE993}
%endif
