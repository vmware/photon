%define libflux_version 0.191.0
%define libflux_vendor kapacitor-libflux-vendor-%{libflux_version}.tar.gz
%define network_required 1
Name:           kapacitor
Version:        1.6.6
Release:        14%{?dist}
Summary:        Open source framework for processing, monitoring, and alerting on time series data
URL:            https://www.influxdata.com/time-series-platform/kapacitor
Source0:        https://github.com/influxdata/kapacitor/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=55f8452c47220034928c4a8d22b88083c60d71ed3f2be8468599493bcf6d5167f4666e785dfd44926bd8e9a2af8011e9d4bb332db8b5c119085677a5eb017158
Source1:        %{libflux_vendor}
%define sha512  %{name}-libflux-vendor=fb2b13caea5235090db5b0439111c98d97f82ddaf27db7608c21183ac73f1a57c89376aa7767983d7fa4fa6730ab093b93330defc3089aa00aaae44989d6a0f9
Source2:        %{name}.sysusers

Source3: license.txt
%include %{SOURCE3}
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System/Monitoring
BuildRequires:  go
BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  rust
Requires:       systemd
Requires:       systemd-rpm-macros

Patch0:         fix-build-1.patch
Patch1:         fix-build-2.patch

%description
Kapacitor is an Open source framework for processing, monitoring, and alerting on time series data.

%prep
%autosetup -a 1 -n %{name}-%{version} -p1
mkdir -p ~/.cargo
mv kapacitor-libflux-vendor-%{libflux_version} ~/.cargo/vendor
cat > ~/.cargo/config.toml << _EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "${HOME}/.cargo/vendor"
_EOF

%build
go env -w GO111MODULE=auto
cd ..
mkdir -p build/src/github.com/influxdata/kapacitor
mv %{name}-%{version}/* build/src/github.com/influxdata/%{name}
cd build
export GOPATH=$PWD
export PKG_CONFIG=${GOPATH}/src/github.com/influxdata/kapacitor/pkg-config.sh
export CARGO_NET_OFFLINE=true
cd src/github.com/influxdata/kapacitor
go build ./cmd/kapacitor
go build ./cmd/kapacitord
go build ./tick/cmd/tickfmt

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/systemd/system
mkdir -p %{buildroot}%{_sharedstatedir}/kapacitor
mkdir -p %{buildroot}%{_localstatedir}/log/kapacitor
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/kapacitor
cd ../build/src/github.com/influxdata/kapacitor
cp -r kapacitor %{buildroot}%{_bindir}
cp -r kapacitord %{buildroot}%{_bindir}
cp -r tickfmt %{buildroot}%{_bindir}
cp -r usr/share/bash-completion/completions/kapacitor %{buildroot}%{_datadir}/bash-completion/completions/
cp -r scripts/kapacitor.service %{buildroot}%{_libdir}/systemd/system/
cp -r etc/logrotate.d/kapacitor %{buildroot}%{_sysconfdir}/logrotate.d/
cp -r etc/kapacitor/kapacitor.conf %{buildroot}%{_sysconfdir}/kapacitor
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%clean
rm -rf %{buildroot}/*

%pre
if [ $1 -eq 1 ]; then
    # Initial installation.
    %sysusers_create_compat %{SOURCE2}
fi

%post
chown -R %{name}:%{name} /var/lib/%{name}
chown -R %{name}:%{name} /var/log/%{name}
%systemd_post kapacitor.service

%preun
%systemd_preun kapacitor.service

%postun
%systemd_postun_with_restart kapacitor.service

%files
%defattr(-,root,root,755)
%dir %config(noreplace) %{_sysconfdir}/kapacitor
%dir %{_sharedstatedir}/kapacitor
%dir %{_localstatedir}/log/kapacitor
%{_bindir}/kapacitor
%{_bindir}/kapacitord
%{_bindir}/tickfmt
%{_datadir}/bash-completion/completions/kapacitor
%{_libdir}/systemd/system/kapacitor.service
%config(noreplace) %{_sysconfdir}/logrotate.d/kapacitor
%config(noreplace) %{_sysconfdir}/kapacitor/kapacitor.conf
%{_sysusersdir}/%{name}.sysusers

%changelog
* Fri Jan 10 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.6.6-14
- Fix go input dependencies which have Capital letters in name.
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.6.6-13
- Release bump for network_required packages
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.6.6-12
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.6.6-11
- Bump version as a part of go upgrade
* Sun Sep 08 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.6.6-10
- Support offline build
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.6.6-9
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.6.6-8
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.6.6-7
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.6-6
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.6-5
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.6-4
- Bump up version to compile with new go
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.6.6-3
- Resolving systemd-rpm-macros for group creation
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.6.6-2
- Bump up version to compile with new go
* Mon Jul 03 2023 Srish Srinivasan <ssrish@vmware.com> 1.6.6-1
- Update to v1.6.6 to fix multiple CVEs
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.9-9
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.9-8
- Bump up version to compile with new go
* Sun Mar 12 2023 Piyush Gupta <gpiyush@vmware.com> 1.5.9-7
- Bump up version to compile with new go
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.5.9-6
- Use systemd-rpm-macros for user creation
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.9-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.9-4
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.5.9-3
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.5.9-2
- Bump up version to compile with new go
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.5.9-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.5.6-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.5.6-2
- Bump up version to compile with new go
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.6-1
- Automatic Version Bump
* Fri Aug 03 2018 Keerthana K <keerthanak@vmware.com> 1.5.0-1
- Initial kapacitor package for Photon.
