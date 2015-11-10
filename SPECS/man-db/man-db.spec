Summary:	Programs for finding and viewing man pages
Name:		man-db
Version:	2.6.6
Release:	2%{?dist}
License:	GPLv2+
URL:		http://www.nongnu.org/man-db
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		%{name}-%{version}.tar.xz
%define sha1 man-db=ba27924ef024527ad562017d956ffd3375bccc8d
Requires:	libpipeline
Requires:	gdbm
Requires:	xz
Requires: 	groff
BuildRequires:	libpipeline
BuildRequires:	gdbm
BuildRequires:	xz
BuildRequires: 	groff
%description
The Man-DB package contains programs for finding and viewing man pages.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--sysconfdir=%{_sysconfdir} \
	--disable-setuid \
	--with-browser=%{_bindir}/lynx \
	--with-vgrind=%{_bindir}/vgrind \
	--with-grap=%{_bindir}/grap \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
%find_lang %{name} --all-name
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
%{_sysconfdir}/man_db.conf
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/man-db/*
%{_libdir}/man-db/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%changelog
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.6.6-2
-	Handled locale files with macro find_lang
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.6.6-1
-	Initial build. First version
