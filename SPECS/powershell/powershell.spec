Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        6.1.1
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://microsoft.com/powershell
Group:          shells
Source0:        %{name}-%{version}.tar.gz
%define sha1    powershell=03abf8fa557974e5e765743bad870ab03e301e5b
Source1:        build.sh
BuildArch:      x86_64
BuildRequires:  dotnet-sdk = 2.1.403
BuildRequires:  dotnet-runtime = 2.2.0
BuildRequires:  psmisc
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  git
Requires:       dotnet-runtime
Requires:       icu

%description
PowerShell is an automation and configuration management platform.
It consists of a cross-platform command-line shell and associated scripting language.

%prep
%setup -qn PowerShell-%{version}

%build
cp %{SOURCE1} .
chmod +x ./build.sh
./build.sh

%install
rm -rf src/%{name}-unix/bin/{Debug, Linux}
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_docdir}/%{name}
mv src/%{name}-unix/bin/ThirdPartyNotices.txt %{buildroot}%{_docdir}/%{name}
mv src/%{name}-unix/bin/LICENSE.txt %{buildroot}%{_docdir}/%{name}
cp -r src/%{name}-unix/bin/* %{buildroot}/%{_libdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libdir}/%{name}/pwsh %{buildroot}%{_bindir}/pwsh


%files
    %defattr(-,root,root,0755)
    %exclude %{_libdir}/debug
    %{_libdir}/*
    %{_bindir}/pwsh
    %{_docdir}/*

%changelog
*   Mon Jan 14 2019 Dweep Advani <dadvani@vmware.com> 6.1.1-1
-   upgraded version to 6.1.1
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0.1-1
-   Initial build for photon
