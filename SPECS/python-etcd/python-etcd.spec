%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-etcd
Version:        0.4.5
Release:        2%{?dist}
Summary:        Python API for etcd
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/python-etcd
Source0:        %{name}-%{version}.tar.gz
Patch0:         auth-api-compatibility.patch
%define sha1    python-etcd=9e79ae82429cf2ffbe2b5647e14bc29571afd766
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-pip
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  python-dnspython
BuildRequires:  python-urllib3
BuildRequires:  python-pyOpenSSL
BuildRequires:  etcd
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  libffi-devel
%endif
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
%if %{with_check}
BuildRequires:  python3-dnspython
BuildRequires:  python3-urllib3
BuildRequires:  python3-pyOpenSSL
%endif

%description -n python3-etcd
Python3 API for etcd

%prep
%setup -n %{name}-%{version}
%patch0 -p1
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
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 nose
python2 setup.py test
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-etcd
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Dec 04 2018 Ashwin H<ashwinh@vmware.com> 0.4.5-2
-   Add %check
*   Sat Aug 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.5-1
-   Initial version of python etcd for PhotonOS.
