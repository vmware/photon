%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A tool to check your Python code
Name:           python-pycodestyle
Version:        2.5.0
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/python-pam/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}=8d25df191e57d6602bc8ccaf6f6d4f84181301d6

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python2
Requires:       python2-libs

%description
pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

%package -n     python3-pycodestyle
Summary:        python-pycodestyle
Requires:       python3
Requires:       python3-libs

%description -n python3-pycodestyle

Python 3 version.

%prep
%setup -q -n pycodestyle-%{version}
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

%files -n python3-pycodestyle
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/pycodestyle

%changelog
*   Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> 2.5.0-1
-   Initial packaging for Photon
