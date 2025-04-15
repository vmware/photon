%global debug_package   %{nil}
%global realname        sd_notify
%global output_dir      _build/default/lib/sd_notify/ebin
%global elixir_version  1.16.3

Name:            erlang-%{realname}
Summary:         Erlang Bindings for sd_notify()
Version:         1.1
Release:         4%{?dist}
License:         MIT
URL:             https://github.com/systemd/erlang-%{realname}
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages

Source0: https://github.com/systemd/erlang-%{realname}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=2c21e3e904b8b7d6c39b2ee81524537421994c80fe5a019bb37e8401da337ddf7e92c56deef757c505d9bdf9d16e8ab7de1e43fa93e4d0c129c36ee7fc4bfba9

BuildRequires:   erlang >= 24
BuildRequires:   elixir >= 1.13.4
BuildRequires:   which
BuildRequires:   systemd-devel

%description
Erlang module for native access to the systemd-notify facilities.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
cp %{_datadir}/elixir/%{elixir_version}/lib/mix/test/fixtures/rebar3 .
chmod +x rebar3
%make_build all

%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 -p %{output_dir}/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 -p %{output_dir}/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%files
%defattr(-,root,root)
%doc LICENSE
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam

%changelog
* Thu Apr 10 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.1-4
- Bump release for upating erlang
* Tue Jun 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1-3
- Bump version as a part of erlang, elixir upgrade
* Tue Nov 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1-2
- Use reabr built with erlang >= 24
* Thu Jul 09 2020 Keerthana K <keerthanak@vmware.com> 1.1-1
- Update to 1.1
* Mon Nov 04 2019 Keerthana K <keerthanak@vmware.com> 1.0-1
- Initial  package for PhotonOS.
