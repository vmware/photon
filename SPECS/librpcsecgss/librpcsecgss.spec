Summary:        This library implements rpcsec_gss
Name:           librpcsecgss
Version:        0.19
Release:        3%{?dist}
License:        BSD
URL:            http://www.citi.umich.edu/projects/nfsv4/linux/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.citi.umich.edu/projects/nfsv4/linux/librpcsecgss/%{name}-%{version}.tar.gz
%define sha1    librpcsecgss=28522737949977d9733e876c91ccea5ce6b1f58b
BuildRequires:  libgssglue-devel
BuildRequires:  libtirpc-devel

%description
This library implements rpcsec_gss (RFC 2203) which allows secure rpc
communication using gss-api security mechanisms.
%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
Requires:       libtirpc-devel
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q
%build
%configure --prefix=/usr --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete

%post

%files
%defattr(-,root,root)
%{_libdir}/librpcsecgss.so.*

%files  devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/librpcsecgss.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 0.19-3
-   Use libtirpc instead of glibc/rpc.
*   Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> 0.19-2
-   Resolved compilation error for aarch64
*   Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 0.19-1
-   Initial build. First version
