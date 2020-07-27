%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        An implementation of the OAuth request-signing logic
Name:           python3-oauthlib
Version:        3.1.0
Release:        1%{?dist}
License:        BSD
Url:            https://pypi.python.org/pypi/python-oauthlib/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/fa/2e/25f25e6c69d97cf921f0a8f7d520e0ef336dd3deca0142c0b634b0236a90/oauthlib-%{version}.tar.gz
%define sha1    oauthlib=a61703d89f11dd35ec76dd8097aa8ce3a5373e00

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  libffi-devel
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
OAuthLib is a generic utility which implements the logic of OAuth without assuming a specific HTTP request object or web framework


%prep
%setup -q -n oauthlib-%{version}

%build
python3 setup.py build


%install
rm -rf %{buildroot}
python3 setup.py install --root=%{buildroot}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 mock
python3 setup.py test

%files
%defattr(-, root, root, -)
%{python3_sitelib}/*

%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.0-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.1.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.1.0-1
-   Update to version 2.1.0
*   Fri Jul 07 2017 Chang Lee <changlee@vmware.com> 2.0.2-3
-   Add  libffi-devel in BuildRequires and install mock python module in %check
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.2-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Apr 13 2017 Anish Swaminathan <anishs@vmware.com> 2.0.2-1
-   Initial packaging for Photon

