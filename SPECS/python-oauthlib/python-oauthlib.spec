%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        An implementation of the OAuth request-signing logic
Name:           python-oauthlib
Version:        2.0.2
Release:        2%{?dist}
License:        BSD
Url:            https://pypi.python.org/pypi/python-oauthlib/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/fa/2e/25f25e6c69d97cf921f0a8f7d520e0ef336dd3deca0142c0b634b0236a90/oauthlib-2.0.2.tar.gz
%define sha1    oauthlib=e9d2d2dba4526cad5db3d6a18bf2ca168087efcf

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
OAuthLib is a generic utility which implements the logic of OAuth without assuming a specific HTTP request object or web framework

%package -n python3-oauthlib
Summary:        Python3 package for oauthlib
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-oauthlib
Python 3 version of oauthlib

%prep
%setup -q -n oauthlib-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build

pushd ../p3dir
python3 setup.py build
popd


%install
rm -rf %{buildroot}
python2 setup.py install --root=%{buildroot}

pushd ../p3dir
python3 setup.py install --root=%{buildroot}
popd

%check
python2 setup.py test

pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-, root, root, -)
%{python2_sitelib}/*

%files -n python3-oauthlib
%{python3_sitelib}/*

%changelog
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.2-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Apr 13 2017 Anish Swaminathan <anishs@vmware.com> 2.0.2-1
-   Initial packaging for Photon

