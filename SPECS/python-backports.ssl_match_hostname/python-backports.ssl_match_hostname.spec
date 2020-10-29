%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-backports.ssl_match_hostname
Version:        3.7.0.1
Release:        2%{?dist}
Summary:        Backported python ssl_match_hostname
License:        PSFL
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/backports.ssl_match_hostname/%{version}
Source0:        https://pypi.python.org/packages/76/21/2dc61178a2038a5cb35d14b61467c6ac632791ed05131dda72c20e7b9e23/backports.ssl_match_hostname-%{version}.tar.gz
%define sha1    backports.ssl_match_hostname=b832201f353ad35215fd5132857ac9bbb55b77c1

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Backported python ssl_match_hostname feature

%prep
%setup -n backports.ssl_match_hostname-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
%{__rm} -f %{buildroot}%{python3_sitelib}/backports/__init__.py*
find %{buildroot}%{python3_sitelib}/ -name '*.pyc' -delete -o \
    -name '*__pycache__' -delete

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Oct 28 2020 Dweep Advani <dadvani@vmware.com> 3.7.0.1-2
-   Fixed install conflicts with python3-configparser
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.7.0.1-1
-   Automatic Version Bump
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.5.0.1-2
-   Mass removal python2
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.5.0.1-1
-   Initial version of python backports.ssl_match_hostname for PhotonOS.
