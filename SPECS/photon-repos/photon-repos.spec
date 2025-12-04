Summary:        Photon repo files, gpg keys
Name:           photon-repos
Version:        4.0
Release:        5%{?dist}
License:        Apache License
Group:          System Environment/Base
URL:            https://vmware.github.io/photon/
Source1:        VMWARE-RPM-GPG-KEY
Source2:        VMWARE-RPM-GPG-KEY-4096
Source3:        photon.repo
Source4:        photon-updates.repo
Source5:        photon-iso.repo
Source6:        photon-debuginfo.repo
Source7:        photon-extras.repo
Source8:        photon-release.repo
Source9:        migrate-repo-url.inc
Vendor:         VMware, Inc.
Distribution:   Photon
Provides:       photon-repos
BuildArch:      noarch
%include %{SOURCE9}

%description
Photon repo files and gpg keys

%build
# Nothing to do

%post
[ $1 -gt 1 ] || exit 0
# On upgrade, migrate the baseurl of remote repos
%{migrate_vmw_repo_url \
  photon \
  photon-extras \
  photon-release \
  photon-updates \
  photon-debuginfo \
}

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE3} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE4} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE5} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE6} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE7} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE8} %{buildroot}/etc/yum.repos.d

install -d -m 755 %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE1} %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE2} %{buildroot}/etc/pki/rpm-gpg

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
/etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
/etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY-4096
%config(noreplace) /etc/yum.repos.d/photon-debuginfo.repo
%config(noreplace) /etc/yum.repos.d/photon-iso.repo
%config(noreplace) /etc/yum.repos.d/photon.repo
%config(noreplace) /etc/yum.repos.d/photon-updates.repo
%config(noreplace) /etc/yum.repos.d/photon-extras.repo
%config(noreplace) /etc/yum.repos.d/photon-release.repo

%changelog
*   Wed Dec 03 2025 Bo Gan <bo.gan@broadcom.com> 4.0-5
-   Patch old broadcom URLs to new ones
*   Wed Jul 23 2025 Bo Gan <bo.gan@broadcom.com> 4.0-4
-   Update baseurl and logic to patch existing (noreplace) files
*   Tue Mar 1 2022 Oliver Kurth <okurth@vmware.com> 4.0-3
-   add 4096 bit RSA key
-   disable filelists metadata in photon.repo
*   Fri Feb 19 2021 Anish Swaminathan <anishs@vmware.com> 4.0-2
-   Add a release repo and all updates repo
*   Wed Oct 07 2020 Anish Swaminathan <anishs@vmware.com> 4.0-1
-   Update to 4.0
*   Wed Sep 23 2020 Michelle Wang <michellew@vmware.com> 3.0-5
-   Add sources0 for OSSTP tickets
*   Thu Mar 26 2020 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-4
-   Change baseurl to packages.vmware.com
*   Sat Jan 04 2020 Neal Gompa <ngompa13@gmail.com> 3.0-3
-   Fix all the repo definitions to not require arch-specific mangling
*   Mon Oct 1 2018 Ajay Kaher <akaher@vmware.com> 3.0-2
-   Fix arch name in repos
*   Mon Sep 24 2018 Anish Swaminathan <anishs@vmware.com> 3.0-1
-   Update to 3.0
*   Thu Jul 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0-1
-   Maintenance for 2.0
*   Fri Nov 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-5
-   Remove requires for rpm
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-4
-   GA - Bump release of all rpms
*   Mon May 23 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-3
-   Add photon-debuginfo repo.
*   Mon Apr 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-2
-   Fix regression in photon-extras gpg key location
*   Mon Apr 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-1
-   Initial
