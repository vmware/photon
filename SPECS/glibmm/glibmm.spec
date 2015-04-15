Summary:	My summary.
Name:		glibmm
Version:	2.42.0
Release:	1
License:	LGPLv2+
URL:		http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.42/glibmm-2.42.0.tar.xz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.42/%{name}-%{version}.tar.xz
BuildRequires:	python2 >= 2.7
BuildRequires:	libsigc++
BuildRequires:	glib-devel
Requires:	libsigc++
Requires:	glib-devel
Requires:	XML-Parser

%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps GTK+ 2.
Highlights include typesafe callbacks, widgets extensible via inheritance and 
a comprehensive set of widget classes that can be freely combined to quickly create complex user interfaces.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir}/glibmm-2.4/proc/*
%{_libdir}/glibmm-2.4/include/*
%{_libdir}/giomm-2.4/include/*
%{_includedir}/*
%{_datadir}/*
%changelog
*	Thu Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.42.0-1
	Initial version
