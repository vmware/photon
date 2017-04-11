%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-pip
Version:        9.0.1
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/pip
Summary:        The PyPA recommended tool for installing Python packages.
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-%{version}.tar.gz 
%define sha1 pip=57ff41e99cb01b6a1c2b0999161589b726f0ec8b
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
The PyPA recommended tool for installing Python packages.

%package -n     python3-pip
Summary:        python-pip
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-pip
Python 3 version.

%prep
%setup -q -n pip-%{version}
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
easy_install freezegun
%{__python2} setup.py test
pushd ../p3dir
easy_install freezegun
%{__python3} setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/*

%files -n python3-pip
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
*   Mon Apr 10 2017 Sarah Choi <sarahc@vmware.com> 9.0.1-2
-   Support python3
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 9.0.1-1
-   Upgrade version to 9.0.1
*   Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 8.1.2-1
-   Initial packaging for Photon
