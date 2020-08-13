%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-asn1crypto
Version:        1.4.0
Release:        1%{?dist}
Summary:        A fast, pure Python library for parsing and serializing ASN.1 structures.
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/packages/67/14/5d66588868c4304f804ebaff9397255f6ec5559e46724c2496e0f26e68d6/asn1crypto-0.22.0.tar.gz
Source0:        asn1crypto-%{version}.tar.gz
%define sha1    asn1crypto=dc957cec576a75a7d915b1c01ca0337736d98c1c

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
A fast, pure Python library for parsing and serializing ASN.1 structures.


%prep
%setup -qn asn1crypto-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

#%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.0-1
-   Automatic Version Bump
*   Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.24.0-2
-   Removed python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.24.0-1
-   Update to version 0.24.0
*   Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 0.22.0-3
-   Removed %check because the source does not include the test module
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.22.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.22.0-1
-   Initial
