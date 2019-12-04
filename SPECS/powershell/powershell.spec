Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        6.2.3
Release:        3%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://microsoft.com/powershell
Group:          shells
Source0:        %{name}-%{version}.tar.gz
%define sha1    powershell=ab7e1d7fbdf4a90fd160cf85b5dc56eb294a7755
Source1:        %{name}-native-6.2.0.tar.gz
%define sha1    powershell-native=b748288e87e16a13783a0cc57a5cfe818445ab2b
Source2:        %{name}-linux-%{version}-x64.tar.gz
%define sha1    powershell-linux=38efbb5c76ceb2a0d0d3c364a9c82241f2144faa
Source3:        build.sh
Source4:        Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets
BuildArch:      x86_64
BuildRequires:  dotnet-sdk = 2.1.509
BuildRequires:  dotnet-runtime = 2.2.3
BuildRequires:  psmisc
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  git
Requires:       icu
#gallery download scripts will fail without this
Requires:       zlib-devel

%description
PowerShell is an automation and configuration management platform.
It consists of a cross-platform command-line shell and associated scripting language.

%prep
%setup -qn PowerShell-%{version}
%setup -qTDb 1 -n PowerShell-Native-6.2.0
%setup -qcTDa 2 -n %{name}-linux-%{version}-x64

%build
cd %{_builddir}/PowerShell-%{version}
sed -i -e '/refs\/tags\/v%{version}/{n;q}' .git/packed-refs
cp %{SOURCE3} .
cp %{SOURCE4} src
chmod +x ./build.sh
./build.sh

%install
cd %{_builddir}/PowerShell-%{version}
rm -rf src/powershell-unix/bin/{Debug, Linux}
mkdir -p %{buildroot}%{_libdir}/powershell
mkdir -p %{buildroot}%{_docdir}/powershell
mv src/powershell-unix/bin/ThirdPartyNotices.txt %{buildroot}%{_docdir}/powershell
mv src/powershell-unix/bin/LICENSE.txt %{buildroot}%{_docdir}/powershell
cp -r src/powershell-unix/bin/* %{buildroot}/%{_libdir}/powershell
mkdir -p %{buildroot}%{_bindir}
chmod 0755 %{buildroot}/%{_libdir}/powershell/pwsh
ln -sf %{_libdir}/powershell/pwsh %{buildroot}%{_bindir}/pwsh
mkdir -p %{buildroot}%{_libdir}/powershell/ref
cp %{_builddir}/powershell-linux-%{version}-x64/ref/* %{buildroot}%{_libdir}/powershell/ref
cp -r %{_builddir}/powershell-linux-%{version}-x64/Modules/{PSReadLine,PowerShellGet,PackageManagement} \
%{buildroot}%{_libdir}/powershell/Modules

%post
#in case of upgrade, delete the soft links
if [ $1 -eq 2 ] ; then
    pushd %{_libdir}/powershell/ref
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
    %exclude %{_libdir}/debug
    %{_libdir}/*
    %{_bindir}/pwsh
    %{_docdir}/*

%changelog
*   Wed Dec 04 2019 Tapas Kundu <tkundu@vmware.com> 6.2.3-3
-   Fixed ref folder to have right dlls
*   Tue Dec 03 2019 Tapas Kundu <tkundu@vmware.com> 6.2.3-2
-   Fix post in case of upgrade
*   Wed Nov 13 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.2.3-1
-   update to 6.2.3
-   refactor build script
-   include PSReadLine, PowerShellGet and PackageManagement modules
*   Wed Feb 13 2019 Ajay Kaher <akaher@vmware.com> 6.1.1-2
-   Fix version mismatch issue.
*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 6.1.1-1
-   upgrade version to 6.1.1
*   Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 6.0.1-2
-   upgrade version of dotnet-runtime
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0.1-1
-   Initial build for photon
