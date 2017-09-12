%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pexpect is a Pure Python Expect-like module
Name:           python-pexpect
Version:        4.2.1
Release:        1%{?dist}
License:        ISC
Url:            https://github.com/pexpect/pexpect
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/pexpect/pexpect/archive/pexpect-4.2.1.tar.gz
%define sha1    pexpect=9941c99b7f1501c0210dbb98f8b26940a4429565

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Pexpect is a pure Python module for spawning child applications; controlling them;
and responding to expected patterns in their output. Pexpect works like Don Libes Expect.
Pexpect allows your script to spawn a child application and control it as if a human 
were typing commands.

%package -n python3-pexpect
Summary:        Python3 package for pexpect
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-libs

%description -n python3-pexpect
Python 3 version of pexpect

%prep
%setup -q -n pexpect-%{version}
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

%files
%defattr(-, root, root, -)
%{python2_sitelib}/*

%files -n python3-pexpect
%{python3_sitelib}/*

%changelog
*   Mon Sep 11 2017 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-1
-   Initial packaging for Photon

