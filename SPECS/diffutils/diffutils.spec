Summary:	Programs that show the differences between files or directories
Name:		diffutils
Version:	3.5
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/diffutils
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/diffutils/%{name}-%{version}.tar.xz
%define sha1 diffutils=1169cce8eaaf7290dc087d65db7ed75de0dceb93
BuildRequires:	coreutils
%description
The Diffutils package contains programs that show the
differences between files or directories.
%prep
%setup -q
sed -i 's:= @mkdir_p@:= /bin/mkdir -p:' po/Makefile.in.in
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
sed -i 's/test-update-copyright.sh //' gnulib-tests/Makefile
chmod g+w . -R
useradd test -G root -m
sudo -u test make check && userdel test -r -f

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%changelog
*       Mon Jul 31 2017 Chang Lee <changlee@vmware.com> 3.5-2
-       fixed %check
*       Wed Apr 19 2017 Bo Gan <ganb@vmware.com> 3.5-1
-       Update to 3.5
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.3-4
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3-3
-	GA - Bump release of all rpms
*	Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 3.3-2
-	Adding coreutils package to build requires
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.3-1
-	Initial build.	First version
