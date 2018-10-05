%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-jsonpointer
Version:        2.0
Release:        1%{?dist}
Summary:        Applying JSON Patches in Python
License:        Modified BSD License
Group:          Development/Languages/Python
URL:            https://pypi.python.org/packages/source/j/jsonpointer/jsonpointer-%{version}.tar.gz
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        jsonpointer-%{version}.tar.gz
%define sha1    jsonpointer=f0733349a44b0c777ef9b8e0256d628e2530624b

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires: python2
Requires: python2-libs

BuildArch:      noarch

%description
Library to apply JSON Patches according to RFC 6902.

%package -n     python3-jsonpointer
Summary:        python-jsonpointer

Requires:       python3
Requires:       python3-libs

%description -n python3-jsonpointer

%prep
%setup -n jsonpointer-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%check
python2 tests.py
pushd ../p3dir
python3 tests.py
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/jsonpointer %{buildroot}/%{_bindir}/jsonpointer3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
%{_bindir}/jsonpointer

%files -n python3-jsonpointer
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/jsonpointer3

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.0-1
-   Update to version 2.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.10-6
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Wed Apr 26 2017 Sarah Choi <sarahc@vmware.com> 1.10-5
-   Rename jsonpointer for python3
*   Thu Apr 06 2017 Sarah Choi <sarahc@vmware.com> 1.10-4
-   support python3
*   Tue Oct 04 2016 ChangLee <changlee@vmware.com> 1.10-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10-1
-   Updated to version 1.10
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
