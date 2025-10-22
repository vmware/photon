%global build_if %{photon_subrelease} >= 92

Summary:        Authoritative DNS server for A/AAAA container records
Name:           aardvark-dns
Version:        2.0.0
Release:        1%{?dist}
URL:            https://github.com/containers/aardvark-dns
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containers/netavark/archive/refs/tags/%{name}-%{version}.tar.gz

# Steps to generate this tarball:
# Extract aardvark-dns tarball
# Trigger build
# cd ~/.cargo
# tar czf <tar-name>.tar.gz registry

Source1: %{name}-registry-%{version}-1%{?dist}.tar.gz

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  rust

%description
Aardvark-dns is an authoritative dns server for A/AAAA container records. It can forward other requests to configured resolvers.

%prep
%autosetup -p1 -a0 -a1 -n %{name}-%{version}
mkdir -p $HOME/.cargo/
mv registry $HOME/.cargo/

%build
export CARGO_NET_OFFLINE=true
%{make_build}

%install
export CARGO_NET_OFFLINE=true
%{make_install} %{?_smp_mflags} LIBEXECDIR=%{_libexecdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/%{name}

%changelog
* Mon Nov 03 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.0-1
- Initial Build
