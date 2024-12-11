Summary:        Reliable PostgreSQL Backup & Restore
Name:           pgbackrest
Version:        2.48
Release:        3%{?dist}
Url:            https://pgbackrest.org
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pgbackrest/pgbackrest/archive/refs/tags/release/%{name}-%{version}.tar.gz
%define sha512 %{name}=63b3803adbeeea5362e42d9d437d6d5426261c42d725d044e6ee5ef460bcaf5101a511f7395c3c83858caab11e5cad5ffb43cfa7242a801abdfb3b8361c36362

Source1: %{name}.conf

Source2: license.txt
%include %{SOURCE2}

BuildRequires: openssl-devel
BuildRequires: libxml2-devel
BuildRequires: lz4-devel
BuildRequires: postgresql15-devel
BuildRequires: cmake
BuildRequires: libyaml-devel

Requires: openssl
Requires: xz-libs
Requires: zstd-libs
Requires: bzip2-libs
Requires: lz4
Requires: libxml2
Requires: (postgresql15-libs or postgresql14-libs or postgresql13-libs)

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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.48-3
- Release bump for SRP compliance
* Thu Dec 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.48-2
- Build with pgsql15, this was a mishap during cherry picking
* Thu Nov 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.48-1
- Initial version.
