Summary:    Python serial port access library
Name:       python3-pyserial
Version:    3.5
Release:    2%{?dist}
Vendor:     VMware, Inc.
Group:      Development/Libraries
Distribution: Photon
URL:        http://pypi.python.org/pypi/pyserial

Source0: https://github.com/pyserial/pyserial/archive/refs/tags/pyserial-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.5-2
- Release bump for SRP compliance
* Mon Aug 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.5-1
- Initial build, needed for cloud-init >= v22.3
