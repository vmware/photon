Name:           python3-yamlloader
Version:        1.1.0
Release:        2%{?dist}
Summary:        Ordered YAML loader and dumper for PyYAML.
License:        MIT License
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/9e/10/fbb1fb0d600f167b4ddeb83a5e66307c5c0d56860595e02c9387861b686d/yamlloader-1.1.0.tar.gz
Source0:        yamlloader-%{version}.tar.gz
%define sha1    yamlloader=77013d2299b5305848b3873341d7272dcb59d03a
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch
Provides:       python%{python3_version}dist(yamlloader)

%description
This module provides loaders and dumpers for PyYAML. Currently, an OrderedDict loader/dumper is implemented, allowing to keep items order when loading resp. dumping a file from/to an OrderedDict (Python 3.7+: Also regular dicts are supported and are the default items to be loaded to. As of Python 3.7 preservation of insertion order is a language feature of regular dicts.)

%prep
%autosetup -n yamlloader-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.1.0-2
-   Update release to compile with python 3.10,use python3 macros file
*   Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.1.0-1
-   Initial packaging for python3-yamlloader
