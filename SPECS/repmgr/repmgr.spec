Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr
Version:        5.3.2
Release:        1%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org/
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://repmgr.org/download/%{name}-%{version}.tar.gz
%define sha512  %{name}=803f94ea99454f59cd753db4a8f64066f3988e347b5b8e3de08b941c09ac9128ba48beeecaface7a729b0b4f296ccb4470c18128fdd6c2e418e8e3fbbefcda1e

BuildRequires:  postgresql-devel cpio

Requires:       postgresql-libs

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

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/postgresql/*
%exclude %dir %{_libdir}/debug
%{_datadir}/*

%changelog
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
