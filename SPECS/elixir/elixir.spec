%global debug_package %{nil}

Name:            elixir
Summary:         A modern approach to programming for the Erlang VM
Version:         1.16.3
Release:         2%{?dist}
License:         ASL 2.0
URL:             http://elixir-lang.org
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages

Source0: https://github.com/elixir-lang/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=1511fb78bdcc50850cbf91007ed11c6a89e947d0a743c1e9ed30e1c93c1b47b5377fced17eeb66ac511d4f151d2e00ef2ecc6fb425d0d4afe2451be41a6ba6ee

BuildRequires:   git
BuildRequires:   sed
BuildRequires:   erlang
BuildRequires:   openldap

Requires:        erlang

Conflicts:       toybox < 0.8.2-3

%description
Elixir is a programming language built on top of the Erlang VM.
As Erlang, it is a functional language built to support distributed,
fault-tolerant, non-stop applications with hot code swapping.

%prep
%autosetup -p1

%build
export LANG="en_US.UTF-8"
%make_build compile

%install
mkdir -p %{buildroot}%{_datadir}/%{name}/%{version} \
         %{buildroot}%{_bindir}

cp -a bin lib %{buildroot}%{_datadir}/%{name}/%{version}

ln -sv %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}%{_bindir}/

%check
export LANG="en_US.UTF-8"
%make_build test

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}

%changelog
* Thu Apr 10 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.16.3-2
- Bump release for updating erlang
* Wed Jun 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.16.3-1
- Upgrade to v1.16.3
* Tue Nov 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.1-1
- Upgrade to v1.14.1
* Mon Dec 21 2020 Sujay G <gsujay@vmware.com> 1.10.4-3
- Fix %check
* Fri Aug 14 2020 Sujay G <gsujay@vmware.com> 1.10.4-2
- Added openldap in buildrequires to fix package build issues
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.10.4-1
- Automatic Version Bump
* Tue Jun 30 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.8.2-2
- Do not conflict with toybox >= 0.8.2-3
* Tue Oct 29 2019 Keerthana K <keerthanak@vmware.com> 1.8.2-1
- Update to 1.8.2
* Mon Aug 26 2019 Keerthana K <keerthanak@vmware.com> 1.5.0-1
- Initial package for PhotonOS.
