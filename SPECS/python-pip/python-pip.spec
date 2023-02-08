%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           python-pip
Version:        18.0
Release:        4%{?dist}
Url:            https://pypi.python.org/pypi/pip
Summary:        The PyPA recommended tool for installing Python packages.
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-%{version}.tar.gz
%define sha512  pip=51b8708756a8cbe5ca284fa09908d4acf1127493e4b645f2756ae55e4afd5dec619a017cedb695a044aa24a377909810a1caea4242bb3dc475bfe3435fcaa1bc
# To get tests:
# git clone https://github.com/pypa/pip && cd pip
# git checkout 9.0.1 && tar -czvf ../pip-tests-9.0.1.tar.gz tests/
Source1:        pip-tests-%{version}.tar.gz
%define sha512 pip-tests=123fe62681261ddeac7496a9f68d80d956d2fc810a164c66e8bfc65916672ccd1f9983de8446d1d5e7eef137fda19d7e69f45c9a622c9e2c5804010cc0451947
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:	mercurial
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python-xml
BuildRequires:  PyYAML
%endif

Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
Requires:       python-xml

BuildArch:      noarch

%description
The PyPA recommended tool for installing Python packages.

%prep
%autosetup -n pip-%{version}
tar -xf %{SOURCE1}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 freezegun mock pretend virtualenv scripttest pytest==4.6 pytest-capturelog
python setup.py test

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/*

%changelog
* Sun Feb 12 2023 Prashant S Chauhan <psinghchuha@vmware.com> 18.0-4
- Bump up as part of python3-PyYAML update
* Mon Sep 09 2019 Shreyas B. <shreyasb@vmware.com> 18.0-3
- Fix makecheck.
* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 18.0-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0-1
- Update to version 18.0
* Thu Jul 20 2017 Divya Thaluru <dthaluru@vmware.com> 9.0.1-6
- Fixed make check errors
* Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 9.0.1-5
- Use python2 explicitly
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 9.0.1-4
- Add python-xml to requires.
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.0.1-3
- Fix arch
* Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 9.0.1-2
- Added python-setuptools to requires.
* Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 9.0.1-1
- Upgrade version to 9.0.1
* Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 8.1.2-1
- Initial packaging for Photon
