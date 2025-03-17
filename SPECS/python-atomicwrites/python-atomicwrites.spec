Summary:        Python Atomic file writes
Name:           python3-atomicwrites
Version:        1.4.1
Release:        3%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/untitaker/python-atomicwrites
Source0:        https://pypi.python.org/packages/a1/e1/2d9bc76838e6e6667fde5814aa25d7feb93d6fa471bf6816daac2596e8b2/atomicwrites-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-attrs
BuildRequires:  python3-pytest
BuildRequires:  python3-six
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildArch:      noarch

%description
Python Atomic file writes

%prep
%autosetup -p1 -n atomicwrites-%{version}

%build
%py3_build

%install
%py3_install

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 funcsigs pathlib2 pluggy more-itertools
cp tests/test_atomicwrites.py .
python3 test_atomicwrites.py

%files
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.1-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.4.1-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.4.1-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.4.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 1.2.1-4
- Mass removal python2
* Mon Aug 26 2019 Shreyas B. <shreyasb@vmware.com> 1.2.1-3
- Fixed make check
* Mon Nov 12 2018 Tapas Kundu <tkundu@vmware.com> 1.2.1-2
- Fixed make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.2.1-1
- Update to version 1.2.1
* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 1.1.5-2
- Fixed rpm check errors
* Fri Jul 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.1.5-1
- Initial packaging for Photon
