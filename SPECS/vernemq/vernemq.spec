Summary:          VerneMQ is a high-performance, distributed MQTT message broker
Name:             vernemq
Version:          1.12.6.2
Release:          5%{?dist}
License:          Apache License, Version 2.0
URL:              https://github.com/vernemq/vernemq
Group:            Applications/System
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://github.com/vernemq/vernemq/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=be171617ee827a9fa9a1dcd836b3d1f9b53975ecc6a3865c3e5d4c2c6abcdee124ef92a546035b549416235c1d9e9271f9f034e590397d5505b941eb8268bc97

Source1: %{name}_vendor-%{version}.tar.gz
%define sha512 vernemq_vendor=45acfa62b6bebddad19ce02461e5ab212dd868b37ab9d2ed89df1c7b3d9ad2ec7281d61f8d4e1171f6018010607a8129bc99eee837f900a2449617d7935af0d1

Source2:    vars.config
Source3:    %{name}.service
Source4:    %{name}.sysusers
Patch0: local_version.patch

# leveldb(core dependency) build on aarch64 is currently not supported
# hence vernemq is restricted to x86_64
BuildArch:        x86_64

BuildRequires:    erlang
BuildRequires:    which
BuildRequires:    make
BuildRequires:    libstdc++-devel
BuildRequires:    snappy-devel
BuildRequires:    systemd-devel

Requires:         snappy
Requires:         libstdc++
Requires:         systemd
Requires:         openssl
Requires:         ncurses
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd

%description
A high-performance, distributed MQTT message broker.

%prep
# Using autosetup is not feasible
%setup -q
# Using autosetup is not feasible
%setup -Tq -D -b 1
%autopatch -p1 -m0 -M2

%build
export LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
mv ../%{name}_vendor-%{version}/_checkouts _checkouts
cp %{SOURCE2} ./vars.config
# make doesn't support _smp_mflags
make rel

%install
install -vdm 0755 %{buildroot}%{_sharedstatedir}/%{name}/broker
install -vdm 0755 %{buildroot}%{_sharedstatedir}/%{name}/msgstore
install -vdm 0755 %{buildroot}%{_sysconfdir}/%{name}
install -vpm 0644 -t %{buildroot}%{_sysconfdir}/%{name} _build/default/rel/%{name}/etc/%{name}.conf
install -vpm 0644 -t %{buildroot}%{_sysconfdir}/%{name} _build/default/rel/%{name}/etc/vmq.acl
install -vdm 0755 %{buildroot}%{_libdir}/%{name}

cp -pr _build/default/rel/%{name}/bin \
       _build/default/rel/%{name}/lib \
       _build/default/rel/%{name}/erts-* \
       _build/default/rel/%{name}/releases \
       %{buildroot}%{_libdir}/%{name}

install -vdm 0755 %{buildroot}%{_datadir}
cp -r _build/default/rel/%{name}/share %{buildroot}%{_datadir}/%{name}
install -vdm 0755 %{buildroot}%{_localstatedir}/log/%{name}/sasl

mkdir -p %{buildroot}%{_unitdir}
cp %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service

install -vdm755 %{buildroot}%{_presetdir}
echo "enable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

mkdir -p %{buildroot}%{_tmpfilesdir}
cat >> %{buildroot}%{_tmpfilesdir}/%{name}.conf << EOF
d /run/%{name} 0755 %{name} %{name} -
EOF

install -vdm 0755 %{buildroot}%{_sbindir}
ln -sfv %{_lib64dir}/%{name}/bin/%{name} %{buildroot}%{_sbindir}
ln -sfv %{_lib64dir}/%{name}/bin/vmq-admin %{buildroot}%{_sbindir}
ln -sfv %{_lib64dir}/%{name}/bin/vmq-passwd %{buildroot}%{_sbindir}
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%pre
%sysusers_create_compat %{SOURCE4}

%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE.txt
%attr(0755,%{name},%{name}) %{_sharedstatedir}/%{name}
%attr(0755,%{name},%{name}) %{_localstatedir}/log/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_sbindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.sysusers

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.12.6.2-5
- Bump version as a part of openssl upgrade
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.12.6.2-4
- Resolving systemd-rpm-macros for group creation
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 1.12.6.2-3
- Bump version as a part of ncurses upgrade to v6.4
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.12.6.2-2
- Use systemd-rpm-macros for user creation
* Fri Dec 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.12.6.2-1
- Upgrade to v1.12.6.2
* Wed Nov 09 2022 Harinadh D <hdommaraju@vmware.com> 1.12.5-2
- fix applying patches in prep section
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.12.5-1
- Upgrade to v1.12.5
* Tue Jul 13 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.12.0-2
- Add Requires on useradd, groupadd for pre and userdel, groupdel for postun
* Wed Jun 09 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.12.0-1
- Upgrade to 1.12.0 version
* Sun Feb 28 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.11.0-1
- Initial build. First version
