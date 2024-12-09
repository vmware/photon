Summary:        Library that Implements a typesafe callback system for standard C++.
Name:           libsigc++
Version:        3.2.0
Release:        2%{?dist}
URL:            http://libsigc.sourceforge.net
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.99/%{name}-%{version}.tar.xz
%define sha512 libsigc=91315cecc79a1ad6ea165b66a13a5afd4e5bc101842f9d4c58811ea78536c07fc8821c51aa5110a032ed71c09f85790b3a02f2ad7fe8cc3aed6e03b2bafcd70c

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  mm-common
BuildRequires:  libxslt-devel
BuildRequires:  doxygen

Requires: libgcc

%description
It allows to define signals and to connect those signals to any callback function,
either global or a member function, regardless of whether it is static or virtual.
It also contains adaptor classes for connection of dissimilar callbacks,
and has an ease of use unmatched by other C++ callback libraries.

%package        devel
Summary:        Development & header files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
Development & header files for %{name}

%prep
%autosetup -p1

%build
sh ./autogen.sh --prefix=%{_prefix}
%configure --disable-documentation
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/sigc++-3.0/include/*.h
%{_includedir}/*

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.2.0-2
- Release bump for SRP compliance
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.0-1
- Upgrade to v3.2.0
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.4-5
- Bump version as a part of libxslt upgrade
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.4-4
- Remove .la files
- Introduce devel sub package
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.0.4-3
- Bump version as a part of libxslt upgrade
* Tue Apr 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.0.4-2
- Fix build errors
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.4-1
- Automatic Version Bump
* Thu May 25 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.10.0-1
- Revert back to the stable version 2.10.0-1
* Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 2.99.8-1
- Updated to version 2.99.8
* Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 2.10.0-1
- Updated to version 2.10.0
* Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.8.0-1
- Updated to version 2.8.0-1
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.6.2-2
- GA - Bump release of all rpms
* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 2.6.2-1
- Updated to version 2.6.2
* Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.4.0-1
- Initial version
