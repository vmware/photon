%global build_if %{photon_subrelease} >= 92

%global get_cargo_registry  0

%if 0%{?get_cargo_registry} || 0%{?with_check}
%define network_required 1
%endif

Summary:    Command-line frontends for Sequoia
Name:       sequoia-sq
Version:    1.5.0
Release:    1%{?dist}
URL:        https://crates.io/crates/sequoia-sq
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz

%if 0%{?get_cargo_registry} == 0
Source1: %{name}-%{version}-cargo-registry.tar.gz
%endif

Source2: license.txt
%include %{SOURCE2}

Source3: sequoia.config

BuildRequires: rust
BuildRequires: capnproto-devel
BuildRequires: clang-devel
BuildRequires: sqlite-devel

%if 0%{?with_check}
BuildRequires: nettle-devel
BuildRequires: shadow
BuildRequires: sudo
%endif

%description
Command-line frontends for Sequoia.

%prep
%autosetup -p1 -n %{name}-%{name}-v%{version}

%if %{get_cargo_registry}
cargo fetch
mv $HOME/.cargo/registry %{name}-%{version}-cargo-registry
resTarball="%{name}-%{version}-cargo-registry.tar.gz"
tar czf ${resTarball} %{name}-%{version}-cargo-registry
echo "${resTarball} is at $(realpath ${resTarball})"
exit 1
%endif

mkdir -p $HOME/.cargo
tar xf %{SOURCE1} --no-same-owner -C $HOME/.cargo
mv $HOME/.cargo/%{name}-%{version}-cargo-registry $HOME/.cargo/registry

%build
export CARGO_TARGET_DIR=target
export ASSET_OUT_DIR=target
export CARGO_NET_OFFLINE=true

cargo build -v \
  --release \
  --frozen \
  --no-default-features \
  --features crypto-openssl

%install
install -vDm 755 target/release/sq -t %{buildroot}%{_bindir}

install -Dpm 0644 tool/target/shell-completions/sq.bash \
    %{buildroot}%{_datadir}/bash-completion/completions/sq.bash

install -Dpm 0644 %{SOURCE3} \
    %{buildroot}%{_sysconfdir}/crypto-policies/back-ends/sequoia.config

%if 0%{?with_check}
%check
check_home="$PWD/.test-home"

id -u sq-test &>/dev/null || \
  useradd -r -U -M -d "$check_home" -s /bin/sh sq-test

mkdir -p "$check_home/.cargo"
cp -a "${CARGO_HOME:-$HOME/.cargo}/." "$check_home/.cargo/"
chown -R sq-test:sq-test "$PWD"

sudo -u sq-test env \
  HOME="$check_home" \
  CARGO_HOME="$check_home/.cargo" \
  PATH=/usr/bin:/bin:/usr/sbin:/sbin \
  cargo test \
    --no-default-features \
    --features crypto-openssl
%endif

%files
%defattr(-,root,root)
%{_bindir}/sq
%{_datadir}/bash-completion/completions/sq.bash
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/crypto-policies/back-ends/sequoia.config

%changelog
* Mon Oct 26 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.5.0-1
- Initial version.
