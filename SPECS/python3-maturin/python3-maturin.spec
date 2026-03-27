%global build_if %{photon_subrelease} >= 92

%global srcname maturin

Summary:        Rust/Python Interoperability
Name:           python3-maturin
Version:        1.14.1
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/cryptography
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/0c/18/8b2eebd3ea086a5ec73d7081f95ec64918ceda1900075902fc296ea3ad55/%{srcname}-%{version}.tar.gz

# Steps to generate this tarball:
# Extract maturin tarball
# Trigger build
# export OPENSSL_NO_VENDOR=1
# cargo fetch
# cargo build --release
# cd ~/.cargo
# tar czf <tar-name>.tar.gz registry

Source1: %{name}-registry-%{version}-1%{?dist}.tar.gz

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools-rust
BuildRequires:  python3-packaging
BuildRequires:  rust

Requires:       python3
Requires:       rust

%description
Build and publish crates with pyo3, cffi and uniffi bindings as well as rust binaries as python packages

%prep
%autosetup -p1 -a0 -a1 -n %{srcname}-%{version}
mkdir -p $HOME/.cargo/
mv registry $HOME/.cargo/

%build
export CARGO_NET_OFFLINE=true
%{py3_build_wheel}

%install
export CARGO_NET_OFFLINE=true
%{py3_install_wheel}
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
cargo test --offline
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{_bindir}/maturin
%{python3_sitelib}/*

%changelog
* Fri Jul 10 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.14.1-1
- Initial build required by python3-cryptopraghy
