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
Source0:        https://download.microsoft.com/download/A/7/8/A78F1D25-8D5C-4411-B544-C7D527296D5E/%{name}-%{version}-linux-x64.tar.gz
%define sha1    dotnet-runtime=7f9815101143463f2d244fa15c51cc9098328920
Requires:       curl libunwind krb5 lttng-ust

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%setup -c %{name}-%{version}

%build

%install
mkdir -p %{buildroot}%{_libdir}/dotnet
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/%{name}-%{version}
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
*   Mon Jan 14 2019 Dweep Advani <dadvani@vmware.com> 2.2.0-1
-   Upgraded to version 2.2.0
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.5-1
-   Initial build for photon
