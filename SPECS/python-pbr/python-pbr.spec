Summary:        Python Build Reasonableness
Name:           python3-pbr
Version:        5.5.1
Release:        2%{?dist}
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://docs.openstack.org/developer/pbr/
Source0:        https://pypi.io/packages/source/p/pbr/pbr-%{version}.tar.gz
%define sha1    pbr=a79db0e5a9d9d2f1ba4c6369b3a83f0f5d37a62c
Patch0:         disable-test-wsgi.patch
BuildRequires:  python3-docutils
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-xml
%if 0
%if %{with_check}
BuildRequires:  git
BuildRequires:  gnupg
BuildRequires:  python3-pip
%endif
%endif
Requires:       python3
BuildArch:      noarch
%description
A library for managing setuptools packaging needs in a consistent manner.


%prep
%autosetup -p1 -n pbr-%{version}

%build
export SKIP_PIP_INSTALL=1
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/pbr %{buildroot}/%{_bindir}/pbr3

%if 0
%check
ln -sfv /usr/bin/gpg2 /usr/bin/gpg
pip3 install coverage hacking mock testrepository testresources testscenarios virtualenv wheel
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
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 5.5.1-2
-   Update release to compile with python 3.10
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
