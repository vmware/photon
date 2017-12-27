Summary:	redis database
Name:		redis
Version:	4.0.6
Release:	1%{?dist}
Vendor:		VMware, Inc.
Distribution:	Photon
License:	BSD
Url:		http://redis.io
Group:		Applications/Database

Source0:	%{name}-%{version}.tar.gz
%define sha1 redis=9097893771863d56a69dbf233c6c97a78aaddedf

%description
Redis is an in-memory database that persists on disk. The data model is key-value, but many different kind of values are supported: Strings, Lists, Sets, Sorted Sets, Hashes, HyperLogLogs, Bitmaps.

%prep
%setup -q

%build
cd src
make OPTIMIZATION="-g" %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_prefix}
make PREFIX=%{buildroot}%{_prefix} install

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
    %defattr(-,root,root)
    %{_bindir}/*

%changelog
*       Wed Dec 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.0.6-1
-       Initial build for photon.
