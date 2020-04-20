%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.7.16
Release:        2%{?dist}
License:        GPLv3+
URL:            https://www.ansible.com
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
%define sha1 ansible=612a7439465f66e996ec62d9b3c29e3077b9440b

Patch0:         CVE-2020-1733.patch
Patch1:         CVE-2020-1735.patch
Patch2:         CVE-2020-1738.patch
Patch3:         CVE-2020-1739.patch
Patch4:         CVE-2020-1740.patch
Patch5:         CVE-2020-10684.patch

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
python2 setup.py build

%install
%{__rm} -rf %{buildroot}
python2 setup.py install -O1 --skip-build \
    --root "%{buildroot}"

%files
%defattr(-, root, root)
%{_bindir}/*
%{python2_sitelib}/*

%changelog
*   Mon Apr 20 2020 Shreenidhi Shedi <<sshedi@vmware.com> 2.7.16-2
-   Fix CVE-2020-1733, CVE-2020-1739
*   Fri Apr 03 2020 Shreenidhi Shedi <<sshedi@vmware.com> 2.7.16-1
-   Upgrade to version 2.7.16 & various CVE fixes
*   Thu Feb 06 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.7.9-3
-   Fix for CVE-2019-14864
*   Mon Aug 12 2019 Shreenidhi Shedi <sshedi@vmware.com> 2.7.9-2
-   Fix for CVE-2019-10156
*   Fri Apr 19 2019 Siju Maliakkal <smaliakkal@vmware.com> 2.7.9-1
-   Upgrading to 2.7.9 to mitigate CVE-2019-3828
*   Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0.0-1
-   Version update to 2.4.0.0
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.2.0-2
-   Use python2 explicitly
*   Thu Apr 6 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.2.0-1
-   Version update
*   Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.1.0-1
-   Initial build. First version
