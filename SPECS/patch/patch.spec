Summary:        Program for modifying or creating files
Name:           patch
Version:        2.7.5
Release:        9%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/%{name}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        ftp://ftp.gnu.org/gnu/patch/%{name}-%{version}.tar.gz
%define sha1    %{name}=04d23f6e48e95efb07d12ccf44d1f35fb210f457

Patch0:         patch-CVE-2018-6951.patch
Patch1:         patch-CVE-2018-1000156.patch
Patch2:         patch-CVE-2018-6952.patch
Patch3:         CVE-2019-13636.patch
Patch4:         CVE-2019-13638.patch
Patch5:         CVE-2019-10713.patch

Conflicts:      toybox < 0.7.3-7

%description
Program for modifying or creating files by applying a patch
file typically created by the diff program.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
sed -i "s/ulimit -n 32/ulimit -n 1024/g" tests/deep-directories
make  %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Mon Sep 13 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.7.5-9
- Conflict only with toybox < 0.7.3-7
* Thu Aug 08 2019 Shreenidhi Shedi <sshedi@vmware.com> 2.7.5-8
- Fix for CVE-2019-13636, CVE-2019-13638, CVE-2019-10713
* Mon Oct 08 2018 Sujay G <gsujay@vmware.com> 2.7.5-7
- Apply patch for CVE-2018-6952
* Thu May 17 2018 Xiaolin Li <xiaolinl@vmware.com> 2.7.5-6
- Apply patch for CVE-2018-1000156
* Tue Apr 17 2018 Xiaolin Li <xiaolinl@vmware.com> 2.7.5-5
- Apply patch for CVE-2018-6951
* Fri Apr 28 2017 Divya Thaluru <dthaluru@vmware.com> 2.7.5-4
- Fixed ulimit in test script
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 2.7.5-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.5-2
- GA - Bump release of all rpms
* Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 2.7.5-1
- Updating to 2.7.5 version
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.7.1-1
- Initial build. First version
