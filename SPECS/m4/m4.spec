Summary:	A macro processor
Name:		m4
Version:	1.4.18
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/m4
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/m4/%{name}-%{version}.tar.gz
%define sha1 m4=2f76f8105a45b05c8cfede97b3193cd88b31c657

%description
The M4 package contains a macro processor

%prep
%setup -q
%build
#make some fixes required by glibc-2.28:
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h

./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%check
sed -i -e '41s/ENOENT/& || errno == EINVAL/' tests/test-readlink.h
make  %{?_smp_mflags}  check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 1.4.18-2
- Fix compilation issue against glibc-2.28
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 1.4.18-1
- Update package version
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 1.4.17-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.17-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.4.17-1
- Initial build. First version
