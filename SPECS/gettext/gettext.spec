Summary:	Utilities for internationalization and localization
Name:		gettext
Version:	0.18.3.2
Release:	1%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/gettext
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.gz
%define sha1 gettext=a2dc46d788edb0078ab20da7bd194bdb6da2f0d9
%description
These allow programs to be compiled with NLS
(Native Language Support), enabling them to output
messages in the user's native language.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/usr/share/doc/gettext-%{version}/examples
rm -rf %{buildroot}%{_infodir}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/gettext/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a
%{_datarootdir}/aclocal/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%lang(be) %{_datarootdir}/locale/be/LC_MESSAGES/gettext-runtime.mo
%lang(be) %{_datarootdir}/locale/be/LC_MESSAGES/gettext-tools.mo
%lang(bg) %{_datarootdir}/locale/bg/LC_MESSAGES/gettext-runtime.mo
%lang(bg) %{_datarootdir}/locale/bg/LC_MESSAGES/gettext-tools.mo
%lang(ca) %{_datarootdir}/locale/ca/LC_MESSAGES/gettext-runtime.mo
%lang(ca) %{_datarootdir}/locale/ca/LC_MESSAGES/gettext-tools.mo
%lang(cs) %{_datarootdir}/locale/cs/LC_MESSAGES/gettext-runtime.mo
%lang(cs) %{_datarootdir}/locale/cs/LC_MESSAGES/gettext-tools.mo
%lang(da) %{_datarootdir}/locale/da/LC_MESSAGES/gettext-runtime.mo
%lang(da) %{_datarootdir}/locale/da/LC_MESSAGES/gettext-tools.mo
%lang(de) %{_datarootdir}/locale/de/LC_MESSAGES/gettext-runtime.mo
%lang(de) %{_datarootdir}/locale/de/LC_MESSAGES/gettext-tools.mo
%lang(el) %{_datarootdir}/locale/el/LC_MESSAGES/gettext-runtime.mo
%lang(el) %{_datarootdir}/locale/el/LC_MESSAGES/gettext-tools.mo
%lang(en@boldquot) %{_datarootdir}/locale/en@boldquot/LC_MESSAGES/gettext-runtime.mo
%lang(en@boldquot) %{_datarootdir}/locale/en@boldquot/LC_MESSAGES/gettext-tools.mo
%lang(en@quot) %{_datarootdir}/locale/en@quot/LC_MESSAGES/gettext-runtime.mo
%lang(en@quot) %{_datarootdir}/locale/en@quot/LC_MESSAGES/gettext-tools.mo
%lang(eo) %{_datarootdir}/locale/eo/LC_MESSAGES/gettext-runtime.mo
%lang(es) %{_datarootdir}/locale/es/LC_MESSAGES/gettext-runtime.mo
%lang(es) %{_datarootdir}/locale/es/LC_MESSAGES/gettext-tools.mo
%lang(et) %{_datarootdir}/locale/et/LC_MESSAGES/gettext-runtime.mo
%lang(et) %{_datarootdir}/locale/et/LC_MESSAGES/gettext-tools.mo
%lang(eu) %{_datarootdir}/locale/eu/LC_MESSAGES/gettext-tools.mo
%lang(fi) %{_datarootdir}/locale/fi/LC_MESSAGES/gettext-runtime.mo
%lang(fi) %{_datarootdir}/locale/fi/LC_MESSAGES/gettext-tools.mo
%lang(fr) %{_datarootdir}/locale/fr/LC_MESSAGES/gettext-runtime.mo
%lang(fr) %{_datarootdir}/locale/fr/LC_MESSAGES/gettext-tools.mo
%lang(ga) %{_datarootdir}/locale/ga/LC_MESSAGES/gettext-runtime.mo
%lang(gl) %{_datarootdir}/locale/gl/LC_MESSAGES/gettext-runtime.mo
%lang(gl) %{_datarootdir}/locale/gl/LC_MESSAGES/gettext-tools.mo
%lang(hr) %{_datarootdir}/locale/hr/LC_MESSAGES/gettext-runtime.mo
%lang(id) %{_datarootdir}/locale/id/LC_MESSAGES/gettext-runtime.mo
%lang(id) %{_datarootdir}/locale/id/LC_MESSAGES/gettext-tools.mo
%lang(it) %{_datarootdir}/locale/it/LC_MESSAGES/gettext-runtime.mo
%lang(it) %{_datarootdir}/locale/it/LC_MESSAGES/gettext-tools.mo
%lang(ja) %{_datarootdir}/locale/ja/LC_MESSAGES/gettext-runtime.mo
%lang(ja) %{_datarootdir}/locale/ja/LC_MESSAGES/gettext-tools.mo
%lang(ko) %{_datarootdir}/locale/ko/LC_MESSAGES/gettext-runtime.mo
%lang(ko) %{_datarootdir}/locale/ko/LC_MESSAGES/gettext-tools.mo
%lang(nb) %{_datarootdir}/locale/nb/LC_MESSAGES/gettext-runtime.mo
%lang(nb) %{_datarootdir}/locale/nb/LC_MESSAGES/gettext-tools.mo
%lang(nl) %{_datarootdir}/locale/nl/LC_MESSAGES/gettext-runtime.mo
%lang(nl) %{_datarootdir}/locale/nl/LC_MESSAGES/gettext-tools.mo
%lang(nn) %{_datarootdir}/locale/nn/LC_MESSAGES/gettext-runtime.mo
%lang(nn) %{_datarootdir}/locale/nn/LC_MESSAGES/gettext-tools.mo
%lang(pa) %{_datarootdir}/locale/pa/LC_MESSAGES/gettext-tools.mo
%lang(pl) %{_datarootdir}/locale/pl/LC_MESSAGES/gettext-runtime.mo
%lang(pl) %{_datarootdir}/locale/pl/LC_MESSAGES/gettext-tools.mo
%lang(pt) %{_datarootdir}/locale/pt/LC_MESSAGES/gettext-runtime.mo
%lang(pt) %{_datarootdir}/locale/pt/LC_MESSAGES/gettext-tools.mo
%lang(pt_BR) %{_datarootdir}/locale/pt_BR/LC_MESSAGES/gettext-runtime.mo
%lang(pt_BR) %{_datarootdir}/locale/pt_BR/LC_MESSAGES/gettext-tools.mo
%lang(ro) %{_datarootdir}/locale/ro/LC_MESSAGES/gettext-runtime.mo
%lang(ro) %{_datarootdir}/locale/ro/LC_MESSAGES/gettext-tools.mo
%lang(ru) %{_datarootdir}/locale/ru/LC_MESSAGES/gettext-runtime.mo
%lang(ru) %{_datarootdir}/locale/ru/LC_MESSAGES/gettext-tools.mo
%lang(sk) %{_datarootdir}/locale/sk/LC_MESSAGES/gettext-runtime.mo
%lang(sk) %{_datarootdir}/locale/sk/LC_MESSAGES/gettext-tools.mo
%lang(sl) %{_datarootdir}/locale/sl/LC_MESSAGES/gettext-runtime.mo
%lang(sl) %{_datarootdir}/locale/sl/LC_MESSAGES/gettext-tools.mo
%lang(sr) %{_datarootdir}/locale/sr/LC_MESSAGES/gettext-runtime.mo
%lang(sr) %{_datarootdir}/locale/sr/LC_MESSAGES/gettext-tools.mo
%lang(sv) %{_datarootdir}/locale/sv/LC_MESSAGES/gettext-runtime.mo
%lang(sv) %{_datarootdir}/locale/sv/LC_MESSAGES/gettext-tools.mo
%lang(tr) %{_datarootdir}/locale/tr/LC_MESSAGES/gettext-runtime.mo
%lang(tr) %{_datarootdir}/locale/tr/LC_MESSAGES/gettext-tools.mo
%lang(uk) %{_datarootdir}/locale/uk/LC_MESSAGES/gettext-runtime.mo
%lang(uk) %{_datarootdir}/locale/uk/LC_MESSAGES/gettext-tools.mo
%lang(vi) %{_datarootdir}/locale/vi/LC_MESSAGES/gettext-runtime.mo
%lang(vi) %{_datarootdir}/locale/vi/LC_MESSAGES/gettext-tools.mo
%lang(zh_CN) %{_datarootdir}/locale/zh_CN/LC_MESSAGES/gettext-runtime.mo
%lang(zh_CN) %{_datarootdir}/locale/zh_CN/LC_MESSAGES/gettext-tools.mo
%lang(zh_HK) %{_datarootdir}/locale/zh_HK/LC_MESSAGES/gettext-runtime.mo
%lang(zh_TW) %{_datarootdir}/locale/zh_TW/LC_MESSAGES/gettext-runtime.mo
%lang(zh_TW) %{_datarootdir}/locale/zh_TW/LC_MESSAGES/gettext-tools.mo
%{_mandir}/*/*
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 0.18.3.2-1
-	Initial build. First version
