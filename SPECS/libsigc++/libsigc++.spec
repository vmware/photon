Summary:    Library that Implements a typesafe callback system for standard C++.
Name:       libsigc++
Version:    2.10.0
Release:    2%{?dist}
License:    LGPLv2+
URL:        http://libsigc.sourceforge.net
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.99/%{name}-%{version}.tar.xz
%define sha512 libsigc=5b96df21d6bd6ba41520c7219e77695a86aabc60b7259262c7a9f4b8475ce0e2fd8dc37bcf7c17e24e818ff28c262d682b964c83e215b51bdbe000f3f58794ae

%description
It allows to define signals and to connect those signals to any callback function, either global or a member function, regardless of whether it is static or virtual. It also contains adaptor classes for connection of dissimilar callbacks and has an ease of use unmatched by other C++ callback libraries.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/sigc++-2.0/include/*.h
%{_includedir}/*
%{_datadir}/*

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.10.0-2
- Remove .la files
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
