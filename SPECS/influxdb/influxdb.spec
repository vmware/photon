%global build_if %{photon_subrelease} >= 91

%define network_required    1
%define gopath  %{_var}/tmp/gopath
%define libflux_version 0.196.0

Name:           influxdb
Version:        1.12.4
Release:        2%{?dist}
Summary:        InfluxDB is an open source time series database
URL:            https://influxdata.com
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/Database

Source0:        https://github.com/influxdata/influxdb/archive/%{name}-%{version}.tar.gz
Source1:        libflux-vendor-%{libflux_version}.tar.gz
Source2:        %{name}.sysusers

Source3: license.txt
%include %{SOURCE3}

Patch0: 0001-fix-libflux-build-with-newer-rust.patch
Patch1: 0001-Perform-offline-cargo-build.patch

BuildRequires:  go
BuildRequires:  git
BuildRequires:  systemd-devel
BuildRequires:  rust

Requires:       systemd-rpm-macros
Requires:       systemd
Requires:       shadow

%description
InfluxDB is an open source time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%prep
%autosetup -p1 -N
# Using autosetup is not feasible
%setup -q -T -D -a 1

%build
export PKG_CONFIG="$PWD/pkg-config.sh"
export CGO_PKG_CONFIG=$PWD/pkg-config.sh
export GOPATH="%{gopath}"

go mod download

FLUXDIR=$(go list -m -f '{{.Dir}}' github.com/influxdata/flux)
pushd $FLUXDIR
patch -p1 < %{PATCH0}
patch -p1 < %{PATCH1}

pushd libflux
mkdir -p .cargo
cat > .cargo/config.toml <<'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "%{_builddir}/%{buildsubdir}/libflux-vendor-%{libflux_version}"
EOF

popd
popd

go install \
  -ldflags="-X main.version=%{version}-%{release} -X main.branch=v%{version}" \
  ./...

%install
mkdir -p \
  %{buildroot}%{_bindir} \
  %{buildroot}%{_sysconfdir}/%{name} \
  %{buildroot}%{_unitdir} \
  %{buildroot}%{_sharedstatedir}/%{name} \
  %{buildroot}%{_var}/log/%{name}

cp -a %{gopath}/bin/influx* %{buildroot}%{_bindir}

install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

mkdir -p -m 755 %{buildroot}%{_libdir}/%{name}/scripts

pushd $PWD/.circleci/packages/%{name}/fs
for i in init.sh influxd-systemd-start.sh; do
  file="usr/lib/%{name}/scripts/${i}"
  install -p -m 0755 "${file}" %{buildroot}%{_libdir}/%{name}/scripts/"${i}"
done
cp lib/systemd/system/%{name}.service  %{buildroot}%{_unitdir}
popd

cp etc/config.sample.toml %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%clean
rm -rf %{buildroot}/*

%pre
%sysusers_create_compat %{SOURCE2}

%post
for dir in %{_sharedstatedir}/%{name} %{_var}/log/%{name}; do
  [ -d "$dir" ] && chown -R %{name}:%{name} "$dir" || :
done
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,755)
%dir %config(noreplace) %{_sysconfdir}/%{name}
%attr(755,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
%attr(755,%{name},%{name}) %dir %{_var}/log/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_libdir}/%{name}/scripts/init.sh
%{_libdir}/%{name}/scripts/influxd-systemd-start.sh
%{_unitdir}/%{name}.service
%{_bindir}/influxd
%{_bindir}/influx
%{_bindir}/influx_inspect
%{_bindir}/influx_tools
%{_sysusersdir}/%{name}.conf

%changelog
* Tue Jun 30 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.12.4-2
- Use vendored sources for libflux
* Wed Jun 03 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.12.4-1
- Upgrade to v1.12.4
* Wed Feb 04 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.10-19
- Bump version as a part of go upgrade
* Thu Oct 09 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.8.10-18
- Bump version as a part of go upgrade
* Tue Sep 30 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 1.8.10-17
- Fix to show version,branch and commit details in influxd command
* Thu May 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.8.10-16
- Renaming sysusers to conf to fix auto user creation
* Fri Jan 10 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.8.10-15
- Fix srp input declaration when package names have Capital letters
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.8.10-14
- Release bump for network_required packages
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.8.10-13
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.8.10-12
- Bump version as a part of go upgrade
* Fri Aug 23 2024 Bo Gan <bo.gan@broadcom.com> 1.8.10-11
- Simplify build scripts. Godep is removed in favor of gomod.
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.8.10-10
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.8.10-9
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.8.10-8
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-7
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-6
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-5
- Bump up version to compile with new go
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.8.10-4
- Resolving systemd-rpm-macros for group creation
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-3
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.10-2
- Bump up version to compile with new go
* Thu May 18 2023 Anmol Jain <anmolja@vmware.com> 1.8.10-1
- Version Bump
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-10
- Bump up version to compile with new go
* Sun Mar 12 2023 Piyush Gupta <gpiyush@vmware.com> 1.8.2-9
- Bump up version to compile with new go
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.8.2-8
- Use systemd-rpm-macros for user creation
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.2-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.2-6
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.2-5
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.2-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.8.2-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.8.2-2
- Bump up version to compile with new go
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.2-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.1-1
- Automatic Version Bump
* Tue Jan 29 2019 Keerthana K <keerthanak@vmware.com> 1.6.0-5
- Using golang dep to resolve dependencies.
* Fri Jan 25 2019 Keerthana K <keerthanak@vmware.com> 1.6.0-4
- Added make check.
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.6.0-3
- Build using go 1.9.7
* Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 1.6.0-2
- Fix for aarch64
* Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
- Initial influxdb package for Photon.
