Summary:	Photon repo files, gpg keys
Name:		photon-repos
Version:	1.0
Release:	4%{?dist}
License:	Apache License
Group:		System Environment/Base
URL:		https://vmware.github.io/photon/
Source:		%{name}-%{version}-3.tar.gz
%define sha1 photon-repos=f0ef82f7fa696ccfa241e00fef34c71b4dfc1ea2
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	photon-repos
BuildArch:	noarch
Requires:       rpm

%description
Photon repo files and gpg keys 

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in *repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 VMWARE-RPM-GPG-KEY $RPM_BUILD_ROOT/etc/pki/rpm-gpg

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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-4
-	GA - Bump release of all rpms
*       Mon May 23 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-3
-       Add photon-debuginfo repo.
*       Mon Apr 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-2
-       Fix regression in photon-extras gpg key location
*       Mon Apr 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-1
-       Initial
