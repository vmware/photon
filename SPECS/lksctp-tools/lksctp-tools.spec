Summary:       User-space access to Linux Kernel SCTP
Name:          lksctp-tools
Version:       1.0.19
Release:       1%{?dist}
License:       LGPL
Group:         System Environment/Libraries
URL:           http://lksctp.sourceforge.net
Source0:       %{name}-%{version}.tar.gz
Vendor:        VMware, Inc.
Distribution:  Photon
%define sha1   lksctp-tools=d410a596485c38464177a38ae7c7081444e6589e
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: automake
BuildRequires: autoconf

%description
This is the lksctp-tools package for Linux Kernel SCTP Reference
Implementation.
This package contains the base run-time library & command-line tools.

%package       devel
Summary:       Development kit for lksctp-tools
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      glibc-devel

%description   devel
Development kit for lksctp-tools

%package       doc
Summary:       Documents pertaining to SCTP
Group:         System Environment/Libraries
Requires:      %{name} = %{version}-%{release}

%description   doc
Documents pertaining to LKSCTP & SCTP in general

%prep
%setup -q

%build
autoreconf -i
%configure --enable-shared --enable-static
make

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog COPYING.lib
%{_bindir}/*
%{_libdir}/libsctp.so.*
%{_libdir}/%{name}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}
%{_libdir}/libsctp.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libsctp.a
%{_libdir}/libsctp.la
%{_datadir}/%{name}/*
%{_mandir}/*

%files doc
%defattr(-,root,root,-)
%doc doc/*.txt

%changelog
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.0.19-1
- Automatic Version Bump
* Mon Jun 15 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.0.18-2
- Fix packaging of sctp.h header
* Thu Dec 26 2019 Anish Swaminathan <anishs@vmware.com> 1.0.18-1
- Initial packaging
