Summary:	Programs for searching through files
Name:		grep
Version:	3.0
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/grep
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://ftp.gnu.org/gnu/grep/%{name}-%{version}.tar.xz
%define sha1 grep=7b742a6278f28ff056da799c62c1b9e417fe86ba
%description
The Grep package contains programs for searching through files.
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
make  %{?_smp_mflags} check
%files -f %{name}.lang
%defattr(-,root,root)
/bin/*
%{_mandir}/*/*
%changelog
*       Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0-1
-       Upgrading grep to 3.0 version
*       Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.21-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.21-2
-	GA - Bump release of all rpms
*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.21-1
-   Upgrading grep to 2.21 version, and adding 
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.16-1
-	Initial build. First version
