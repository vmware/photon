%global build_if %{photon_subrelease} >= 91

# powershell's make files use -D_FORTIFY_SOURCE=2, which conflicts
# with =3 from adjust-gcc-specs.sh, failing the build with error:
# `"_FORTIFY_SOURCE" redefined [-Werror]`
# Use `nofortify` until powershell move to =3.
%global security_hardening nofortify

%global gen_nuget_deps  0
%if 0%{?gen_nuget_deps} == 1
%define network_required 1
%endif

Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        7.6.5
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
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

# This is downloaded from github release page of PowerShell
# For example:
# https://github.com/PowerShell/PowerShell/releases/download/v7.2.0/powershell-7.2.0-linux-x64.tar.gz
Source1: %{name}-%{version}-linux-x64.tar.gz

Source2: build.sh
Source3: Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets

# After extracting Powershell original archive (Source0 in this spec), run:
# dotnet restore .
# Then archive $HOME/.nuget directory
# mv $HOME/.nuget <NAME>-<VERSION>-nuget-deps
# tar cJf <NAME>-<VERSION>-nuget-deps.tar.xz <NAME>-<VERSION>-nuget-deps
%if 0%{?gen_nuget_deps} == 0
Source4: %{name}-%{version}-nuget-deps.tar.xz
%endif

Source5: license.txt
%include %{SOURCE5}

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
Requires:       dotnet-sdk = 10.0.303

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
         %{buildroot}%{_datadir}/%{name}

cd %{_builddir}/PowerShell-%{version}
mv bin/ThirdPartyNotices.txt bin/LICENSE.txt %{buildroot}%{_docdir}/%{name}
cp -a bin/* %{buildroot}%{_datadir}/%{name}

chmod 755 %{buildroot}%{_datadir}/%{name}/pwsh
ln -srv %{buildroot}%{_datadir}/%{name}/pwsh %{buildroot}%{_bindir}/pwsh

cp -a %{_builddir}/%{name}-linux-%{version}/ref %{buildroot}%{_datadir}/%{name}/

cp -a %{_builddir}/%{name}-linux-%{version}/Modules/{PSReadLine,PowerShellGet,PackageManagement} \
      %{buildroot}%{_datadir}/%{name}/Modules

%post
#in case of upgrade, delete the soft links
if [ $1 -eq 2 ]; then
  pushd %{_datadir}/%{name}/ref
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
%{_datadir}/*
%{_bindir}/pwsh

%changelog
* Sat Aug 15 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.6.5-1
- Upgrade to v7.6.5
* Mon Jun 15 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.6.2-2
- Bump version as a part of dotnet-runtime upgrade
* Fri May 29 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.6.2-1
- Upgrade to v7.6.2
* Wed May 20 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.15-2
- Build for all subreleases
* Mon May 11 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 7.4.15-1.1
- Move to /90
* Thu Apr 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.15-1
- Upgrade to v7.4.15
* Tue Mar 10 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 7.4.11-4
- Set security_hardening nofortify
* Wed Feb 25 2026 Mukul Sikka <mukul.sikka@broadcom.com> 7.4.11-3
- Bump version as a part of dotnet-runtime 8.0.24 upgrade
* Tue Sep 02 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.11-2
- Rebuild with clang shared libs
* Sun Aug 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.11-1
- Upgrade to v7.4.11
* Thu Jun 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.7-2
- Bump version as a part of dotnet-runtime upgrade
* Thu Apr 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.7-1
- Upgrade to v7.4.7
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.3-3
- Release bump for SRP compliance
* Wed Sep 04 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.3-2
- Do fully offline build
* Thu Jul 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.4.3-1
- Upgrade to v7.4.3
* Thu Jan 11 2024 Anmol Jain <anmolja@vmware.com> 7.4.1-1
- Version update
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
