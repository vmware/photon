Summary:	Reading, writing, and converting info pages
Name:		texinfo
Version:	5.2
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/texinfo/
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	%{name}-%{version}.tar.xz
%define sha1 texinfo=fbbc35c5857d11d1164c8445c78b66ad6d472072
%description
The Texinfo package contains programs for reading, writing,
and converting info pages.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} TEXMF=%{_datarootdir}/texmf install-tex
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%dir %{_datarootdir}/texinfo
%{_datarootdir}/texinfo/*
%dir %{_datarootdir}/texmf
%{_datarootdir}/texmf/*
%lang(de.us-ascii) %{_datarootdir}/locale/de.us-ascii/LC_MESSAGES/texinfo_document.mo
%lang(eo) %{_datarootdir}/locale/eo/LC_MESSAGES/texinfo_document.mo
%lang(es.us-ascii) %{_datarootdir}/locale/es.us-ascii/LC_MESSAGES/texinfo_document.mo
%lang(fr) %{_datarootdir}/locale/fr/LC_MESSAGES/texinfo_document.mo
%lang(hu) %{_datarootdir}/locale/hu/LC_MESSAGES/texinfo_document.mo
%lang(it) %{_datarootdir}/locale/it/LC_MESSAGES/texinfo_document.mo
%lang(nl) %{_datarootdir}/locale/nl/LC_MESSAGES/texinfo_document.mo
%lang(no.us-ascii) %{_datarootdir}/locale/no.us-ascii/LC_MESSAGES/texinfo_document.mo
%lang(pl) %{_datarootdir}/locale/pl/LC_MESSAGES/texinfo_document.mo
%lang(pt.us-ascii) %{_datarootdir}/locale/pt.us-ascii/LC_MESSAGES/texinfo_document.mo
%lang(pt_BR.us-ascii) %{_datarootdir}/locale/pt_BR.us-ascii/LC_MESSAGES/texinfo_document.mo
%changelog
*	Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 5.2-2
-	Removing perl-libintl package from run-time required packages
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2-1
-	Upgrade version
