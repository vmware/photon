Summary:        VerneMQ is a high-performance, distributed MQTT message broker
Name:           vernemq
Version:        1.11.0
Release:        1%{?dist}
License:        Apache License, Version 2.0
URL:            https://github.com/vernemq/vernemq
Source0:        https://github.com/%{name}/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1    vernemq=c046b71b9106cd51ccf0a1f0f82209b459059a30
Source1:        %{name}_vendor-%{version}.tar.gz
%define sha1    vernemq_vendor=5dc12229fbcc8bc26b18943df4935a2c521428d5
Source2:        vars.config
Source3:        vernemq.service
Patch0:         local_version.patch
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
# leveldb(core dependency) build on aarch64 is currently not supported
# hence vernemq is restricted to x86_64
BuildArch:      x86_64
BuildRequires:  erlang
BuildRequires:  which
BuildRequires:  make
BuildRequires:  snappy-devel
BuildRequires:  systemd
Requires:       snappy
Requires:       libstdc++
Requires:       systemd

%description
A high-performance, distributed MQTT message broker.

%prep
%setup -q
%setup -D -b 1
%patch0 -p1

%build
LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
mv ../%{name}_vendor-%{version}/_checkouts _checkouts
cp %{SOURCE2} ./vars.config
mkdir -p _build/default/lib
ln -s ../../../_checkouts/cuttlefish _build/default/lib/cuttlefish
ln -s ../../../_checkouts/riak_sysmon _build/default/lib/riak_sysmon
ln -s ../../../_checkouts/eleveldb _build/default/lib/eleveldb
make rel

%install
install -vdm 0755 %{buildroot}/%{_sharedstatedir}/%{name}/broker
install -vdm 0755 %{buildroot}/%{_sharedstatedir}/%{name}/msgstore
install -vdm 0755 %{buildroot}/%{_sysconfdir}/%{name}
install -vpm 0644 -t %{buildroot}/%{_sysconfdir}/%{name} _build/default/rel/%{name}/etc/%{name}.conf
install -vpm 0644 -t %{buildroot}/%{_sysconfdir}/%{name} _build/default/rel/%{name}/etc/vmq.acl
install -vdm 0755 %{buildroot}/%{_libdir}/%{name}
cp -r _build/default/rel/%{name}/bin %{buildroot}/%{_libdir}/%{name}
cp -r _build/default/rel/%{name}/lib %{buildroot}/%{_libdir}/%{name}
cp -r _build/default/rel/%{name}/erts-* %{buildroot}/%{_libdir}/%{name}
cp -r _build/default/rel/%{name}/releases %{buildroot}/%{_libdir}/%{name}
install -vdm 0755 %{buildroot}/%{_datadir}
cp -r _build/default/rel/%{name}/share %{buildroot}/%{_datadir}/%{name}
install -vdm 0755 %{buildroot}/%{_localstatedir}/log/%{name}/sasl

mkdir -p %{buildroot}/lib/systemd/system
cp %{SOURCE3} %{buildroot}/lib/systemd/system/%{name}.service

install -vdm755 %{buildroot}/lib/systemd/system-preset
echo "enable vernemq.service" > %{buildroot}/lib/systemd/system-preset/50-%{name}.preset

mkdir -p %{buildroot}%{_libdir}/tmpfiles.d
cat >> %{buildroot}%{_libdir}/tmpfiles.d/%{name}.conf << EOF
d /run/vernemq 0755 vernemq vernemq -
EOF

install -vdm 0755 %{buildroot}/%{_sbindir}
ln -sf /usr/lib64/%{name}/bin/%{name} %{buildroot}/%{_sbindir}
ln -sf /usr/lib64/%{name}/bin/vmq-admin %{buildroot}/%{_sbindir}
ln -sf /usr/lib64/%{name}/bin/vmq-passwd %{buildroot}/%{_sbindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE.txt
%attr(0755,vernemq,vernemq) %{_sharedstatedir}/%{name}
%attr(0755,vernemq,vernemq) %{_localstatedir}/log/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_sbindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
/lib/systemd/system/%{name}.service
/lib/systemd/system-preset/50-%{name}.preset
%{_libdir}/tmpfiles.d/%{name}.conf

%pre
getent group %{name} >/dev/null || /usr/sbin/groupadd -r %{name}
getent passwd %{name} >/dev/null || /usr/sbin/useradd --comment "VerneMQ" --shell /bin/bash -M -r --groups %{name} --home %{_sharedstatedir}/%{name} %{name}

%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
if [ $1 -eq 0 ] ; then
    /usr/sbin/userdel %{name}
    /usr/sbin/groupdel %{name}
fi

%changelog
*   Sun Feb 28 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.11.0-1
-   Initial build. First version
