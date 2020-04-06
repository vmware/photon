%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-deepmerge
Version:        0.0.5
Release:        1%{?dist}
Summary:        Python toolset to deeply merge python dictionaries.
Group:          Development/Libraries
License:        MIT
URL:            https://pypi.org/project/deepmerge
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/n/deepmerge/deepmerge-%{version}.tar.gz
%define sha1    deepmerge=7479145628eb83eed4ccf8d20e19a56b31fb295c
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python-xml
BuildRequires:  python3-xml
BuildRequires:  curl-devel
Requires:       python2
Requires:       python2-libs
%if %{with_check}
BuildRequires:  python-pytest
BuildRequires:  python3-pytest
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-six
BuildRequires:  python-atomicwrites
BuildRequires:  python-attrs
BuildRequires:  python-six
BuildRequires:  python-requests
BuildRequires:  python3-requests
BuildRequires:  python-pip
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
A tools to handle merging of nested data structures in python.

%package -n python3-deepmerge
Summary:        Python toolset to deeply merge python dictionaries.
Requires:       python3
Requires:       python3-libs

%description -n python3-deepmerge
A tools to handle merging of nested data structures in python.

%prep
%setup -q -n deepmerge-%{version}
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
pushd deepmerge/tests/
pip install pluggy
pip install more-itertools
pip install funcsigs
pytest2
popd
pushd ../p3dir/deepmerge/tests/
pip3 install pluggy
pip3 install more-itertools
pip3 install funcsigs
pytest3
popd

%clean
rm -rf %{buildroot}/*


%files
%defattr(-,root,root)
%doc README.rst
%{python2_sitelib}/*

%files -n python3-deepmerge
%defattr(-,root,root)
%doc README.rst
%{python3_sitelib}/*

%changelog
*  Tue Jul 23 2019 Tapas Kundu <tkundu@vmware.com> 0.0.5-1
-  Initial packaging for photon OS
