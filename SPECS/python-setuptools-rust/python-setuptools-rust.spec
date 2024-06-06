Name:           python3-setuptools-rust
Version:        1.9.0
Release:        2%{?dist}
Summary:        Setuptools plugin for Rust support
License:        MIT
Group:          Development/Languages/Python
Url:            https://github.com/PyO3/setuptools-rust
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/source/s/setuptools-rust/setuptools-rust-%{version}.tar.gz
%define sha512 setuptools-rust=8658ab89833affca2f7882f7a386442b40f5a7decc651f37a4ee65be50a002dad81d929f0b970ba53f628597efc852d7708f78bf90fab91a14bcb42048f374a6

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-typing-extensions
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-six
BuildRequires:  python3-attrs
BuildRequires:  python3-pluggy
BuildRequires:  python3-more-itertools
BuildRequires:  python3-atmoicwrites
%endif

Requires:       python3
Requires:       python3-semantic-version
Requires:       python3-tomli

BuildArch:      noarch

%description
setuptools-rust is a plugin for setuptools to build Rust Python extensions implemented with PyO3 or rust-cpython.
Compile and distribute Python extensions written in Rust as easily as if they were written in C.

%prep
%autosetup -n setuptools-rust-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
%pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Jun 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.9.0-2
- Add tomli to requires
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.9.0-1
- Upgrade to v1.9.0
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.2-1
- Initial Build
