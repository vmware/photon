%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Library to implement a well-behaved Unix daemon process.
Name:           python-daemon
Version:        2.1.2
Release:        2%{?dist}
License:        Apache-2
Url:            https://pypi.python.org/pypi/python-daemon/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/python-daemon/python-daemon-2.1.2.tar.gz
%define sha1    python-daemon=e333e9031424611b8974d2b2d2804dd26c4fae8e

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-docutils
Requires:       python2

BuildArch:      noarch

%description
This library implements the well-behaved daemon specification of PEP 3143, “Standard daemon process library”.

A well-behaved Unix daemon process is tricky to get right, but the required steps are much the same for every daemon program. A DaemonContext instance holds the behaviour and configured process environment for the program; use the instance as a context manager to enter a daemon state.

%package -n python3-daemon
Summary:        Python3-daemon
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
Requires:       python3

%description -n python3-daemon
Python 3 version.

%prep
%setup -q
rm -rf ../p3dir
cp -a . ../p3dir
pushd ../p3dir
sed -i 's/distclass=version.ChangelogAwareDistribution,/ /g' setup.py
popd

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
python2 setup.py test

pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-, root, root, -)
%{python2_sitelib}/*

%files -n python3-daemon
%{python3_sitelib}/*

%changelog
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.2-2
-   Corrected an error in command
*   Fri Mar 24 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-1
-   Initial packaging for Photon

