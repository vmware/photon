Summary:    	Docker
Name:       	docker
Version:    	1.11.2
Release:    	2%{?dist}
License:    	ASL 2.0
URL:        	http://docs.docker.com
Group:      	Applications/File
Vendor:     	VMware, Inc.
Distribution:   Photon
Source0:	https://get.docker.com/builds/Linux/x86_64/%{name}-%{version}.tgz
%define sha1 docker=1bfd065784e0f422c000d86da4feda87cd63ced8
Source1: 	docker.service
Source2: 	docker-containerd.service
Source3:  docker.socket
Source4:  docker.default
BuildRequires:  systemd
Requires:       systemd

%description
Docker is a platform for developers and sysadmins to develop, ship and run applications.
%prep
%setup -qn docker
%build
%install
install -vdm755 %{buildroot}/usr/bin
install -vdm755 %{buildroot}/etc/default
mv -v %{_builddir}/%{name}/* %{buildroot}/usr/bin/
install -vd %{buildroot}/usr/lib/systemd/system
cp %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service
cp %{SOURCE2} %{buildroot}/usr/lib/systemd/system/%{name}-containerd.service
cp %{SOURCE3} %{buildroot}/usr/lib/systemd/system/%{name}.socket
cp %{SOURCE4} %{buildroot}/etc/default/%{name}

%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%preun
%systemd_preun docker.service
%systemd_preun docker-containerd.service

%post
/sbin/ldconfig
%systemd_post docker.service
%systemd_post docker-containerd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart docker-containerd.service
%systemd_postun_with_restart docker.service


%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}
/usr/lib/systemd/system/%{name}.service
/usr/lib/systemd/system/%{name}.socket
/usr/lib/systemd/system/%{name}-containerd.service
/etc/default/%{name}

%changelog
*   Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> 1.11.2-2
-   Add socket activation back
*   Tue Jun 28 2016 Anish Swaminathan <anishs@vmware.com> 1.11.2-1
-   Upgraded to version 1.11.2
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  1.11.0-6
-   Fixed logic to restart the active services after upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11.0-5
-   GA - Bump release of all rpms
*   Tue May 10 2016 Anish Swaminathan <anishs@vmware.com> 1.11.0-4
-   Remove commented post actions
*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  1.11.0-3
-   Fixing spec file to handle rpm upgrade scenario correctly
*   Sat Apr 30 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11.0-2
-   Add $DOCKER_OPTS to start in docker.service
*   Fri Apr 15 2016 Anish Swaminathan <anishs@vmware.com> 1.11.0-1
-   Updated to version 1.11.0.
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.2-1
-   Upgraded to version 1.10.2
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.9.0-2
-   Add systemd to Requires and BuildRequires.
-   Use systemctl to enable/disable service.
*   Fri Nov 06 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.9.0-1
-   Update to version 1.9.0
*   Mon Aug 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.1-1
-   Update to new version 1.8.1.
*   Fri Jun 19 2015 Fabio Rapposelli <fabio@vmware.com> 1.7.0-1
-   Update to new version.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.6.0-3
-   Update according to UsrMove.
*   Fri May 15 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.0-2
-   Updated to version 1.6
*   Mon Mar 2 2015 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
-   Initial build. First version
