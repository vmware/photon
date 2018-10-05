%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-backports.ssl_match_hostname
Version:        3.5.0.1
Release:        1%{?dist}
Summary:        Backported python ssl_match_hostname
License:        PSFL
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/backports.ssl_match_hostname/%{version}
Source0:        https://pypi.python.org/packages/76/21/2dc61178a2038a5cb35d14b61467c6ac632791ed05131dda72c20e7b9e23/backports.ssl_match_hostname-%{version}.tar.gz
%define sha1    backports.ssl_match_hostname=0567c136707a5f53b95aa793b79cc8d5c61d8e22

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Backported python ssl_match_hostname feature

%prep
%setup -n backports.ssl_match_hostname-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.5.0.1-1
-   Initial version of python backports.ssl_match_hostname for PhotonOS.
