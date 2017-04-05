%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-netaddr
Version:        0.7.19
Release:        2%{?dist}
Summary:        A network address manipulation library for Python
License:        BSD
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/source/n/netaddr/netaddr-%{version}.tar.gz
Source0:        netaddr-%{version}.tar.gz
%define sha1    netaddr=00e0ce7d7ebc1d6e7943e884aa51ccb7becdc9ea

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
A network address manipulation library for Python

%package -n python3-netaddr
Summary:        Python3-netaddr
BuildRequires:  python3-devel

%description -n python3-netaddr
Python 3 version.

%prep
%setup -n netaddr-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/netaddr %{buildroot}/%{_bindir}/netaddr3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}


%check
easy_install py
python2 test_netadr.py
pushd ../p3dir
python3 test_netadr.py
popd

%files
%defattr(-,root,root,-)
/usr/bin/netaddr
%{python2_sitelib}/*

%files -n python3-netaddr
%defattr(-,root,root,-)
/usr/bin/netaddr3
%{python3_sitelib}/*

%changelog
*   Mon Mar 27 2017 XIaolin Li <xiaolinl@vmware.com> 0.7.19-2
-   Added python3 package.
*   Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.19-1
-   Initial version of python-netaddr package for Photon.
