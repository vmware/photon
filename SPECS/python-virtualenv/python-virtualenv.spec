%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-virtualenv
Version:        20.0.31
Release:        1%{?dist}
Summary:        Virtual Python Environment builder
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/virtualenv
Source0:        virtualenv-%{version}.tar.gz
%define sha1    virtualenv=e645d4d1395b712b38fb4ec742e748ab3a47b88d
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  curl-devel
Requires:       python3
Requires:       python3-libs
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
virtualenv is a tool to create isolated Python environment.

%prep
%setup -n virtualenv-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{_bindir}/virtualenv
%{python3_sitelib}/*

%changelog
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.31-1
-   Automatic Version Bump
*   Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.30-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.28-1
-   Automatic Version Bump
*   Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 16.0.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 16.0.0-1
-   Update to version 16.0.0
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 15.1.0-1
-   Initial version of python-virtualenv package for Photon.
