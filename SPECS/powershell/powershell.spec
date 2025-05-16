%global ps_native_ver 7.2.0
%global libmi_tag 1.6.9-0

Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        7.2.24
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://microsoft.com/powershell
Group:          shells

BuildArch:      x86_64

# Clone PowerShell source repo from https://github.com/PowerShell/PowerShell.git
# Checkout to desired tag & create tarball from that branch
#
# For example:
# git clone https://github.com/PowerShell/PowerShell.git
# mv PowerShell PowerShell-7.2.0 && cd PowerShell-7.2.0
# git checkout -b v7.2.0 tags/v7.2.0
# cd .. && tar czf powershell-7.2.0.tar.gz PowerShell-7.2.0
Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=7ceaec1cfddab2c25fa474a391730b98eea7527ab3174a58ae87903bcd866fad32c80571a51bfe853abbfceec786a10687e8eef47fc581940b9dac52648c25d9

# Same as Source0 but from https://github.com/PowerShell/PowerShell-Native.git
# And use --> git clone --recurse-submodules https://github.com/PowerShell/PowerShell-Native.git
# PowerShell-Native uses googletest submodule in it, we need that as well
Source1: %{name}-native-%{ps_native_ver}.tar.gz
%define sha512 %{name}-native=872d8c88e6825a06bc664a36aec864e7ca2a639457a0129aa8d2a12296ebb5c3e0d38ee593c08bbfba0678354123e914cb1096a92c09cd48964618225a1c2836

# This is downloaded from github release page of PowerShell
# For example:
# https://github.com/PowerShell/PowerShell/releases/download/v7.2.0/powershell-7.2.0-linux-x64.tar.gz
Source2: %{name}-%{version}-linux-x64.tar.gz
%define sha512 %{name}-%{version}-linux=0a5fc2b976a39cd051f738c85413d93a925d15fe1905a1713237bf97ecfcf21ffe661e887536a385da9cf72185513f025f1cff65a9fd667fa445f45b584613c1

Source3: build.sh
Source4: Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets

# The default libmi.so file that comes with powershell (for example powershell-7.1.5-linux-x64.tar.gz)
# needs libcrypto.1.0.0, we need it to be linked with openssl-1.1.1 (what's present in Photon)
# Hence we need to re-build it.
# https://github.com/microsoft/omi/archive/refs/tags/v1.6.9-0.tar.gz
Source5: omi-%{libmi_tag}.tar.gz
%define sha512 omi-%{libmi_tag}=97dbd968bd4a3075b534af9ebfe03c7003e3dfa07b0cc3923842fe6aecfbebff29fd2537195eb2ee27ff8e8e7a3779a4ba26156b7029a916c4a5eba4024d8009

# After extracting Powershell original archive (Source0 in this spec), run:
# dotnet restore .
# Then archive $HOME/.nuget directory
# mv $HOME/.nuget <NAME>-<VERSION>-nuget-deps
# tar czf <NAME>-<VERSION>-nuget-deps.tar.gz <NAME>-<VERSION>-nuget-deps
Source6: %{name}-%{version}-nuget-deps.tar.gz
%define sha512 %{name}-%{version}-nuget-deps=ba7d9893da9355260ac296819cc1851ca9fee32a30ebea3adb62f1c8ffdd6aa9173e3467c001d3d9e8cc4c94f6c1fe05ccfe53b54dabb4c4dd45c0593b8973af

Patch0: fix-nuget-url.patch

BuildRequires:  dotnet-sdk = 6.0.428
BuildRequires:  dotnet-runtime = 6.0.36
BuildRequires:  psmisc
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  git
BuildRequires:  photon-release
BuildRequires:  build-essential
BuildRequires:  openssl-devel
BuildRequires:  wget
BuildRequires:  Linux-PAM-devel
BuildRequires:  krb5-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  which
BuildRequires:  icu-devel
BuildRequires:  zlib-devel

Requires: icu >= 70.1
Requires: zlib
Requires: dotnet-sdk = 6.0.428

%description
PowerShell is an automation and configuration management platform.
It consists of a cross-platform command-line shell and associated scripting language.

%prep
# Using autosetup is not feasible
%setup -qn PowerShell-%{version}
# Using autosetup is not feasible
%setup -qcTDa 1 -n PowerShell-Native
# Using autosetup is not feasible
%setup -qcTDa 2 -n %{name}-linux-%{version}
# Using autosetup is not feasible
%setup -qcTDa 5 -n omi

pushd %{_builddir}/PowerShell-%{version}
%patch -p1 0
popd

tar xf %{SOURCE6}
rm -rf ${HOME}/.nuget
mv %{name}-%{version}-nuget-deps ${HOME}/.nuget

# to fix dubious ownership error by git
chown -R $(whoami) %{_builddir}

%build
# Build libmi
cd %{_builddir}/omi/omi-%{libmi_tag}/Unix && \
  ./configure && \
  make %{?_smp_mflags}

mv ./output/lib/libmi.so %{_builddir}/powershell-linux-%{version}

cd %{_builddir}/PowerShell-%{version}
cp %{SOURCE3} .
cp %{SOURCE4} src
bash -x build.sh
cd %{_builddir}/PowerShell-Native/PowerShell-Native-%{ps_native_ver}

