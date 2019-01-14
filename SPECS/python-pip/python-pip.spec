%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           python-pip
Version:        18.0
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/pip
Summary:        The PyPA recommended tool for installing Python packages.
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-%{version}.tar.gz
%define sha1    pip=337f4694bfcd4d698d9b02b38a7520fabc42a1d9
# To get tests:
# git clone https://github.com/pypa/pip && cd pip
# git checkout 9.0.1 && tar -czvf ../pip-tests-9.0.1.tar.gz tests/
Source1:        pip-tests-%{version}.tar.gz
%define sha1 pip-tests=f469fa967798bbae82039151e93d696bc2abfd87
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
%setup -q -n pip-%{version}
tar -xf %{SOURCE1}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 freezegun mock pretend virtualenv scripttest pytest pytest-capturelog

#Disabled svn, bazaar, git related tests
#Disabled non_local_distutils test
#PYTHONPATH=%{buildroot}%{python2_sitelib} py.test -m 'not network' -k 'not svn and not bazaar and not bzr and not git and not non_local_distutils
python setup.py test


%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/*

%changelog
*   Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 18.0-2
-   Fix make check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0-1
-   Update to version 18.0
*   Thu Jul 20 2017 Divya Thaluru <dthaluru@vmware.com> 9.0.1-6
-   Fixed make check errors
*   Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 9.0.1-5
-   Use python2 explicitly
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 9.0.1-4
-   Add python-xml to requires.
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.0.1-3
-   Fix arch
*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 9.0.1-2
-   Added python-setuptools to requires.
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 9.0.1-1
-   Upgrade version to 9.0.1
*   Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 8.1.2-1
-   Initial packaging for Photon
