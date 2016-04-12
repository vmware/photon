Summary:	Photon repo files, gpg keys
Name:		photon-repos
Version:	1.0
Release:	1%{?dist}
License:	Apache License
Group:		System Environment/Base
URL:		https://vmware.github.io/photon/
Source:		%{name}-%{version}.tar.gz
%define sha1 photon-repos=0be4c46922ad6f990e28e05fef75e2d1341aaf4a
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
%config(noreplace) /etc/yum.repos.d/photon-iso.repo
%config(noreplace) /etc/yum.repos.d/photon.repo
%config(noreplace) /etc/yum.repos.d/photon-updates.repo
%config(noreplace) /etc/yum.repos.d/lightwave.repo
%config(noreplace) /etc/yum.repos.d/photon-extras.repo

%changelog
*       Mon Apr 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0
-       Initial
