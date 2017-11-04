%define __debug_install_post %{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}" %{nil}
Name:       emqttd
Version:    2.1.2
Release:    1%{?dist}
Summary:    emqttd
Group:      System Environment/Daemons
License:    Apache License Version 2.0
URL:        http://www.emqtt.io
Source0:    %{name}-%{version}.tar.gz
BuildRoot:  %_topdir/BUILDROOT
Requires:   shadow gawk sed

%description
(Erlang MQTT Broker) is a distributed, massively scalable, highly extensible MQTT message broker written in Erlang/OTP.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
#make install DESTDIR=%{buildroot}
%define relpath             %{_builddir}/%{buildsubdir}/_rel/emqttd
%define emq_home            %{buildroot}/opt/emqttd
%define buildroot_etc       %{emq_home}/etc
%define buildroot_bin       %{emq_home}/bin
%define buildroot_log       %{emq_home}/log
%define buildroot_data      %{emq_home}/data

mkdir -p %{emq_home}
mkdir -p %{buildroot_etc}
mkdir -p %{buildroot_bin}
mkdir -p %{buildroot_log}
mkdir -p %{buildroot_data}
mkdir -p %{buildroot}%{_localstatedir}/run/emqttd

install -p -D -m 0755 %{relpath}/bin/emqttd %{buildroot_bin}
install -p -D -m 0755 %{relpath}/bin/emqttd_ctl %{buildroot_bin}

cp -R %{relpath}/lib        %{emq_home}
cp -R %{relpath}/erts-*     %{emq_home}
cp -R %{relpath}/releases   %{emq_home}

cp %{relpath}/bin/cuttlefish               %{buildroot_bin}
cp %{relpath}/bin/install_upgrade_escript  %{buildroot_bin}
cp %{relpath}/bin/nodetool                 %{buildroot_bin}
cp %{relpath}/bin/start_clean.boot         %{buildroot_bin}
cp %{relpath}/bin/emqenv                   %{buildroot_bin}
cp %{relpath}/bin/emqttd.cmd               %{buildroot_bin}
cp %{relpath}/bin/emqttd_ctl.cmd           %{buildroot_bin}
cp -R %{relpath}/etc/*                     %{buildroot_etc}
cp %{_topdir}/emq.conf                     %{buildroot_etc}
cp %{_topdir}/emq_dashboard.conf           %{buildroot_etc}/plugins/
cp -R %{relpath}/data/*                    %{buildroot_data}

command -v systemctl >/dev/null 2>&1 && { mkdir -p %{buildroot}%{_unitdir}/; install -m644  %{_topdir}/emqttd.service %{buildroot}%{_unitdir}/; }

%pre
# Pre-install script
if ! getent group emqtt >/dev/null 2>&1; then
    groupadd -r emqtt
fi

if getent passwd emqtt >/dev/null 2>&1; then
    usermod -d /opt/emqttd/data emqtt || true
else
    useradd -r -g emqtt \
           --home /opt/emqttd/data \
           --comment "emqtt user" \
           --shell /bin/bash \
           emqtt
fi

%post
if [ $1 == 1 ];then
    if command -v systemctl > /dev/null ; then
        systemctl enable emqttd.service
    fi
fi

%preun
# Pre-uninstall script

# Only on uninstall, not upgrades
if [ "$1" = 0 ] ; then
    if command -v systemctl > /dev/null ; then
        systemctl stop emqttd
        systemctl disable emqttd
        systemctl daemon-reload
    fi
fi

exit 0


%files
%defattr(-,emqtt,emqtt)
/opt/emqttd
/lib/systemd/system/emqttd.service
%doc

%clean
rm -rf %{buildroot}

%changelog
* Tue Oct 31 2017 Rajeev Bakshi <bakshir@vmware.com> 2.1.2.0
- Initial build for first version.
