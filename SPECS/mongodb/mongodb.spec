Name:           mongodb
Version:        3.4.10
Release:        2%{?dist}
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
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel

%description
MongoDB (from "humongous") is a scalable, high-performance, open source, document-oriented database.

%prep
%setup -qn mongo-r%{version}

%build
scons %{?_smp_mflags} MONGO_VERSION=%{version} \
    --disable-warnings-as-errors \
    --use-system-pcre \
    --use-system-zlib

%install
scons %{?_smp_mflags} MONGO_VERSION=%{version} install \
    --prefix=%{buildroot}%{_prefix} \
    --use-system-pcre \
    --use-system-zlib
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
*   Tue Feb 04 2020 Shreyas B <shreyasb@vmware.com> 3.4.10-2
-   Use locally build packages(i.e. pcre, valgrind, zlib) to build mongodb.
*   Tue Dec 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.4.10-1
-   Update to version 3.4.10, fix CVE-2017-15535
*   Sun Oct 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.4-1
-   Initial build.  First version
