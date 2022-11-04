Name:           docker-vsock
Summary:        vsock Listener launcher for docker engine
Version:        0.0.1
Release:        1%{?dist}
License:        Apache License, Version 2.0
URL:            http://www.vmware.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        dockerd-vsock.c
Source1:        dockerd-vsock.conf

BuildRequires:  systemd-devel

Requires:       docker-engine

%description
docker-vsock provides an wrapper utility that make docker engine (dockerd) listen on vsock.

%prep

%build
gcc -Os -Wall -Werror -o dockerd-vsock %{SOURCE0}

%install
install -d -m 755 %{buildroot}%{_bindir}
install -p -m 755 dockerd-vsock %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_unitdir}/docker.service.d
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/docker.service.d/

%post
systemctl daemon-reload >/dev/null 2>&1 || :

%postun
systemctl daemon-reload >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%{_bindir}/dockerd-vsock
%{_unitdir}/docker.service.d/dockerd-vsock.conf

%changelog
* Mon Nov 29 2021 Bo Gan <ganb@vmware.com> 0.0.1-1
- Initial packaging
