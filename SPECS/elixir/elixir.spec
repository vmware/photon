%global debug_package %{nil}

Name:            elixir
Summary:         A modern approach to programming for the Erlang VM
Version:         1.14.0
Release:         1%{?dist}
License:         ASL 2.0
URL:             http://elixir-lang.org
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages

Source0: https://github.com/elixir-lang/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=74fa0364260710e7139474437846035aaa764fcc138bedd7c15dd729c72242f56a9d99232524d99701b811e2ddebed84c27586351f4b88cb0091f89fada43ad6

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
make compile %{?_smp_mflags}

%check
export LANG="en_US.UTF-8"
make test %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_datadir}/%{name}/%{version}
cp -ra bin lib %{buildroot}%{_datadir}/%{name}/%{version}

mkdir -p %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}

%changelog
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
