Summary:        Software library for fast, message-based applications
Name:           python3-zmq
Version:        19.0.2
Release:        1%{?dist}
License:        LGPLv3+ and BSD3
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pyzmq
Source0:        https://pypi.python.org/packages/af/37/8e0bf3800823bc247c36715a52e924e8f8fd5d1432f04b44b8cd7a5d7e55/pyzmq-%{version}.tar.gz
%define sha512  pyzmq=aca37b54e07fe6c3c16be56aa5bd856bbf0f4d7bebd11bd9fdecc6e74b7f996572f1dc52e32ae94562c5a63391975a1caeb04d3c0af9f82f780dbee37aae1a9f

BuildRequires:  zeromq-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  cython3
Requires:       python3
Provides:       python%{python3_version}dist(pyzmq)
Provides:       python-zmq = %{version}-%{release}
Obsoletes:      python-zmq < 19.0.2-1

%description
python bindings for zeromq

%prep
%autosetup -n pyzmq-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%doc README.md COPYING.* examples/
%{python3_sitelib}/pyzmq-*.egg-info
%{python3_sitelib}/zmq

%changelog
* Fri Dec 16 2022 Prashant S Chauhan <psinghchauha@vmware.com> 19.0.2-1
- Updated to 19.0.2
* Thu Sep 20 2018 Tapas Kundu <tkundu@vmware.com> 17.1.2-1
- Updated to release 17.1.2
* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.0.2-2
- Add python3-libs to BuildRequires
* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.0.2-1
- Initial packaging for Photon
