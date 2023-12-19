Summary:    Archiving program
Name:       tar
Version:    1.30
Release:    7%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software/tar
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    tar/%{name}-%{version}.tar.xz
%define sha512 tar=9c8b2cacf8f6ca1b19f788d4ec0410127c4d71e54b9c9cac99ee5af6c002189ccc521302955510bb22a54a069ffd00fc2de12ac776985cbbeb3f1ecf38a4f8d9
Patch0:     tar-CVE-2019-9923.patch
Patch1:         tar-CVE-2018-20482.patch
%if 0%{?with_check}
Patch2:         make-check-failure.patch
%endif
Patch3:         tar-CVE-2021-20193.patch
Patch4:         tar-CVE-2022-48303.patch
Patch5:         CVE-2023-39804.patch

%description
Contains GNU archiving program
%prep
%autosetup -p1

%build
autoreconf -i --force
FORCE_UNSAFE_CONFIGURE=1  ./configure \
    --prefix=%{_prefix} \
    --bindir=/bin \
    --disable-silent-rules
make %{?_smp_mflags}
%install
install -vdm 755 %{buildroot}%{_sbindir}
make DESTDIR=%{buildroot} %{?_smp_mflags} install
make DESTDIR=%{buildroot} %{?_smp_mflags} -C doc install-html docdir=%{_defaultdocdir}/%{name}-%{version}
install -vdm 755 %{buildroot}/usr/share/man/man1
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}
%check
make  %{?_smp_mflags} check
%files -f %{name}.lang
%defattr(-,root,root)
/bin/tar
%{_libexecdir}/rmt
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%changelog
*       Tue Dec 19 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 1.30-7
-       Fix CVE-2023-39804
*       Thu Feb 09 2023 Mukul Sikka <msikka@vmware.com> 1.30-6
-       Fix CVE-2022-48303
*       Fri Apr 16 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.30-5
-       Fix CVE-2021-20193
*       Tue Oct 22 2019 Prashant S Chauhan <psinghchauha@vmware.com> 1.30-4
-       Fix make check, Added a patch.
*       Fri May 24 2019 Keerthana K <keerthanak@vmware.com> 1.30-3
-       Fix CVE-2018-20482
*   Wed Apr 24 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.30-2
-   Fix CVE-2019-9923
*       Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 1.30-1
-       Update to version 1.30
*       Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.29-1
-       Update to version 1.29.
*       Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.28-3
-       Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-2
-   GA - Bump release of all rpms
*   Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-1
-   Update to 1.28-1.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.27.1-1
-   Initial build.  First version
