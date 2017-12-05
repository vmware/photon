%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Software library for fast, message-based applications
Name:           python-zmq
Version:        16.0.2
Release:        2%{?dist}
License:        LGPLv3+ and BSD3
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://zeromq.org/bindings:python
Source0:        https://pypi.python.org/packages/af/37/8e0bf3800823bc247c36715a52e924e8f8fd5d1432f04b44b8cd7a5d7e55/pyzmq-%{version}.tar.gz
%define sha1	pyzmq=ad91c8d50f4c85e2e321511914d2420ad3603c49

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  zeromq-devel
BuildRequires:  cython

%description
python bindings for zeromq

%package -n     python3-zmq
Summary:        Software library for fast, message-based applications
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  cython3
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
*   Mon Dec 04 2017 Kumar Kaushik <kaushikk@vmware.com> 16.0.2-2
-   Release bump to use python 3.5.4.
*   Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.0.2-1
-   Initial packaging for Photon
