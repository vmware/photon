%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        Extensions to the standard Python datetime module
Name:           python-dateutil
Version:        2.6.1
Release:        1%{?dist}
License:        Simplified BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/python-dateutil
Source0:        https://pypi.python.org/packages/54/bb/f1db86504f7a49e1d9b9301531181b00a1c7325dc85a29160ee3eaa73a54/python-dateutil-%{version}.tar.gz
%define         sha1 python-dateutil=db2ace298dee7e47fd720ed03eb790885347bf4e
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six
Requires:       python2
Requires:       python2-libs
Requires:       python-six
BuildArch:      noarch

%description
The dateutil module provides powerful extensions to the datetime module available in the Python standard library.

%package -n     python3-dateutil
Summary:        python3-dateutil
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs
Requires:       python3-six

%description -n python3-dateutil
Python 3 version.

%prep
%setup -q -n python-dateutil-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-dateutil
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon Dec 18 2017 Kumar Kaushik <kaushikk@vmware.com> 2.6.1-1
-   Initial packaging for photon.
