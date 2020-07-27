%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        MessagePack (de)serializer.
Name:           python3-msgpack
Version:        1.0.0
Release:        1%{?dist}
License:        Apache Software License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://msgpack.org/
Source0:        https://pypi.io/packages/source/m/msgpack-python/msgpack-%{version}.tar.gz
%define sha1    msgpack=d55eda443260ae6af169f007e2dcf4e56529f4f0

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description
MessagePack is a fast, compact binary serialization format, suitable for similar data to JSON. This package provides CPython bindings for reading and writing MessagePack data.


%prep
%setup -q -n msgpack-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.0-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.5.6-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.5.6-1
-   Update to version 0.5.6
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.8-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu May 25 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.8-1
-   Initial version
