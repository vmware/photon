Summary:	Programs that show the differences between files or directories
Name:		diffutils
Version:	3.3
Release:	3%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/diffutils
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/diffutils/%{name}-%{version}.tar.xz
%define sha1 diffutils=6463cce7d3eb73489996baefd0e4425928ecd61e
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
make %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3-3
-	GA - Bump release of all rpms
*	Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 3.3-2
-	Adding coreutils package to build requires
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.3-1
-	Initial build.	First version
