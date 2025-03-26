Summary:        Python Build Reasonableness
Name:           python3-pbr
Version:        5.10.0
Release:        3%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://docs.openstack.org/developer/pbr/
Source0:        https://pypi.io/packages/source/p/pbr/pbr-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-docutils
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-xml
%if 0
%if 0%{?with_check}
BuildRequires:  git
BuildRequires:  gnupg
%endif
%endif
Requires:       python3
BuildArch:      noarch
%description
A library for managing setuptools packaging needs in a consistent manner.

%prep
%autosetup -n pbr-%{version}

%build
export SKIP_PIP_INSTALL=1
%py3_build

%install
%py3_install
mv %{buildroot}/%{_bindir}/pbr %{buildroot}/%{_bindir}/pbr3

%if 0
%check
ln -sfv /usr/bin/gpg2 /usr/bin/gpg
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 coverage
$easy_install_3 hacking
$easy_install_3 mock
$easy_install_3 testrepository
$easy_install_3 testresources
$easy_install_3 testscenarios
$easy_install_3 virtualenv
$easy_install_3 wheel
python3 setup.py test

%endif

%files
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_bindir}/pbr3
%{python3_sitelib}/pbr-%{version}-*.egg-info
%{python3_sitelib}/pbr

%changelog
*   Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.10.0-3
-   Release bump for SRP compliance
*   Tue May 23 2023 Shivani Agarwal <shivania2@vmware.com> 5.10.0-2
-   Bump up version to compile with new gnupg
*   Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 5.10.0-1
-   Automatic Version Bump
*   Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 5.5.1-1
-   Automatic Version Bump
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 5.5.0-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.4.5-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 4.2.0-3
-   Mass removal python2
*   Wed Jan 16 2019 Tapas Kundu <tkundu@vmware.com> 4.2.0-2
-   Disabled the make check as the requirements can not be fulfilled
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.2.0-1
-   Update to version 4.2.0
*   Wed Jul 19 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.0-5
-   Fixed make check failure
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.0-4
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.0-3
-   Create pbr3 script
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
-   Fix arch
*   Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.0-1
-   Initial packaging for Photon
