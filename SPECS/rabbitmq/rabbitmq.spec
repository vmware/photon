Name:          rabbitmq-server
Summary:       RabbitMQ messaging server
Version:       3.6.9
Release:       2%{?dist}
Group:         Applications
Vendor:        VMware, Inc.
Distribution:  Photon
License:       MPLv1.1
URL:           http://www.rabbitmq.com
Source0:       %{name}-%{version}.tar.xz
%define sha1 rabbitmq=559372baa7df9ebf853f3cbf2a15a1fc14cd38ee
Source1:       rabbitmq.config
Source2:       rabbitmq-server.service
Requires:      erlang
Requires:      shadow
Requires:      sed
BuildRequires: erlang
BuildRequires: rsync
BuildRequires: zip
BuildRequires: libxslt
BuildRequires: python-xml
BuildArch:     noarch

%description
rabbitmq messaging server

%prep
%setup -q

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT \
             PREFIX=%{_prefix} \
             RMQ_ROOTDIR=/usr/lib/rabbitmq/

install -vdm755 %{buildroot}/var/lib/rabbitmq/
install -vdm755 %{buildroot}/%{_sysconfdir}/rabbitmq/
install -vdm755 %{buildroot}/usr/lib/systemd/system/

cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/rabbitmq/
cp %{SOURCE2} %{buildroot}/usr/lib/systemd/system/

%pre
if ! getent group rabbitmq >/dev/null; then
  groupadd -r rabbitmq
fi

if ! getent passwd rabbitmq >/dev/null; then
  useradd -r -g rabbitmq -d %{_localstatedir}/lib/rabbitmq rabbitmq \
  -s /sbin/nologin -c "RabbitMQ messaging server"
fi

%post
chown -R rabbitmq:rabbitmq /var/lib/rabbitmq
chown -R rabbitmq:rabbitmq /etc/rabbitmq
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*
%{_sysconfdir}/*
/var/lib/*

%changelog
* Wed Apr 26 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.9-2
- Fix arch
* Wed Apr 5 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.9-1
- Updating package to the latest
* Mon Dec 12 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.6-1
- Initial.
