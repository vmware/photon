Summary:        FIPS Libraries for openssl
Name:           openssl-fips-provider
Version:        3.0.8
Release:        5%{?dist}
License:        OpenSSL
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.openssl.org/source/openssl-%{version}.tar.gz
%define sha512 openssl=8ce10be000d7d4092c8efc5b96b1d2f7da04c1c3a624d3a7923899c6b1de06f369016be957e36e8ab6d4c9102eaeec5d1973295d547f7893a7f11f132ae42b0d

Source1: provider_fips.cnf

Requires: bash
Requires: glibc
Requires: libgcc
Requires: openssl >= %{version}

%description
Fips library for enabling fips.

%prep
if grep -q "^Patch[0-9]*:" %{_specdir}/%{name}.spec; then
  echo "ERROR: Patches detected in the %{name} spec file" 1>&2
  exit 1
fi
%autosetup -n openssl-%{version}

%build
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

%install
make install_fips DESTDIR=%{buildroot} %{?_smp_mflags}

install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/ssl/$(basename %{SOURCE1})

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
%exclude %{_sysconfdir}/ssl/fipsmodule.cnf

%changelog
* Thu Sep 19 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.8-5
- Fix requires for latest fips
- Build fips.so from source
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.8-4
- Move fips provider to spec of its own
