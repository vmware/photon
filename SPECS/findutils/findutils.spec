Summary:	This package contains programs to find files
Name:		findutils
Version:	4.6.0
Release:	5%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/findutils
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/findutils/%{name}-%{version}.tar.gz
%define sha1 findutils=f18e8aaee3f3d4173a1f598001003be8706d28b0
Conflicts:      toybox
%description
These programs are provided to recursively search through a
directory tree and to create, maintain, and search a database
(often faster than the recursive find, but unreliable if the
database has not been recently updated).

%package lang
Summary: Additional language files for findutils
Group:   Applications/File
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of findutils

%prep
%setup -q
%build
#make some fixes required by glibc-2.28:
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' gl/lib/*.c
sed -i '/unistd/a #include <sys/sysmacros.h>' gl/lib/mountlist.c
echo "#define _IO_IN_BACKUP 0x100" >> gl/lib/stdio-impl.h

./configure \
	--prefix=%{_prefix} \
	--localstatedir=%{_sharedstatedir}/locate \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/find %{buildroot}/bin
sed -i 's/find:=${BINDIR}/find:=\/bin/' %{buildroot}%{_bindir}/updatedb
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
/bin/find
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/*/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 4.6.0-5
- Fix compilation issue against glibc-2.28
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 4.6.0-4
- Added conflicts toybox
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 4.6.0-3
- Add lang package.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.6.0-2
- GA - Bump release of all rpms
* Tue Apr 26 2016 Anish Swaminathan <anishs@vmware.com> 4.6.0-1
- Updated to version 4.6.0
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.4.2-1
- Initial build. First version
