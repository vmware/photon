# One spec for every 5.0 subrelease: kernel 6.1 up to photon_subrelease 90,
# kernel 6.12 from 91. The per-kernel preamble and changelog are included
# below; sections that differ carry photon_subrelease conditionals.

Summary:        Kernel
Name:           linux-esx
URL:            http://www.kernel.org
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%if 0%{?photon_subrelease} <= 90
Version:        6.1.183
%else
Version:        6.12.109
%endif
Source0:        http://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz

Source990:      linux-esx-6.1.inc
Source991:      linux-esx-6.12.inc
Source992:      linux-esx-6.1-changelog.inc
Source993:      linux-esx-6.12-changelog.inc

%if 0%{?photon_subrelease} <= 90
%include %{SOURCE990}
%else
%include %{SOURCE991}
%endif

BuildRequires: bc
BuildRequires: kbd
BuildRequires: kmod-devel
BuildRequires: glib-devel
BuildRequires: libmspack-devel
BuildRequires: Linux-PAM-devel
BuildRequires: openssl-devel
BuildRequires: procps-ng-devel
BuildRequires: lz4
BuildRequires: elfutils-libelf-devel
BuildRequires: elfutils-devel
BuildRequires: dwarves-devel
Requires: kmod
Requires: filesystem

%description
The Linux kernel build for GOS for VMware hypervisor.
# Enable post FIPS certification
%if 0
This kernel is FIPS certified.
%endif
%if 0%{?vmxnet3_sw_timestamp}
- vmxnet3 with software timestamping enabled
%endif

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
%if 0%{?photon_subrelease} <= 90
Requires:      python3 gawk
%else
Requires:      python3 gawk dwarves-devel
%endif
Requires:      %{name} = %{version}-%{release}
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:       Kernel docs
Group:         System Environment/Kernel
Requires:      python3
Requires:      %{name} = %{version}-%{release}
%description docs
The Linux package contains the Linux kernel doc files

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
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
%if 0%{?photon_subrelease} <= 90
%autopatch -p1 -m0 -M48

# apparmor
%autopatch -p1 -m100 -M100

# seccomp
%autopatch -p1 -m101 -M101
%else
%autopatch -p1 -m0 -M49
%endif

%ifarch x86_64
%if 0%{?photon_subrelease} <= 90
%autopatch -p1 -m49 -M49
%endif
# VMW x86
%if 0%{?photon_subrelease} <= 90
%autopatch -p1 -m50 -M59
%else
%autopatch -p1 -m50 -M60
%endif
%endif

# linux-esx
%if 0%{?photon_subrelease} <= 90
%autopatch -p1 -m60 -M85
%else
%autopatch -p1 -m61 -M89

# Backward compatibility
%if "%{dist}" == ".ph5"
%autopatch -p1 -m91 -M91
%endif
%endif

%ifarch aarch64
# aarch64 patches
%if 0%{?photon_subrelease} <= 90
%autopatch -p1 -m250 -M260
%else
%autopatch -p1 -m200 -M219
%endif
%endif

# 9P
%autopatch -p1 -m300 -M309

%if 0%{?photon_subrelease} <= 90
# crypto
%autopatch -p1 -m500 -M504

%ifarch x86_64
%autopatch -p1 -m505 -M508
%endif

%if 0%{?fips}
%autopatch -p1 -m509 -M513
%endif

%ifarch x86_64
# SEV on VMware
%autopatch -p1 -m600 -M609
%endif

%autopatch -p1 -m1000 -M1001

%ifarch x86_64
cp -a ../jitterentropy-%{jent_major_version}-%{jent_ph_version}/ \
       crypto/jitterentropy-%{jent_major_version}/

cp %{SOURCE33} \
   %{SOURCE34} \
   %{SOURCE35} \
   crypto/jitterentropy-%{jent_major_version}/

cp %{SOURCE36} crypto/
%endif

%make_build mrproper
cp %{SOURCE1} .config

cp %{SOURCE21} photon-cert-bundle.pem

