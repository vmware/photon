%define debug_package %{nil}

Summary:      Systemd service files for Google Compute Engine Linux images
Name:         google-compute-engine-services
Version:      20170426
Release:      1%{?dist}
License:      Apache License 2.0
Group:        System Environment/Base
Vendor:       VMware, Inc.
Distribution: Photon
URL:          https://github.com/GoogleCloudPlatform/compute-image-packages/
Source0:      https://github.com/GoogleCloudPlatform/compute-image-packages/archive/compute-image-packages-%{version}.tar.gz
%define sha1  compute-image-packages=6852588ecae9cc39bac7683f1e21f88a5d41e831

Requires:     systemd
Requires:     google-compute-engine

Obsoletes:    google-startup-scripts

BuildArch:      noarch

%description
Collection of service files for packages installed on Google supported Compute Engine images.

%prep
%setup -q -n compute-image-packages-%{version}

%build

%install
install -d %{buildroot}%{_libdir}/systemd/system
cp google_compute_engine_init/systemd/*.service %{buildroot}%{_libdir}/systemd/system

%post
systemctl stop --no-block google-accounts-daemon
systemctl stop --no-block google-clock-skew-daemon
systemctl stop --no-block google-ip-forwarding-daemon

systemctl enable google-accounts-daemon.service
systemctl enable google-clock-skew-daemon.service
systemctl enable google-instance-setup.service
systemctl enable google-ip-forwarding-daemon.service
systemctl enable google-network-setup.service
systemctl enable google-shutdown-scripts.service
systemctl enable google-startup-scripts.service

systemctl start --no-block google-accounts-daemon
systemctl start --no-block google-clock-skew-daemon
systemctl start --no-block google-ip-forwarding-daemon

%postun
systemctl stop --no-block google-accounts-daemon
systemctl stop --no-block google-clock-skew-daemon
systemctl stop --no-block google-ip-forwarding-daemon

systemctl --no-reload disable google-accounts-daemon.service
systemctl --no-reload disable google-clock-skew-daemon.service
systemctl --no-reload disable google-instance-setup.service
systemctl --no-reload disable google-ip-forwarding-daemon.service
systemctl --no-reload disable google-network-setup.service
systemctl --no-reload disable google-shutdown-scripts.service
systemctl --no-reload disable google-startup-scripts.service

%files
%defattr(-,root,root)
%{_libdir}/systemd/system/*.service

%changelog
* Fri Apr 28 2017 Anish Swaminathan <anishs@vmware.com> 20170426-1
- Initial packaging for Photon

