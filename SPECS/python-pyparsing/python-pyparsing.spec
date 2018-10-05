%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python parsing module.
Name:           python-pyparsing
Version:        2.2.0
Release:        3%{?dist}
URL:            https://pypi.python.org/pypi/pyparsing/%{version}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pyparsing-%{version}.tar.gz
%define sha1    pyparsing=f8504f4f8baa69de5b63fd2275a0ebf36a2cf74b

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python2
Requires:       python2-libs

%description
Python parsing module.

%package -n     python3-pyparsing
Summary:        python-pyparsing

Requires:       python3
Requires:       python3-libs

%description -n python3-pyparsing

Python 3 version.

%prep
%setup -q -n pyparsing-%{version}
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

#%check
#Tests are not available

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-pyparsing
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 2.2.0-3
-   Disabled check section as tests are not available
*   Tue Jun 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.0-2
-   Add build dependency with python-setuptools to handle 1.0 update
*   Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 2.2.0-1
-   Update to 2.2.0 and remove build dependency with python-setuptools
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.10-1
-   Initial packaging for Photon