%if 0%{?fips}
cp %{SOURCE37} \
   %{SOURCE38} \
   %{SOURCE39} \
   %{SOURCE40} \
   %{SOURCE41} \
   %{SOURCE42} \
   crypto/

cp ../fips-canister-%{fips_canister_version}/fips_canister.o \
   ../fips-canister-%{fips_canister_version}/.fips_canister.o.cmd \
   ../fips-canister-%{fips_canister_version}/fips_canister-kallsyms \
   crypto/

patch -p1 < %{PATCH514}

mkdir -p %{struct_comp_dir}/%{vmlinux_definition_loc}
cp %{SOURCE9}  %{struct_comp_dir}
cp %{SOURCE43} \
   %{SOURCE44} \
   %{SOURCE45} \
   %{SOURCE46} \
   %{SOURCE47} \
   %{struct_comp_dir}/%{vmlinux_definition_loc}
%endif

sed -i 's/CONFIG_LOCALVERSION="-esx"/CONFIG_LOCALVERSION="-%{release}-esx"/' .config

%ifarch x86_64
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@LINUX_PH_GEN@@,%{linux_photon_generation},g" \
    %{SOURCE25} > linux-sbat.csv
%endif

%include %{SOURCE4}

%else
# prep for viomem out-of-tree module
mkdir -p ../viomem
pushd ../viomem
cp %{SOURCE30} Makefile
cp %{SOURCE31} .
popd

# Jitterentropy support and FIPS compliance
%autopatch -p1 -m10000 -M10000

%if 0%{?fips}

# Using autosetup is not feasible
%setup -q -T -D -b 10000 -n linux-%{version}

cp -rf ../%{jent_name}/ crypto/
rm crypto/jitterentropy-kcapi.c
pushd crypto/%{jent_name}
%autopatch -p1 -m10050 -M10050
popd
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

%make_build mrproper
cp %{SOURCE1} .config
cp %{SOURCE21} photon-cert-bundle.pem

sed -i 's/CONFIG_LOCALVERSION="-esx"/CONFIG_LOCALVERSION="-%{release}-esx"/' .config

%if 0%{?photon_subrelease} >= 92
# Update toolchain config for gcc 12.5.0 and binutils 2.46.1
sed -i 's/CONFIG_CC_VERSION_TEXT="gcc (GCC) 12.2.0"/CONFIG_CC_VERSION_TEXT="gcc (GCC) 12.5.0"/' .config
sed -i 's/CONFIG_GCC_VERSION=120200/CONFIG_GCC_VERSION=120500/' .config
sed -i 's/CONFIG_AS_VERSION=23900/CONFIG_AS_VERSION=24601/' .config
sed -i 's/CONFIG_LD_VERSION=23900/CONFIG_LD_VERSION=24601/' .config
sed -i 's/CONFIG_GCC_ASM_GOTO_OUTPUT_BROKEN=y/CONFIG_CC_HAS_ASM_GOTO_OUTPUT=y\nCONFIG_CC_HAS_ASM_GOTO_TIED_OUTPUT=y/' .config
%endif

%if 0%{?fips}
tar -xvf /usr/lib/fips-canister/fips-canister-%{fips_canister_version}.tar.bz2
# fips_canister.o is mentioned in obj-y. So, Makefile.modpost expects
# corresponding .cmd file. Empty content is ok, since we are not going
# to rebuild it.
touch crypto/.fips_canister.o.cmd
%else
sed -i "s/# CONFIG_CRYPTO_JITTERENTROPY_MEMSIZE_2 is not set/CONFIG_CRYPTO_JITTERENTROPY_MEMSIZE_2=y/" .config
sed -i "s/CONFIG_CRYPTO_JITTERENTROPY_MEMSIZE_32=y/# CONFIG_CRYPTO_JITTERENTROPY_MEMSIZE_32 is not set/" .config

