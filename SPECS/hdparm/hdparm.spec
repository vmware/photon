Summary:	command line utility to set and view hardware parameters
Name:		hdparm
Version:	9.56
Release:	1%{?dist}
License:	BSD
URL:		http://sourceforge.net/projects/%{name}/
Source0:	http://downloads.sourceforge.net/hdparm/%{name}-%{version}.tar.gz
%define sha1 hdparm=9e143065115229c4f929530157627dc92e5f6deb
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon

%description
The Hdparm package contains a utility that is useful for controlling ATA/IDE
controllers and hard drives both to increase performance and sometimes to increase stability.

%prep
%setup -q
%build
sed -i 's/STRIP ?= strip/STRIP=$(STRIP)/' Makefile
sed -i 's/LDFLAGS = -s/LDFLAGS=$(LDFLAGS)/' Makefile
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS="" STRIP="/bin/true"
%install
make DESTDIR=%{buildroot} binprefix=%{_prefix} install

#%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root)
%{_sbindir}/hdparm
%{_mandir}/man8/hdparm.8*
%changelog
* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 9.56-1
- Version update to fix compilation issue againts glibc-2.28
* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 9.51-3
- Removed %check  due to no test existence.
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.51-2
- Ensure non empty debuginfo
* Wed Jan 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 9.51-1
- Initial build. First version
