%global debug_package %{nil}

Name:            elixir
Summary:         A modern approach to programming for the Erlang VM
Version:         1.16.3
Release:         4%{?dist}
URL:             http://elixir-lang.org
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages

Source0: https://github.com/elixir-lang/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:   git
BuildRequires:   sed
BuildRequires:   erlang

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

# don't create relative symlinks, this must be absolute symlink
# or else some builds fail with weird errors (rabbimq for example)
ln -sv %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}%{_bindir}

%check
export LANG="en_US.UTF-8"
%make_build test

%files
%defattr(-,root,root)
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}

%changelog
* Tue Apr 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.16.3-4
- Bump release for updating erlang
* Thu Apr 10 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.16.3-3
- Bump release for updating erlang
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.16.3-2
- Release bump for SRP compliance
* Tue Jun 18 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.16.3-1
- Upgrade to v1.16.3
* Wed Feb 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.14.2-2
- Bump version as a part of openldap upgrade
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.14.2-1
- Automatic Version Bump
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 1.14.1-1
- Automatic Version Bump
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.0-1
- Upgrade to v1.14.0
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.13.4-1
- Automatic Version Bump
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.11.4-1
- Automatic Version Bump
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
- Initial  package for PhotonOS.
