%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pexpect is a Pure Python Expect-like module
Name:           python-pexpect
Version:        4.6.0
Release:        2%{?dist}
License:        ISC
Url:            https://github.com/pexpect/pexpect
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/pexpect/pexpect/archive/pexpect-%{version}.tar.gz
Patch0:         fix_test_before_across_chunks.patch
%define sha1    pexpect=3d79bb7de5436cd0a8417a6249c765595a33abcf

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python-atomicwrites
BuildRequires:  python-pytest
BuildRequires:  python-attrs
BuildRequires:  python-ptyprocess
BuildRequires:  man-db
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-ptyprocess

BuildArch:      noarch

%description
Pexpect is a pure Python module for spawning child applications; controlling them;
and responding to expected patterns in their output. Pexpect works like Don Libes Expect.
Pexpect allows your script to spawn a child application and control it as if a human
were typing commands.

%package -n python3-pexpect
Summary:        Python3 package for pexpect
BuildRequires:  python3-devel
%if %{with_check}
BuildRequires:  python3-setuptools
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-pytest
BuildRequires:  python3-attrs
BuildRequires:  python3-ptyprocess
BuildRequires:  python3-xml
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-ptyprocess

%description -n python3-pexpect
Python 3 version of pexpect

%prep
%setup -q -n pexpect-%{version}
%patch0 -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build

pushd ../p3dir
python3 setup.py build
popd


%install
rm -rf %{buildroot}
python2 setup.py install --root=%{buildroot}

pushd ../p3dir
python3 setup.py install --root=%{buildroot}
popd

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 pathlib2 funcsigs pluggy more_itertools
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python2_sitelib} \
py.test2

easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pathlib2 funcsigs pluggy more_itertools
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python3_sitelib} \
py.test3

%files
%defattr(-, root, root, -)
%{python2_sitelib}/*

%files -n python3-pexpect
%{python3_sitelib}/*

%changelog
*   Wed Dec 05 2018 Ashwin H <ashwinh@vmware.com> 4.6.0-2
-   Add %check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.6.0-1
-   Update to version 4.6.0
*   Tue Sep 19 2017 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-2
-   Adding requires on ptyprocess
*   Mon Sep 11 2017 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-1
-   Initial packaging for Photon

