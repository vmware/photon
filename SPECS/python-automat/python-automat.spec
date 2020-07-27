%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Self-service finite-state machines for the programmer on the go.
Name:           python3-automat
Version:        20.2.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Automat
Source0:        https://files.pythonhosted.org/packages/source/A/Automat/Automat-%{version}.tar.gz
%define sha1    Automat=7e1827bbfed916fd0f754f632af8b06bfabce8c5

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-m2r
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-attrs
BuildRequires:  python3-six
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-docutils
BuildRequires:  python3-mistune
BuildRequires:  python3-graphviz
BuildRequires:  python3-Twisted

Requires:       python3
Requires:       python3-libs
Requires:       python3-attrs
Requires:       python3-six
Requires:       python3-graphviz
Requires:       python3-Twisted

BuildArch:      noarch

%description
Self-service finite-state machines for the programmer on the go.

Automat is a library for concise, idiomatic Python expression of finite-state automata (particularly deterministic finite-state transducers).

%prep
%setup -q -n Automat-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/automat-visualize %{buildroot}/%{_bindir}/automat-visualize3

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/automat-visualize3

%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.2.0-1
-   Automatic Version Bump
*   Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.7.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.7.0-1
-   Update to version 0.7.0
*   Mon Jul 17 2017 Divya Thaluru <dthaluru@vmware.com> 0.5.0-4
-   Fixed run time dependencies
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.5.0-2
-   Separate the python3 and python2 scripts in bin directory
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-1
-   Initial packaging for Photon
