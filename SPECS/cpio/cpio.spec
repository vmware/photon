Summary:	cpio archive utility
Name:		cpio
Version:	2.13
Release:	4%{?dist}
License:	GPLv3+
URL:        http://www.gnu.org/software/cpio/
Group:      System Environment/System utilities
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/pub/gnu/cpio/%{name}-%{version}.tar.bz2
%define sha1 cpio=4dcefc0e1bc36b11506a354768d82b15e3fe6bb8
Conflicts:      toybox < 0.8.2-2
Patch0:         newca-new-archive-format.patch
Patch1:         cpio-2.12-gcc-10.patch
BuildRequires:  lua
Requires:       lua

%description
The cpio package contains tools for archiving.

%package lang
Summary: Additional language files for cpio
Group:   System Environment/System utilities
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of cpio

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%build
sed -i -e '/gets is a/d' gnu/stdio.in.h
%configure \
        --enable-mt   \
        --with-rmt=/usr/libexec/rmt
make %{?_smp_mflags}
makeinfo --html            -o doc/html      doc/cpio.texi
makeinfo --html --no-split -o doc/cpio.html doc/cpio.texi
makeinfo --plaintext       -o doc/cpio.txt  doc/cpio.texi
%install
make DESTDIR=%{buildroot} install
install -v -m755 -d %{buildroot}/%{_docdir}/%{name}-%{version}/html
install -v -m644    doc/html/* %{buildroot}/%{_docdir}/%{name}-%{version}/html
install -v -m644    doc/cpio.{html,txt} %{buildroot}/%{_docdir}/%{name}-%{version}
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_docdir}/%{name}-%{version}/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Tue Mar 23 2021 Piyush Gupta <gpiyush@vmware.com> 2.13-4
- Internal version bump up in order to compile with new lua.
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
