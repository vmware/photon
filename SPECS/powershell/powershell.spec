%global ps_native_ver   7.3.2
%global libmi_tag       1.6.11-0

Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        7.3.10
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://microsoft.com/powershell
Group:          shells

# Clone PowerShell source repo from https://github.com/PowerShell/PowerShell.git
# Checkout to desired tag & create tarball from that branch
#
# For example:
# git clone https://github.com/PowerShell/PowerShell.git
# mv PowerShell PowerShell-7.2.0 && cd PowerShell-7.2.0
# git checkout -b v7.2.0 tags/v7.2.0
# cd .. && tar czf powershell-7.2.0.tar.gz PowerShell-7.2.0
Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=233c5e57bbac4f7a5f29922f0650fbb0350a3a11112f6e350204b9c5c3e89c3c8326619d772d1e293511d75c0fe360375c76c299569f471612b1d124a6d53c76

# Same as Source0 but from https://github.com/PowerShell/PowerShell-Native.git
# And use --> git clone --recurse-submodules https://github.com/PowerShell/PowerShell-Native.git
# PowerShell-Native uses googletest submodule in it, we need that as well
Source1: %{name}-native-%{ps_native_ver}.tar.gz
%define sha512 %{name}-native=7b13b2700fc9ce20525414ccf244aad92b005a0d8e5231d72d27e5fe8bfefc9a573ff81cff6702bd0547e6eebcf3f192d797d6f0415846d49a4db79edc33ebb7

# This is downloaded from github release page of PowerShell
# For example:
# https://github.com/PowerShell/PowerShell/releases/download/v7.2.0/powershell-7.2.0-linux-x64.tar.gz
Source2: %{name}-%{version}-linux-x64.tar.gz
%define sha512 %{name}-%{version}-linux=be4f33de51b6bd8838168cf72a607160411288bd081fc84d19e07f9e57ccf8288103b5160a94a72d479242246a044a408119fbf88731d2d642e5b00ccf8e08b2

Source3: build.sh
Source4: Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets

# The default libmi.so file that comes with powershell (for example powershell-7.1.5-linux-x64.tar.gz)
# needs libcrypto.1.0.0, we need it to be linked with openssl-3.x (what's present in Photon)
# Hence we need to re-build it.
# https://github.com/microsoft/omi/archive/refs/tags/v1.6.9-0.tar.gz
Source5: omi-%{libmi_tag}.tar.gz
%define sha512 omi-%{libmi_tag}=3710cd8a0bc4d5478049a982b5f3a18d80c0167eb152cc6711887c965191c7727af7b4809b56d4e4b10a35b7a1853c3a72a13d8af9b1454fb43b1636b306c952

BuildArch:      x86_64

BuildRequires:  dotnet-sdk = 7.0.404
BuildRequires:  dotnet-runtime = 7.0.14
BuildRequires:  psmisc
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  git
BuildRequires:  photon-release

# Needed for libmi
BuildRequires:  build-essential
BuildRequires:  openssl-devel
BuildRequires:  wget
BuildRequires:  Linux-PAM-devel
BuildRequires:  krb5-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  which
BuildRequires:  icu-devel >= 70.1
# Gallery download scripts will fail without this
BuildRequires:  zlib-devel

Requires:       icu >= 70.1
Requires:       zlib

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

%build
# Build libmi
cd %{_builddir}/omi/omi-%{libmi_tag}/Unix && sh ./configure && %make_build
mv ./output/lib/libmi.so %{_builddir}/powershell-linux-%{version}

cd %{_builddir}/PowerShell-%{version}
cp %{SOURCE3} .
cp %{SOURCE4} src
bash -x build.sh

cd %{_builddir}/PowerShell-Native/PowerShell-Native-%{ps_native_ver}
pushd src/libpsl-native
%{__cmake} -DCMAKE_BUILD_TYPE=Debug
%make_build
popd

%install
cd %{_builddir}/PowerShell-%{version}
rm -rf src/%{name}-unix/bin/{Debug,Linux}
mkdir -p %{buildroot}%{_libdir}/%{name} %{buildroot}%{_docdir}/%{name}
mv bin/ThirdPartyNotices.txt bin/LICENSE.txt %{buildroot}%{_docdir}/%{name}
cp -r bin/* %{buildroot}%{_libdir}/%{name}
rm -f %{buildroot}%{_libdir}/%{name}/libpsl-native.so

cp -rf %{_builddir}/PowerShell-Native/PowerShell-Native-%{ps_native_ver}/src/%{name}-unix/libpsl-native.so \
        %{buildroot}%{_libdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_libdir}/%{name}/pwsh
ln -sf %{_libdir}/%{name}/pwsh %{buildroot}%{_bindir}/pwsh
mkdir -p %{buildroot}%{_libdir}/%{name}/ref

cp %{_builddir}/%{name}-linux-%{version}/ref/* %{buildroot}%{_libdir}/%{name}/ref
cp %{_builddir}/%{name}-linux-%{version}/libmi.so %{buildroot}%{_libdir}/%{name}/

cp -r %{_builddir}/%{name}-linux-%{version}/Modules/{PSReadLine,PowerShellGet,PackageManagement} \
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
#in case of upgrade, delete the soft links
if [ $1 -eq 2 ]; then
  pushd %{_libdir}/%{name}/ref
  find -type l -exec unlink {} \;
  popd
fi

grep -qF %{_bindir}/pwsh %{_sysconfdir}/shells || echo "%{_bindir}/pwsh" >> %{_sysconfdir}/shells

%preun
#remove on uninstall
if [ $1 -eq 0 ]; then
  sed -i '\/usr\/bin\/pwsh/d' %{_sysconfdir}/shells
fi

%files
%defattr(-,root,root,0755)
%exclude %dir %{_libdir}/debug
%{_libdir}/%{name}/*
%{_bindir}/pwsh
%{_docdir}/*

%changelog
* Thu Dec 21 2023 Anmol Jain <anmolja@vmware.com> 7.3.10-1
- Version update to fix CVE-2023-36013
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 7.3.4-2
- Bump version as a part of krb5 upgrade
* Thu Jun 08 2023 Anmol Jain <anmolja@vmware.com> 7.3.4-1
- Bump version to use dotnet 7.0.5 version
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.3.2-2
- Bump version as a part of zlib upgrade
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.3.2-1
- Upgrade to v7.3.2
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.3.0-preview.8.1
- Bump version as a part of icu upgrade
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.3.0-preview.8
- Upgrade to v7.3.0-rc1
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.2.0-3
- Fix binary path
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
