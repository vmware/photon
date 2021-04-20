Summary:	Library that Implements a typesafe callback system for standard C++.
Name:		libsigc++
Version:	3.0.4
Release:	2%{?dist}
License:	LGPLv2+
URL:		http://libsigc.sourceforge.net
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.99/%{name}-%{version}.tar.xz
%define sha1    libsigc=cdf724ac91e4b41fb8b7539b6bd6360cb1bcfe43
BuildRequires:  mm-common
BuildRequires:  libxslt
BuildRequires:  doxygen

%description
It allows to define signals and to connect those signals to any callback function,
either global or a member function, regardless of whether it is static or virtual.
It also contains adaptor classes for connection of dissimilar callbacks,
and has an ease of use unmatched by other C++ callback libraries.

%prep
%setup -q

%build
./autogen.sh --prefix=%{_prefix}
%configure --disable-documentation
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/sigc++-3.0/include/*.h
%{_includedir}/*

%changelog
*   Tue Apr 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.0.4-2
-   Fix build errors
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.4-1
-   Automatic Version Bump
*   Thu May 25 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.10.0-1
-   Revert back to the stable version 2.10.0-1
*   Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 2.99.8-1
-   Updated to version 2.99.8
*   Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 2.10.0-1
-   Updated to version 2.10.0
*   Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.8.0-1
-   Updated to version 2.8.0-1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.6.2-2
-   GA - Bump release of all rpms
*   Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 2.6.2-1
-   Updated to version 2.6.2
*   Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.4.0-1
-   Initial version
