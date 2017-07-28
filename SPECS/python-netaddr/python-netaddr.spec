%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-netaddr
Version:        0.7.19
Release:        5%{?dist}
Summary:        A network address manipulation library for Python
License:        BSD
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/source/n/netaddr/netaddr-%{version}.tar.gz
Source0:        netaddr-%{version}.tar.gz
%define sha1    netaddr=00e0ce7d7ebc1d6e7943e884aa51ccb7becdc9ea
Patch0:         0001-fixed-broken-tests-in-issue-149-python-3-regression.patch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  python-pytest
%endif

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
A network address manipulation library for Python

%package -n python3-netaddr
Summary:        Python3-netaddr
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pytest
%endif
%description -n python3-netaddr
Python 3 version.

%prep
%setup -n netaddr-%{version}
%patch0 -p1
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
PYTHONPATH=./ py.test2
pushd ../p3dir
LANG=en_US.UTF-8 PYTHONPATH=./ py.test3
popd

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
%{_bindir}/netaddr

%files -n python3-netaddr
%defattr(-,root,root,-)
%{_bindir}/netaddr3
%{python3_sitelib}/*

%changelog
*   Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 0.7.19-5
-   Fixed test command and added patch to fix test issues.
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.19-4
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.19-3
-   Separate python2 and python3 bindings
*   Mon Mar 27 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.19-2
-   Added python3 package.
*   Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.19-1
-   Initial version of python-netaddr package for Photon.
