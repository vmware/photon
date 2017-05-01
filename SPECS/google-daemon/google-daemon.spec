Summary:	Google Daemon
Name:		google-daemon
Version:	1.3.3
Release:	2%{?dist}
License:	Apache License
Group:		System Environment/Base
URL:		https://github.com/GoogleCloudPlatform/compute-image-packages/
Source0:	compute-image-packages-%{version}.tar.gz
%define sha1 compute-image-packages=dd115b7d56c08a3c62180a9b72552a54f7babd4f
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:	noarch
Requires:	python2

%description
Google daemon runs in the background and provides the following services:
Creates new accounts based on the instance metadata.
Configures ssh to accept the accounts' public keys from the instance metadata.


%prep
%setup -q -n compute-image-packages-%{version}/%{name}

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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.3-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.3.3-1
-   Updated to version 1.3.3
*   Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 1.3.1-1
-   Upgrade version
*   Mon Aug 10 2015 Anish Swaminathan <anishs@vmware.com> 1.2.7-1
-   Updated version.
