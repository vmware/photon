Summary:        cpio archive utility
Name:           cpio
Version:        2.13
Release:        7%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/cpio
Group:          System Environment/System utilities
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnu.org/pub/gnu/cpio/%{name}-%{version}.tar.bz2
%define sha512  %{name}=459398e69f7f48201c04d1080218c50f75edcf114ffcbb236644ff6fcade5fcc566929bdab2ebe9be5314828d6902e43b348a8adf28351df978c8989590e93a3

Patch0:         newca-new-archive-format.patch
Patch1:         newca-large-files-support.patch
Patch2:         cpio-2.12-gcc-10.patch
Patch3:         cpio-CVE-2021-38185.patch
Patch4:         cpio-CVE-2021-38185_2.patch
Patch5:         cpio-CVE-2021-38185_3.patch

BuildRequires:  lua

Requires:       lua

%description
The cpio package contains tools for archiving.

%package        lang
Summary:        Additional language files for cpio
Group:          System Environment/System utilities
Requires:       %{name} = %{version}-%{release}

%description    lang
These are the additional language files of cpio

%prep
%autosetup -p1

%build
sed -i -e '/gets is a/d' gnu/stdio.in.h
%configure \
        --enable-mt \
        --with-rmt=%{_libexecdir}/rmt

%make_build

makeinfo --html -o doc/html doc/cpio.texi
makeinfo --html --no-split -o doc/cpio.html doc/cpio.texi
makeinfo --plaintext -o doc/cpio.txt doc/cpio.texi

%install
%make_install %{?_smp_mflags}
install -v -m755 -d %{buildroot}%{_docdir}/%{name}-%{version}/html
install -v -m644 doc/html/* %{buildroot}%{_docdir}/%{name}-%{version}/html
install -v -m644 doc/cpio.{html,txt} %{buildroot}%{_docdir}/%{name}-%{version}
rm -rf %{buildroot}%{_infodir}

%find_lang %{name}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_docdir}/%{name}-%{version}/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Wed Mar 29 2023 Shivani Agarwal <shivania2@vmware.com> 2.13-7
- Updated newca new archive format patch
* Mon Oct 04 2021 Alexey Makhalov <amakhalov@vmware.com> 2.13-6
- newca: large files support
- conflict toybox is not needed for next Photon OS release
* Wed Sep 01 2021 Ankit Jain <ankitja@vmware.com> 2.13-5
- Additional changes to fix CVE-2021-38185
* Fri Aug 20 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.13-4
- Adding security patch for CVE-2021-38185
* Mon Feb 01 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.13-3
- Fix build with new rpm
* Tue Jan 12 2021 Alexey Makhalov <amakhalov@vmware.com> 2.13-2
- GCC-10 support
* Thu May 28 2020 Alexey Makhalov <amakhalov@vmware.com> 2.13-1
- Version update
- newca: new archive format support
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 2.12-5
- Do not conflict with toybox >= 0.8.2-2
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 2.12-4
- Added conflicts toybox
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 2.12-3
- Add lang package
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.12-2
- GA - Bump release of all rpms
* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 2.12-1
- Updated to version 2.12
* Fri Aug 14 2015 Divya Thaluru <dthaluru@vmware.com> 2.11-2
- Adding security patch for CVE-2014-9112
* Tue Nov 04 2014 Divya Thaluru <dthaluru@vmware.com> 2.11-1
- Initial build. First version
