%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pygobject
Version:        3.24.0
Release:	1%{?dist}
Summary:        Python Bindings for GObject
Group:          Development/Languages
License:        LGPLv2+
Vendor:		VMware, Inc.
Distribution:	Photon
URL:            http://ftp.gnome.org
Source0:        http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.24/pygobject-3.24.0.tar.xz
%define sha1 pygobject=a9b58dcbc58b1b8f671095fc48956e4c67e5846b
Requires:	python2
Requires:	gobject-introspection
Requires:	glib-devel
Provides:	pygobject
BuildRequires: 	python2-devel
BuildRequires: 	python2-libs
BuildRequires: 	gobject-introspection-devel
BuildRequires: 	glib-devel

%description
Python2 and python3  bindings for GLib and GObject.

%package -n     pygobject3
Summary:        pygobject3
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n pygobject3

Python 3 version.

%prep
%setup -q -n pygobject-%{version}

%build
./configure --prefix=/usr --disable-cairo --without-cairo
make

%install
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/python*/*
%{_includedir}/*

%files -n pygobject3
%defattr(-,root,root,-)

%changelog
*       Wed Mar 29 2017 Rongrong Qiu <rqiu@vmware.com> 3.24.0-1
-       Upgrade to 3.24.0 and add pygobject3 for python3
*       Mon Oct 03 2016 ChangLee <changLee@vmware.com> 3.10.2-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.10.2-2
-	GA - Bump release of all rpms
*	Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
-	Initial build.	First version
