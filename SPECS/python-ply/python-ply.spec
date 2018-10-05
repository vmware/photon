%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-ply
Version:        3.11
Release:        1%{?dist}
Summary:        Python Lex & Yacc
License:        BSD-3-Clause
Group:          Development/Languages/Python
URL:            http://www.dabeaz.com/ply/
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/dabeaz/ply/archive/ply-%{version}.tar.gz
%define sha1    ply=10a555a32095991fbc7f7ed10c677a14e21fad1d
BuildRequires:  python2-devel
BuildRequires:  python3-devel
Requires:       python2
BuildArch:      noarch

%description
PLY is yet another implementation of lex and yacc for Python. Some notable
features include the fact that its implemented entirely in Python and it
uses LALR(1) parsing which is efficient and well suited for larger grammars.

PLY provides most of the standard lex/yacc features including support for empty
productions, precedence rules, error recovery, and support for ambiguous grammars.

PLY is extremely easy to use and provides very extensive error checking.
It is compatible with both Python 2 and Python 3.

%package -n     python3-ply
Summary:        python3 version
Requires:       python3

%description -n python3-ply
Python 3 version.

%prep
%setup -q -n ply-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
CFLAGS="%{optflags}" python2 setup.py build
pushd ../p3dir
CFLAGS="%{optflags}" python3 setup.py build
popd

%install
rm -rf %{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
chmod a-x test/*
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
chmod a-x test/*
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-ply
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.11-1
-   Update to version 3.11
*   Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.10-1
-   Initial packaging.
