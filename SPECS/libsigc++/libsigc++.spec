Summary:    Library that Implements a typesafe callback system for standard C++.
Name:       libsigc++
Version:    3.0.4
Release:    4%{?dist}
License:    LGPLv2+
URL:        http://libsigc.sourceforge.net
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/3.0/%{name}-%{version}.tar.xz
%define sha512 libsigc=b84ae7da6708e02302d08e295d6a566f12fb2c6f0d02f811661a0a541d7969e96a1e920218394dd109b3f362d102f2956aa968539710fa180d7d97e9676fb83d

BuildRequires:  mm-common
BuildRequires:  libxslt-devel
BuildRequires:  doxygen

Requires: pkg-config
Requires: libgcc
Requires: libstdc++

%description
It allows to define signals and to connect those signals to any callback function,
either global or a member function, regardless of whether it is static or virtual.
It also contains adaptor classes for connection of dissimilar callbacks,
and has an ease of use unmatched by other C++ callback libraries.

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

%clean
rm -rf %{buidlroot}/*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/sigc++-3.0/include/*.h
%{_includedir}/*

%changelog
* Fri May 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.4-4
- Fix requires
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.4-3
- Remove .la files
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
