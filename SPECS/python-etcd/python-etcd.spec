%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-etcd
Version:        0.4.5
Release:        1%{?dist}
Summary:        Python API for etcd
License:        MIT
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/python-etcd
Source0:        %{name}-%{version}.tar.gz
%define sha1    python-etcd=9e79ae82429cf2ffbe2b5647e14bc29571afd766
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-pip
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
BuildArch:      noarch

%description
Python API for etcd

%package -n     python3-etcd
Summary:        Python3 API for etcd

%description -n python3-etcd
Python3 API for etcd

%prep
%setup -n %{name}-%{version}
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

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-etcd
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sat Aug 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.5-1
-   Initial version of python etcd for PhotonOS.
