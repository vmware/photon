Summary:	Google Daemon
Name:		google-daemon
Version:	1.3.1
Release:	1%{?dist}
License:	Apache License
Group:		System Environment/Base
URL:		https://github.com/GoogleCloudPlatform/compute-image-packages/
Source0:	google-daemon-%{version}.tar.gz
%define sha1 google-daemon=c55ad60bd29a46afb12d70158d6fa2c5569ec2b4
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	google-daemon
BuildArch:	noarch
Requires:	python2

%description
Google daemon runs in the background and provides the following services:
Creates new accounts based on the instance metadata.
Configures ssh to accept the accounts' public keys from the instance metadata.


%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
cp -rpf * $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mv $RPM_BUILD_ROOT/etc/init.d/* $RPM_BUILD_ROOT/etc/rc.d/init.d/
rm -rf $RPM_BUILD_ROOT/etc/init.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/etc/*
/usr/*
%exclude /README.md
%exclude /LICENSE

%changelog
*   Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 1.3.1-1
-   Upgrade version
*   Mon Aug 10 2015 Anish Swaminathan <anishs@vmware.com> 1.2.7-1
-   Updated version.
