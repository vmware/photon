%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           pycairo
Version:        1.17.1
Release:        1%{?dist}
Summary:        Pycairo is a Python module providing bindings for the cairo graphics library.
License:        LGPL version 2.1 or MPL version 1.1
Group:          Development/Languages/Python
Url:            https://github.com/pygobject/pycairo
Source0:        %{name}-%{version}.tar.gz
%define sha1    pycairo=6667cae30b6a3ce1e71bcb05d4cbeda659f1e16c
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-pip
BuildRequires:  python-setuptools
BuildRequires:  pkg-config
BuildRequires:  glib-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libpng-devel
BuildRequires:  cairo-devel
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools

%description
Pycairo is a Python module providing bindings for the cairo graphics library.

%package -n     python3-pycairo
Summary:        Python3 API for etcd
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  glib-devel
BuildRequires:  libpng-devel
BuildRequires:  python3-setuptools
BuildRequires:  fontconfig-devel
BuildRequires:  pkg-config
BuildRequires:  cairo-devel

%description -n python3-pycairo
Pycairo is a Python module providing bindings for the cairo graphics library.

%prep
%setup -n %{name}-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
#python2 setup.py build
#pushd ../p3dir
#python3 setup.py build
#popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
/usr/lib/python2.7/site-packages/cairo/*
/usr/lib/python2.7/site-packages/pycairo-1.17.1-py2.7.egg-info
/usr/include/pycairo/py3cairo.h
/usr/include/pycairo/pycairo.h
/usr/lib/pkgconfig/py3cairo.pc
/usr/lib/pkgconfig/pycairo.pc

%files -n python3-pycairo
%defattr(-,root,root,-)
#%{python3_sitelib}/*
/usr/lib/python3.6/site-packages/cairo/*
/usr/lib/python3.6/site-packages/pycairo-1.17.1-py3.6.egg-info
/usr/include/pycairo/py3cairo.h
/usr/include/pycairo/pycairo.h
/usr/lib/pkgconfig/py3cairo.pc
/usr/lib/pkgconfig/pycairo.pc

%changelog
*   Thu Sep 27 2018 Tapas Kundu <tkundu@vmware.com> 1.17.1-1
-   Initial version of python pycairo for PhotonOS.
