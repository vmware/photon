%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Utility tools for control groups of Linux
Name:           cgroup-utils
Version:        0.6
Release:        4%{?dist}
License:        GPLv2
Group:          Development/Libraries
URL:            https://pypi.python.org/pypi/cgroup-utils/0.6

Source0:        https://github.com/peo3/cgroup-utils/archive/%{name}-%{version}.tar.gz
%define sha1    cgroup-utils=c0c9c6ddcd7e5ce2eb04394aa1ad46e1b05eb669

BuildRequires:  python-setuptools
BuildRequires:  python2-devel

Requires:       python2

%description
cgroup-utils provides utility tools and libraries for control groups of Linux. For example, 
cgutil top is a top-like tool which shows activities of running processes in control groups.

%package -n     python3-cgroup-utils
Summary:        python3-cgroup-utils
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%description -n python3-cgroup-utils
%prep
%setup -q
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
mv %{buildroot}/%{_bindir}/cgutil %{buildroot}/%{_bindir}/cgutil3
popd
python2 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}

%check
python test_all.py
pushd ../p3dir
python3 test_all.py
popd

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/cgutil
%{python2_sitelib}/*

%files -n python3-cgroup-utils
%defattr(-,root,root)
%{_bindir}/cgutil3
%{python3_sitelib}/*

%changelog
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.6-4
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.6-3
-   Added python3 subpackage.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-2
-   GA - Bump release of all rpms
*   Wed Jan 6 2016 Xiaolin Li <xiaolinl@vmware.com> 0.6-1
-   Initial build.  First version