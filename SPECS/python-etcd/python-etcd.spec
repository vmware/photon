%define sha1    etcd=61955fde080a81c36b00dfd98a2216a098baa986
%define sha1    etcd=61955fde080a81c36b00dfd98a2216a098baa986

Name:           python-etcd
Version:        2.0.8
Release:        1%{?dist}
Summary:        Python API for etcd
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/python-etcd
Source0:        %{name}-%{version}.tar.gz
%define sha1    etcd=61955fde080a81c36b00dfd98a2216a098baa986
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
Python API for etcd

%package -n     python3-etcd
Summary:        Python3 API for etcd
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools

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
*   Fri Sep 07 2018 Tapas Kundu <tkundu@vmware.com> 2.0.8-1
-   Update to version 2.0.8
*   Sat Aug 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.5-1
-   Initial version of python etcd for PhotonOS.
