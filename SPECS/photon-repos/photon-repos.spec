%global subrelease %{?photon_subrelease}%{!?photon_subrelease:0}

Summary:        Photon repo files, gpg keys
Name:           photon-repos
Version:        5.0
Release:        9.%{subrelease}%{?dist}
Group:          System Environment/Base
URL:            https://vmware.github.io/photon/
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source1:        VMWARE-RPM-GPG-KEY
Source2:        VMWARE-RPM-GPG-KEY-4096
Source3:        photon.repo
Source4:        photon-updates.repo
Source5:        photon-iso.repo
Source6:        photon-debuginfo.repo
Source7:        photon-release.repo
Source8:        photon-srpms.repo
Source9:        photon-extras.repo
Source10:       photon-snapshot.repo
Source11:       migrate-repo-url.inc
Source12:       license.txt

%include %{SOURCE11}
%include %{SOURCE12}

Requires:       photon-release
Provides:       photon-repos

%description
Photon repo files and gpg keys

%build
%if %{subrelease} < 92
# Disable photon-updates repo for 90 and 91 by default
sed -i 's|^enabled=1|enabled=0|g' %{SOURCE4}
%else
# Disable photon-snapshot repo for 92 by default
sed -i 's|^enabled=1|enabled=0|g' %{SOURCE10}
%endif

%post
[ $1 -gt 1 ] || exit 0
# On upgrade, migrate the baseurl of remote repos
%{migrate_vmw_repo_url \
  photon \
  photon-srpms \
  photon-extras \
  photon-release \
  photon-updates \
  photon-debuginfo \
}

%install
install -d -m 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/yum.repos.d

install -d -m 755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pki/rpm-gpg

# Set subrelease and updatenumber tdnf variable
mkdir -p %{buildroot}%{_sysconfdir}/tdnf/vars
echo "latest" > %{buildroot}%{_sysconfdir}/tdnf/vars/updatenumber
echo %{subrelease} > %{buildroot}%{_sysconfdir}/tdnf/vars/subrelease

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/yum.repos.d
%{_sysconfdir}/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
%{_sysconfdir}/pki/rpm-gpg/VMWARE-RPM-GPG-KEY-4096
%config(noreplace) %{_sysconfdir}/tdnf/vars/updatenumber
# subrelease file is intentionally not marked as config(noreplace)
# When upgrading to new subrelease, photon-repos must be upgraded as well.
%config %{_sysconfdir}/tdnf/vars/subrelease
%config(noreplace) %{_sysconfdir}/yum.repos.d/photon-debuginfo.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/photon-iso.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/photon.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/photon-updates.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/photon-release.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/photon-srpms.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/photon-extras.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/photon-snapshot.repo

%changelog
* Mon Mar 30 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-9.%{subrelease}
-   Set skip_md_filelists in snapshot repo
*   Wed Mar 04 2026 Bo Gan <bo.gan@broadcom.com> 5.0-8.%{subrelease}
-   Add photon-snapshot repo file, and enable (by default) for 90 and 91
-   Disable photon-updates repo for 92
-   Change the versioning with sub-release suffix
*   Wed Dec 03 2025 Bo Gan <bo.gan@broadcom.com> 5.0-7
-   Patch old broadcom URLs to new ones
*   Wed Jul 23 2025 Bo Gan <bo.gan@broadcom.com> 5.0-6
-   Update baseurl and logic to patch existing (noreplace) files
*   Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-5
-   Release bump for SRP compliance
*   Tue Jul 18 2023 Piyush Gupta <gpiyush@vmware.com> 5.0-4
-   Add photon-extras.repo.
*   Fri Mar 24 2023 Tapas Kundu <tkundu@vmware.com> 5.0-3
-   Disable photon-release.repo
-   All latest rpms for every pkg can be picked from photon-updates
*   Thu Mar 09 2023 Oliver Kurth <okurth@vmware.com> 5.0-2
-   add photon-srpms.repo for source packages
-   remove photom-extras.repo
*   Wed Dec 21 2022 Tapas Kundu <tkundu@vmware.com> 5.0-1
-   Update to 5.0
*   Mon Jul 18 2022 Piyush Gupta <gpiyush@vmware.com> 4.0-4
-   Add photon-release as requires of photon-repos.
*   Thu Feb 24 2022 Oliver Kurth <okurth@vmware.com> 4.0-3
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
