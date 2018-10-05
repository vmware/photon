%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-asn1crypto
Version:        0.24.0
Release:        1%{?dist}
Summary:        A fast, pure Python library for parsing and serializing ASN.1 structures.
License:        MIT
Group:          Development/Languages/Python
URL:            https://pypi.python.org/packages/67/14/5d66588868c4304f804ebaff9397255f6ec5559e46724c2496e0f26e68d6/asn1crypto-0.22.0.tar.gz
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        asn1crypto-%{version}.tar.gz
%define sha1    asn1crypto=c8f64e99bc01d90c412891cdad97675d8fe79cc7

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
A fast, pure Python library for parsing and serializing ASN.1 structures.

%package -n     python3-asn1crypto
Summary:        A fast, pure Python library for parsing and serializing ASN.1 structures.
Requires:       python3
Requires:       python3-libs

%description -n python3-asn1crypto
Python 3 version of asn1crypto

%prep
%setup -qn asn1crypto-%{version}
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

#%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-asn1crypto
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.24.0-1
-   Update to version 0.24.0
*   Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 0.22.0-3
-   Removed %check because the source does not include the test module
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.22.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.22.0-1
-   Initial
