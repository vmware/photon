Summary:	Docker
Name:		docker
Version:	1.5.0
Release:	1
License:	ASL 2.0
URL:		http://docs.docker.com
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	docker-1.5.0.tar.gz

%description
Docker is a platform for developers and sysadmins to develop, ship and run applications.
%prep
%setup -q
%build
%install
install -vdm755 %{buildroot}/bin
mv -v %{_builddir}/%{name}-%{version}/bin/* %{buildroot}/bin/
install -vd %{buildroot}/lib/systemd/system
#install -vdm755 %{buildroot}/etc/systemd/system/multi-user.target.wants
#ln -sfv ../../../../lib/systemd/system/docker.service  %{buildroot}/etc/systemd/system/multi-user.target.wants/docker.service

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

%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/bin/*
/lib/systemd/system/docker.service
#/etc/systemd/system/multi-user.target.wants/docker.service
%changelog
*	Mon Mar 4 2015 Divya Thaluru <dthaluru@vmware.com> 1.5.0-3
-	Initial build.	First version
