%define debug_package %{nil}
Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        2.2.100
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools
Source0:        https://download.microsoft.com/download/D/5/9/D593CD8F-04E7-425D-962C-86FF4C90B1DA/dotnet-sdk-2.2.100-preview2-009404-linux-x64.tar.gz
%define sha1    dotnet-sdk=b8133981c7de5150b933eada5a25a4a13fa81b0d
BuildArch:      x86_64
Requires:       dotnet-runtime icu

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%setup -c dotnet-sdk-%{version}

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet/sdk
mkdir -p %{buildroot}%{_docdir}/dotnet-sdk-%{version}
cp -r sdk/%{version}-preview2-009404 %{buildroot}%{_libdir}/dotnet/sdk
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/dotnet-sdk-%{version}

%files
    %defattr(-,root,root,0755)
    %{_libdir}/*
    %{_docdir}/*

%changelog
*   Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 2.2.100-1
-   Upgraded to version 2.2.100
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.4-1
-   Initial build for photon
