%global build_if %{photon_subrelease} >= 91

Name:       python3-passlib
Version:    1.9.3
Release:    1%{?dist}
Summary:    Comprehensive password hashing framework supporting over 20 schemes
URL:        https://github.com/notypecheck/passlib
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

BuildArch: noarch

Source0: https://github.com/notypecheck/passlib/archive/refs/tags/passlib-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: 0001-Removed-unsupported-versions-to-make-hatchling-happy.patch

BuildRequires: python3
BuildRequires: python3-build
BuildRequires: python3-packaging
BuildRequires: python3-installer
BuildRequires: python3-hatchling

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-bcrypt
%endif

Requires: python3

%description
Passlib is a password hashing library for Python, which provides
cross-platform implementations of over 20 password hashing algorithms,
as well as a framework for managing existing password hashes. It is
designed to be useful for a wide range of tasks, from verifying a hash
found in /etc/shadow, to providing full-strength password hashing for
multi-user application.

%prep
%autosetup -p1 -n passlib-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel

%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
%pytest
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Tue May 26 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.9.3-1
- Initial additon, needed by photon-os-installer as a replacement to crypt
