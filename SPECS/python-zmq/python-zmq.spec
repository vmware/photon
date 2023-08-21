Summary:        Software library for fast, message-based applications
Name:           python3-zmq
Version:        23.2.0
Release:        1%{?dist}
License:        LGPLv3+ and BSD3
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pyzmq
Source0:        https://files.pythonhosted.org/packages/36/80/50962c33a3ad813b086fe2bf023bb8b79cb232f8e15b1b54a4d5b05b62ff/pyzmq-23.2.0.tar.gz
%define sha512  pyzmq=f2709a1f18301696266a8c4fe0fad57ec116be71b1feb245576c53159476d574def9e61ec4c511293068c52e27d5f2d121308f0c0af53c92bac48d29fb31b784

BuildRequires:  zeromq-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  cython3
BuildRequires:  python3-packaging
BuildRequires:  python3-setuptools
Requires:       python3
Provides:       python%{python3_version}dist(pyzmq)
Provides:       python-zmq = %{version}-%{release}
Obsoletes:      python-zmq < 23.2.0-1

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
* Mon Aug 21 2023 Derek Ardolf <dereka@vmware.com> 23.2.0-1
- Updated to 23.2.0
* Fri Dec 16 2022 Prashant S Chauhan <psinghchauha@vmware.com> 19.0.2-1
- Updated to 19.0.2
* Thu Sep 20 2018 Tapas Kundu <tkundu@vmware.com> 17.1.2-1
- Updated to release 17.1.2
* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.0.2-2
- Add python3-libs to BuildRequires
* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.0.2-1
- Initial packaging for Photon
