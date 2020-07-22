%global debug_package %{nil}
Name:            elixir
Summary:         A modern approach to programming for the Erlang VM
Version:         1.10.4
Release:         1%{?dist}
License:         ASL 2.0
URL:             http://elixir-lang.org/
Source0:         https://github.com/elixir-lang/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages
%define sha1 elixir=d8634700f61c72c0e97f1a212919803a86016d2a
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
%setup -q -n %{name}-%{version}

%build
export LANG="en_US.UTF-8"
make compile

%check
make test

%install
mkdir -p %{buildroot}/%{_datadir}/%{name}/%{version}
cp -ra bin lib %{buildroot}/%{_datadir}/%{name}/%{version}

mkdir -p %{buildroot}/%{_bindir}
ln -s %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}/%{_bindir}/

%files
%license LICENSE
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}

%changelog
*   Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.10.4-1
-   Automatic Version Bump
*   Tue Jun 30 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.8.2-2
-   Do not conflict with toybox >= 0.8.2-3
*   Tue Oct 29 2019 Keerthana K <keerthanak@vmware.com> 1.8.2-1
-   Update to 1.8.2
*   Mon Aug 26 2019 Keerthana K <keerthanak@vmware.com> 1.5.0-1
-   Initial  package for PhotonOS.
