Summary:        Pure Python Vi Implementation.
Name:           python3-pyvim
Version:        3.0.3
Release:        3%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/service_identity

Source0:        pyvim-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# To get tests:
# git clone https://github.com/jonathanslenders/pyvim.git && cd pyvim
# git checkout 6860c413 && tar -czvf ../pyvim-tests-0.0.20.tar.gz tests/
#Source1:        pyvim-tests-%{version}.tar.gz
#do not see test updated after 2.0.24, hence not packaging tests

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pyflakes
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-prompt_toolkit
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-xml
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-prompt_toolkit
Requires:       python3-pyflakes
BuildArch:      noarch

%description
An implementation of Vim in Python.

%prep
%autosetup -p1 -n pyvim-%{version}
#tar -xf %{SOURCE1} --no-same-owner

%build
%py3_build

%install
%py3_install
mv %{buildroot}/%{_bindir}/pyvim %{buildroot}/%{_bindir}/pyvim3

%check
pip3 install pathlib2 funcsigs pluggy more-itertools pyflakes
PYTHONPATH=./ py.test3

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/pyvim3

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.0.3-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.0.3-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 3.0.3-1
- Automatic Version Bump
* Fri Jul 09 2021 Tapas Kundu <tkundu@vmware.com> 3.0.2-3
- Fix dependency issue
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.2-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.2-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 2.0.22-6
- Mass removal python2
* Wed Feb 26 2020 Tapas Kundu <tkundu@vmware.com> 2.0.22-5
- Fix makecheck
* Mon Sep 09 2019 Tapas Kundu <tkundu@vmware.com> 2.0.22-4
- Fix makecheck
* Mon Nov 26 2018 Tapas Kundu <tkundu@vmware.com> 2.0.22-3
- Fix makecheck
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 2.0.22-2
- Use --no-same-owner for tar
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.0.22-1
- Update to version 2.0.22
* Mon Jul 24 2017 Divya Thaluru <dthaluru@vmware.com> 0.0.20-4
- Fixed runtime dependencies and make check errors
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.20-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.0.20-2
- Rectified python3 version
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.20-1
- Initial packaging for Photon.
