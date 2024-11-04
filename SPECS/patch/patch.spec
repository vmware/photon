Summary:        Program for modifying or creating files
Name:           patch
Version:        2.7.6
Release:        7%{?dist}
URL:            http://www.gnu.org/software/%{name}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        ftp://ftp.gnu.org/gnu/patch/%{name}-%{version}.tar.gz
%define sha512  patch=75d4e1544484da12185418cd4a1571994398140a91ac606fa08dd067004187dad77d1413f0eb3319b3fe4df076714615c98b29df06af052bb65960fa8b0c86bf

Source1: license.txt
%include %{SOURCE1}

Patch0:         CVE-2018-6951.patch
Patch1:         CVE-2018-1000156.patch
#CVE-2018-6952.patch is an incomplete fix which introduced CVE-2019-20633
#CVE-2018-6952 is just Crash in CLI tool, no security impact,complete fix not yet available
#in upstream.
#Patch2         CVE-2018-6952.patch
Patch3:         CVE-2019-13636.patch
Patch4:         CVE-2019-13638.patch

Conflicts:      toybox < 0.8.2-2

%description
Program for modifying or creating files by applying a patch
file typically created by the diff program.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install %{?_smp_mflags}

%check
sed -i "s/ulimit -n 32/ulimit -n 1024/g" tests/deep-directories
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.7.6-7
-   Release bump for SRP compliance
*   Wed Feb 07 2024 Harinadh D <hdommaraju@vmware.com> 2.7.6-6
-   Avoid applying in-complete fix for CVE-2018-6952
*   Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 2.7.6-5
-   Do not conflict with toybox >= 0.8.2-2
*   Thu Aug 08 2019 Shreenidhi Shedi <sshedi@vmware.com> 2.7.6-4
-   Apply patch for CVE-2019-13636, CVE-2019-13638
*   Mon Nov 19 2018 Siju Maliakkal <smaliakkal@vmware.com> 2.7.6-3
-   Add patches for CVE-2018-6951,CVE-2018-1000156,CVE-2018-6952
*   Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 2.7.6-2
-   Add conflicts toybox.
*   Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.7.6-1
-   Upgrade to 2.7.6.
*   Fri Apr 28 2017 Divya Thaluru <dthaluru@vmware.com> 2.7.5-4
-   Fixed ulimit in test script.
*   Fri Oct 07 2016 ChangLee <changlee@vmware.com> 2.7.5-3
-   Modified %check.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.5-2
-   GA - Bump release of all rpms.
*   Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 2.7.5-1
-   Updating to 2.7.5 version.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.7.1-1
-   Initial build First version.
