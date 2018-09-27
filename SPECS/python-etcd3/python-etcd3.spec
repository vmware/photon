%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-etcd3
Version:        0.8.1
Release:        1%{?dist}
Summary:        Python client for the etcd API v3
License:        Apache Software License (Apache Software License 2.0)
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/etcd3
Source0:        etcd3-%{version}.tar.gz
%define sha1    etcd3=42dcb3d54bff818202ec4c1b1f4257f7c9c70d34
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-pip
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
BuildArch:      noarch

%description
Python client for the etcd API v3

%package -n     python3-etcd3
Summary:        Python3 API for etcd
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools

%description -n python3-etcd3
Python client for the etcd API v3

%prep
%setup -n etcd3-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-etcd3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Sep 27 2018 Tapas Kundu <tkundu@vmware.com> 0.8.1-1
-   Initial version of python etcd3 for PhotonOS.
