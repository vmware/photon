Summary:        Python C parser
Name:           python3-pycparser
Version:        2.21
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/pycparser
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://pypi.python.org/packages/source/p/pycparser/pycparser-%{version}.tar.gz
%define sha512  pycparser=e61fbdde484d1cf74d4b27bdde40cf2da4b7028ca8ecd37c83d77473dab707d457321aecaf97da3b114c1d58a4eb200290b76f9c958044b57e5fed949895b5f0

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

BuildArch:      noarch

%description
pycparser is a complete parser of the C language, written in pure Python using the PLY parsing library. It parses C code into an AST and can serve as a front-end for C compilers or analysis tools.

%prep
%autosetup -p1 -n pycparser-%{version}

%build
%py3_build

%install
%py3_install

%check
cd tests
python3 all_tests.py

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.21-2
- Release bump for SRP compliance
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.21-1
- Update to 2.21
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.20-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 2.18-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.18-1
- Update to version 2.18
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.17-3
- Use python2 instead of python
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.17-2
- Fix arch
* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.17-1
- Updated to version 2.17.
* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.14-4
- Added python3 site-packages.
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 2.14-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.14-2
- GA - Bump release of all rpms
* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.14-1
- Initial packaging for Photon
