%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python Build Reasonableness
Name:           python3-pbr
Version:        4.2.0
Release:        3%{?dist}
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://docs.openstack.org/developer/pbr/
Source0:        https://pypi.io/packages/source/p/pbr/pbr-%{version}.tar.gz
%define sha1    pbr=10165d4998cbe252676ee95306d8f2c843ad2fe6
Patch0:         disable-test-wsgi.patch
BuildRequires:  python3-docutils
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-xml
%if 0
%if %{with_check}
BuildRequires:  git
BuildRequires:  gnupg
%endif
%endif
Requires:       python3
BuildArch:      noarch
%description
A library for managing setuptools packaging needs in a consistent manner.


%prep
%setup -q -n pbr-%{version}
%patch0 -p1

%build
export SKIP_PIP_INSTALL=1
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/pbr %{buildroot}/%{_bindir}/pbr3

%if 0
%check
ln -sfv /usr/bin/gpg2 /usr/bin/gpg
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 coverage
$easy_install_3 hacking
$easy_install_3 mock
$easy_install_3 testrepository
$easy_install_3 testresources
$easy_install_3 testscenarios
$easy_install_3 virtualenv
$easy_install_3 wheel
python3 setup.py test

%endif

%files
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_bindir}/pbr3
%{python3_sitelib}/pbr-%{version}-*.egg-info
%{python3_sitelib}/pbr

%changelog
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 4.2.0-3
-   Mass removal python2
*   Wed Jan 16 2019 Tapas Kundu <tkundu@vmware.com> 4.2.0-2
-   Disabled the make check as the requirements can not be fulfilled
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.2.0-1
-   Update to version 4.2.0
*   Wed Jul 19 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.0-5
-   Fixed make check failure
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.0-4
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.0-3
-   Create pbr3 script
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
-   Fix arch
*   Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.0-1
-   Initial packaging for Photon
