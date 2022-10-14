%global debug_package %{nil}
%global realname sd_notify
%global output_dir _build/default/lib/sd_notify/ebin
%global elixir_version 1.13.4
Name:            erlang-%{realname}
Summary:         Erlang Bindings for sd_notify()
Version:         1.1
Release:         4%{?dist}
License:         MIT
URL:             https://github.com/systemd/erlang-%{realname}
Source0:         https://github.com/systemd/erlang-%{realname}/archive/%{name}-%{version}.tar.gz
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages
%define sha512   erlang-sd_notify=2c21e3e904b8b7d6c39b2ee81524537421994c80fe5a019bb37e8401da337ddf7e92c56deef757c505d9bdf9d16e8ab7de1e43fa93e4d0c129c36ee7fc4bfba9
BuildRequires:   erlang >= 24
BuildRequires:   elixir >= 1.13.4
BuildRequires:   which
BuildRequires:   systemd-devel

%description
Erlang module for native access to the systemd-notify facilities.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
cp %{_datadir}/elixir/%{elixir_version}/lib/mix/test/fixtures/rebar .
cp %{_datadir}/elixir/%{elixir_version}/lib/mix/test/fixtures/rebar3 .
chmod +x rebar3
%make_build all

%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
pushd _build/default/lib/sd_notify/
install -m 644 -p ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 -p ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
popd

%files
%defattr(-,root,root)
%doc LICENSE
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam

%changelog
* Fri Oct 14 2022 Ankit Jain <ankitja@vmware.com> 1.1-4
- Release Bump up to build with erlang-25.1-2
* Tue Oct 04 2022 Harinadh D <hdommaraju@vmware.com> 1.1-3
- version bump to use new elixir version
* Mon Sep 05 2022 Harinadh D <hdommaraju@vmware.com> 1.1-2
- use reabr built with erlang >= 24
* Thu Nov 12 2020 Harinadh D <hdommaraju@vmware.com> 1.1-1
- Update to 1.1
* Mon Nov 04 2019 Keerthana K <keerthanak@vmware.com> 1.0-1
- Initial  package for PhotonOS.
