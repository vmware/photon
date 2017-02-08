%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        XML and HTML with Python
Name:           python-lxml
Version:        3.5.0b1
Release:        3%{?dist}
Group:          Development/Libraries
License:        BSD
URL:            http://lxml.de
Source0:        https://github.com/lxml/lxml/archive/lxml-%{version}.tar.gz
%define sha1    lxml=59763f575c589069b4477b737129a0430df68252
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-xml
BuildRequires:  libxslt
BuildRequires:  libxslt-devel
BuildRequires:  cython
Requires:       python2
Requires:       libxslt

%description
The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt. It is unique in that it combines the speed and XML feature completeness of these libraries with the simplicity of a native Python API, mostly compatible but superior to the well-known ElementTree API. 

%package -n     python3-lxml
Summary:        python-lxml
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  libxslt
BuildRequires:  libxslt-devel
BuildRequires:  cython
Requires:       libxslt
Requires:       python3
Requires:       python3-libs

%description -n python3-lxml
Python 3 version.

%prep
%setup -q -n lxml-lxml-%{version}

%build
%{__python} setup.py build
python3 setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitearch}/lxml/*
%{python_sitearch}/lxml-3.5.0b1-py2.7.egg-info

%files -n python3-lxml
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Feb 08 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.0b1-3
-   Added python3 site-packages.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.0b1-2
-   GA - Bump release of all rpms
*   Wed Oct 28 2015 Divya Thaluru <dthaluru@vmware.com> 3.5.0b1-1
-   Initial build.
