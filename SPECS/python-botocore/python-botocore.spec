%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        Amazon Web Services Library.
Name:           python3-botocore
Version:        1.18.10
Release:        1%{?dist}
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/boto/botocore
Source0:        https://github.com/boto/botocore/archive/botocore-%{version}.tar.gz
%define sha1    botocore=2c3bcfaff95937e43606fefac321eb85bc4d8ca5
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-dateutil
BuildRequires:  python3-urllib3
%endif
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch

%description
A low-level interface to a growing number of Amazon Web Services. The botocore package is the foundation for the AWS CLI as well as boto3.


%prep
%setup -q -n botocore-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip3 install nose
pip3 install mock
pip3 install jmespath
nosetests tests/unit

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 1.18.10-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.18.5-1
-   Automatic Version Bump
*   Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.59-1
-   Automatic Version Bump
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.58-1
-   Automatic Version Bump
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.53-1
-   Automatic Version Bump
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.49-1
-   Automatic Version Bump
*   Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.41-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.28-1
-   Automatic Version Bump
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.12.0-3
-   Mass removal python2
*   Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 1.12.0-2
-   Fix make check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.12.0-1
-   Update to version 1.12.0
*   Sun Jan 07 2018 Kumar Kaushik <kaushikk@vmware.com> 1.8.15-1
-   Initial packaging for photon.
