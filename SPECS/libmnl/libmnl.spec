Summary:    Netlink helper library
Name:       libmnl
Version:    1.0.4
Release:    1%{?dist}
License:    LGPLv2+
URL:        http://www.netfilter.org/projects/libmnl/index.html
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha1 libmnl=2db40dea612e88c62fd321906be40ab5f8f1685a


%description
libmnl is a minimalistic user-space library oriented to Netlink developers. There are a lot of common tasks in parsing, validating, constructing of both the Netlink header and TLVs that are repetitive and easy to get wrong.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libmnl-devel package contains libraries and header files for libmnl


%package 	static
Summary:        Static development files for %{name}
Group:          Development/Libraries
Requires: %{name} = %{version}-%{release}

%description 	static
The libmnl-static package contains static libraries for libmnl.

%prep
%setup -q

%build
%configure --enable-static
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%doc examples
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so

%files static
%{_libdir}/*.a

%changelog
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.4-1
-   Initial packaging


