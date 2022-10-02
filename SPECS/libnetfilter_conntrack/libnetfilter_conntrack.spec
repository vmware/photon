Summary:    Netfilter conntrack userspace library
Name:       libnetfilter_conntrack
Version:    1.0.8
Release:    2%{?dist}
License:    GPLv2+
URL:        http://www.netfilter.org/projects/libnetfilter_conntrack/index.html
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha512  %{name}=ddc70e7e3f2d764ed1e115e4a03fe8848b8c04bd69eea0952e63131dd4dae3c23f33b8be518673e1ec3b5dbf708f5f86eac97be46fe265d95386a5e902bd0b82

BuildRequires:  libmnl-devel
BuildRequires:  libnfnetlink-devel
BuildRequires:  linux-api-headers

%description
libnetfilter_conntrack is a userspace library providing a programming interface (API) to the in-kernel connection tracking state table. The library libnetfilter_conntrack has been previously known as libnfnetlink_conntrack and libctnetlink.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libnfnetlink-devel
Requires:       linux-api-headers

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.8-2
- Remove .la files
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.8-1
- Automatic Version Bump
* Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 1.0.7-1
- Update to 1.0.7
* Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.6-1
- Initial packaging
