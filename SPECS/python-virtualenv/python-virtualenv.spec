%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-virtualenv
Version:        16.0.0
Release:        3%{?dist}
Summary:        Virtual Python Environment builder
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/virtualenv
Source0:        virtualenv-%{version}.tar.gz
%define sha1    virtualenv=33831525c360459671d25f9e5abac931c414d2f7
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
Requires:       python2
Requires:       python2-libs
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python-pip
BuildRequires:  python3-devel
Requires:       python3-devel
BuildRequires:  python3-pip
BuildRequires:  python-pip
%endif

BuildArch:      noarch

%description
virtualenv is a tool to create isolated Python environment.

%package -n     python3-virtualenv
Summary:        Virtual Python Environment builder
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-libs
BuildRequires:  python3-setuptools

%description -n python3-virtualenv
Python 3 version.

%prep
%setup -n virtualenv-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip install zipp>=0.5
pip install pytest
pip install mock
python2 setup.py test
pushd ../p3dir
pip3 install pytest
pip3 install mock
python3 setup.py test
popd

%files
%defattr(-,root,root,-)
%{_bindir}/virtualenv
%{python_sitelib}/*

%files -n python3-virtualenv
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Mar 02 2020 Shreyas B. <shreyasb@vmware.com> 16.0.0-3
-   Fix make check.
*   Mon Sep 09 2019 Shreyas B. <shreyasb@vmware.com> 16.0.0-2
-   Fix make check.
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 16.0.0-1
-   Update to version 16.0.0
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 15.1.0-1
-   Initial version of python-virtualenv package for Photon.
