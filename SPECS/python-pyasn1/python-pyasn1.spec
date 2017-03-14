Name:           python-pyasn1
Version:        0.2.3
Release:        1%{?dist}
Summary:        Implementation of ASN.1 types and codecs in Python programming language
License:        BSD
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/p/pyasn1/pyasn1-%{version}.tar.gz
Source0:        pyasn1-%{version}.tar.gz
%define sha1    pyasn1=e30253a024d1388a96be8e84245a0d38f47467ff

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires: python2
Requires: python2-libs

BuildArch:      noarch

%description
This is an implementation of ASN.1 types and codecs in Python programming language. It has been first written to support particular protocol (SNMP) but then generalized to be suitable for a wide range of protocols based on ASN.1 specification.

%prep
%setup -n pyasn1-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 0.2.3-1
-   Updated to version 0.2.3.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.9-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.1.9-1
-   Upgraded to version 0.1.9
*   Thu Aug 6 2015 Anish Swaminathan <anishs@vmware.com>
-   Added sha1sum
*   Fri Mar 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
