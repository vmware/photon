%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-PyHamcrest
Version:        1.9.0
Release:        1%{?dist}
Summary:        Python Hamcrest framework for matcher objects
Group:          Development/Libraries
License:        BSD License (New BSD)
URL:            https://pypi.org/project/PyHamcrest
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/n/deepmerge/PyHamcrest-%{version}.tar.gz
%define sha1    PyHamcrest=e9edf0bd613f10540a92e403005fbdaccbc8c868
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python-xml
BuildRequires:  python3-xml
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch

%description
PyHamcrest is a framework for writing matcher objects, allowing you to declaratively define “match” rules.

%package -n python3-PyHamcrest
Summary:        Python Hamcrest framework for matcher objects
Requires:       python3
Requires:       python3-libs

%description -n python3-PyHamcrest
PyHamcrest is a framework for writing matcher objects, allowing you to declaratively define “match” rules.

%prep
%setup -q -n PyHamcrest-%{version}
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
#no test folder in source tar

%clean
rm -rf %{buildroot}/*


%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-PyHamcrest
%defattr(-,root,root)
%doc README.rst
%doc LICENSE.txt
%{python3_sitelib}/*

%changelog
*  Fri Aug 30 2019 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
-  Initial packaging for photon OS
