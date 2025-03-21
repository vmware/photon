Summary:          VerneMQ is a high-performance, distributed MQTT message broker
Name:             vernemq
Version:          2.0.1
Release:          2%{?dist}
License:          Apache License, Version 2.0
URL:              https://github.com/vernemq/vernemq
Group:            Applications/System
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://github.com/%{name}/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=e4f1cd4c74d2cb67ab1524a76bdc6071e7b1e38ede574bc11e5ffe861bff99321647be0730f5f17d724dd792aa0fb86d0e9a92417f45bc43fef1461f1f64ae52

# Building this tarball is not a straight forward process
#
# Setup your environment with desired version of erlang
# Extract vernemq tarball
# Run `make rel` (this command should succeed)
# This will bring all dependencies into _build/default/lib/
# mkdir -p vernemq_vendor-<version>/_checkouts
# mv _build/default/lib/* vernemq_vendor-<version>/_checkouts
# mv _build/default/plugins vernemq_vendor-<version>/
#
# Now do, rm -rf _build
# mkdir -p _build/default/
# cp -a vernemq_vendor-<version>/plugins _build/default/
# cp -a vernemq_vendor-<version>/_checkouts .
#
# Ensure that no sources are fetched from web during build
# If anything is fetched from web, it must be fixed
#
# Clear all built files
# find . \( -name "*.so" -or -name "*.so.*" -or -name "*.o" -or -name "*.a" -or -name "*.beam" \) -delete
#
# Once all done, create vendor tarball
#
# XZ_OPT=-9 tar cJf vernemq_vendor-version>.tar.xz
Source1: %{name}_vendor-%{version}.tar.xz
%define sha512 %{name}_vendor=f0a57b95ad487544717004c0af449d9fd589be37d9a66e03c6e51bdc7ff5e444a224c6a88c219a08fcd6f08c6bfa4c60ae8d6e8e8733a1d6d54b83608bc73b26

Source2:    vars.config
Source3:    %{name}.service
Source4:    %{name}.sysusers

Patch0: 0001-local_version.patch

# leveldb(core dependency) build on aarch64 is currently not supported
# hence vernemq is restricted to x86_64
BuildArch:        x86_64

BuildRequires:    erlang
BuildRequires:    which
BuildRequires:    make
BuildRequires:    libstdc++-devel
BuildRequires:    snappy-devel
BuildRequires:    systemd-devel

Requires:         erlang = 26.2.5
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
%autosetup -p1 -b0 -b1

%build
export LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
mv ../%{name}_vendor-%{version}/_checkouts _checkouts

mkdir -p _build/default
mv ../%{name}_vendor-%{version}/plugins _build/default/

cp %{SOURCE2} ./vars.config

find . \( -name "*.so" -or -name "*.so.*" -or -name "*.o" -or -name "*.a" -or -name "*.beam" \) -delete

cp -a _build/default/plugins/* _checkouts/

# make doesn't support _smp_mflags
REBAR_OFFLINE=1 make rel

%install
install -vdm 0755 %{buildroot}%{_sharedstatedir}/%{name}/broker
install -vdm 0755 %{buildroot}%{_sharedstatedir}/%{name}/msgstore
install -vdm 0755 %{buildroot}%{_sysconfdir}/%{name}
install -vpm 0644 -t %{buildroot}%{_sysconfdir}/%{name} _build/default/rel/%{name}/etc/%{name}.conf
install -vpm 0644 -t %{buildroot}%{_sysconfdir}/%{name} _build/default/rel/%{name}/etc/vmq.acl
install -vdm 0755 %{buildroot}%{_libdir}/%{name}

erts_dir="$(find %{_libdir}/erlang/ -maxdepth 1 -type d -name erts-*)"
[ -z "${erts_dir}" ] && exit 1
erts_dir="$(basename ${erts_dir})"

ln -sv %{_libdir}/erlang/${erts_dir}/bin/* \
          _build/default/rel/%{name}/${erts_dir}/bin/

cp -a _build/default/rel/%{name}/bin \
      _build/default/rel/%{name}/lib \
      _build/default/rel/%{name}/${erts_dir} \
      _build/default/rel/%{name}/releases \
      %{buildroot}%{_libdir}/%{name}

install -vdm 0755 %{buildroot}%{_libdir}/erlang/lib
pushd %{buildroot}%{_usr}
for i in bridge commons server; do
  ln -srv lib/vernemq/lib/vmq_${i}-0.0.0 lib/erlang/lib/
done
popd

install -vdm 0755 %{buildroot}%{_datadir}
cp -a _build/default/rel/%{name}/share %{buildroot}%{_datadir}/%{name}
install -vdm 0755 %{buildroot}%{_var}/log/%{name}/sasl

mkdir -p %{buildroot}%{_unitdir}
cp %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service

install -vdm755 %{buildroot}%{_presetdir}
echo "enable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

mkdir -p %{buildroot}%{_tmpfilesdir}
cat >> %{buildroot}%{_tmpfilesdir}/%{name}.conf << EOF
d %{_rundir}/%{name} 0755 %{name} %{name} -
EOF

install -vdm 0755 %{buildroot}%{_sbindir}
ln -sv %{_libdir}/%{name}/bin/%{name} %{buildroot}%{_sbindir}
ln -sv %{_libdir}/%{name}/bin/vmq-admin %{buildroot}%{_sbindir}
ln -sv %{_libdir}/%{name}/bin/vmq-passwd %{buildroot}%{_sbindir}
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%pre
%sysusers_create_compat %{SOURCE4}

%preun
%systemd_preun %{name}.service

%post
# for pipe dir, after first installation
mkdir -m 755 -p %{_rundir}/%{name}
chown -R %{name}:%{name} %{_rundir}/%{name}

%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE.txt
%attr(0755,%{name},%{name}) %{_sharedstatedir}/%{name}
%attr(0755,%{name},%{name}) %{_var}/log/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_sbindir}/*
%attr(0755,%{name},%{name}) %{_libdir}/%{name}
%attr(0755,%{name},%{name}) %{_libdir}/erlang/lib/*
%attr(0755,%{name},%{name}) %{_datadir}/%{name}
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.sysusers

%changelog
* Wed Sep 04 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.1-2
- Do fully offline build
* Fri Jun 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.1-1
- Upgrade to v2.0.1
- Avoid repackaging erlng binaries, use system provided erlang
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
