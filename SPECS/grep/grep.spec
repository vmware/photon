Summary:	Programs for searching through files
Name:		grep
Version:	3.1
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/grep
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://ftp.gnu.org/gnu/grep/%{name}-%{version}.tar.xz
%define sha1 grep=d1d677e959c7d874e18e7e3839f26a0f0c1733d5
Conflicts:      toybox
%description
The Grep package contains programs for searching through files.

%package lang
Summary: Additional language files for grep
Group:   System Environment/Base
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of grep

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=/bin \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
#disable grep -P, not suppported.
sed -i '1474d' tests/Makefile
sed -i '2352,2358d' tests/Makefile
make  %{?_smp_mflags} check

%files
%defattr(-,root,root)
/bin/*
%{_mandir}/*/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 3.1-1
- Update to version 3.1
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 3.0-4
- Added conflicts toybox
* Wed Aug 23 2017 Rongrong Qiu <rqiu@vmware.com> 3.0-3
- Disable grep -P for make check bug 1900287
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 3.0-2
- Add lang package.
* Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0-1
- Upgrading grep to 3.0 version
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.21-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.21-2
- GA - Bump release of all rpms
* Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.21-1
- Upgrading grep to 2.21 version, and adding
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.16-1
- Initial build. First version
