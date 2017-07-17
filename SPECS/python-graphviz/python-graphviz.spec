%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Graph visualization dot render
Name:           python-graphviz
Version:        0.8
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/graphviz
#wget https://github.com/xflr6/graphviz/archive/0.8.tar.gz -O graphviz-0.8.tar.gz
Source0:        graphviz-%{version}.tar.gz
%define         sha1 graphviz=2aee1f3576b1ba08e0b70a0c83ef8e9e7d82d82f
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-xml
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
This package facilitates the creation and rendering of graph descriptions in the DOT language of the Graphviz graph drawing software (repo) from Python.

%package -n     python3-graphviz
Summary:        Provide support for Graphviz software dot render in python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-graphviz
Python 3 version.

%prep
%setup -q -n graphviz-%{version}
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
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-graphviz
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Thu Jul 13 2017 Divya Thaluru <dthaluru@vmware.com> 0.8-1
-   Initial packaging for Photon
