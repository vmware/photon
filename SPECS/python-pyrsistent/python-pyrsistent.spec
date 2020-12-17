%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Persistent/Functional/Immutable data structures
Name:           python3-pyrsistent
Version:        0.17.3
Release:        2%{?dist}
License:        MIT License (MIT)
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pyrsistent
Source0:        https://files.pythonhosted.org/packages/9f/0d/cbca4d0bbc5671822a59f270e4ce3f2195f8a899c97d0d5abb81b191efb5/pyrsistent-%{version}.tar.gz
%define sha1    pyrsistent=d762223188b86093fa89ddb239a24bdf972a1259
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-six
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-hypothesis
BuildRequires:  python3-attrs
BuildRequires:  python3-sortedcontainers
Requires:       python3-attrs
Requires:       python3
Requires:       python3-libs

%description
Pyrsistent is a number of persistent collections (by some referred to as functional data structures).
Persistent in the sense that they are immutable.

All methods on a data structure that would normally mutate it instead return a new copy of the structure containing the requested updates.
The original structure is left untouched.

This will simplify the reasoning about what a program does since no hidden side effects ever can take place to these data structures.
You can rest assured that the object you hold a reference to will remain the same throughout its lifetime and need not worry that
somewhere five stack levels below you in the darkest corner of your application someone has decided to remove that element that you expected to be there.

Pyrsistent is influenced by persistent data structures such as those found in the standard library of Clojure.
The data structures are designed to share common elements through path copying. It aims at taking these concepts
and make them as pythonic as possible so that they can be easily integrated into any python program without hassle.

%prep
%setup -q -n pyrsistent-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.17.3-2
-   Fix build with new rpm
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.17.3-1
-   Automatic Version Bump
*   Thu Jul 30 2020 Tapas Kundu <tkundu@vmware.com> 0.16.0-1
-   Initial packaging for Photon
