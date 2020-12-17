%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Core utilities for Python packages
Name:           python3-packaging
Version:        20.4
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/packaging
License:        BSD or ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pypi.python.org/packages/source/p/packaging/packaging-%{version}.tar.gz
%define sha1    packaging=b99fa7af153646722b2d1817bb09906cc5a94bc6
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%if %{with_check}
BuildRequires:  python3-setuptools
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-xml
BuildRequires:  python3-pyparsing
BuildRequires:  python3-six
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-pyparsing
Requires:       python3-six

BuildArch:      noarch

Provides: python3.9dist(packaging)

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.


%prep
%setup -q -n packaging-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pretend pytest
PYTHONPATH=./ pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 20.4-3
-   Fix build with new rpm
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 20.4-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.4-1
-   Automatic Version Bump
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 17.1-3
-   Mass removal python2
*   Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 17.1-2
-   Fix makecheck
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.1-1
-   Update to version 17.1
*   Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 16.8-4
-   Fixed rpm check errors
-   Fixed runtime dependencies
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 16.8-3
-   Fix arch
*   Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 16.8-2
-   Remove python-setuptools from BuildRequires
*   Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> 16.8-1
-   Initial packaging for Photon