sed -i "s/CONFIG_CRYPTO_JITTERENTROPY_MEMORY_BLOCKS=128/CONFIG_CRYPTO_JITTERENTROPY_MEMORY_BLOCKS=64/" .config
sed -i "s/CONFIG_CRYPTO_JITTERENTROPY_MEMORY_BLOCKSIZE=256/CONFIG_CRYPTO_JITTERENTROPY_MEMORY_BLOCKSIZE=32/" .config
%endif
%dnl canister/.config handling, shared with linux.spec
%include %{SOURCE5}
%ifarch x86_64
sed -e "s,@@NAME@@,%{name},g" \
    -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    -e "s,@@LINUX_PH_GEN@@,%{linux_photon_generation},g" \
    %{SOURCE25} > linux-sbat.csv
%endif

%include %{SOURCE4}

%endif
%build
%make_build KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH=%{arch}

%if 0%{?photon_subrelease} >= 91
# build viomem module
%endif
bldroot="${PWD}"
%if 0%{?photon_subrelease} <= 90

# build viomem module
mkdir ../viomem
%endif
pushd ../viomem
%if 0%{?photon_subrelease} <= 90
cp %{SOURCE100} Makefile
cp %{SOURCE101} .
cd ../viomem
%make_build -C ${bldroot} M="${PWD}" V=1 modules
%else
%make_build -C ${bldroot} M="${PWD}" modules
%endif
popd

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

%endif
%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
%if 0%{?photon_subrelease} <= 90
%make_build ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install
%else

%make_build ARCH=%{arch} \
        INSTALL_MOD_PATH=%{buildroot} \
        modules_install
%endif

%ifarch x86_64
install -vm 644 arch/%{archdir}/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
%if "%{?signing_script}" != ""
%{signing_script} --file_type pe \
      --config_file %{signing_params} \
      --auth_file %{signing_auth} \
      --artifact %{buildroot}/boot/vmlinuz-%{uname_r}
%endif
%endif

%ifarch aarch64
install -vm 644 arch/%{archdir}/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?photon_subrelease} >= 91
# install viomem module
%endif
bldroot="${PWD}"
%if 0%{?photon_subrelease} <= 90
# install viomem module
%endif
pushd ../viomem
%if 0%{?photon_subrelease} <= 90
%make_build -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} modules_install
%else
%make_build -C ${bldroot} M="${PWD}" INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra \
    modules_install
%endif
popd

%if 0%{?photon_subrelease} <= 90
%if 0%{?__debug_package}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
%endif

# TODO: noacpi acpi=off noapic pci=conf1,nodomains pcie_acpm=off pnpacpi=off
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp cpu_init_udelay=0
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# cleanup dangling symlinks
%else
%if 0%{?_enable_debug_packages}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
%endif

# TODO: noacpi acpi=off noapic pci=conf1,nodomains pcie_acpm=off pnpacpi=off
cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp cpu_init_udelay=0
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Cleanup dangling symlinks
%endif
rm -f %{buildroot}%{_modulesdir}/source \
      %{buildroot}%{_modulesdir}/build

# create /use/src/linux-headers-*/ content
%if 0%{?photon_subrelease} <= 90
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
%else
find . -name Makefile* -o -name Kconfig* -o -name *.pl | \
    xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/%{archdir}/include include scripts -type f | \
    xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | \
    xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

find arch/%{archdir}/include Module.symvers include scripts -type f | \
    xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

%endif
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
%if 0%{?photon_subrelease} <= 90
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%else
install -vsm 755 tools/objtool/{objtool,fixdep} \
    %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}/tools/objtool/
%endif
%endif

# copy .config manually to be where it's expected to be
cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
%if 0%{?photon_subrelease} <= 90
# symling to the build folder
ln -sf "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
%else
# Symlink to the build folder
ln -sfv "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
%endif
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE20} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

%include %{SOURCE2}
%include %{SOURCE3}
%include %{SOURCE19}

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%if 0%{?photon_subrelease} <= 90
/lib/modules/*
%else
%{_modulesdir}/*
%endif
%exclude %{_modulesdir}/build

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files docs
%defattr(-,root,root)
%{_docdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}

%if 0%{?photon_subrelease} <= 90
%include %{SOURCE992}
%else
%include %{SOURCE993}
%endif
