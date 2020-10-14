%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-ply
Version:        3.11
Release:        4%{?dist}
Summary:        Python Lex & Yacc
License:        BSD-3-Clause
Group:          Development/Languages/Python
Url:            http://www.dabeaz.com/ply/
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/dabeaz/ply/archive/ply-%{version}.tar.gz
%define sha1    ply=10a555a32095991fbc7f7ed10c677a14e21fad1d
BuildRequires:  python3-devel
%if %{with_check}
BuildRequires:  python3-six
%endif
Requires:       python3
BuildArch:      noarch

%description
PLY is yet another implementation of lex and yacc for Python. Some notable
features include the fact that its implemented entirely in Python and it
uses LALR(1) parsing which is efficient and well suited for larger grammars.

PLY provides most of the standard lex/yacc features including support for empty
productions, precedence rules, error recovery, and support for ambiguous grammars.

PLY is extremely easy to use and provides very extensive error checking.
It is compatible with both Python 2 and Python 3.

%prep
%setup -q -n ply-%{version}

%build
CFLAGS="%{optflags}" python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
chmod a-x test/*

%check
pushd test

python3 testlex.py
python3 testyacc.py
python3 testcpp.py

popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Oct 15 2020 Prashant S Chauhan <psinghchauha@vmware.com> 3.11-4
-   Fix makecheck
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 3.11-3
-   Mass removal python2
*   Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> 3.11-2
-   Add %check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.11-1
-   Update to version 3.11
*   Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.10-1
-   Initial packaging.
