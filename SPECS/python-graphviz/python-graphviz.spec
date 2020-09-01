%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Graph visualization dot render
Name:           python3-graphviz
Version:        0.14.1
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/graphviz
#wget https://github.com/xflr6/graphviz/archive/0.8.tar.gz -O graphviz-0.8.tar.gz
Source0:        graphviz-%{version}.zip
%define sha1    graphviz=95624b2fba248b0447ab1af6481a7670a3aedfd6
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  unzip
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch

%description
This package facilitates the creation and rendering of graph descriptions in the DOT language of the Graphviz graph drawing software (repo) from Python.


%prep
%setup -q -n graphviz-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 0.14.1-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.9-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.9-1
-   Update to version 0.9
*   Thu Jul 13 2017 Divya Thaluru <dthaluru@vmware.com> 0.8-1
-   Initial packaging for Photon
