%global build_if %{photon_subrelease} >= 92

%global debug_package %{nil}

%global srcname uv

Summary:        The uv build backend
Name:           python3-uv-build
Version:        0.9.30
Release:        1%{?dist}
Url:            https://github.com/astral-sh/uv
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:  https://github.com/astral-sh/uv/archive/refs/tags/0.9.30.tar.gz#/uv-build-0.9.30.tar.gz

# Steps to generate this tarball:
# Extract uv-build tarball
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
BuildRequires:  python3-packaging
BuildRequires:  python3-maturin
BuildRequires:  rust

Requires:       python3

%description
An extremely fast Python package and project manager, written in Rust.

%prep
%autosetup -p1 -a1 -n %{srcname}-%{version}
mkdir -p $HOME/.cargo/
mv registry $HOME/.cargo/

%build
export CARGO_NET_OFFLINE=true
cd crates/uv-build
%py3_build_wheel

%install
export CARGO_NET_OFFLINE=true
cd crates/uv-build
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
cargo test --offline --manifest-path crates/uv-build/Cargo.toml
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{_bindir}/uv-build
%{python3_sitelib}/*

%changelog
* Tue Jul 14 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.9.30-1
- Initial build, required by python3-CacheControl
