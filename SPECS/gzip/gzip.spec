Summary:	Programs for compressing and decompressing files
Name:		gzip
Version:	1.12
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/gzip/%{name}-%{version}.tar.xz
%define sha1 gzip=318107297587818c8f1e1fbb55962f4b2897bc0b
%if %{with_check}
BuildRequires:	less
%endif
%description
The Gzip package contains programs for compressing and
decompressing files.
%prep
%autosetup -p1
%build
#make some fixes required by glibc-2.28:
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h

%configure --disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%changelog
* Thu Apr 07 2022 Siju Maliakkal <smaliakkal@vmware.com> 1.12-1
- Upgrade to l.12 to mitigate CVE-2022-1271
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.10-1
- Automatic Version Bump
* Thu Aug 22 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 1.9-2
- Fix for make check failure
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.9-1
- Update to version 1.9
* Sat Sep 08 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8-2
- Fix compilation issue against glibc-2.28
* Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.8-1
- Upgrading to version 1.8
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.6-1
- Initial build. First version
