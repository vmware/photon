Summary:        Photon repo files, gpg keys
Name:           photon-repos
Version:        3.0
Release:        7%{?dist}
License:        Apache License
Group:          System Environment/Base
URL:            https://vmware.github.io/photon/
Source0:        photon-repos-3.0.tar.gz
%define sha1 photon-repos=6dcaac0748e7fba12c4f5f01f05f6aeae5ec7fa3
Source1:        VMWARE-RPM-GPG-KEY
Source2:        VMWARE-RPM-GPG-KEY-4096
Source3:        photon.repo
Source4:        photon-updates.repo
Source5:        photon-iso.repo
Source6:        photon-debuginfo.repo
Source7:        photon-extras.repo
Vendor:         VMware, Inc.
Distribution:   Photon
Provides:       photon-repos
BuildArch:      noarch

%description
Photon repo files and gpg keys

%build
# Nothing to do

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE3} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE4} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE5} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE6} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE7} %{buildroot}/etc/yum.repos.d

install -d -m 755 %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE1} %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE2} %{buildroot}/etc/pki/rpm-gpg

%clean
rm -rf %{buildroot}

%post
# if the file has not been replaced because it was edited and does not contain
# the skip_md_filelists option yet, append it to the file
for f in /etc/yum.repos.d/photon{,-debuginfo,-iso,-updates,-extras}.repo ; do
    if ! grep -q skip_md_filelists $f ; then
        echo "skip_md_filelists=1" >> $f
    fi
done

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

%changelog
*   Wed Mar 2 2022 Oliver Kurth <okurth@vmware.com> 3.0-7
-   add 4096 bit RSA key
-   add skip_md_filelists=1 option in %post in case file was not replaced
*   Wed Feb 23 2022 Oliver Kurth <okurth@vmware.com> 3.0-6
-   add skip_md_filelists=1 option
*   Thu Mar 26 2020 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-5
-   Change baseurl to packages.vmware.com
*   Sat Jan 04 2020 Neal Gompa <ngompa13@gmail.com> 3.0-4
-   Fix all the repo definitions to not require arch-specific mangling
*   Tue May 7 2019 Michelle Wang <michellew@vmware.com> 3.0-3
-   Add sources0 for OSSTP tickets
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
