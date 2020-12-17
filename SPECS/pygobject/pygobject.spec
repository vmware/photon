%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-pygobject
Version:        3.38.0
Release:        3%{?dist}
Summary:        Python Bindings for GObject
Group:          Development/Languages
License:        LGPLv2+
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/PyGObject
Source0:        https://pypi.org/project/PyGObject/#files/PyGObject-%{version}.tar.gz
Patch0:         pygobject-makecheck-fixes.patch
%define sha1    PyGObject=9d87678c9b8e8771280f074d107e1e0cd612f307
Requires:       python3
Requires:       gobject-introspection
Requires:       glib
BuildRequires:  python3-setuptools
BuildRequires:  glib-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  gobject-introspection-devel
BuildRequires:  which
BuildRequires:  python3
%if %{with_check}
BuildRequires:  python3-setuptools
BuildRequires:  python3-gobject-introspection
BuildRequires:  python3-test
BuildRequires:  glib-schemas
BuildRequires:  dbus
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-xml
%endif

%description
Python bindings for GLib and GObject.


%package        devel
Summary:        Development files for embedding PyGObject introspection support
Requires:       python3-pygobject = %{version}-%{release}

%description    devel
Development files for pygobject.

%prep
%setup -q -n PyGObject-%{version}
%patch0 -p1

%build
export PYGOBJECT_WITHOUT_PYCAIRO='True'
python3 setup.py build

%install
export PYGOBJECT_WITHOUT_PYCAIRO='True'
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest
python3 setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%files  devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%changelog
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.38.0-3
-   Fix build with new rpm
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.38.0-2
-   openssl 1.1.1
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.38.0-1
-   Automatic Version Bump
*   Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 3.36.1-1
-   Automatic Version Bump
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 3.30.1-3
-   Mass removal python2
*   Thu Dec 06 2018 Tapas Kundu <tkundu@vmware.com> 3.30.1-2
-   Fix makecheck
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
