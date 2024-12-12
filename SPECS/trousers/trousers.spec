Summary:        TCG Software Stack (TSS)
Name:           trousers
Version:        0.3.15
Release:        5%{?dist}
URL:            https://sourceforge.net/projects/trousers
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://sourceforge.net/projects/trousers/files/trousers/0.3.15/%{name}-%{version}.tar.gz
%define sha512  %{name}=769c7d891c6306c1b3252448f86e3043ee837e566c9431f5b4353512113e2907f6ce29c91e8044c420025b79c5f3ff2396ddce93f73b1eb2a15ea1de89ac0fdb
Source1:        %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}
BuildRequires:  systemd-devel
Requires:       systemd-rpm-macros
Requires:       libtspi = %{version}-%{release}

%description
Trousers is an open-source TCG Software Stack (TSS), released under
the BSD License. Trousers aims to be compliant with the
1.1b and 1.2 TSS specifications available from the Trusted Computing

%package        devel
Summary:        The libraries and header files needed for TSS development.
Requires:       libtspi = %{version}-%{release}

%description    devel
The libraries and header files needed for TSS development.

%package -n     libtspi
Summary:        TSPI library

%description -n libtspi
TSPI library

%prep
%autosetup -p1

%build
sh bootstrap.sh
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%post
%sysusers_create_compat %{SOURCE1}
mkdir -p %{_sharedstatedir}/tpm
chown -R tss:tss %{_sharedstatedir}/tpm

%post -n libtspi -p /sbin/ldconfig
%postun -n libtspi -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
%{_mandir}/man5
%{_mandir}/man8
%{_sysusersdir}/%{name}.sysusers
%exclude %dir /var

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libtspi.so
%{_libdir}/libtspi.so.1
%{_mandir}/man3

%files -n libtspi
%defattr(-,root,root)
%{_libdir}/libtspi.so.1.2.0
%exclude %dir %{_libdir}/debug
%exclude %{_libdir}/libtddl.a

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 0.3.15-5
- Release bump for SRP compliance
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 0.3.15-4
- Use systemd-rpm-macros for user creation
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.3.15-3
- Remove .la files
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.3.15-2
- Fix binary path
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 0.3.15-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.3.14-5
- Bump up release for openssl
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 0.3.14-4
- GCC-10 support.
* Wed Aug 19 2020 Shreyas B <shreyasb@vmware.com> 0.3.14-3
- Fix for CVE-2020-24330, CVE-2020-24331 & CVE-2020-24332
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.3.14-2
- Use standard configure macros
* Thu Mar 2 2017 Alexey Makhalov <amakhalov@vmware.com> 0.3.14-1
- Initial build. First version
