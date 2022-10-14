Summary:          VerneMQ is a high-performance, distributed MQTT message broker
Name:             vernemq
Version:          1.12.5
Release:          3%{?dist}
License:          Apache License, Version 2.0
URL:              https://github.com/vernemq/vernemq
Source0:          https://github.com/%{name}/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512    vernemq=3e30e20745f7b53d015a2a0f5371d17ce0e002c041b85f80cdd1db4f40be648bb103bc1d484f494d1b79ecd0c99c2c915a8f909887f717a63b6c0d259ade7aab
Source1:          %{name}_vendor-%{version}.tar.gz
%define sha512    vernemq_vendor=20b95694449f44fb99f7b136176031ce7ccfc1359bc26f590ced3d0fd575aed405d0eb455c52c0ae0c14769594e0380200e8810b3779441b236c89704ed4df8e
Source2:          vars.config
Source3:          vernemq.service
Patch0:           local_version.patch
Patch1:           bump_plumtree.patch
Patch2:           add_otp_25.patch
Group:            Applications/System
Vendor:           VMware, Inc.
Distribution:     Photon
# leveldb(core dependency) build on aarch64 is currently not supported
# hence vernemq is restricted to x86_64
BuildArch:        x86_64
BuildRequires:    erlang
BuildRequires:    which
BuildRequires:    make
BuildRequires:    libstdc++-devel
BuildRequires:    snappy-devel
BuildRequires:    systemd
Requires:         snappy
Requires:         libstdc++
Requires:         systemd
Requires:         openssl
Requires:         ncurses
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

%description
A high-performance, distributed MQTT message broker.

%prep
# Using autosetup is not feasible
%setup -q
# Using autosetup is not feasible
%setup -D -b 1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
mv ../%{name}_vendor-%{version}/_checkouts _checkouts
cp %{SOURCE2} ./vars.config
# make doesn't support _smp_mflags
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
* Fri Oct 14 2022 Ankit Jain <ankitja@vmware.com> 1.12.5-3
- Release Bump up to build with erlang-25.1-2
* Wed Sep 14 2022 Harinadh D <hdommaraju@vmware.com> 1.12.5-2
- Use erlang/otp version 25.1
* Wed Sep 14 2022 Harinadh D <hdommaraju@vmware.com> 1.12.5-1
- Use erlang/otp version 24
* Wed Jun 09 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.12.0-1
- Upgrade to 1.12.0 version
- Add Requires on useradd, groupadd for pre and userdel, groupdel for postun
* Sun Feb 28 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.11.0-1
- Initial build. First version
