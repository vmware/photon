Name:           python-etcd
Version:        0.4.5
Release:        4%{?dist}
Summary:        Python API for etcd
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/python-etcd
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/jplana/python-etcd/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=c59d7a67492a2e4e72b1ae3ea73ac85a073b9d4516d1ebc48601ba67ac9609fbc45574d97e8dfae3ed4f511f090343ff980160043676252125ce2e2edc7bd154

Patch0: auth-api-compatibility.patch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%if 0%{?with_check}
BuildRequires: python-pip
BuildRequires: python-dnspython
BuildRequires: python-urllib3
BuildRequires: python-pyOpenSSL
BuildRequires: etcd
BuildRequires: openssl-devel
BuildRequires: curl-devel
BuildRequires: libffi-devel
BuildRequires: python3-dnspython
BuildRequires: python3-urllib3
BuildRequires: python3-pyOpenSSL
BuildRequires: python3-pip
%endif

Requires: python2
Requires: python-setuptools

BuildArch: noarch

%description
Python API for etcd

%package -n     python3-etcd
Summary: Python3 API for etcd
Requires: python3
Requires: python3-setuptools
Requires: python3-dnspython
Requires: python3-urllib3

%description -n python3-etcd
Python3 API for etcd

%prep
%autosetup -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
%py_build
pushd ../p3dir
%py3_build
popd

%install
%py_install

pushd ../p3dir
%py3_install
popd

%if 0%{?with_check}
%check
pip3 install nose mock
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%files -n python3-etcd
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Feb 28 2024 Anmol Jain <anmolja@vmware.com> 0.4.5-4
- Bump version as a part of etcd upgrade
* Wed Aug 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.4.5-3
- Add python3-dnspython to requires
* Tue Dec 04 2018 Ashwin H<ashwinh@vmware.com> 0.4.5-2
- Add %check
* Sat Aug 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.5-1
- Initial version of python etcd for PhotonOS.
