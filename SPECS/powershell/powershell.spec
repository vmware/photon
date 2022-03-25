%global ps_native_ver 7.2.0
%global libmi_tag 1.6.9-0

Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        7.1.5
Release:        3%{?dist}
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
# mv PowerShell PowerShell-7.1.5 && cd PowerShell-7.1.5
# git checkout -b v7.1.5 tags/v7.1.5
# cd .. && tar czf powershell-7.1.5.tar.gz PowerShell-7.1.5
Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}=c49308ce4ba68862c1747fae94af2179363e7da1

# Same as Source0 but from https://github.com/PowerShell/PowerShell-Native.git
# And use --> git clone --recurse-submodules https://github.com/PowerShell/PowerShell-Native.git
# PowerShell-Native uses googletest submodule in it, we need that as well
Source1:        %{name}-native-%{ps_native_ver}.tar.gz
%define sha1    %{name}-native=0aa26684c8aded1e34527bc1d322621c941f960c

# This is downloaded from github release page of PowerShell
# For example:
# https://github.com/PowerShell/PowerShell/releases/download/v7.1.5/powershell-7.1.5-linux-x64.tar.gz
Source2:        %{name}-%{version}-linux-x64.tar.gz
%define sha1    %{name}-%{version}-linux=f27146aa4348b3c7d588f4099e8da5c56533d7c9

Source3:        build.sh
Source4:        Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets

# The default libmi.so file that comes with powershell (for example powershell-7.1.5-linux-x64.tar.gz)
# needs libcrypto.1.0.0, we need it to be linked with openssl-1.1.1 (what's present in Photon)
# Hence we need to re-build it.
# https://github.com/microsoft/omi/archive/refs/tags/v1.6.9-0.tar.gz
Source5:        omi-%{libmi_tag}.tar.gz
%define sha1    omi-%{libmi_tag}=823cbc445b631a094217d36050d35b59772a1407

Patch0:         Remove-workarounds-for-.NET-5-RTM-builds.patch

BuildArch:      x86_64

BuildRequires:  dotnet-sdk = 5.0.402
BuildRequires:  dotnet-runtime = 5.0.11
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

Requires:       icu
#gallery download scripts will fail without this
Requires:       zlib-devel

%description
PowerShell is an automation and configuration management platform.
It consists of a cross-platform command-line shell and associated scripting language.

%prep
# Using autosetup is not feasible
%setup -qn PowerShell-%{version}
%patch0 -p1
# Using autosetup is not feasible
%setup -qcTDa 1 -n PowerShell-Native
# Using autosetup is not feasible
%setup -qcTDa 2 -n %{name}-linux-%{version}
# Using autosetup is not feasible
%setup -qcTDa 5 -n omi

%build
# Build libmi
cd %{_builddir}/omi/omi-%{libmi_tag}/Unix && ./configure && make %{?_smp_mflags}
mv ./output/lib/libmi.so %{_builddir}/powershell-linux-%{version}

cd %{_builddir}/PowerShell-%{version}
cp %{SOURCE3} .
cp %{SOURCE4} src
bash -x build.sh
cd %{_builddir}/PowerShell-Native/PowerShell-Native-%{ps_native_ver}
pushd src/libpsl-native
cmake -DCMAKE_BUILD_TYPE=Debug .

make %{?_smp_mflags}

%install
cd %{_builddir}/PowerShell-%{version}
rm -rf src/%{name}-unix/bin/{Debug,Linux}
mkdir -p %{buildroot}%{_libdir}/%{name} %{buildroot}%{_docdir}/%{name}
mv bin/ThirdPartyNotices.txt bin/LICENSE.txt %{buildroot}%{_docdir}/%{name}
cp -r bin/* %{buildroot}%{_libdir}/%{name}
rm -f %{buildroot}/%{_libdir}/%{name}/libpsl-native.so
cp -rf %{_builddir}/PowerShell-Native/PowerShell-Native-%{ps_native_ver}/src/%{name}-unix/libpsl-native.so %{buildroot}%{_libdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_libdir}/%{name}/pwsh
ln -sf %{_libdir}/%{name}/pwsh %{buildroot}%{_bindir}/pwsh
mkdir -p %{buildroot}%{_libdir}/%{name}/ref

cp %{_builddir}/%{name}-linux-%{version}/ref/* %{buildroot}%{_libdir}/%{name}/ref
cp %{_builddir}/%{name}-linux-%{version}/libmi.so %{buildroot}%{_libdir}/%{name}/
cp -r %{_builddir}/%{name}-linux-%{version}/Modules/{PSReadLine,PowerShellGet,PackageManagement} \
  %{buildroot}%{_libdir}/%{name}/Modules

%check
%if 0%{?with_check}
cd %{_builddir}/PowerShell-%{version}/test/xUnit
dotnet test
export LANG=en_US.UTF-8
cd %{_builddir}/PowerShell-Native/PowerShell-Native-%{ps_native_ver}/src/libpsl-native
make test %{?_smp_mflags}
%endif

%post
#in case of upgrade, delete the soft links
if [ $1 -eq 2 ] ; then
  pushd %{_libdir}/%{name}/ref
  find -type l -exec unlink {} \;
  popd
fi

grep -qF /usr/bin/pwsh /etc/shells || echo "/usr/bin/pwsh" >> /etc/shells

%preun
#remove on uninstall
if [ $1 -eq 0 ]; then
  sed -i '\/usr\/bin\/pwsh/d' /etc/shells
fi

%files
%defattr(-,root,root,0755)
%{_bindir}/pwsh
%{_docdir}/*
%{_libdir}/%{name}/*
%exclude %dir %{_libdir}/debug

%changelog
* Sat Mar 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.1.5-3
- Exclude debug symbols properly
* Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 7.1.5-2
- Version Bump to build with new version of cmake
* Tue Oct 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 7.1.5-1
- Upgrade to version 7.1.5
* Tue Sep 21 2021 Shreyas B <shreyasb@vmware.com> 7.1.4-1
- Upgrade powershell to 7.1.4
* Tue Jul 27 2021 Tapas Kundu <tkundu@vmware.com> 7.1.2-2
- Rebuild with updated clang
* Mon Jan 18 2021 Shreyas B <shreyasb@vmware.com> 7.1.2-1
- Upgrade powershell to 7.1.2
* Wed Jan 13 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.0.3-3
- Fix Powershell build issue
* Fri Oct 16 2020 Ashwin H <ashwinh@vmware.com> 7.0.3-2
- Bump up to use new icu lib.
* Sun Oct 11 2020 Shreyas B <shreyasb@vmware.com> 7.0.3-1
- Upgrade powershell & powershell-linux to 7.0.3 to address CVE-2020-1108
* Fri Aug 07 2020 Shreyas B <shreyasb@vmware.com> 7.0.0-2
- Update dotnet-runtime v3.1.6
* Sat Apr 11 2020 Shreyas B <shreyasb@vmware.com> 7.0.0-1
- Upgrade powershell to 7.0.0
* Thu Dec 19 2019 Shreyas B <shreyasb@vmware.com> 6.2.3-5
- Adding make check for powershell & powershell-native.
- Fix Test failre in libpsl-native/test/test-locale.cpp.
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
