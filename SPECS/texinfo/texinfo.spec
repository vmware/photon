Summary:        Reading, writing, and converting info pages
Name:           texinfo
Version:        6.3
Release:        2%{?dist}
License:        GPLv3+
URL:            http://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.xz
%define sha1    texinfo=64568f2791d1309aaccc22e63758458fd249ec8b
BuildRequires:  perl

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

%find_lang %{name} --all-name

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%dir %{_datarootdir}/texinfo
%{_datarootdir}/texinfo/*
%dir %{_datarootdir}/texmf
%{_datarootdir}/texmf/*
%{_libdir}/texinfo/*

%changelog
*   Tue Apr 18 2017 Robert Qi <qij@vmware.com> 6.3-2
-   Updated to version 6.3-2 due to perl build requires.
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 6.3-1
-   Updated to version 6.3.
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 6.1-4
-   Modified %check
*   Wed Jun 27 2016 Divya Thaluru <dthaluru@vmware.com> 6.1-3
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
