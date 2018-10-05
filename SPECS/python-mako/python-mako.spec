%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-mako
Version:        1.0.7
Release:        1%{?dist}
Summary:        Python templating language
License:        MIT
Group:          Development/Languages/Python
URL:            https://pypi.python.org/packages/56/4b/cb75836863a6382199aefb3d3809937e21fa4cb0db15a4f4ba0ecc2e7e8e/Mako-%{version}.tar.gz
Source0:        Mako-%{version}.tar.gz
%define sha1    Mako=bf0c1f4cdfca4dd37bc0c9f83e984a0558268b42

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytest

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
A super-fast templating language that borrows the best ideas from the existing templating languages. Mako is a template library written in Python. It provides a familiar, non-XML syntax which compiles into Python modules for maximum performance. Mako’s syntax and API borrows from the best ideas of many others, including Django templates, Cheetah, Myghty, and Genshi.

%package -n     python3-mako
Summary:        python-mako
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-libs

%description -n python3-mako
Python 3 version.
%prep
%setup -n Mako-%{version}
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
mv %{buildroot}/%{_bindir}/mako-render %{buildroot}/%{_bindir}/mako-render3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/mako-render

%files -n python3-mako
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/mako-render3

%changelog
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
