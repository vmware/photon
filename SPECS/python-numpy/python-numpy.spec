%define srcname numpy

Summary:        Array processing for numbers, strings, records, and objects
Name:           python3-numpy
Version:        1.23.4
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/numpy

Source0: https://files.pythonhosted.org/packages/64/8e/9929b64e146d240507edaac2185cd5516f00b133be5b39250d253be25a64/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=727ca8950b0fbd5670e939b1c9c5cea852781ec4254d56a1659a91dc0430fc10b01ffdd16e1bb28a62319f91029e087024f4c6298bfc859a6050bfb507edcff8

BuildRequires: python3-setuptools
BuildRequires: python3-devel
BuildRequires: lapack-devel
BuildRequires: unzip
BuildRequires: cython3

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-hypothesis
BuildRequires: python3-test
BuildRequires: python3-typing-extensions
%endif

Requires: python3
Requires: lapack

%description
NumPy is a general-purpose array-processing package designed to efficiently
manipulate large multi-dimensional arrays of arbitrary records without
sacrificing too much speed for small multi-dimensional arrays.
NumPy is built on the Numeric code base and adds features introduced by
numarray as well as an extended C-API and the ability to create arrays of
arbitrary type which also makes NumPy suitable for interfacing with
general-purpose data-base applications.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %python3 runtests.py --no-build

%files
%defattr(-,root,root,-)
%{_bindir}/f2py3
%{_bindir}/f2py
%{_bindir}/f2py%{python3_version}
%{python3_sitelib}/*

%changelog
* Sat Aug 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.23.4-2
- Add lapack to requires
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.23.4-1
- Update to 1.23.4
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.4-1
- Automatic Version Bump
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 1.19.2-3
- Build with python 3.9
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.19.2-2
- openssl 1.1.1
* Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.2-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.1-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.15.1-3
- Mass removal python2
* Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> 1.15.1-2
- Fixed make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.15.1-1
- Update to version 1.15.1
* Fri Aug 25 2017 Alexey Makhalov <amakhalov@vmware.com> 1.12.1-5
- Fix compilation issue for glibc-2.26
* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 1.12.1-4
- Fixed rpm check errors
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.12.1-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu May 04 2017 Sarah Choi <sarahc@vmware.com> 1.12.1-2
- Fix typo in Source0
* Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.12.1-1
- Upgrade version to 1.12.1
* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.2-1
- Initial packaging for Photon
