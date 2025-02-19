%define network_required 1
%global services        google-guest-agent.service google-startup-scripts.service google-shutdown-scripts.service
%global goipath         github.com/GoogleCloudPlatform/guest-agent
Summary:       Google Compute Engine guest environment
Name:          google-guest-agent
Version:       20250122.00
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
URL:           https://github.com/GoogleCloudPlatform/guest-agent
Distribution:  Photon

Source0:       https://github.com/GoogleCloudPlatform/guest-agent/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=f86520161ee3da6b26f190280af9148a75ef590cb93656daaac9fd673f369186a5b8a05ab6d0c79d463ba5c11077f35d5d51e9c52d4e3aa191594d184abe9f65

Source1: license.txt
%include %{SOURCE1}

BuildRequires: go
BuildRequires: ca-certificates
BuildRequires: systemd-rpm-macros

Requires:      systemd

Conflicts:     google-compute-engine <= 20191210-4
Conflicts:     google-compute-engine-services <= 20191210-4

%description
This package contains scripts, configuration, and init files
for features specific to the Google Compute Engine cloud environment.

%prep
%autosetup -n guest-agent-%{version} -p1

%build
for cmd in google_guest_agent google_metadata_script_runner; do
  go build -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vd                     %{buildroot}%{_sysconfdir}/default
install -m 0755 -vd                     %{buildroot}%{_unitdir}
install -m 0755 -vp %{gobuilddir}/bin/*             %{buildroot}%{_bindir}
install -m 0644 -vp instance_configs.cfg            %{buildroot}%{_sysconfdir}/default
install -m 0644 -vp google-guest-agent.service      %{buildroot}%{_unitdir}
install -m 0644 -vp google-startup-scripts.service  %{buildroot}%{_unitdir}
install -m 0644 -vp google-shutdown-scripts.service %{buildroot}%{_unitdir}

%post
%systemd_post %{services}

%preun
%systemd_preun %{services}

%postun
%systemd_postun_with_restart %{services}

%files
%defattr(-,root,root)
%doc CONTRIBUTING.md README.md
%config(noreplace) %{_sysconfdir}/default/instance_configs.cfg
%{_bindir}/google_guest_agent
%{_bindir}/google_metadata_script_runner
%{_unitdir}/google-guest-agent.service
%{_unitdir}/google-startup-scripts.service
%{_unitdir}/google-shutdown-scripts.service

%changelog
* Mon Feb 03 2025 Tapas Kundu <tapas.kundu@broadcom.com> 20250122.00-1
- Initial version
