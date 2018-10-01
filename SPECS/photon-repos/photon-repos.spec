Summary:	Photon repo files, gpg keys
Name:		photon-repos
Version:	3.0
Release:	2%{?dist}
License:	Apache License
Group:		System Environment/Base
URL:		https://vmware.github.io/photon/
Source0:        VMWARE-RPM-GPG-KEY
Source1:        photon.repo
Source2:        photon-updates.repo
Source3:        photon-iso.repo
Source4:        photon-debuginfo.repo
Source5:        photon-extras.repo
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	photon-repos
BuildArch:	noarch

%description
Photon repo files and gpg keys 

%build
sed -i 's/_arch/%{_arch}/g' %{SOURCE1} \
         %{SOURCE2} %{SOURCE3} \
         %{SOURCE4} %{SOURCE5}

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/etc/yum.repos.d

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/etc/pki/rpm-gpg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
/etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
%config(noreplace) /etc/yum.repos.d/photon-debuginfo.repo
%config(noreplace) /etc/yum.repos.d/photon-iso.repo
%config(noreplace) /etc/yum.repos.d/photon.repo
%config(noreplace) /etc/yum.repos.d/photon-updates.repo
%config(noreplace) /etc/yum.repos.d/photon-extras.repo

%changelog
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

