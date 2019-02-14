%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-imagesize
Version:        1.1.0
Release:        1%{?dist}
Summary:        python module to analyze jpeg/jpeg2000/png/gif image header and return image size.
License:        MIT
Group:          Development/Languages/Python
Url:            https://github.com/shibukawa/imagesize_py
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/53/72/6c6f1e787d9cab2cc733cf042f125abec07209a58308831c9f292504e826/imagesize-%{version}.tar.gz
%define sha1    imagesize=48b7277a450654db77dc956812020525f5e478c8

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
python module to analyze jpeg/jpeg2000/png/gif image header and return image size.

%package -n     python3-imagesize
Summary:        python module to analyze jpeg/jpeg2000/png/gif image header and return image size.
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-imagesize

Python 3 version.

%prep
%setup -n imagesize-%{version}
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
py.test2
py.test3

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-imagesize
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.1.0-1
-   Update to version 1.1.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.1-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.1-2
-   Change python to python2
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.1-1
-   Initial
