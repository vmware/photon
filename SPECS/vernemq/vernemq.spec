Summary:          VerneMQ is a high-performance, distributed MQTT message broker
Name:             vernemq
Version:          2.1.0
Release:          1%{?dist}
License:          Apache License, Version 2.0
URL:              https://github.com/vernemq/vernemq
Group:            Applications/System
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://github.com/%{name}/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=219ec809d4360e101dd64818e0932700c7700a4a0cec90671f69042b33010f6949574d90a130c27631e12d5133820c50d0e5b80652a6d66a42f186e55f9512f4

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
%define sha512 %{name}_vendor=dbe64a919eea5152b09e34348306f9d8f9480887facaa68abc748cee95562aee9273112ff275755f2f2425e1573aafd1692cc6cbe3f3cb68823dfda8d12e742b

Source2: vars.config
Source3: %{name}.service

Patch0: 0001-local_version.patch

# leveldb(core dependency) build on aarch64 is currently not supported
# hence vernemq is restricted to x86_64
BuildArch:        x86_64

BuildRequires:    erlang >= 27.3.4
BuildRequires:    which
BuildRequires:    make
BuildRequires:    libstdc++-devel
BuildRequires:    snappy-devel
BuildRequires:    systemd-devel

Requires:         erlang >= 27.3.4
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
%autosetup -p1 -b0 -b1

%build
LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
mv ../%{name}_vendor-%{version}/_checkouts _checkouts

cp %{SOURCE2} ./vars.config

find . \( -name "*.so" -or -name "*.so.*" -or -name "*.o" -or -name "*.a" -or -name "*.beam" \) -delete

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
      _build/default/rel/%{name}//${erts_dir} \
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

%pre
getent group %{name} >/dev/null || groupadd -r %{name}

getent passwd %{name} >/dev/null || \
  useradd --comment "VerneMQ" --shell \
    /bin/bash -M -r --groups %{name} --home %{_sharedstatedir}/%{name} %{name}

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

%changelog
* Tue Nov 18 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 2.1.0-1
- Update to 2.1.0
* Tue Oct 14 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.1-5
- Bump version as a part of erlang upgrade
* Tue Apr 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.0.1-4
- Bump release for updating erlang
* Thu Apr 10 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.0.1-3
- Bump release for updating erlang
* Wed Sep 04 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.1-2
- Do fully offline build
* Fri Jun 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.1-1
- Upgrade to v2.0.1
* Wed Nov 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.12.5-1
- Upgrade to v1.12.5
* Tue Nov 30 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.12.0-3
- Increment for openssl 3.0.0 compatibility
* Tue Jul 13 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.12.0-2
- Add Requires on useradd, groupadd for pre and userdel, groupdel for postun
* Wed Jun 09 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.12.0-1
- Upgrade to 1.12.0 version
* Sun Feb 28 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.11.0-1
- Initial build. First version
