%global debug_package   %{nil}
%global realname        sd_notify
%global output_dir      _build/default/lib/sd_notify/ebin
%global elixir_version  1.16.3

Name:            erlang-%{realname}
Summary:         Erlang Bindings for sd_notify()
Version:         1.1
Release:         8%{?dist}
URL:             https://github.com/systemd/erlang-%{realname}
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages

Source0: https://github.com/systemd/erlang-%{realname}/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Tue Apr 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.1-8
- Bump release for upating erlang
* Thu Apr 10 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.1-7
- Bump release for upating erlang
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.1-6
- Release bump for SRP compliance
* Tue Jun 18 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1-5
- Bump version as a part of elixir upgrade
* Mon Dec 19 2022 Shivani Agarwal <shivania2@vmware.com> 1.1-4
- Bump version to build with new elixir
* Tue Nov 08 2022 Harinadh D <hdommaraju@vmware.com> 1.1-3
- use reabr built with erlang >= 24
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1-2
- Bump version as a part of erlang upgrade
* Thu Jul 09 2020 Keerthana K <keerthanak@vmware.com> 1.1-1
- Update to 1.1
* Mon Nov 04 2019 Keerthana K <keerthanak@vmware.com> 1.0-1
- Initial  package for PhotonOS.
