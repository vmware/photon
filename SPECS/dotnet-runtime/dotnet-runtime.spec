Summary:        Microsoft .NET Core Runtime
Name:           dotnet-runtime
Version:        2.2.0
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools
BuildArch:      x86_64

%ifarch x86_64
Source0:        https://download.microsoft.com/download/A/7/8/A78F1D25-8D5C-4411-B544-C7D527296D5E/dotnet-runtime-2.2.0-linux-x64.tar.gz
%define sha1    dotnet-runtime=7f9815101143463f2d244fa15c51cc9098328920
# BuildArch:      x86_64
%endif

%ifarch aarch64
Source0:        https://download.microsoft.com/download/A/7/8/A78F1D25-8D5C-4411-B544-C7D527296D5E/dotnet-runtime-2.1.4-linux-arm64.tar.gz
%define sha1    dotnet-runtime=0470e1ed3ab4cb3e3321f6dd11f9dc7abac171d6
# BuildArch:      aarch64
%endif

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
*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.2.0-1
-   upgraded to version 2.2.0
*   Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 2.1.4-1
-   upgraded to version 2.1.4
-   add aarch64 support
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.5-1
-   Initial build for photon
