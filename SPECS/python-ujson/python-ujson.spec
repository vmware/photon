%global debug_package %{nil}

Summary:        Ultra fast JSON encoder and decoder written in pure C
Name:           python3-ujson
Version:        5.4.0
Release:        3%{?dist}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/ujson

Source0:        https://files.pythonhosted.org/packages/fb/94/44fbbb059fe5d295f1f73e731a0b9c2e1b5073c2c6b58bb9c068715e9b72/ujson-%{version}.tar.gz
%define sha512  ujson=9622e872391d5467455b32e324d7b680487664ca486bfc56ba8c3969853e5db94725cd45e81b535dca80af4a3c718af171ce7adb6dcb9b98a37a8068824f89c6

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  double-conversion-devel
BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3

%description
UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python.

%prep
%autosetup -p1 -n ujson-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_check}
%check
%pytest -v
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE.txt
%doc README.md
%{python3_sitearch}/ujson-%{version}.dist-info/
%{python3_sitearch}/ujson*.so

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.4.0-3
- Release bump for SRP compliance
* Mon Jun 03 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.4.0-2
- Use system provided packages to do offline build
* Wed Oct 12 2022 Nitesh Kumar <kunitesh@vmware.com> 5.4.0-1
- Initial version, Needed by python3-pydantic
