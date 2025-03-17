Summary:        C extensions for Python3
Name:           cython3
Version:        0.29.32
Release:        4%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://cython.org/

Source0:        https://github.com/cython/cython/archive/Cython-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-xml

Requires:       python3

%description
Cython is an optimising static compiler for both the Python programming language,
and the extended Cython programming language (based on Pyrex).
It makes writing C extensions for Python as easy as Python itself.

%prep
%autosetup -p1 -n cython-%{version}

%build
%py3_build

%install
python3 setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/cython %{buildroot}%{_bindir}/cython3
mv %{buildroot}%{_bindir}/cythonize %{buildroot}%{_bindir}/cythonize3
mv %{buildroot}%{_bindir}/cygdb %{buildroot}%{_bindir}/cygdb3

%check
sed -i 's/PYTHON?=python/PYTHON?=python3/g' Makefile
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/Cython/*
%{python3_sitelib}/cython.py*
%{python3_sitelib}/pyximport/*
%{python3_sitelib}/__pycache__/*

%changelog
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.29.32-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.29.32-3
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.29.32-2
- Update release to compile with python 3.11
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 0.29.32-1
- Automatic Version Bump
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 0.29.28-1
- Automatic Version Bump
* Wed Apr 14 2021 Gerrit Photon <photon-checkins@vmware.com> 0.29.23-1
- Automatic Version Bump
* Wed Oct 14 2020 Tapas Kundu <tkundu@vmware.com> 3.0a6-1
- Update to 3.0a6
* Mon Jul 27 2020 Tapas Kundu <tkundu@vmware.com> 0.29.21-2
- Build with python3
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 0.29.21-1
- Automatic Version Bump
* Fri Jan 11 2019 Michelle Wang <michellew@vmware.com> 0.28.5-2
- Fix make check tests for cython3.
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 0.28.5-1
- Upgraded to version 0.28.5.
* Thu Jul 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.25.2-4
- Keeping uniformity across all spec files.
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.25.2-3
- Add python3-xml to python3 sub package Buildrequires.
* Wed Apr 26 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.25.2-2
- Updated python3 site path.
* Mon Apr 24 2017 Bo Gan <ganb@vmware.com> 0.25.2-1
- Update to 0.25.2.
* Fri Jan 27 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.23.4-1
- Initial build.
