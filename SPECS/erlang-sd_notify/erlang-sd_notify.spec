%global debug_package %{nil}
%global realname sd_notify
%global output_dir _build/default/lib/sd_notify/ebin
Name:            erlang-%{realname}
Summary:         Erlang Bindings for sd_notify()
Version:         1.1
Release:         1%{?dist}
License:         MIT
URL:             https://github.com/systemd/erlang-%{realname}
Source0:         https://github.com/systemd/erlang-%{realname}/archive/%{name}-%{version}.tar.gz
%define sha1     erlang-sd_notify=fb33582e8003484fb26d25e9040b7d3355d7ef6a
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages
BuildRequires:   erlang
BuildRequires:   which
BuildRequires:   systemd-devel

%description
Erlang module for native access to the systemd-notify facilities.

%prep
%setup -q -n %{name}-%{version}

%build
chmod +x rebar3
make all

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
*   Thu Jul 09 2020 Keerthana K <keerthanak@vmware.com> 1.1-1
-   Update to 1.1
*   Mon Nov 04 2019 Keerthana K <keerthanak@vmware.com> 1.0-1
-   Initial  package for PhotonOS.
