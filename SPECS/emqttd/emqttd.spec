Name:          emqttd
Version:       2.3.11
Release:       2%{?dist}
Summary:       emqttd
License:       Apache License Version 2.0
Group:	       System Environment/Daemons
Vendor:        VMware, Inc.
Distribution:  Photon
URL:	       http://www.emqtt.io
Source0:       emqx-rel-%{version}.tar.gz
%define sha1   emqx-rel=3992706d8c0c48565d582cbc536fa34a68b39fde
Source1:       emqttd.service
Patch0:        vars.config.patch
BuildRequires: erlang
BuildRequires: git
BuildRequires: openssl-devel
Requires:      shadow gawk sed

%description
(Erlang MQTT Broker) is a distributed, massively scalable, highly extensible MQTT message broker written in Erlang/OTP.

%prep
%setup -qn emqx-rel-%{version}
%patch0 -p0

%build
make

%install
#make install DESTDIR=%{buildroot}
%define relpath       %{_builddir}/%{buildsubdir}/_rel/emqttd
%define buildroot_lib %{buildroot}%{_libdir}/emqttd
%define buildroot_etc %{buildroot}%{_sysconfdir}/emqttd
%define buildroot_bin %{buildroot_lib}/bin

mkdir -p %{buildroot_etc}
mkdir -p %{buildroot_lib}
mkdir -p %{buildroot}%{_localstatedir}/lib/emqttd
mkdir -p %{buildroot}%{_localstatedir}/log/emqttd
mkdir %{buildroot_bin}
mkdir -p %{buildroot}/usr/sbin/

install -p -D -m 0755 %{relpath}/bin/emqttd %{buildroot}/usr/sbin
install -p -D -m 0755 %{relpath}/bin/emqttd_ctl %{buildroot}/usr/sbin

cp -R %{relpath}/lib           %{buildroot_lib}
cp -R %{relpath}/erts-*        %{buildroot_lib}
cp -R %{relpath}/releases      %{buildroot_lib}

cp %{relpath}/bin/cuttlefish               %{buildroot_bin}
cp %{relpath}/bin/install_upgrade_escript  %{buildroot_bin}
cp %{relpath}/bin/nodetool                 %{buildroot_bin}
cp %{relpath}/bin/start_clean.boot         %{buildroot_bin}

cp -R %{relpath}/etc/* %{buildroot_etc}

mkdir -p %{buildroot}%{_localstatedir}/lib/emqttd

cp -R %{relpath}/data/* %{buildroot}%{_localstatedir}/lib/emqttd

install -vdm755 %{buildroot}/usr/lib/systemd/system
install -D -m 444 %{SOURCE1} %{buildroot}/usr/lib/systemd/system

%pre
# Pre-install script
if ! getent group emqtt >/dev/null 2>&1; then
	groupadd -r emqtt
fi

if getent passwd emqtt >/dev/null 2>&1; then
	usermod -d %{_localstatedir}/lib/emqttd emqtt || true
else
    useradd -r -g emqtt \
           --home %{_localstatedir}/lib/emqttd \
           --comment "emqtt user" \
           --shell /bin/bash \
           emqtt
fi

%post
if [ $1 == 1 ];then
    chown -R emqtt:emqtt /var/log/emqttd/
    chown -R emqtt:emqtt /var/lib/emqttd/
    systemctl >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        systemctl enable emqttd.service
    fi
fi

%preun
# Pre-uninstall script

# Only on uninstall, not upgrades
if [ "$1" = 0 ] ; then
    systemctl >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        systemctl disable emqttd.service
    fi
fi
exit 0

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/
%{_sbindir}
%{_libdir}
%{_localstatedir}/lib/%{name}
%{_localstatedir}/log/%{name}
%exclude %{_libdir}/debug
%doc

%clean
rm -rf %{buildroot}

%changelog
*   Sun Mar 17 2019 Tapas Kundu <tkundu@vmware.com> 2.3.11-2
-   Added openssl-devel as build requires
*   Wed Sep 19 2018 Vinothkumar D <vinothkumard@vmware.com> 2.3.11-1
-   Upgraded to version 2.3.11
*   Thu Dec 07 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-1
-   Initial - modified from https://github.com/emqtt/emq-package
