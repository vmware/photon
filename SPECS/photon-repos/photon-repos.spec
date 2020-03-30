Summary:	Photon repo files, gpg keys
Name:		photon-repos
Version:	1.0
Release:	5%{?dist}
License:	Apache License
Group:		System Environment/Base
URL:		https://vmware.github.io/photon/
Source:		%{name}-%{version}-4.tar.gz
%define sha1 photon-repos=6dcaac0748e7fba12c4f5f01f05f6aeae5ec7fa3
Source1:        VMWARE-RPM-GPG-KEY
Source2:        photon.repo
Source3:        photon-updates.repo
Source4:        photon-iso.repo
Source5:        photon-debuginfo.repo
Source6:        photon-extras.repo
Source7:        lightwave.repo
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	photon-repos
BuildArch:	noarch
Requires:       rpm

%description
Photon repo files and gpg keys 

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc/yum.repos.d

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/pki/rpm-gpg

%post

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
%config(noreplace) /etc/yum.repos.d/lightwave.repo
%config(noreplace) /etc/yum.repos.d/photon-extras.repo

%changelog
*	Mon Mar 30 2020 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-5
-	Change baseurl to point to packages.vmware.com
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-4
-	GA - Bump release of all rpms
*       Mon May 23 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-3
-       Add photon-debuginfo repo.
*       Mon Apr 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-2
-       Fix regression in photon-extras gpg key location
*       Mon Apr 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-1
-       Initial
