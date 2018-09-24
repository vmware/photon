Summary:        Reading, writing, and converting info pages
Name:           texinfo
Version:        6.5
Release:        2%{?dist}
License:        GPLv3+
URL:            http://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.xz
%define sha1    texinfo=72a06b48862911c638787cc3307871b990a59726
BuildRequires:  perl >= 5.28.0

%description
The Texinfo package contains programs for reading, writing,
and converting info pages.
%prep
%setup -q
%build
%configure \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} TEXMF=%{_datarootdir}/texmf install-tex
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
%dir %{_datarootdir}/texinfo
%{_datarootdir}/texinfo/*
%dir %{_datarootdir}/texmf
%{_datarootdir}/texmf/*
%{_libdir}/texinfo/*

%changelog
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 6.5-2
-   Consuming perl version upgrade of 5.28.0
*   Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 6.5-1
-   Update version to 6.5.
*   Fri May 05 2017 Xiaolin Li <xiaolinl@vmware.com> 6.3-3
-   Excluded pdftexi2dvi, texi2dvi, texi2pdf from package,
-   because these commands depend on installation of tex.
*   Tue Apr 18 2017 Robert Qi <qij@vmware.com> 6.3-2
-   Updated to version 6.3-2 due to perl build requires.
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 6.3-1
-   Updated to version 6.3.
*   Tue Oct 04 2016 ChangLee <changlee@vmware.com> 6.1-4
-   Modified %check
*   Mon Jun 27 2016 Divya Thaluru <dthaluru@vmware.com> 6.1-3
-   Removed packaging of debug files
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.1-2
-   GA - Bump release of all rpms
*   Mon Feb 22 2016 Xiaolin Li <xiaolinl@vmware.com> 6.1-1
-   Updated to version 6.1
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 5.2-3
-   Handled locale files with macro find_lang
*   Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 5.2-2
-   Removing perl-libintl package from run-time required packages
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2-1
-   Upgrade version
