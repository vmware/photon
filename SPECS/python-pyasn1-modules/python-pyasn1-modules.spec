%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A collection of ASN.1-based protocols modules.
Name:           python-pyasn1-modules
Version:        0.0.8
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/pyasn1-modules
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pyasn1-modules-%{version}.tar.gz
%define sha1    pyasn1-modules=0ee39382b5b97c8694a3373706edc1baea2e0e71

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
This is a small but growing collection of ASN.1 data structures expressed in Python terms using pyasn1 data model.

It’s thought to be useful to protocol developers and testers.

All modules are py2k/py3k-compliant.

If you happen to convert some ASN.1 module into pyasn1 that is not yet present in this collection and wish to contribute - please send it to me.

Written by Ilya Etingof <ilya@glas.net>.

%package -n     python3-pyasn1-modules
Summary:        python-pyasn1-modules
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-pyasn1-modules

Python 3 version.

%prep
%setup -q -n pyasn1-modules-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-pyasn1-modules
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.8-1
-   Initial packaging for Photon
