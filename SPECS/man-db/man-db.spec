Summary:	Programs for finding and viewing man pages
Name:		man-db
Version:	2.7.5
Release:	1%{?dist}
License:	GPLv2+
URL:		http://www.nongnu.org/man-db
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		%{name}-%{version}.tar.gz
%define sha1 man-db=dbd822f8c6743da9fad95e0bac919b8f844d9264
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
%{_libdir}/tmpfiles.d/man-db.conf
%changelog
*       Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 2.7.5-1
-       Updated to new version.
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.6.6-2
-	Handled locale files with macro find_lang
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.6.6-1
-	Initial build. First version
