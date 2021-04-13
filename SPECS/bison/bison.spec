Summary:	Contains a parser generator
Name:		bison
Version:	3.7.6
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/bison
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/bison/%{name}-%{version}.tar.xz
%define sha1 bison=bbd6362383a7276cd85ed3f19cb5416aeb98e5db
%if %{with_check}
Patch0:         make-check.patch
%endif
BuildRequires:	m4
BuildRequires:	gettext
Requires:	m4
Requires:	gettext
BuildRequires:	flex
%description
This package contains a parser generator
%prep
%setup -q
%if %{with_check}
%patch0 -p1
%endif
%build
#make some fixes required by glibc-2.28:
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h

autoreconf -fiv
%configure \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

%check
make %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.a
%{_datarootdir}/%{name}/*
%{_datarootdir}/aclocal/*
%{_mandir}/*/*
%{_docdir}/bison/*
%changelog
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 3.7.6-1
- Automatic Version Bump
* Tue Jan 26 2021 Anish Swaminathan <anishs@vmware.com> 3.7.1-3
- Add missing dependency for gettext
* Tue Jan 19 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.7.1-2
- Fix make check
* Wed Sep 02 2020 Gerrit Photon <photon-checkins@vmware.com> 3.7.1-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 3.5.2-1
- Automatic Version Bump
* Tue Sep 18 2018 Tapas Kundu <tkundu@vmware.com> 3.1-1
- Updated to release 3.1
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 3.0.4-4
- Fix compilation issue against glibc-2.28
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.4-3
- GA - Bump release of all rpms
* Thu Apr 28 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.4-2
- Removed requires for flex
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.0.4-1
- Updated to version 3.0.4
* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 3.0.2-3
- Handled locale files with macro find_lang
* Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 3.0.2-2
- Adding m4, flex package to build and run time required package
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.2-1
- Initial build. First version.
