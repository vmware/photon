%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        provides a pure-Python implementation of immutable URLs
Name:           python3-hyperlink
Version:        18.0.0
Release:        3%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/python-hyper/hyperlink
Source0:        https://github.com/python-hyper/hyperlink/archive/hyperlink-%{version}.tar.gz
%define sha1    hyperlink=f51f4495795e51ae9468a13dd79ff26b3f457f40

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
%if %{with_check}
BuildRequires:  python3-idna
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
BuildArch:      noarch

%description
Hyperlink provides a pure-Python implementation of immutable URLs. Based on RFC 3986 and 3987, the Hyperlink URL makes working with both URIs and IRIs easy.

%prep
%setup -q -n hyperlink-%{version}

%build
python3 setup.py build


%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest
pytest


%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 18.0.0-3
-   Mass removal python2
*   Thu Dec 06 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-2
-   Fix make check.
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-1
-   Update to version 18.0.0
*   Wed Sep 20 2017 Bo Gan <ganb@vmware.com> 17.3.1-2
-   Fix make check issues
*   Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.3.1-1
-   Initial packaging for Photon
