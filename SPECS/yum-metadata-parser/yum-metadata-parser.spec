%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A fast metadata parser for yum
Name:           yum-metadata-parser
Version:        1.1.4
Release:        4%{?dist}
License:        GPLv2+
Group:          Development/Libraries
URL:            http://devel.linux.duke.edu/cgi-bin/viewcvs.cgi/yum-metadata-parser/
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    yum-metadata-parser=044e69a04ea5ac39d79020d9e1f1a35c9dc64d9b
Patch0:         Upstream-py3-string-split.patch
BuildRequires:  pkg-config
BuildRequires:  python2-devel
BuildRequires:  glib-devel
BuildRequires:  libxml2
BuildRequires:  libxml2-devel
BuildRequires:  sqlite-devel
BuildRequires:  python2-libs
Requires:       libxml2
Requires:       glib
Requires:       python2
%description
Fast metadata parser for yum implemented in C.

%package -n     python3-yum-metadata-parser
Summary:        python3-yum-metadata-parser
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs
Requires:       libxml2
Requires:       glib

%description -n python3-yum-metadata-parser

%prep
%setup
%patch0 -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install -O1 --root=%{buildroot}
pushd ../p3dir
python3 setup.py install -O1 --root=%{buildroot}
popd

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{python2_sitelib}/_sqlitecache.so
%{python2_sitelib}/sqlitecachec.py
%{python2_sitelib}/sqlitecachec.pyc
%{python2_sitelib}/sqlitecachec.pyo
%{python2_sitelib}/*egg-info

%files -n python3-yum-metadata-parser
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 1.1.4-4
-   Added python3 site-packages.
*   Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 1.1.4-3
-   Use sqlite-{devel,libs}
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.4-2
-   GA - Bump release of all rpms