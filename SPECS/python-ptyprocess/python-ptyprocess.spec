%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Run a subprocess in a pseudo terminal.
Name:           python-ptyprocess
Version:        0.6.0
Release:        1%{?dist}
License:        ISC
Url:            https://github.com/pexpect/ptyprocess
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/ptyprocess/ptyprocess-%{version}.tar.gz
%define sha1    ptyprocess=39622a2ff2cb456f17db542d60e5a0782e354128

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Launch a subprocess in a pseudo terminal (pty), and interact with both the
process and its pty.

%package -n python3-ptyprocess
Summary:        Python3 package for ptyprocess
BuildRequires:  python3-devel
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

%files
%defattr(-, root, root, -)
%{python2_sitelib}/*

%files -n python3-ptyprocess
%{python3_sitelib}/*

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.6.0-1
-   Update to version 0.6.0
*   Tue Sep 19 2017 Kumar Kaushik <kaushikk@vmware.com> 0.5.2-1
-   Initial packaging for Photon

