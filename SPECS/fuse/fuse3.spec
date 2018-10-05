Summary:        File System in Userspace (FUSE) utilities
Name:           fuse3
Version:        3.0.1
Release:        2%{?dist}
License:        GPL+
URL:            http://fuse.sourceforge.net/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/libfuse/libfuse/releases/download/fuse-%{version}/fuse-%{version}.tar.gz
%define sha1    fuse=9362ce52c17c2865ba47f9d4fcb9f054c38bd1fc

%description
With FUSE3 it is possible to implement a fully functional filesystem in a
userspace program.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description    devel
It contains the libraries and header files to create fuse applications.

%prep
%setup -q -n fuse-%{version}

%build
%configure --disable-static INIT_D_PATH=/tmp/init.d &&
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
make install \
    prefix=%{buildroot}%{_prefix}

install -v -m755 -d /usr/share/doc/%{name}-%{version} &&
install -v -m644    doc/kernel.txt \
                    /usr/share/doc/%{name}-%{version}
find %{buildroot} -name '*.la' -delete

%files
%defattr(-, root, root)
%{_libdir}/libfuse3.so.*
%{_libdir}/udev/rules.d/*
%{_bindir}/*
%{_datadir}/man/*
%{_sbindir}/mount.fuse3

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/fuse3.pc
%{_libdir}/libfuse3.so

%changelog
*   Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.1-2
-   Move pkgconfig folder to devel package.
*   Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 3.0.1-1
-   Initial version.
