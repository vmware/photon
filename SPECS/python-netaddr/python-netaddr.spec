%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-netaddr
Version:        0.7.19
Release:        1%{?dist}
Summary:        A network address manipulation library for Python
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/0c/13/7cbb180b52201c07c796243eeff4c256b053656da5cfe3916c3f5b57b3a0/netaddr-0.7.19.tar.gz
Source0:        netaddr-%{version}.tar.gz
%define sha1    netaddr=00e0ce7d7ebc1d6e7943e884aa51ccb7becdc9ea

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
A network address manipulation library for Python

%prep
%setup -n netaddr-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
%{__python} test_netadr.py

%files
%defattr(-,root,root,-)
/usr/bin/netaddr
%{python_sitelib}/*

%changelog
*   Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.19-1
-   Initial version of python-netaddr package for Photon.
