Summary:	Programs for finding and viewing man pages
Name:		man-db
Version:	2.6.6
Release:	1%{?dist}
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
%find_lang %{name}
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
%lang(af) %{_datarootdir}/locale/af/LC_MESSAGES/man-db-gnulib.mo
%lang(be) %{_datarootdir}/locale/be/LC_MESSAGES/man-db-gnulib.mo
%lang(bg) %{_datarootdir}/locale/bg/LC_MESSAGES/man-db-gnulib.mo
%lang(ca) %{_datarootdir}/locale/ca/LC_MESSAGES/man-db-gnulib.mo
%lang(cs) %{_datarootdir}/locale/cs/LC_MESSAGES/man-db-gnulib.mo
%lang(da) %{_datarootdir}/locale/da/LC_MESSAGES/man-db-gnulib.mo
%lang(de) %{_datarootdir}/locale/de/LC_MESSAGES/man-db-gnulib.mo
%lang(de) %{_datarootdir}/locale/eo/LC_MESSAGES/man-db-gnulib.mo
%lang(el) %{_datarootdir}/locale/el/LC_MESSAGES/man-db-gnulib.mo
%lang(es) %{_datarootdir}/locale/es/LC_MESSAGES/man-db-gnulib.mo
%lang(et) %{_datarootdir}/locale/et/LC_MESSAGES/man-db-gnulib.mo
%lang(eu) %{_datarootdir}/locale/eu/LC_MESSAGES/man-db-gnulib.mo
%lang(fi) %{_datarootdir}/locale/fi/LC_MESSAGES/man-db-gnulib.mo
%lang(fr) %{_datarootdir}/locale/fr/LC_MESSAGES/man-db-gnulib.mo
%lang(ga) %{_datarootdir}/locale/ga/LC_MESSAGES/man-db-gnulib.mo
%lang(gl) %{_datarootdir}/locale/gl/LC_MESSAGES/man-db-gnulib.mo
%lang(hu) %{_datarootdir}/locale/hu/LC_MESSAGES/man-db-gnulib.mo
%lang(it) %{_datarootdir}/locale/it/LC_MESSAGES/man-db-gnulib.mo
%lang(ja) %{_datarootdir}/locale/ja/LC_MESSAGES/man-db-gnulib.mo
%lang(ko) %{_datarootdir}/locale/ko/LC_MESSAGES/man-db-gnulib.mo
%lang(ms) %{_datarootdir}/locale/ms/LC_MESSAGES/man-db-gnulib.mo
%lang(nb) %{_datarootdir}/locale/nb/LC_MESSAGES/man-db-gnulib.mo
%lang(nl) %{_datarootdir}/locale/nl/LC_MESSAGES/man-db-gnulib.mo
%lang(pl) %{_datarootdir}/locale/pl/LC_MESSAGES/man-db-gnulib.mo
%lang(pt) %{_datarootdir}/locale/pt/LC_MESSAGES/man-db-gnulib.mo
%lang(pt) %{_datarootdir}/locale/pt_BR/LC_MESSAGES/man-db-gnulib.mo
%lang(ro) %{_datarootdir}/locale/ro/LC_MESSAGES/man-db-gnulib.mo
%lang(ru) %{_datarootdir}/locale/ru/LC_MESSAGES/man-db-gnulib.mo
%lang(rw) %{_datarootdir}/locale/rw/LC_MESSAGES/man-db-gnulib.mo
%lang(sk) %{_datarootdir}/locale/sk/LC_MESSAGES/man-db-gnulib.mo
%lang(sl) %{_datarootdir}/locale/sl/LC_MESSAGES/man-db-gnulib.mo
%lang(sr) %{_datarootdir}/locale/sr/LC_MESSAGES/man-db-gnulib.mo
%lang(sv) %{_datarootdir}/locale/sv/LC_MESSAGES/man-db-gnulib.mo
%lang(tr) %{_datarootdir}/locale/tr/LC_MESSAGES/man-db-gnulib.mo
%lang(uk) %{_datarootdir}/locale/uk/LC_MESSAGES/man-db-gnulib.mo
%lang(vi) %{_datarootdir}/locale/vi/LC_MESSAGES/man-db-gnulib.mo
%lang(zh_CN) %{_datarootdir}/locale/zh_CN/LC_MESSAGES/man-db-gnulib.mo
%lang(zh_TW) %{_datarootdir}/locale/zh_TW/LC_MESSAGES/man-db-gnulib.mo
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.6.6-1
-	Initial build. First version
