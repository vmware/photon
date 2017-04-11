%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-ipaddress
Version:        1.0.18
Release:        2%{?dist}
Summary:        Port of the 3.3+ ipaddress module to 2.6, 2.7, 3.2
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/ipaddress
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:        ipaddress-%{version}.tar.gz
%define sha1    ipaddress=f15a3714e4bea2ddfe54e80ad6f7b5de57cc94c5

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
IPv4/IPv6 manipulation library

%package -n     python3-ipaddress
Summary:        python-ipaddress
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-ipaddress
Python 3 version.

%prep
%setup -n ipaddress-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python2 setup.py build
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
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-ipaddress
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Apr 10 2017 Sarah Choi <sarahc@vmware.com> 1.0.18-2
-   Support python3
*   Thu Feb 16 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.18-1
-   Initial packaging for Photon