pushd src/libpsl-native
%{__cmake} -DCMAKE_BUILD_TYPE=Debug .
%make_build
popd

%install
cd %{_builddir}/PowerShell-%{version}
rm -rf src/%{name}-unix/bin/{Debug,Linux}

mkdir -p %{buildroot}%{_libdir}/%{name} \
         %{buildroot}%{_docdir}/%{name}

mv bin/ThirdPartyNotices.txt bin/LICENSE.txt %{buildroot}%{_docdir}/%{name}

cp -a bin/* %{buildroot}%{_libdir}/%{name}

rm -f %{buildroot}%{_libdir}/%{name}/libpsl-native.so

cp -a %{_builddir}/PowerShell-Native/PowerShell-Native-%{ps_native_ver}/src/%{name}-unix/libpsl-native.so \
  %{buildroot}%{_libdir}/%{name}

mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_libdir}/%{name}/ref

chmod 755 %{buildroot}%{_libdir}/%{name}/pwsh
ln -sfrv %{_libdir}/%{name}/pwsh %{buildroot}%{_bindir}/pwsh

cp -a %{_builddir}/%{name}-linux-%{version}/ref/* %{buildroot}%{_libdir}/%{name}/ref
cp -a %{_builddir}/%{name}-linux-%{version}/libmi.so %{buildroot}%{_libdir}/%{name}/

cp -a %{_builddir}/%{name}-linux-%{version}/Modules/{PSReadLine,PowerShellGet,PackageManagement} \
  %{buildroot}%{_libdir}/%{name}/Modules

%if 0%{?with_check}
%check
cd %{_builddir}/PowerShell-%{version}/test/xUnit
dotnet test
export LANG=en_US.UTF-8
cd %{_builddir}/PowerShell-Native/PowerShell-Native-%{ps_native_ver}/src/libpsl-native
make test %{?_smp_mflags}
%endif

%post
/sbin/ldconfig
#in case of upgrade, delete the soft links
if [ $1 -eq 2 ] ; then
  pushd %{_libdir}/%{name}/ref
  find -type l -exec unlink {} \;
  popd
fi

grep -qF /usr/bin/pwsh /etc/shells || echo "/usr/bin/pwsh" >> /etc/shells

%postun
/sbin/ldconfig

%preun
#remove on uninstall
if [ $1 -eq 0 ]; then
  sed -i '\/usr\/bin\/pwsh/d' /etc/shells
fi

%files
%defattr(-,root,root,0755)
%exclude %dir %{_libdir}/debug
%{_libdir}/%{name}/*
%{_bindir}/pwsh
%{_docdir}/*

%changelog
* Fri May 16 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.2.24-1
- Upgrade to v7.2.24
* Mon Jan 22 2024 Anmol Jain <anmolja@vmware.com> 7.2.18-1
- Version upgrade
* Wed Dec 20 2023 Anmol Jain <anmolja@vmware.com> 7.2.17-1
- Fixed CVE-2022-23267
* Tue Nov 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.2.7-2
- Bump version as a part of llvm upgrade
* Mon Oct 31 2022 Anmol Jain <anmolja@vmware.com> 7.2.7-1
- Fixed CVE-2022-26788
* Mon Oct 31 2022 Anmol Jain <anmolja@vmware.com> 7.2.0-4
- Fixed CVE-2022-23267
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.2.0-3
- Exclude debug symbols properly
* Tue Dec 07 2021 Alexey Makhalov <amakhalov@vmware.com> 7.2.0-2
- Requires specific version of icu
* Mon Nov 15 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.2.0-1
- Upgrade to version 7.2.0
* Tue Oct 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 7.1.5-1
- Upgrade to version 7.1.5
* Tue Mar 9 2021 Shreyas B <shreyasb@vmware.com> 7.1.2-1
- Upgrade powershell to 7.1.2
* Wed Jan 13 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.0.3-2
- Fix Powershell build issue
* Mon Dec 07 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.0.3-1
- Upgrade powershell, powershell-linux to 7.0.3 to address CVE-2020-1108
* Sat Oct 17 2020 Satya Naga Rajesh <svasamsetty@vmware.com> 7.0.0-2
- Fix powershell compatibility with openssl 1.1.1
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 7.0.0-1
- Automatic Version Bump
* Thu Mar 26 2020 Alexey Makhalov <amakhalov@vmware.com> 6.2.3-5
- Fix compilation issue with glibc >= 2.30.
* Mon Dec 16 2019 Shreyas B <shreyasb@vmware.com> 6.2.3-4
- Build PowerShell with locally build "libpsl-native.so" from PowerShell-Native(6.2.0).
* Wed Dec 04 2019 Tapas Kundu <tkundu@vmware.com> 6.2.3-3
- Fixed ref folder to have right dlls
* Tue Dec 03 2019 Tapas Kundu <tkundu@vmware.com> 6.2.3-2
- Fix post in case of upgrade
* Wed Nov 13 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.2.3-1
- update to 6.2.3
- refactor build script
- include PSReadLine, PowerShellGet and PackageManagement modules
* Wed Feb 13 2019 Ajay Kaher <akaher@vmware.com> 6.1.1-2
- Fix version mismatch issue.
* Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 6.1.1-1
- upgrade version to 6.1.1
* Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 6.0.1-2
- upgrade version of dotnet-runtime
* Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0.1-1
- Initial build for photon
