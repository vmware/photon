%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-netaddr
Version:        0.7.19
Release:        7%{?dist}
Summary:        A network address manipulation library for Python
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://files.pythonhosted.org/packages/source/n/netaddr/netaddr-%{version}.tar.gz
Source0:        netaddr-%{version}.tar.gz
%define sha1    netaddr=00e0ce7d7ebc1d6e7943e884aa51ccb7becdc9ea
Patch0:         0001-fixed-broken-tests-in-issue-149-python-3-regression.patch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
A network address manipulation library for Python


%prep
%setup -n netaddr-%{version}
%patch0 -p1

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/netaddr %{buildroot}/%{_bindir}/netaddr3

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest
LANG=en_US.UTF-8 PYTHONPATH=./ python3 setup.py test


%files
%defattr(-,root,root,-)
%{_bindir}/netaddr3
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkudu@vmware.com> 0.7.19-7
-   Mass removal python2
*   Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> 0.7.19-6
-   Fixed make check.
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
