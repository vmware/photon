Summary:       OS Login Guest Environment for Google Compute Engine
Name:          google-guest-oslogin
Version:       20250123.00
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
URL:           https://github.com/GoogleCloudPlatform/guest-oslogin
Distribution:  Photon

Source0:       https://github.com/GoogleCloudPlatform/guest-oslogin/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=cbdc553d6847b61b61c93cb1335fc23d932385ff787a5b2321afb033635bfbee5a37962791cd09f8ccb40f2366a44f03a0d1733609b381e079b528caa6305f89

Source1: license.txt
%include %{SOURCE1}

BuildRequires: Linux-PAM-devel
BuildRequires: curl-devel
BuildRequires: json-c-devel
BuildRequires: gtest-devel
BuildRequires: systemd-rpm-macros

Requires:      curl
Requires:      json-c
Requires:      systemd

Patch0: fix_systemd_prefix_path.patch

%description
This repository contains the system components responsible for providing Google Cloud OS Login features on Google Compute Engine instances.

%package test
Requires:   %{name} = %{version}-%{release}
Summary:    Test binary for %{name}.

%description test
%{summary}

%prep
%autosetup -n guest-oslogin-%{version} -p1

%build
%make_build

GTEST_DIR=/usr/src/gtest \
  %make_build -C test test_runner

%install
%make_install %{?_smp_mflags}

install -vDm 755 test/test_runner \
  %{buildroot}%{_libexecdir}/%{name}/test_runner

%post
/sbin/ldconfig
%systemd_post google-oslogin-cache.service google-oslogin-cache.timer

%preun
%systemd_preun google-oslogin-cache.service google-oslogin-cache.timer

%postun
/sbin/ldconfig
%systemd_postun_with_restart google-oslogin-cache.service google-oslogin-cache.timer

%files
%defattr(-,root,root)
%{_presetdir}/90-google-compute-engine-oslogin.preset
%{_unitdir}/google-oslogin-cache.service
%{_unitdir}/google-oslogin-cache.timer
%{_bindir}/google_authorized_keys
%{_bindir}/google_authorized_keys_sk
%{_bindir}/google_authorized_principals
%{_bindir}/google_oslogin_nss_cache
%{_libdir}/libnss_cache_oslogin-.so
%{_libdir}/libnss_cache_oslogin.so.2
%{_libdir}/libnss_oslogin-.so
%{_libdir}/libnss_oslogin.so.2
%{_libdir}/security/pam_oslogin_admin.so
%{_libdir}/security/pam_oslogin_login.so
%{_mandir}/man8/libnss_cache_oslogin.so.2.8.gz
%{_mandir}/man8/libnss_oslogin.so.2.8.gz
%{_mandir}/man8/nss-cache-oslogin.8.gz
%{_mandir}/man8/nss-oslogin.8.gz

%files test
%defattr(-,root,root)
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/test_runner

%changelog
* Wed Mar 05 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20250123.00-2
- Introduce test subpackage
* Mon Feb 03 2025 Tapas Kundu <tapas.kundu@broadcom.com> 20250123.00-1
- Initial version
