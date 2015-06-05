Summary:	Docker
Name:		docker
Version:	1.6.2
Release:	3
License:	ASL 2.0
URL:		http://docs.docker.com
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://get.docker.com/builds/Linux/x86_64/%{name}-%{version}.tgz

%description
Docker is a platform for developers and sysadmins to develop, ship and run applications.
%prep
%autosetup -c %{name}-%{version}
%build
%install
install -vdm755 %{buildroot}/bin
install -vm755 %{_builddir}/%{name}-%{version}/usr/local/bin/docker %{buildroot}/bin/
install -vd %{buildroot}/lib/systemd/system

cat > %{buildroot}/lib/systemd/system/docker.service <<- "EOF"
[Unit]
Description=Docker Daemon

[Service]
ExecStart=/bin/docker -d -s overlay
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=always

[Install]
WantedBy=multi-user.target

EOF

%check
%clean
rm -rf %{buildroot}/*
%files
/bin/docker
/lib/systemd/system/docker.service
%changelog
*	Mon May 18 2015 Tom McPhail <tmcphail@vmware.com> 1.6.2-3
-	Updated to version 1.6.2 and cleaned up spec
*	Fri May 15 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.0-2
-	Updated to version 1.6
*	Mon Mar 4 2015 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
-	Initial build. First version
