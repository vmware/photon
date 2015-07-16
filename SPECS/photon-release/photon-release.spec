Summary:	Photon release files
Name:		photon-release
Version:	1.1
Release:	1%{?dist}
License:	Apache License
Group:		System Environment/Base
URL:		http://photon.org
Source:		photon-release-%{version}.tar.gz
%define sha1 photon-release=88312b408fcfc626acf0c13002c1a87cc384a9ff
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
for file in photon*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 PHOTON-RPM-GPG-KEY $RPM_BUILD_ROOT/etc/pki/rpm-gpg

%post
# Remove __db* files to workaround BD version check bug in rpm
rm -f /var/lib/rpm/__db*
rpm --import /etc/pki/rpm-gpg/PHOTON-RPM-GPG-KEY

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
/etc/pki/rpm-gpg/PHOTON-RPM-GPG-KEY
%config(noreplace) /etc/yum.repos.d/photon-iso.repo
%config(noreplace) /etc/yum.repos.d/photon.repo
%config(noreplace) /etc/yum.repos.d/photon-updates.repo

%changelog
*       Wed Jun 17 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1
-       Install photon key
