%define debug_package %{nil}
Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        5.0.400
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools
Source0:        %{name}-%{version}-linux-x64.tar.gz
%define sha1    dotnet-sdk=87ca6aca124f4d0133ca6e99972a7542f2dd7d82
BuildArch:      x86_64
Requires:       dotnet-runtime icu

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%autosetup -c dotnet-sdk-%{version}

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet/sdk
mkdir -p %{buildroot}%{_docdir}/dotnet-sdk-%{version}
cp -r sdk/%{version} %{buildroot}%{_libdir}/dotnet/sdk
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/dotnet-sdk-%{version}

%files
    %defattr(-,root,root,0755)
    %{_libdir}/*
    %{_docdir}/*

%changelog
*   Tue Sep 21 2021 Shreyas B. <shreyasb@vmware.com> 5.0.400-1
-   upgrade to v5.0.400
*   Mon Jan 18 2021 Shreyas B. <shreyasb@vmware.com> 5.0.103-1
-   upgrade to version 5.0.103
*   Fri Oct 16 2020 Ashwin H <ashwinh@vmware.com> 3.1.201-2
-   Bump up to use new icu lib.
*   Sat Apr 11 2020 Shreyas B. <shreyasb@vmware.com> 3.1.201-1
-   upgrade to version 3.1.201
*   Thu Nov 07 2019 Shreyas B. <shreyasb@vmware.com> 2.1.509-1
-   upgraded to version 2.1.509
*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.1.403-1
-   upgraded to version 2.1.403
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.4-1
-   Initial build for photon
