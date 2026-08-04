%global build_if %{photon_subrelease} == 91

Summary:        Reliable PostgreSQL Backup & Restore
Name:           pgbackrest
Version:        2.58.0
Release:        6%{?dist}
Url:            https://pgbackrest.org
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pgbackrest/pgbackrest/archive/refs/tags/release/%{name}-%{version}.tar.gz

Source1: %{name}.conf

Source2: license.txt
%include %{SOURCE2}

BuildRequires: openssl-devel
BuildRequires: libxml2-devel
BuildRequires: lz4-devel
BuildRequires: postgresql18-devel
BuildRequires: libyaml-devel
BuildRequires: libssh2-devel
BuildRequires: meson

Requires: libssh2
Requires: openssl
Requires: xz-libs
Requires: zstd-libs
Requires: bzip2-libs
Requires: lz4
Requires: libxml2
Requires: (postgresql18-libs or postgresql17-libs or postgresql16-libs or postgresql15-libs or postgresql14-libs)

%description
pgBackRest aims to be a reliable, easy-to-use backup and restore solution
that can seamlessly scale up to the largest databases and workloads by
utilizing algorithms that are optimized for database-specific requirements.

%prep
%autosetup -p1 -n %{name}-release-%{version}

%build
ln -sv $(pg_config --libdir)/pkgconfig/* %{_libdir}/pkgconfig/

%{meson}
%{meson_build}

%install
%{meson_install}

mkdir -p %{buildroot}%{_sysconfdir}/%{name} \
         %{buildroot}%{_var}/log/%{name}

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%dir %{_var}/log/%{name}
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/%{name}/%{name}.conf

%changelog
* Fri Jun 26 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.58.0-6
- Restore postgresql14 and postgresql15 support
* Mon Jun 08 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 2.58.0-5
- Release version bump as part of libxml2/libxslt
* Thu Jun 04 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.58.0-4
- Remove postgresql15 support
* Sat May 16 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.58.0-3
- Remove postgresql v13, 14, 15 support
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.58.0-2
- Extended to build for subrelease 91 and above
* Fri Feb 13 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.58.0-1
- Upgrade version to v2.58.0, which supports pgsql18
* Fri Aug 29 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.54.2-3
- Build with pgsql17
* Thu Apr 10 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.54.2-2
- Build with pgsql16
* Mon Mar 03 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.54.2-1
- Update to 2.54.2
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.48-3
- Release bump for SRP compliance
* Thu Dec 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.48-2
- Build with pgsql15, this was a mishap during cherry picking
* Thu Nov 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.48-1
- Initial version.
