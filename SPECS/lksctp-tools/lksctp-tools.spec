Summary:       User-space access to Linux Kernel SCTP
Name:          lksctp-tools
Version:       1.0.19
Release:       3%{?dist}
Group:         System Environment/Libraries
URL:           http://lksctp.sourceforge.net
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/sctp/lksctp-tools/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=e56a4b00206acfb88cab1b8fc7424a1a4996f67ef925c29a97395c44c57f2cbcb3fc36ec2648f5e5a5ce29d8d61ee1f7a5e7869e6bbd68bff85590b6ec521883

Source1: license.txt
%include %{SOURCE1}

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
%autosetup -p1

%build
autoreconf -i
%configure --enable-shared --enable-static
%make_build

%install
%make_install %{?_smp_mflags}

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
%{_datadir}/%{name}/*
%{_mandir}/*

%files doc
%defattr(-,root,root,-)
%doc doc/*.txt

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.0.19-3
- Release bump for SRP compliance
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.19-2
- Remove .la files
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.0.19-1
- Automatic Version Bump
* Mon Jun 15 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.0.18-2
- Fix packaging of sctp.h header
* Thu Dec 26 2019 Anish Swaminathan <anishs@vmware.com> 1.0.18-1
- Initial packaging
