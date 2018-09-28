%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           pygobject
Version:        3.30.1
Release:        1%{?dist}
Summary:        Python Bindings for GObject
Group:          Development/Languages
License:        LGPLv2+
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/PyGObject
Source0:        https://pypi.org/project/PyGObject/#files/PyGObject-%{version}.tar.gz
Patch0:         pygobject-makecheck-fixes.patch
Patch1:         build_without_cairo.patch
%define sha1    PyGObject=d5a369f15dfd415dba7fad4c0f9811b56c597e10
Requires:       python2
Requires:       gobject-introspection
Requires:       glib
BuildRequires:  glib-devel
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  gobject-introspection-devel
BuildRequires:  which
%if %{with_check}
BuildRequires:  gobject-introspection-python
BuildRequires:  python3-test
BuildRequires:  python2-test
BuildRequires:  glib-schemas
BuildRequires:  dbus
%endif

%description
Python bindings for GLib and GObject.

%package -n     python3-pygobject
Summary:        python-pygobject
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs
Requires:       gobject-introspection
Requires:       glib

%description -n python3-pygobject
Python 3 version.

%package        devel
Summary:        Development files for embedding PyGObject introspection support
Requires:       pygobject = %{version}-%{release}
Requires:       python3-pygobject = %{version}-%{release}

%description    devel
Development files for pygobject.

%prep
%setup -q -n PyGObject-%{version}
%patch0 -p1
%patch1 -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd


%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-pygobject
%defattr(-,root,root,-)
%{python3_sitelib}/*

%files  devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%changelog
*   Thu Sep 27 2018 Tapas Kundu <tkundu@vmware.com> 3.30.1-1
-   Updated to release 3.30.1
*   Tue Sep 19 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.24.1-3
-   Skip some ui make check paths that failed.
*   Thu Aug 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.24.1-2
-   Fix make check
*   Fri Apr 14 2017 Xiaolin Li <xiaolinl@vmware.com> 3.24.1-1
-   Updated to version 3.24.1 and added python3 package.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 3.10.2-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.10.2-2
-   GA - Bump release of all rpms
*   Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
-   Initial build.  First version
