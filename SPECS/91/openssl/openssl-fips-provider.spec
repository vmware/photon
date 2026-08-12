%global build_if %{photon_subrelease} == 91

Summary:        FIPS Libraries for openssl
Name:           openssl-fips-provider
Version:        3.1.2
Release:        4%{?dist}
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.openssl.org/source/openssl-%{version}.tar.gz

Source1: provider_fips.cnf

Source2: provider_base.cnf

Source3: license.txt
%include %{SOURCE3}

Requires: bash
Requires: glibc
Requires: libgcc
Requires: openssl >= 3.0

%description
Fips library for enabling fips.

%prep
if grep -q "^Patch[0-9]*:" %{_specdir}/%{name}.spec; then
  echo "ERROR: Patches detected in the %{name} spec file" 1>&2
  exit 1
fi
%autosetup -n openssl-openssl-%{version}

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
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/ssl/$(basename %{SOURCE2})

%post
OPENSSL_CONF=/dev/null openssl fipsinstall -out %{_sysconfdir}/ssl/fipsmodule.cnf -module %{_libdir}/ossl-modules/fips.so

# Enable provider_fips, provider_base and enable provider_default
sed -i '/^#.include \/etc\/ssl\/provider_fips.cnf/s/^#//g' %{_sysconfdir}/ssl/distro.cnf
sed -i '/^#.include \/etc\/ssl\/provider_base.cnf/s/^#//g' %{_sysconfdir}/ssl/distro.cnf
sed -i '/^#.include \/etc\/ssl\/provider_default.cnf/s/^#//g' %{_sysconfdir}/ssl/distro.cnf

%postun
# complete uninstall, not an upgrade
if [ "$1" = 0 ]; then
  rm -f %{_sysconfdir}/ssl/fipsmodule.cnf
  sed -i '/^.include \/etc\/ssl\/provider_fips.cnf/s/^/#/g' %{_sysconfdir}/ssl/distro.cnf
  sed -i '/^.include \/etc\/ssl\/provider_base.cnf/s/^/#/g' %{_sysconfdir}/ssl/distro.cnf
  # Always enable provider_default
  sed -i '/^#.include \/etc\/ssl\/provider_default.cnf/s/^#//g' %{_sysconfdir}/ssl/distro.cnf
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/ossl-modules/fips.so
%{_sysconfdir}/ssl/provider_fips.cnf
%{_sysconfdir}/ssl/provider_base.cnf
%exclude %{_sysconfdir}/ssl/fipsmodule.cnf

%changelog
* Thu Jun 11 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 3.1.2-4
- Always enable default provider.
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.1.2-3
- Extended to build for subrelease 91 and above
* Wed Apr 08 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 3.1.2-2
- Release bump for openssl upgrade.
* Tue Jun 24 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.1.2-1
- Update OpenSSL Fips Provider to 3.1.2
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.0.8-7
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.8-6
- Release bump for SRP compliance
* Thu Sep 19 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.8-5
- Fix requires for latest fips
- Build fips.so from source
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0.8-4
- Move fips provider to spec of its own
