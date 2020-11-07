%global debug_package %{nil}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        scp module for paramiko
Name:           python3-scp
Version:        0.13.3
Release:        1%{?dist}
License:        GNU Library or Lesser General Public License (LGPL) (LGPL)
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/scp
Source0:        https://files.pythonhosted.org/packages/05/e0/ac4169e773e12a08d941ca3c006cb8c91bee9d6d80328a15af850b5e7480/scp-%{version}.tar.gz
%define sha1    scp=69c92bf48efad3243a790839a1acd28c452dd48b

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
BuildRequires:  python3-paramiko

Requires:       python3
Requires:       python3-libs
Requires:       python3-paramiko

%description
The scp.py module uses a paramiko transport to send and recieve files via the scp1 protocol.
This is the protocol as referenced from the openssh scp program, and has only been tested with this implementation.


%prep
%setup -q -n scp-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%check

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 0.13.3-1
-   Automatic Version Bump
*   Wed Aug 12 2020 Tapas Kundu <tkundu@vmware.com> 0.13.2-1
-   Initial packaging for Photon
