Name:           ceph-deploy
Version:        1.5.37
Release:        2%{?dist}
Url:            http://ceph.com/
Summary:        Admin and deploy tool for Ceph
License:        MIT
Group:          System/Filesystems
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/23/f0/f144b1b55534a3e10d269dbfbe092e0aaa1c4b826c24f5df9320ae9bdfce/%{name}-%{version}.tar.gz
%define sha1 ceph-deploy=5c19b318320f2729c5b15da7159aa9824b885c1a
Patch0:		ceph-deploy-init.patch
Patch1:		ceph-deploy-package-manager.patch
Patch2:		ceph-deploy-remote.patch
Patch3:		ceph-deploy-photon-distro-init.patch
Patch4:		ceph-deploy-photon-distro-install.patch
Patch5:		ceph-deploy-photon-distro-uninstall.patch
Patch6:		ceph-deploy-photon-distro-mon-init.patch

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:	python2
Requires:	python-setuptools
BuildArch:      noarch

%description
An easy to use admin tool for deploy ceph storage clusters.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -m 0755 -D scripts/ceph-deploy $RPM_BUILD_ROOT/usr/bin

%check
#No check as it requires addditional packages just for checking.

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%{python_sitelib}/*
%{_bindir}/ceph-deploy

%changelog
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.37-2
-   Fix arch
*   Thu Mar 30 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.37-1
-   Upgrading to version 1.5.37
*   Thu Mar 9 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.36-2
-   Adding python-setuptools to Requires section
*   Mon Jan 23 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.36-1
-   Initial packaging for Photon
