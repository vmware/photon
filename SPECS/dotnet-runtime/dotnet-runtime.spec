%global debug_package %{nil}

Summary:        Microsoft .NET Core Runtime
Name:           dotnet-runtime
Version:        5.0.3
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools
BuildArch:      x86_64
Source0:        %{name}-%{version}-linux-x64.tar.gz
%define sha1    dotnet-runtime=b995c64c9477b493c9f018404278ca4543e6a0ec
Requires:       curl libunwind krb5 lttng-ust

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%setup -c dotnet-runtime-%{version}

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet
mkdir -p %{buildroot}%{_docdir}/dotnet-runtime-%{version}
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/dotnet-runtime-%{version}
rm LICENSE.txt ThirdPartyNotices.txt
cp -r * %{buildroot}%{_libdir}/dotnet
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libdir}/dotnet/dotnet %{buildroot}%{_bindir}/dotnet

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig

# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

# Post-uninstall
%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%files
    %defattr(-,root,root,0755)
    %exclude %{_libdir}/debug
    %{_docdir}/*
    %{_bindir}/dotnet
    %{_libdir}/*

%changelog
*   Mon Jan 18 2021 Shreyas B. <shreyasb@vmware.com> 5.0.3-1
-   Upgrade to v5.0.3
*   Fri Aug 07 2020 Shreyas B. <shreyasb@vmware.com> 3.1.6-1
-   Upgrade to latest v3.1.6 to address CVE-2020-1147, CVE-2020-1108, CVE-2020-1066
*   Sat Apr 11 2020 Shreyas B. <shreyasb@vmware.com> 3.1.3-1
-   Upgrade to v3.1.3
*   Mon Nov 11 2019 Shreyas B. <shreyasb@vmware.com> 2.2.3-1
-   Upgraded to v2.2.3
*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.2.0-1
-   upgraded to version 2.2.0
*   Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 2.1.4-1
-   upgraded to version 2.1.4
-   add aarch64 support
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.5-1
-   Initial build for photon
