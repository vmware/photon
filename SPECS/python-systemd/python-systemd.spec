%global srcname  python-systemd

Summary:       Python module wrapping libsystemd functionality
Name:          python3-systemd
Version:       235
Release:       2%{?dist}
URL:           https://github.com/systemd/python-systemd
Group:         Development/Languages/Python
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/systemd/%{srcname}/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: systemd-devel
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires: systemd-libs

%description
Python module for native access to the libsystemd facilities. Functionality
includes sending of structured messages to the journal and reading journal
files, querying machine and boot identifiers and a lists of message identifiers
provided by systemd. Other functionality provided the library is also wrapped.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitearch}/systemd/
%{python3_sitearch}/systemd_python*.egg-info

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 235-2
- Release bump for SRP compliance
* Tue Feb 14 2023 Nitesh Kumar <kunitesh@vmware.com> 235-1
- Initial build
