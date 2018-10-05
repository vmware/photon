%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Attributes without boilerplate.
Name:           python-attrs
Version:        18.2.0
Release:        1%{?dist}
URL:            https://pypi.python.org/pypi/attrs
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        attrs-%{version}.tar.gz
%define sha1    attrs=51a52e1afdd9e8c174ac0b65c2905a8360788dd2

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python2
Requires:       python2-libs

%description
Attributes without boilerplate.

%package -n     python3-attrs
Summary:        python-attrs

Requires:       python3
Requires:       python3-libs

%description -n python3-attrs

Python 3 version.

%prep
%setup -q -n attrs-%{version}
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
python2 setup.py test
#python3 does not support zope module for tests

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-attrs
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.2.0-1
-   Update to version 18.2.0
*   Thu Jul 06 2017 Chang Lee <changlee@vmware.com> 16.3.0-3
-   Updated %check
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.3.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 16.3.0-1
-   Initial packaging for Photon
