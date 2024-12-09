Name:           python3-ply
Version:        3.11
Release:        7%{?dist}
Summary:        Python Lex & Yacc
Group:          Development/Languages/Python
Url:            http://www.dabeaz.com/ply/
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/dabeaz/ply/archive/ply-%{version}.tar.gz
%define sha512  ply=37e39a4f930874933223be58a3da7f259e155b75135f1edd47069b3b40e5e96af883ebf1c8a1bbd32f914a9e92cfc12e29fec05cf61b518f46c1d37421b20008

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
%if 0%{?with_check}
BuildRequires:  python3-six
%endif
Requires:       python3
BuildArch:      noarch
Provides:       python%{python3_version}dist(ply)

%description
PLY is yet another implementation of lex and yacc for Python. Some notable
features include the fact that its implemented entirely in Python and it
uses LALR(1) parsing which is efficient and well suited for larger grammars.

PLY provides most of the standard lex/yacc features including support for empty
productions, precedence rules, error recovery, and support for ambiguous grammars.

PLY is extremely easy to use and provides very extensive error checking.
It is compatible with both Python 2 and Python 3.

%prep
%autosetup -n ply-%{version}

%build
CFLAGS="%{optflags}" %py3_build

%install
%py3_install
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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.11-7
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.11-6
- Update release to compile with python 3.11
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 3.11-5
- Added provides
* Thu Oct 15 2020 Prashant S Chauhan <psinghchauha@vmware.com> 3.11-4
- Fix makecheck
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 3.11-3
- Mass removal python2
* Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> 3.11-2
- Add %check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.11-1
- Update to version 3.11
* Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.10-1
- Initial packaging.
