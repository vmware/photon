Summary:	Programs for searching through files
Name:		grep
Version:	2.21
Release:	3%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/grep
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/grep/%{name}-%{version}.tar.xz
%define sha1 grep=c7e6525c5c5aaa1bc3c1774db1697f42b11c2d85
Patch0:     out-of-bound-heap-read-CVE-2015-1345.patch
%description
The Grep package contains programs for searching through files.
%prep
%setup -q
%patch0 -p1
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
*       Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.21-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.21-2
-	GA - Bump release of all rpms
*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.21-1
-   Upgrading grep to 2.21 version, and adding 
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.16-1
-	Initial build. First version
