%global build_if %{photon_subrelease} <= 90

Summary:        Reliable PostgreSQL Backup & Restore
Name:           pgbackrest
Version:        2.54.2
Release:        3.1.1%{?dist}
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
BuildRequires: postgresql17-devel
BuildRequires: cmake
BuildRequires: libyaml-devel

Requires: openssl
Requires: xz-libs
Requires: zstd-libs
Requires: bzip2-libs
Requires: lz4
Requires: libxml2
Requires: (postgresql17-libs or postgresql16-libs or postgresql15-libs or postgresql14-libs or postgresql13-libs)

%description
pgBackRest aims to be a reliable, easy-to-use backup and restore solution
that can seamlessly scale up to the largest databases and workloads by
utilizing algorithms that are optimized for database-specific requirements.

%prep
%autosetup -p1 -n %{name}-release-%{version}

%build
ln -sv $(pg_config --libdir)/pkgconfig/* %{_libdir}/pkgconfig/

pushd src
%configure
%make_build
popd

%install
pushd src
%make_install %{?_smp_mflags}
popd

mkdir -p %{buildroot}%{_sysconfdir}/%{name} \
         %{buildroot}%{_var}/log/%{name}

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%dir %{_var}/log/%{name}
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/%{name}/%{name}.conf

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.54.2-3.1.1
- Adjusted to build for subrelease 90
* Thu Feb 12 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.54.2-3.1
- Bump release after moving to SPECS/91
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
