Name:           mongodb
Version:        3.4.10
Release:        1%{?dist}
Summary:        The MongoDB Database
Group:          Applications/Database
License:        AGPLv3
URL:            http://www.mongodb.org/
Source0:        https://github.com/mongodb/mongo/archive/mongo-r%{version}.tar.gz
%define sha1    mongo-r=39b1e86c650a7b1b3ccc1dee86d088fc95a0a225
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  scons
BuildRequires:  systemd

%description
MongoDB (from "humongous") is a scalable, high-performance, open source, document-oriented database.

%prep
%setup -qn mongo-r%{version}

%build
%ifarch x86_64
scons %{?_smp_mflags} MONGO_VERSION=%{version} \
    --disable-warnings-as-errors
%endif

%ifarch aarch64
scons %{?_smp_mflags} MONGO_VERSION=%{version} CCFLAGS="-march=armv8-a+crc" \
    --disable-warnings-as-errors
%endif



%install
%ifarch x86_64
scons %{?_smp_mflags} MONGO_VERSION=%{version} install \
    --prefix=%{buildroot}%{_prefix} \
    --disable-warnings-as-errors
%endif

%ifarch aarch64
scons %{?_smp_mflags} MONGO_VERSION=%{version} CCFLAGS="-march=armv8-a+crc" install \
    --prefix=%{buildroot}%{_prefix} \
    --disable-warnings-as-errors
%endif

install -d %{buildroot}/var/log/%{name}
install -d %{buildroot}/var/lib/mongo
install -d -m 755 %{buildroot}%{_unitdir}
install -D -m 644 rpm/mongod.service %{buildroot}%{_unitdir}
install -D -m 644 rpm/mongod.conf %{buildroot}/etc/mongod.conf


%clean
rm -rf %{buildroot}

# Pre-install
%pre
if ! getent group mongod >/dev/null; then
    /sbin/groupadd -r mongod
fi
if ! getent passwd mongod >/dev/null; then
    /sbin/useradd -g mongod mongod -s /sbin/nologin
fi

%preun
    %systemd_preun mongod.service

%postun
    %systemd_postun_with_restart mongod.service

%post
    %systemd_post mongod.service


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_unitdir}/mongod.service
%config(noreplace) %attr(0644, mongod, mongod) %{_sysconfdir}/mongod.conf
%attr(0766, mongod, mongod) %dir /var/log/%{name}
%attr(0766, mongod, mongod) %dir /var/lib/mongo

%changelog
*   Fri Mar 16 2018 Dheeraj Shetty <dheerajs@vmware.com> 3.4.10-1
-   Initial build.  First version
