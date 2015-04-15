Summary:	Photon release files
Name:		photon-release
Version:	1.0
Release:	1
License:	Apache License
Group:		System Environment/Base
URL:		http://photon.org
Source:		photon-release-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	photon-release
BuildArch:	noarch

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/photon-iso.repo
%config(noreplace) /etc/yum.repos.d/photon.repo
%config(noreplace) /etc/yum.repos.d/photon-updates.repo
