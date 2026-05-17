%global build_if %{photon_subrelease} >= 91

Summary:        Setuptools extension for CalVer package versions
Name:           python3-calver
Version:        2025.10.20
Release:        2%{?dist}
URL:            https://github.com/di/calver
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://files.pythonhosted.org/packages/source/c/calver/calver-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-packaging
BuildRequires:  python3-build
BuildRequires:  python3-installer

Requires:       python3

%description
Setuptools plugin for CalVer (calendar-based) Python package versions. Required to
build trove-classifiers from source.

%prep
%autosetup -n calver-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel

%{py_byte_compile_and_ghost}

%check
%{__python3} -c "import calver"

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2025.10.20-2
- Extended to build for subrelease 91 and above
* Tue Apr 07 2026 Mukul Sikka <mukul.sikka@broadcom.com> 2025.10.20-1
- Initial build
