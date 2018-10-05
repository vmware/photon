%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-configobj
Version:        5.0.6
Release:        4%{?dist}
Summary:        Config file reading, writing and validation
License:        BSD
Group:          Development/Languages/Python
URL:            https://pypi.python.org/packages/source/c/configobj/configobj-%{version}.tar.gz
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        configobj-%{version}.tar.gz
%define sha1 configobj=add3ae15e3f0d2d28d37370dcad930243cb4145c

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python-six

BuildArch:      noarch

%description
ConfigObj is a simple but powerful config file reader and writer: an ini file round tripper. Its main feature is that it is very easy to use, with a straightforward programmer’s interface and a simple syntax for config files.

%package -n     python3-configobj
Summary:        python-configobj


Requires:       python3-six

%description -n python3-configobj
Python 3 version.

%prep
%setup -n configobj-%{version}
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
python2 validate.py
pushd ../p3dir
python3 validate.py
popd

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*


%files -n python3-configobj
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon May 15 2017 Kumar Kaushik <kaushikk@vmware.com> 5.0.6-4
-   Adding python 3 support.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 5.0.6-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.0.6-2
-   GA - Bump release of all rpms
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
