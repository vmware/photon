%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        provides a pure-Python implementation of immutable URLs
Name:           python-hyperlink
Version:        17.3.1
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/python-hyper/hyperlink
Source0:        https://github.com/python-hyper/hyperlink/archive/hyperlink-%{version}.tar.gz
%define sha1 hyperlink=a577c1d40a14dfa970c74f3b79ad18a98b18a22f

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  python-pytest
%endif

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Hyperlink provides a pure-Python implementation of immutable URLs. Based on RFC 3986 and 3987, the Hyperlink URL makes working with both URIs and IRIs easy.

%package -n     python3-hyperlink
Summary:        provides a pure-Python implementation of immutable URLs
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-libs

%description -n python3-hyperlink
Python 3 version.

%prep
%setup -q -n hyperlink-%{version}
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
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 pip
pip install --upgrade tox
pip install --upgrade pytest-cov
pytest2
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pip
pip install --upgrade tox
pip install --upgrade pytest-cov
pytest3
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-hyperlink
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.3.1-1
-   Initial packaging for Photon
