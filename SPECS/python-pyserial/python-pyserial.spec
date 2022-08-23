Summary:    Python serial port access library
Name:       python3-pyserial
Version:    3.5
Release:    1%{?dist}
License:    BSD
Vendor:     VMware, Inc.
Group:      Development/Libraries
Distribution: Photon
URL:        http://pypi.python.org/pypi/pyserial

Source0: https://github.com/pyserial/pyserial/archive/refs/tags/pyserial-%{version}.tar.gz
%define sha512 pyserial=c2a700f5e08905bdab070c95cec41d6d423c20d2a9648c8c2f048db86de72f39fe2b8df560172d5b9d480be44c35ff0799df8f1d684d3f41f8fc61174105256e

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

BuildArch: noarch

%description
This module encapsulates the access for the serial port. It provides backends
for standard Python running on Windows, Linux, BSD (possibly any POSIX
compliant system) and Jython. The module named "serial" automatically selects
the appropriate backend.

%prep
%autosetup -p1 -n pyserial-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%{python3} test/run_all_tests.py
%endif

%files
%doc LICENSE.txt CHANGES.rst README.rst examples
%{python3_sitelib}/serial
%{python3_sitelib}/pyserial-%{version}-py%{python3_version}.egg-info
%{_bindir}/pyserial-miniterm
%{_bindir}/pyserial-ports

%changelog
* Mon Aug 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.5-1
- Initial build, needed for cloud-init >= v22.3
