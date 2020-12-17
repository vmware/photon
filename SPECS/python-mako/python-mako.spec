%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-mako
Version:        1.1.3
Release:        2%{?dist}
Summary:        Python templating language
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/packages/56/4b/cb75836863a6382199aefb3d3809937e21fa4cb0db15a4f4ba0ecc2e7e8e/Mako-%{version}.tar.gz
Source0:        Mako-%{version}.tar.gz
%define sha1    Mako=098f90baefe938434e426b8682cdfb89fa223eba

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools

%if %{with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
A super-fast templating language that borrows the best ideas from the existing templating languages. Mako is a template library written in Python. It provides a familiar, non-XML syntax which compiles into Python modules for maximum performance. Mako’s syntax and API borrows from the best ideas of many others, including Django templates, Cheetah, Myghty, and Genshi.

%prep
%setup -n Mako-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/mako-render %{buildroot}/%{_bindir}/mako-render3

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/mako-render3

%changelog
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.1.3-2
-   Fix build with new rpm
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.3-1
-   Automatic Version Bump
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 1.0.7-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.0.7-1
-   Update to version 1.0.7
*   Thu Jul 06 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.6-5
-   Fix make check issues.
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.6-4
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.6-3
-   Separate the python2 and python3 specific scripts in the bin directory
*   Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.6-2
-   Added python3 package.
*   Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.6-1
-   Initial version of python-mako package for Photon.
