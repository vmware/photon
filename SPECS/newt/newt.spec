Summary:	A library for text mode user interfaces
Name:		newt
Version:	0.52.18
Release:	2%{?dist}
License:	GNU Library General Public License
URL:		https://admin.fedoraproject.org/pkgdb/package/newt/
Group:		Development/Languages
Source0:	https://fedorahosted.org/releases/n/e/newt/%{name}-%{version}.tar.gz
%define sha1 newt=2992c926bd3699ff0d6fd7549d4a8a018e3ac8fd  
Vendor:		VMware, Inc.
Distribution:	Photon
Requires: slang
BuildRequires: slang-devel
BuildRequires: popt-devel
%description

Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package also contains the
shared library needed by programs built with newt, as well as a
/usr/bin/dialog replacement called whiptail.  Newt is based on the
slang library.

%package	devel
Summary:	Header and development files for ncurses
Requires:	%{name} = %{version}

%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q -n %{name}-%{version}
%build
./configure --prefix=/usr --with-gpm-support --without-python
make
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%{_libdir}/libnewt.so.0*
%{_bindir}/*
%{_datadir}/*


%files devel
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/libnewt.so
%{_libdir}/pkgconfig/*.pc

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.52.18-2
-	GA - Bump release of all rpms
*	Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-	Initial build.	First version
