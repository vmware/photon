Summary:        Code deploy agent installer for AWS 
Name:           code-deploy-agent-installer
Version:        1
Release:        1%{?dist}
Source0:        code-deploy-agent-installer-%{version}.tar.gz
%define sha1    code-deploy-agent-installer=d858011f8a792a62fd0803116e13af7aab33a742
Patch0:         code-deploy-agent-installer.patch
License:        LGPLv2+
URL:            https://aws-codedeploy-us-west-2.s3.amazonaws.com/latest/install
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Requires:       cronie
Requires:       chkconfig
Requires:       ruby
Requires:       wget
Requires:       gawk
Requires:       less

%description
This tool installs a script which in turn installs code deploy agent in AWS instance.

%prep
%setup -qn %{name}
%patch0 -p1

%build

%install
install -d %{buildroot}%{_bindir}/%{name}
install -p -m 755 'install' %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/*

%changelog
*   Fri Jan 12 2018 Dheeraj Shetty <dheerajs@vmware.com> 1-1
-   Added new version of code-deploy-agent-installer


