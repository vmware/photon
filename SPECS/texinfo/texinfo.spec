Summary:        Reading, writing, and converting info pages
Name:           texinfo
Version:        7.0.2
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.gnu.org/software/texinfo
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/texinfo/%{name}-%{version}.tar.xz
%define sha512 %{name}=26dd5bb1392f2197ecde296ba157d4533f4b11fadf1238481da4cf2b3796c665ce96049df8d2f9a6d4fa22b7e9013d9978d195e525288663f0a54482bbc22b2b

BuildRequires:  perl

%description
The Texinfo package contains programs for reading, writing,
and converting info pages.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install %{?_smp_mflags}
%make_install TEXMF=%{_datadir}/texmf %{?_smp_mflags} install-tex
rm -rf %{buildroot}%{_infodir}

%find_lang %{name} --all-name

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%exclude %{_bindir}/pdftexi2dvi
%exclude %{_bindir}/texi2dvi
%exclude %{_bindir}/texi2pdf
%{_bindir}/info
%{_bindir}/install-info
%{_bindir}/makeinfo
%{_bindir}/pod2texi
%{_bindir}/texi2any
%{_bindir}/texindex
%{_mandir}/*/*
%dir %{_datadir}/texinfo
%{_datadir}/texinfo/*
%dir %{_datadir}/texmf
%{_datadir}/texmf/*
%{_libdir}/texinfo/*

%changelog
* Thu Feb 16 2023 Gerrit Photon <photon-checkins@vmware.com> 7.0.2-1
- Automatic Version Bump
* Thu Nov 10 2022 Dweep Advani <dadvani@vmware.com> 6.8-2
- Rebuild for perl version upgrade to 5.36.0
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 6.8-1
- Automatic Version Bump
* Mon Sep 21 2020 Dweep Advani <dadvani@vmware.com> 6.5-3
- Rebuild for perl upgrade to 5.30.1
* Fri Nov 02 2018 Anish Swaminathan <anishs@vmware.com> 6.5-2
- Fix texinfo issue with locales
- http://lists.gnu.org/archive/html/bug-texinfo/2018-06/msg00029.html
* Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 6.5-1
- Update version to 6.5.
* Fri May 05 2017 Xiaolin Li <xiaolinl@vmware.com> 6.3-3
- Excluded pdftexi2dvi, texi2dvi, texi2pdf from package,
- because these commands depend on installation of tex.
* Tue Apr 18 2017 Robert Qi <qij@vmware.com> 6.3-2
- Updated to version 6.3-2 due to perl build requires.
* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 6.3-1
- Updated to version 6.3.
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 6.1-4
- Modified %check
* Mon Jun 27 2016 Divya Thaluru <dthaluru@vmware.com> 6.1-3
- Removed packaging of debug files
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.1-2
- GA - Bump release of all rpms
* Mon Feb 22 2016 Xiaolin Li <xiaolinl@vmware.com> 6.1-1
- Updated to version 6.1
* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 5.2-3
- Handled locale files with macro find_lang
* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 5.2-2
- Removing perl-libintl package from run-time required packages
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2-1
- Upgrade version.
