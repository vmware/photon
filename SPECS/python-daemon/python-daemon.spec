Summary:        Library to implement a well-behaved Unix daemon process.
Name:           python3-daemon
Version:        2.2.4
Release:        3%{?dist}
License:        Apache-2
Url:            https://pypi.python.org/pypi/python-daemon/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://files.pythonhosted.org/packages/source/p/python-daemon/python-daemon-%{version}.tar.gz
%define sha512  python-daemon=9a7a4e23e126f05e4c1c503f15401cddd758c5f9195c370997060ca1bbfe71cc51d82d3ae16bcf0023c28fa50b0b8d6cd406e515b27725ffa9fec10fde3ed64a

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-docutils
BuildRequires:  python3-lockfile
BuildRequires:  python3-xml
BuildRequires:  curl-devel
BuildRequires:  libffi-devel

Requires:       libffi
Requires:       python3
Requires:       python3-lockfile

BuildArch:      noarch

%description
This library implements the well-behaved daemon specification of PEP 3143, “Standard daemon process library”.

A well-behaved Unix daemon process is tricky to get right, but the required steps are much the same for every daemon program. A DaemonContext instance holds the behaviour and configured process environment for the program; use the instance as a context manager to enter a daemon state.

%prep
%autosetup -p1 -n python-daemon-%{version}
sed -i 's/distclass=version.ChangelogAwareDistribution,/ /g' setup.py

%build
python3 setup.py build

%install
rm -rf %{buildroot}
python3 setup.py install --root=%{buildroot}

%check
%if 0%{?with_check}
easy_install_3=$(ls /usr/bin | grep easy_install | grep 3)
$easy_install_3 mock
$easy_install_3 testscenarios
$easy_install_3 testtools
python3 -m unittest discover
%endif

%files
%defattr(-, root, root, -)
%{python3_sitelib}/*

%changelog
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.2.4-3
- Bump version as a part of libffi upgrade
* Thu Aug 13 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.2.4-2
- Added libffi to BuildRequires
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.4-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.2.0-3
- Mass removal python2
* Wed Dec 19 2018 Tapas Kundu <tkundu@vmware.com> 2.2.0-2
- Fix makecheck
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.2.0-1
- Updated to 2.2.0
* Mon Jul 17 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.2-4
- Fixed check command to run unit tests
- Added packages required to run tests
- Added missing runtime dependent packages
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.2-2
- Corrected an error in command
* Fri Mar 24 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-1
- Initial packaging for Photon
