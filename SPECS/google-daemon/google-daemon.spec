Summary:	Google Daemon
Name:		google-daemon
Version:	1.2.2
Release:	1
License:	Apache License
Group:		System Environment/Base
URL:		https://github.com/GoogleCloudPlatform/compute-image-packages/
Source0:	google-daemon-%{version}.tar.gz
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/etc/*
/usr/*
%exclude /README.md
%exclude /LICENSE
