Summary:	command line utility to set and view hardware parameters
Name:		hdparm
Version:	9.63
Release:	1%{?dist}
License:	BSD
URL:		http://sourceforge.net/projects/%{name}/
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon

Source0:	http://downloads.sourceforge.net/hdparm/%{name}-%{version}.tar.gz
%define sha512 hdparm=1d09dc2c79c31f45fa242dd5bf259e84281d1464e49ada9fd53bb6d58cb0458046e534a93f9d6de18478ca5db50b6d36ecbe5b784c0c681a1db29f15fadd525c

%description
The Hdparm package contains a utility that is useful for controlling ATA/IDE
controllers and hard drives both to increase performance and sometimes to increase stability.

%prep
%autosetup -p1

%build
sed -i 's/STRIP ?= strip/STRIP=$(STRIP)/' Makefile
sed -i 's/LDFLAGS = -s/LDFLAGS=$(LDFLAGS)/' Makefile
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS="" STRIP="/bin/true"

%install
make DESTDIR=%{buildroot} binprefix=%{_prefix} install %{?_smp_mflags}

#%%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root)
%{_sbindir}/hdparm
%{_mandir}/man8/hdparm.8*

%changelog
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 9.63-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 9.60-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 9.58-1
- Automatic Version Bump
* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 9.56-1
- Version update to fix compilation issue againts glibc-2.28
* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 9.51-3
- Removed %check  due to no test existence.
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.51-2
- Ensure non empty debuginfo
* Wed Jan 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 9.51-1
- Initial build. First version
