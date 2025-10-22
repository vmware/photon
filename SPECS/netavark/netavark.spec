%global build_if %{photon_subrelease} >= 92

%global majorver 2.0

Summary:        Container network stack
Name:           netavark
Version:        2.0.0
Release:        1%{?dist}
URL:            https://github.com/containers/netavark
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containers/netavark/archive/refs/tags/%{name}-%{version}.tar.gz

# Steps to generate this tarball:
# Extract aardvark-dns tarball
# export OPENSSL_NO_VENDOR=1
# Trigger build
# cd ~/.cargo
# tar czf <tar-name>.tar.gz registry

Source1: %{name}-registry-%{version}-1%{?dist}.tar.gz

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  go
BuildRequires:  rust
BuildRequires:  go-md2man
BuildRequires:  protobuf-devel
BuildRequires:  systemd

Requires:       aardvark-dns >= %{majorver}
Requires:       systemd
Requires:       nftables

%description
Netavark is a rust based network stack for containers.
It is being designed to work with Podman but is also applicable for other OCI container management applications.

%package docs
Summary:    netavark docs
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description docs
Contains man page for netavark

%prep
%autosetup -p1 -a0 -a1
mkdir -p $HOME/.cargo/
mv registry $HOME/.cargo/

%build
%{make_build}

%install
%{make_install} %{?_smp_mflags} PREFIX=%{_prefix} LIBEXECDIR=%{_libexecdir}

%preun
%systemd_preun %{name}-dhcp-proxy.service
%systemd_preun %{name}-firewalld-reload.service

%postun
%systemd_postun %{name}-dhcp-proxy.service
%systemd_postun %{name}-firewalld-reload.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/%{name}*
%{_unitdir}/%{name}-dhcp-proxy.service
%{_unitdir}/%{name}-dhcp-proxy.socket
%{_unitdir}/%{name}-firewalld-reload.service
%{_unitdir}/%{name}-nftables-reload.service

%files docs
%defattr(-,root,root)
%{_mandir}/man1/%{name}.1*
%{_mandir}/man7/%{name}-firewalld.7*

%changelog
* Mon Nov 03 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.0-1
- Initial Build
