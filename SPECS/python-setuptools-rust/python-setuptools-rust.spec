Name:           python3-setuptools-rust
Version:        1.5.2
Release:        2%{?dist}
Summary:        Setuptools plugin for Rust support
Group:          Development/Languages/Python
Url:            https://github.com/PyO3/setuptools-rust
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/s/setuptools-rust/setuptools-rust-%{version}.tar.gz
%define sha512  setuptools-rust=79b1de5581b9558cdf227320c421aa2445b2e6b8583ed9c118ee8d7acdfde9d947e7d11fa6a9697c475d4ca387c86ca6846429099ec30d2eb6e40f8849fcecc0

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-typing-extensions
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-six
BuildRequires:  python3-attrs
BuildRequires:  python3-pluggy
BuildRequires:  python3-more-itertools
BuildRequires:  python3-atmoicwrites
%endif
Requires:       python3

BuildArch:      noarch

%description
setuptools-rust is a plugin for setuptools to build Rust Python extensions implemented with PyO3 or rust-cpython.
Compile and distribute Python extensions written in Rust as easily as if they were written in C.

%prep
%autosetup -n setuptools-rust-%{version}

%build
%py3_build

%install
%py3_install

%check
%pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.5.2-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.2-1
- Initial Build
