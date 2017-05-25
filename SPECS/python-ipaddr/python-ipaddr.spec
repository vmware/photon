%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-ipaddr
Version:        2.1.11
Release:        3%{?dist}
Url:            https://github.com/google/ipaddr-py
Summary:        Google's Python IP address manipulation library
License:        Apache2
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/i/ipaddr/ipaddr-%{version}.tar.gz
%define sha1 ipaddr=f9a16ddb3cf774b8dcf8894c2f4295c4e17d0ed3
Patch0:         ipaddr-python3-compatibility.patch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:	python2-libs

BuildArch:      noarch

%description
ipaddr.py is a library for working with IP addresses, both IPv4 and IPv6. It was developed by Google for internal use, and is now open source.

%package -n     python3-ipaddr
Summary:        python-ipaddr
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-ipaddr
Python 3 version.

%prep
%setup -q -n ipaddr-%{version}
%patch0 -p1
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
python2 ipaddr_test.py
pushd ../p3dir
python3 ipaddr_test.py
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-ipaddr
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed May 24 2017 Kumar Kaushik <kaushikk@vmware.com> 2.1.11-3
-   Adding python 3 support.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.11-2
-   GA - Bump release of all rpms
*   Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
