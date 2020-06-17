%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-appdirs
Version:        1.4.3
Release:        4%{?dist}
Summary:        Python 2 and 3 compatibility utilities
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/appdirs
Source0:        https://pypi.python.org/packages/48/69/d87c60746b393309ca30761f8e2b49473d43450b150cb08f3c6df5c11be5/appdirs-%{version}.tar.gz
%define sha1    appdirs=9ad09395ed489ad66e9688e49087ce1814c64276
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir".

%prep
%setup -n appdirs-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
cd test

PATH=%{buildroot}%{_bindir}:${PATH} \
 PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 test_api.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 1.4.3-4
-   Mass removal python2
*   Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.3-3
-   Changes to check section
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.3-2
-   Change python to python2
*   Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 1.4.3-1
-   Create appdirs 1.4.3
