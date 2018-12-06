%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Run a subprocess in a pseudo terminal.
Name:           python-ptyprocess
Version:        0.6.0
Release:        2%{?dist}
License:        ISC
Url:            https://github.com/pexpect/ptyprocess
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/ptyprocess/ptyprocess-%{version}.tar.gz
%define sha1    ptyprocess=39622a2ff2cb456f17db542d60e5a0782e354128

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python-pytest
BuildRequires:  python-atomicwrites
BuildRequires:  python-attrs
%endif
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Launch a subprocess in a pseudo terminal (pty), and interact with both the
process and its pty.

%package -n python3-ptyprocess
Summary:        Python3 package for ptyprocess
BuildRequires:  python3-devel
%if %{with_check}
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-xml
%endif
Requires:       python3
Requires:       python3-libs

%description -n python3-ptyprocess
Python 3 version of ptyprocess

%prep
%setup -q -n ptyprocess-%{version}
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

%files -n python3-ptyprocess
%{python3_sitelib}/*

%changelog
*   Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> 0.6.0-2
-   Add %check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.6.0-1
-   Update to version 0.6.0
*   Tue Sep 19 2017 Kumar Kaushik <kaushikk@vmware.com> 0.5.2-1
-   Initial packaging for Photon

