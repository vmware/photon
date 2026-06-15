# powershell's make files use -D_FORTIFY_SOURCE=2, which conflicts
# with =3 from adjust-gcc-specs.sh, failing the build with error:
# `"_FORTIFY_SOURCE" redefined [-Werror]`
# Use `nofortify` until powershell move to =3.
%global security_hardening nofortify

%global gen_nuget_deps  0

Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        7.4.15
Release:        2%{?dist}
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
# v="7.4.11"; tag=v${v}
# git clone --branch $tag --depth 1 https://github.com/PowerShell/PowerShell.git
# cd PowerShell && git checkout -b $tag
# cd ..; mv PowerShell PowerShell-$v
# tar czf powershell-$v.tar.gz PowerShell-$v
Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=dd046eab73beb5f814d039084c09a8ade607b3a330f5d2906da1666d8a36c81848927186f17059cf77f2f15e9958f0d5ab5407e2d8d66795b38b69ac1a686e32

# This is downloaded from github release page of PowerShell
# For example:
# https://github.com/PowerShell/PowerShell/releases/download/v7.2.0/powershell-7.2.0-linux-x64.tar.gz
Source1: %{name}-%{version}-linux-x64.tar.gz
%define sha512 %{name}-%{version}-linux=ba135fda6b61f17d66764cc002171a2bd812e0c6e108d7b8d4e8eabf833b6deea2c6c235d8549836b100bbe050a6d332ed3ffe85b326a8b1836cef480fcc6290

Source2: build.sh
Source3: Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets

# After extracting Powershell original archive (Source0 in this spec), run:
# dotnet restore .
# Then archive $HOME/.nuget directory
# mv $HOME/.nuget <NAME>-<VERSION>-nuget-deps
# tar cJf <NAME>-<VERSION>-nuget-deps.tar.xz <NAME>-<VERSION>-nuget-deps
%if 0%{?gen_nuget_deps} == 0
Source4: %{name}-%{version}-nuget-deps.tar.xz
%define sha512 %{name}-%{version}-nuget-deps=064d743352655dff62910f71a5aa3c03fa59d1c872bee0b6260862b31ae57d896b45a97c26af4e8964f6fc89e754c4514f73a1e55a1d11c4af5f01414cbf8f91
%endif

%if 0%{?gen_nuget_deps} == 1
Patch0: fix-nuget-url.patch
%endif

BuildRequires:  dotnet-sdk
BuildRequires:  dotnet-runtime
BuildRequires:  psmisc
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  git
BuildRequires:  photon-release
BuildRequires:  build-essential
BuildRequires:  openssl-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  krb5-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  which
BuildRequires:  icu-devel
BuildRequires:  zlib-devel
%if 0%{?gen_nuget_deps}
BuildRequires:  wget
%endif

Requires:       icu >= 70.1
Requires:       zlib
Requires:       dotnet-sdk = 8.0.420

%description
PowerShell is an automation and configuration management platform.
It consists of a cross-platform command-line shell and associated scripting language.

%prep
# Using autosetup is not feasible
%setup -qn PowerShell-%{version}
# Using autosetup is not feasible
%setup -qcTDa 1 -n %{name}-linux-%{version}

pushd %{_builddir}/PowerShell-%{version}

%if 0%{?gen_nuget_deps} == 0
tar xf %{SOURCE4}
[ -d ${HOME}/.nuget ] && rm -rf ${HOME}/.nuget
mv %{name}-%{version}-nuget-deps ${HOME}/.nuget
%else
%patch -p1 0
dotnet restore .
mv $HOME/.nuget %{name}-%{version}-nuget-deps
tar cJf %{name}-%{version}-nuget-deps.tar.xz %{name}-%{version}-nuget-deps
echo "$PWD/%{name}-%{version}-nuget-deps.tar.xz is ready ..."
echo "You can get the archive from chroot now ..."
echo "Aborting build now ..."
exit 1
%endif

popd

%build
pushd %{_builddir}/PowerShell-%{version}
cp %{SOURCE2} .
cp %{SOURCE3} src
bash -x build.sh
popd

%install
mkdir -p %{buildroot}%{_docdir}/%{name} \
         %{buildroot}%{_bindir} \
         %{buildroot}%{_libdir}/%{name}

cd %{_builddir}/PowerShell-%{version}
mv bin/ThirdPartyNotices.txt bin/LICENSE.txt %{buildroot}%{_docdir}/%{name}
cp -a bin/* %{buildroot}%{_libdir}/%{name}

chmod 755 %{buildroot}%{_libdir}/%{name}/pwsh
ln -srv %{buildroot}%{_libdir}/%{name}/pwsh %{buildroot}%{_bindir}/pwsh

cp -a %{_builddir}/%{name}-linux-%{version}/ref %{buildroot}%{_libdir}/%{name}/

cp -a %{_builddir}/%{name}-linux-%{version}/Modules/{PSReadLine,PowerShellGet,PackageManagement} \
      %{buildroot}%{_libdir}/%{name}/Modules

%post
#in case of upgrade, delete the soft links
if [ $1 -eq 2 ]; then
  pushd %{_libdir}/%{name}/ref
  find -type l -exec unlink {} \;
  popd
fi

grep -qF %{_bindir}/pwsh %{_sysconfdir}/shells || \
  echo "%{_bindir}/pwsh" >> %{_sysconfdir}/shells

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
* Mon Jun 15 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.15-2
- Bump version as a part of dotnet-runtime upgrade
- Cleanup spec
* Thu Apr 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.15-1
- Upgrade to v7.4.15
* Tue Sep 02 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.2.24-2
- Rebuild with clang shared libs
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
