%define debug_package %{nil}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        future is the missing compatibility layer between Python 2 and Python 3
Name:           python-future
Version:        0.18.2
Release:        1%{?dist}
Url:            https://pypi.org/project/future
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/45/0b/38b06fd9b92dc2b68d58b75f900e97884c45bedd2ff83203d933cf5851c9/future-%{version}.tar.gz
%define sha1    future=d8c8b2d3889fc22bb38f049ed8e3dbdc35a83d6e
BuildRequires:  python2
BuildRequires:  python-xml
BuildRequires:  python-setuptools

BuildRequires:  python3
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools

Requires:       python2

%description
future is the missing compatibility layer between Python 2 and Python 3.
It allows you to use a single, clean Python 3.x-compatible codebase to support both Python 2 and Python 3 with minimal overhead.

%package -n     python3-future
Summary:        python3-future
Requires:       python3

%description -n python3-future
Python 3 version.

%prep
%setup -q -n future-%{version}
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
mv %{buildroot}/%{_bindir}/futurize %{buildroot}/%{_bindir}/futurize3
mv %{buildroot}/%{_bindir}/pasteurize %{buildroot}/%{_bindir}/pasteurize3
popd
python2 setup.py install --skip-build --root=%{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/futurize
%{_bindir}/pasteurize
%{python2_sitelib}/*

%files -n python3-future
%defattr(-,root,root,-)
%{_bindir}/futurize3
%{_bindir}/pasteurize3
%{python3_sitelib}/*

%changelog
*   Thu Feb 11 2021 Ankit Jain <ankitja@vmware.com> 0.18.2-1
-   Initial packaging
