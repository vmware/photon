Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        6.0.1
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://microsoft.com/powershell
Group:          shells
Source0:        %{name}-%{version}.tar.gz
%define sha1    powershell=2aac40c972f45d1abb3a8b3a4d8a87fcbe91b889
Source1:        build.sh
BuildArch:      x86_64
BuildRequires:  dotnet-sdk = 2.1.4
BuildRequires:  dotnet-runtime = 2.0.5
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  git
Requires:       dotnet-runtime
Requires:       icu

%description
PowerShell is an automation and configuration management platform.
It consists of a cross-platform command-line shell and associated scripting language.

%prep
%setup -qn PowerShell
sed -i 's/2.0.2/2.1.4/' global.json

%build
cp %{SOURCE1} .
chmod +x ./build.sh
./build.sh

%install
rm -rf src/powershell-unix/bin/{Debug, Linux}
mkdir -p %{buildroot}%{_libdir}/powershell
mkdir -p %{buildroot}%{_docdir}/powershell
mv src/powershell-unix/bin/license_thirdparty_proprietary.txt %{buildroot}%{_docdir}/powershell
cp -r src/powershell-unix/bin/* %{buildroot}/%{_libdir}/powershell
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libdir}/powershell/pwsh %{buildroot}%{_bindir}/pwsh


%files
    %defattr(-,root,root,0755)
    %exclude %{_libdir}/debug
    rm -rf %{_libdir}/debug/.build-id
    rm -rf %{_libdir}/.build-id
    %{_libdir}/*
    %{_bindir}/pwsh
    %{_docdir}/*

%changelog
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0.1-1
-   Initial build for photon
