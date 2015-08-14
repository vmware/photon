Summary:	Photon release files
Name:		photon-release
Version:	1.2
Release:	1%{?dist}
License:	Apache License
Group:		System Environment/Base
URL:		http://photon.org
Source:		photon-release-%{version}.tar.gz
%define sha1 photon-release=8ab4215b1df475d1e5826ce112e2f3ceebe711a0
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	photon-release
BuildArch:	noarch
Requires: rpm

%description
Photon release files such as yum configs and other /etc/ release related files

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in *repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 VMWARE-RPM-GPG-KEY $RPM_BUILD_ROOT/etc/pki/rpm-gpg

%post
# Remove __db* files to workaround BD version check bug in rpm
rm -f /var/lib/rpm/__db*
rpm --import /etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY

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

%changelog
*       Fri Aug 14 2015 Sharath George <sharathg@vmware.com> 1.2
-       Install photon repo links
*       Wed Jun 17 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1
-       Install photon key
