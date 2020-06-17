%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-configobj
Version:        5.0.6
Release:        5%{?dist}
Summary:        Config file reading, writing and validation
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/packages/source/c/configobj/configobj-%{version}.tar.gz
Source0:        configobj-%{version}.tar.gz
%define sha1 configobj=add3ae15e3f0d2d28d37370dcad930243cb4145c

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools

Requires:       python3-six

BuildArch:      noarch

%description
ConfigObj is a simple but powerful config file reader and writer: an ini file round tripper. Its main feature is that it is very easy to use, with a straightforward programmer’s interface and a simple syntax for config files.


%prep
%setup -n configobj-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 validate.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 5.0.6-5
-   Mass removal python2
*   Mon May 15 2017 Kumar Kaushik <kaushikk@vmware.com> 5.0.6-4
-   Adding python 3 support.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 5.0.6-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.0.6-2
-   GA - Bump release of all rpms
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
