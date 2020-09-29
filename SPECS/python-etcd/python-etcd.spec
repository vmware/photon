%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-etcd
Version:        0.4.5
Release:        4%{?dist}
Summary:        Python API for etcd
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/python-etcd
Source0:        python-etcd-%{version}.tar.gz
Patch0:         auth-api-compatibility.patch
%define sha1    python-etcd=9e79ae82429cf2ffbe2b5647e14bc29571afd766
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-dnspython
BuildRequires:  python3-urllib3
BuildRequires:  python3-pyOpenSSL
BuildRequires:  etcd
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  libffi-devel
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch

%description
Python API for etcd


%prep
%setup -n python-etcd-%{version}
%patch0 -p1

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.4.5-4
-   openssl 1.1.1
*   Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 0.4.5-3
-   Mass removal python2
*   Tue Dec 04 2018 Ashwin H<ashwinh@vmware.com> 0.4.5-2
-   Add %check
*   Sat Aug 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.5-1
-   Initial version of python etcd for PhotonOS.
