Name:       xxhash
Version:    0.8.1
Release:    3%{?dist}
Summary:    Extremely fast hash algorithm
URL:        http://www.xxhash.com
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://github.com/Cyan4973/xxHash/archive/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  make
BuildRequires:  gcc

Requires:   %{name}-libs = %{version}-%{release}

%description
xxHash is an Extremely fast Hash algorithm, running at RAM speed
limits. It successfully completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash
functions. Code is highly portable, and hashes are identical on all
platforms (little / big endian).

%package libs
Summary:    Extremely fast hash algorithm - library

%description libs
xxHash is an Extremely fast Hash algorithm, running at RAM speed
limits. It successfully completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash
functions. Code is highly portable, and hashes are identical on all
platforms (little / big endian).

%package devel
Summary:    Extremely fast hash algorithm - development files
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for the xxhash library

%prep
%autosetup -p1 -n xxHash-%{version}

%build
%make_build

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
make test-xxhsum-c %{?_smp_mflags}
%endif

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/xxh*sum
%{_mandir}/man1/xxh*sum.1*
%license cli/COPYING
%doc cli/README.md

%files libs
%defattr(-,root,root)
%{_libdir}/libxxhash.so.*
%license LICENSE
%doc README.md

%files devel
%defattr(-,root,root)
%{_includedir}/xxhash.h
%{_includedir}/xxh3.h
%{_libdir}/libxxhash.so
%{_libdir}/libxxhash.a
%{_libdir}/pkgconfig/libxxhash.pc

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 0.8.1-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.8.1-2
- Release bump for SRP compliance
* Wed Aug 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.8.1-1
- Initial version. Needed for rsync
