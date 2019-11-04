%global realname sd_notify
Name:            erlang-%{realname}
Summary:         Erlang Bindings for sd_notify()
Version:         1.0
Release:         1%{?dist}
License:         MIT
URL:             https://github.com/systemd/erlang-%{realname}
Source0:         https://github.com/systemd/erlang-%{realname}/archive/%{name}-%{version}.tar.gz
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Development/Languages
%define sha1     erlang-sd_notify=fa71e23a839ae32f231ce3330ac7561fc22d4ab5
BuildRequires:   erlang
BuildRequires:   which
BuildRequires:   systemd-devel

%description
Erlang module for native access to the systemd-notify facilities.

%prep
%setup -q -n %{name}-%{version}

%build
make all

%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,priv}
install -m 644 -p ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 -p ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 755 -p priv/%{realname}_drv.so %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv

%files
%defattr(-,root,root)
%doc LICENSE
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/%{realname}_drv.so

%changelog
*   Mon Nov 04 2019 Keerthana K <keerthanak@vmware.com> 1.0-1
-   Initial  package for PhotonOS.
