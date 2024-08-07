# if you are building latest fips, it will be same as openssl version
# if unsure, keep it 0
%define with_latest_fips        1
%define fips_provider_version   3.0.8
%define fips_provider_srcname   fips-provider-%{fips_provider_version}
%define debug_package           %{nil}

Summary:        FIPS Libraries for openssl
Name:           openssl-fips-provider
Version:        3.3.0
Release:        3%{?dist}
License:        OpenSSL
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

%if 0%{?with_latest_fips}
Source0: http://www.openssl.org/source/openssl-%{version}.tar.gz
%define sha512 openssl=1f9daeee6542e1b831c65f1f87befaef98ccedc3abc958c9d17f064ef771924c30849e3ff880f94eed4aaa9d81ea105e3bc8815e6d2e4d6b60b5e890f14fc5da
%endif

%if "0%{?with_latest_fips}" == "00"
Source0: %{fips_provider_srcname}.tar.xz
%define sha512 %{fips_provider_srcname}=3206c96f77ba5ab0553249e13ddf52145995909e68a9acb851c5db6be759e6f7647b9ad960f6da7c989c20b49fbd9e79a7305f2000f24281345c56a1a8b1148f
%endif

Source1: provider_fips.cnf

Requires: bash
Requires: glibc
Requires: libgcc

%if "0%{?with_latest_fips}" == "00"
Requires: openssl >= %{fips_provider_version}
%endif

%if 0%{?with_latest_fips}
Requires: openssl = %{version}-%{release}
%endif

%description
Fips library for enabling fips.

%prep
%if "0%{?with_latest_fips}" == "00"
%autosetup -p1 -n %{fips_provider_srcname}
%endif

%if 0%{?with_latest_fips}
%autosetup -p1 -n openssl-%{version}
%endif

%build
%if 0%{?with_latest_fips}
if [ %{_host} != %{_build} ]; then
#  export CROSS_COMPILE=%{_host}-
  export CC=%{_host}-gcc
  export AR=%{_host}-ar
  export AS=%{_host}-as
  export LD=%{_host}-ld
fi

export CFLAGS="%{optflags}"
export MACHINE=%{_arch}
./config \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --openssldir=%{_sysconfdir}/ssl \
  --api=1.1.1 \
  --shared \
  --with-rand-seed=os,egd \
  enable-egd \
  enable-fips \
  -Wl,-z,noexecstack

%make_build
%endif

%install
%if 0%{?with_latest_fips}
make install_fips DESTDIR=%{buildroot} %{?_smp_mflags}
%endif

install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/ssl/$(basename %{SOURCE1})

%if "0%{?with_latest_fips}" == "00"
install -p -m 644 -D %{_arch}/fips.so %{buildroot}%{_libdir}/ossl-modules/fips.so
%endif

%post
if [ "$1" = 2 ]; then
  # fips.so was just updated. Temporarily disable fips mode to regenerate new fipsmodule.cnf
  sed -i '/^.include \/etc\/ssl\/provider_fips.cnf/s/^/#/g' %{_sysconfdir}/ssl/distro.cnf
fi
openssl fipsinstall -out %{_sysconfdir}/ssl/fipsmodule.cnf -module %{_libdir}/ossl-modules/fips.so
sed -i '/^#.include \/etc\/ssl\/provider_fips.cnf/s/^#//g' %{_sysconfdir}/ssl/distro.cnf

%postun
# complete uninstall, not an upgrade
if [ "$1" = 0 ]; then
  rm -f %{_sysconfdir}/ssl/fipsmodule.cnf
  sed -i '/^.include \/etc\/ssl\/provider_fips.cnf/s/^/#/g' %{_sysconfdir}/ssl/distro.cnf
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/ossl-modules/fips.so
%{_sysconfdir}/ssl/provider_fips.cnf

%if 0%{?with_latest_fips}
%exclude %{_sysconfdir}/ssl/fipsmodule.cnf
%endif

%changelog
* Thu Jul 25 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.3.0-3
- Move fips provider to spec of its own
