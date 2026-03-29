%global build_if %{photon_subrelease} >= 92

Name:           rpm-sequoia
Version:        1.10.0
Release:        1%{?dist}
Summary:        Implementation of the RPM PGP interface using Sequoia
URL:            https://crates.io/crates/rpm-sequoia
Vendor:         VMware, Inc.
Group:          Applications/System
Distribution:   Photon

Source0: https://github.com/rpm-software-management/rpm-sequoia/archive/refs/tags/%{name}-%{version}.tar.gz

# Steps to generate this tarball:
# Extract rpm-sequoia tarball
# Trigger build
# cd ~/.cargo
# tar czf <tar-name>.tar.gz registry
Source1: %{name}-registry-%{version}.tar.gz

Source2: license.txt
%include %{SOURCE2}

Source3: %{name}.config

BuildRequires: openssl-devel
BuildRequires: libgcc-devel

Requires: libgcc
Requires: openssl-libs

%define ExtraBuildRequires rust

%description
An implementation of the RPM PGP interface using Sequoia.

%package devel
Summary:        %{summary}
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for %{name}

%prep
%autosetup -p1 -a0 -a1
mkdir -p $HOME/.cargo/
mv registry $HOME/.cargo/

%build
export CARGO_NET_OFFLINE=true
# build script uses environment variables to populate the pkgconfig file
export PREFIX=%{_prefix}
export LIBDIR=%{_libdir}

cargo build -v \
  --release \
  --no-default-features \
  --features crypto-openssl

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -a target/release/librpm_sequoia.so %{buildroot}%{_libdir}/librpm_sequoia.so.1
# create unversioned symlink
ln -s librpm_sequoia.so.1 %{buildroot}%{_libdir}/librpm_sequoia.so
cp -a target/release/%{name}.pc %{buildroot}%{_libdir}/pkgconfig/

install -D -m 755 %{SOURCE3} \
    %{buildroot}%{_sysconfdir}/crypto-policies/back-ends/$(basename %{SOURCE3})

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/librpm_sequoia.so.1
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/crypto-policies/back-ends/%{name}.config

%files devel
%defattr(-,root,root)
%{_libdir}/librpm_sequoia.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Jan 20 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.10.0-1
- Initial version
