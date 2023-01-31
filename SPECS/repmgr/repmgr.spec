Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr
Version:        5.3.3
Release:        1%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://repmgr.org/download/%{name}-%{version}.tar.gz
%define sha512  %{name}=938eabd6a73296e657c199878050a7fac82285da9613d0fff861e969865a4c3725a13b548e84a17ee035ef536a738b67411b9c93fdafd8698bb76844f0834d15

BuildRequires:  postgresql15-devel
BuildRequires:  cpio

Requires:       readline
Requires:       openssl
Requires:       zlib
Requires:       (postgresql15-libs or postgresql14-libs or postgresql13-libs)

%description
repmgr is an open-source tool suite for managing replication and failover in a cluster of PostgreSQL servers.

%prep
%autosetup -p1

%build
%configure CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
export CFLAGS="-O2 -g -fcommon"
%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_usr}

pg_ver="$(pg_config --version | cut -d' ' -f2 | cut -d. -f1)"

pushd %{buildroot}%{_usr}/pgsql/"${pg_ver}"
mv bin share lib %{buildroot}%{_usr}
popd

rmdir %{buildroot}%{_usr}/pgsql/"${pg_ver}" \
      %{buildroot}%{_usr}/pgsql

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/postgresql/*
%exclude %dir %{_libdir}/debug
%{_datadir}/*

%changelog
* Tue Jan 31 2023 Gerrit Photon <photon-checkins@vmware.com> 5.3.3-1
- Automatic Version Bump
* Fri Jan 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.2-3
- Remove pgsql-12 dependency
* Thu Jan 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.2-2
- Bump version as a part of postgresql fixes
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 5.3.2-1
- Automatic Version Bump
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.3.1-2
- Fix binary path
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 5.3.1-1
- Automatic Version Bump
* Tue Oct 19 2021 Michael Paquier <mpaquier@vmware.com> 5.1.0-5
- Rework dependency list with postgresql
- Add support for autosetup and _smp_mflags
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 5.1.0-4
- GCC-10 support.
* Wed Sep 30 2020 Dweep Advani <photon-checkins@vmware.com> 5.1.0-3
- Preferring libedit
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.1.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.1.0-1
- Automatic Version Bump
* Thu Apr 09 2020 Stanislav Paskalev <spaskalev@vmware.com> 5.0.0-1
- Initial build.  First version
