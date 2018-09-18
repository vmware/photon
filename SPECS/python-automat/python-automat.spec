%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Self-service finite-state machines for the programmer on the go.
Name:           python-automat
Version:        0.7.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Automat
Source0:        https://files.pythonhosted.org/packages/source/A/Automat/Automat-%{version}.tar.gz
%define sha1    Automat=b96a67647f5c1650f0e4cc39bed762fdc2ac90b4

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-m2r
BuildRequires:  python-setuptools_scm
BuildRequires:  python-attrs
BuildRequires:  python-six
BuildRequires:  python-docutils
BuildRequires:  python-mistune
BuildRequires:  python-graphviz
BuildRequires:  python-Twisted


Requires:       python2
Requires:       python2-libs
Requires:       python-attrs
Requires:       python-six
Requires:       python-graphviz
Requires:       python-Twisted

BuildArch:      noarch

%description
Self-service finite-state machines for the programmer on the go.

Automat is a library for concise, idiomatic Python expression of finite-state automata (particularly deterministic finite-state transducers).

%package -n     python3-automat
Summary:        python-automat
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

%description -n python3-automat
Python 3 version.

%prep
%setup -q -n Automat-%{version}
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
mv %{buildroot}/%{_bindir}/automat-visualize %{buildroot}/%{_bindir}/automat-visualize3
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
%{_bindir}/automat-visualize

%files -n python3-automat
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/automat-visualize3

%changelog
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
