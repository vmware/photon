%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python Atomic file writes
Name:           python-atomicwrites
Version:        1.1.5
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/untitaker/python-atomicwrites
Source0:        https://pypi.python.org/packages/a1/e1/2d9bc76838e6e6667fde5814aa25d7feb93d6fa471bf6816daac2596e8b2/atomicwrites-%{version}.tar.gz
%define sha1    atomicwrites=89bfd295abb2c03e20f611a7c2205fc5c09e8509

BuildRequires:  python-setuptools
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
Requires:       python2
BuildArch:      noarch
%description
Python Atomic file writes

%package -n     python3-atomicwrites
Summary:        Python Atomic file writes
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3

%description -n python3-atomicwrites
Python3 version of atomicwrites.

%prep
%setup -q -n atomicwrites-%{version}
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
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python2_sitelib}/*

%files -n python3-atomicwrites
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
*   Fri Jul 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.1.5-1
-   Initial packaging for Photon
