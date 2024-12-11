Summary:    Linux Key Management Utilities
Name:       keyutils
Version:    1.6.1
Release:    3%{?dist}
URL:        http://people.redhat.com/~dhowells/keyutils
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://people.redhat.com/~dhowells/keyutils/keyutils-%{version}.tar.bz2
%define sha512  %{name}=ea6e20b2594234c7f51581eef2b8fd19c109fa9eacaaef8dfbb4f237bd1d6fdf071ec23b4ff334cb22a46461d09d17cf499987fd1f00e66f27506888876961e1

Source1: license.txt
%include %{SOURCE1}

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to user space to get a key
instantiated.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%make_build

%install
make install DESTDIR=%{buildroot} \
             LIBDIR=%{_lib} \
             USRLIBDIR=%{_libdir} \
             BINDIR=%{_bindir} \
             SBINDIR=%{_sbindir} %{?_smp_mflags}

find %{buildroot} -name '*.a' -delete

%clean
rm -rf %{buildroot}

%if 0%{?with_check}
%check
make -k check %{?_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README LICENCE.GPL
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/keyutils
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/request-key.conf
%dir %{_sysconfdir}/request-key.d/

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.6.1-3
- Release bump for SRP compliance
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.1-2
- Fix binary path
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
- Automatic Version Bump
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 1.5.10-1
- Updated to version 1.5.10
* Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.5.9-1
- Initial build. First version
