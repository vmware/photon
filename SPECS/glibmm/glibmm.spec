Summary:	C++ interface to the glib
Name:		glibmm
Version:	2.48.1
Release:	2%{?dist}
License:	LGPLv2+
URL:		http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.46/glibmm-2.46.3.tar.xz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.46/%{name}-%{version}.tar.xz
%define sha1 glibmm=41e4d148da88e458889044421e31b1eaa35d8b0b
BuildRequires:	python2 >= 2.7
BuildRequires:	libsigc++
BuildRequires:	glib-devel glib-schemas
Requires:	libsigc++
Requires:	glib
Requires:	XML-Parser

%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps GTK+ 2.
Highlights include typesafe callbacks, widgets extensible via inheritance and 
a comprehensive set of widget classes that can be freely combined to quickly create complex user interfaces.

%package devel
Summary: Header files for glibmm
Group: Applications/System
Requires: %{name} = %{version}
Requires:	glib-devel libsigc++ 
%description devel
These are the header files of glibmm.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make  %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/glibmm-2.4/proc/*
%files devel 
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/glibmm-2.4/include/*
%{_libdir}/giomm-2.4/include/*
%{_includedir}/*
%{_datadir}/*

%changelog
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.48.1-2
-   Modified %check
*   Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.48.1-1
-   Updated to version 2.48.1-1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.47.3.1-2
-   GA - Bump release of all rpms
*   Thu Apr 14 2016	Harish Udaiya Kumar<hudaiyakumar@vmware.com> 2.47.3.1-1
    Updated to version 2.47.3.1
*   Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 2.46.3-1
-   Updated to version 2.46.3
*	Tue Jul 7 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-3
	Created devel subpackage. Added Summary.
*	Tue Jun 23 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-2
	Added glib-schemas to build requirements.
*	Thu Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.42.0-1
	Initial version
