%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Software library for fast, message-based applications
Name:           python-zmq
Version:        17.1.2
Release:        1%{?dist}
License:        LGPLv3+ and BSD3
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/pyzmq
Source0:        https://pypi.python.org/packages/af/37/8e0bf3800823bc247c36715a52e924e8f8fd5d1432f04b44b8cd7a5d7e55/pyzmq-%{version}.tar.gz
%define sha1	pyzmq=d0e5d7dd59f2398345fc4bacf5ee91241d857f0d

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  zeromq-devel
BuildRequires:  cython
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  cython3

%description
python bindings for zeromq

%package -n     python3-zmq
Summary:        Software library for fast, message-based applications
Requires:       python3

%description -n python3-zmq
Python 3 version bindings for zeromq

%prep
%setup -q -n pyzmq-%{version}
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
%doc README.md COPYING.* examples/
%{python2_sitelib}/pyzmq-*.egg-info
%{python2_sitelib}/zmq

%files -n python3-zmq
%defattr(-,root,root)
%doc README.md COPYING.* examples/
%{python3_sitelib}/pyzmq-*.egg-info
%{python3_sitelib}/zmq

%changelog
*   Thu Sep 20 2018 Tapas Kundu <tkundu@vmware.com> 17.1.2-1
-   Updated to release 17.1.2
*   Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.0.2-2
-   Add python3-libs to BuildRequires
*   Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.0.2-1
-   Initial packaging for Photon
