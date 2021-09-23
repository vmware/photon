Summary:	Programs that show the differences between files or directories
Name:		diffutils
Version:	3.5
Release:	3%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/diffutils
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon

Source0:	http://ftp.gnu.org/gnu/diffutils/%{name}-%{version}.tar.xz
%define sha1 %{name}=1169cce8eaaf7290dc087d65db7ed75de0dceb93

BuildRequires:	coreutils

Conflicts:      toybox < 0.7.3-7

%description
The Diffutils package contains programs that show the
differences between files or directories.

%prep
%setup -q
sed -i 's:= @mkdir_p@:= /bin/mkdir -p:' po/Makefile.in.in

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
sed -i 's/test-update-copyright.sh //' gnulib-tests/Makefile
make %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Thu Sep 23 2021 Tapas Kundu <tkundu@vmware.com> 3.5-3
- Fix configure
* Mon Sep 13 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.5-2
- Conflict only with toybox < 0.7.3-7
* Wed Apr 19 2017 Bo Gan <ganb@vmware.com> 3.5-1
- Update to 3.5
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.3-4
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3-3
- GA - Bump release of all rpms
* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 3.3-2
- Adding coreutils package to build requires
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.3-1
- Initial build. First version
