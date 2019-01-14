%define debug_package %{nil}
Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        2.1.403
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools
Source0:        https://download.microsoft.com/download/1/1/5/115B762D-2B41-4AF3-9A63-92D9680B9409/%{name}-%{version}-linux-x64.tar.gz
%define sha1    dotnet-sdk=0a72a76e833f20da90a052f634d6711ef62d0526
BuildArch:      x86_64
Requires:       dotnet-runtime icu

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%setup -c %{name}-%{version}

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet/sdk
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
cp -r sdk/%{version} %{buildroot}%{_libdir}/dotnet/sdk
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/%{name}-%{version}

%files
    %defattr(-,root,root,0755)
    %{_libdir}/*
    %{_docdir}/*

%changelog
*   Mon Jan 14 2019 Dweep Advani <dadvani@vmware.com> 2.1.403-1
-   upgraded to version 2.1.403
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.4-1
-   Initial build for photon
