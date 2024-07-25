Name:           wireguard-tools
Version:        1.0.20210914
Release:        1%{?dist}
URL:            https://www.wireguard.com/
Summary:        Fast, modern, secure VPN tunnel
License:        GPLv2
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://git.zx2c4.com/wireguard-tools/snapshot/wireguard-tools-%{version}.tar.xz
%define sha512 %{name}=6727ea65551dbb064457449b93a943bd6534ca93bc7fa5704c2f6826266c98688ee9ea28731fda57a5245d5f63c05f3899fcca54e40c0b6251b7c4796e957445

BuildRequires: make
BuildRequires: systemd-devel
BuildRequires: gcc

Requires:      systemd

%description
WireGuard is a novel VPN that runs inside the Linux Kernel and uses
state-of-the-art cryptography (the "Noise" protocol). It aims to be
faster, simpler, leaner, and more useful than IPSec, while avoiding
the massive headache. It intends to be considerably more performant
than OpenVPN. WireGuard is designed as a general purpose VPN for
running on embedded interfaces and super computers alike, fit for
many different circumstances. It runs over UDP.

This package provides the wg binary for controlling WireGuard.

%prep
%autosetup -p1
pushd contrib/dns-hatchet
./apply.sh
popd

%build
%make_build RUNSTATEDIR=%{_rundir} -C src

%install
%make_install BINDIR=%{_bindir} RUNSTATEDIR=%{_rundir} \
WITH_BASHCOMPLETION=yes WITH_WGQUICK=yes WITH_SYSTEMDUNITS=yes -C src

%files
%doc README.md contrib
%license COPYING
%{_bindir}/wg
%{_bindir}/wg-quick
%{_sysconfdir}/wireguard/
%{_datadir}/bash-completion/completions/wg
%{_datadir}/bash-completion/completions/wg-quick
%{_unitdir}/wg-quick@.service
%{_unitdir}/wg-quick.target
%{_mandir}/man8/wg.8*
%{_mandir}/man8/wg-quick.8*

%changelog
* Fri Dec 02 2022 Susant Sahani <ssahani@vmware.com> 1.0.20210914-1
- Initial rpm release
