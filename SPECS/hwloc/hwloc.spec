Summary:        Portable Hardware Locality
Name:           hwloc
Version:        2.2.0
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD
Url:            http://www.open-mpi.org/projects/hwloc/
Group:          Applications/Utilities
Source0:        %{name}-%{version}.tar.bz2
%define sha1    hwloc=1b87ff3820b28e718dfdca626a1d27521ea613f6

%description
The Portable Hardware Locality (hwloc) software package provides a portable abstraction (across OS, versions, architectures, ...) of the hierarchical topology of modern architectures, including NUMA memory nodes, sockets, shared caches, cores and simultaneous multithreading. It also gathers various system attributes such as cache and memory information as well as the locality of I/O devices such as network interfaces, InfiniBand HCAs or GPUs.

%package devel
Summary:  Development libraries for hwloc
Requires: %{name} = %{version}-%{release}

%description devel
Development libraries for hwloc

%package docs
Summary: Documentation for hwloc
Requires: %{name} = %{version}-%{release}

%description docs
Documentation for hwloc

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

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

%clean
rm -rf %{buildroot}/*

%files
    %defattr(-,root,root)
    %{_bindir}/*
    %ifarch x86_64
    %{_sbindir}/*
    %endif
    %{_libdir}/*.so.*
    %{_sysconfdir}/bash_completion.d/hwloc-completion.bash

%files devel
    %defattr(-,root,root)
    %{_includedir}/*
    %{_libdir}/*.so
    %{_libdir}/pkgconfig/*.pc

%files docs
    %defattr(-,root,root)
    %{_mandir}/*
    %{_docdir}/*
    %{_datadir}/%{name}/*

%changelog
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.0-1
- Automatic Version Bump
* Tue Jul 14 2020 Michelle Wang <michellew@vmware.com> 2.1.0-2
- exclude %{_sbindir}/* hwloc aarch64 rpm
* Mon Nov 25 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-1
- Initial build.  First version
