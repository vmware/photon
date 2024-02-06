Summary:        DBus for systemd
Name:           dbus
Version:        1.13.8
Release:        4%{?dist}
License:        GPLv2+ or AFL
URL:            http://www.freedesktop.org/wiki/Software/dbus
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.xz
%define sha512 dbus=8301fa716ade578bd8df2e5f7179a8f09c33e58cc57f36dd76e767bef4dceccfb20f266e20afbea687c88d2b26c1e1d52c8510d2e028008b8277e8ce21dae366

Patch0:         CVE-2019-12749.patch
# Fix for CVE-2022-42010
Patch1:         0001-dbus-marshal-validate_Check_brackets_in_signature_nest.patch
# Fix for CVE-2022-42011
Patch2:         0001-dbus-marshal-validate_Validate_length_of_arrays_of.patch
# Fix for CVE-2022-42012
Patch3:         0001-dbus-marshal-byteswap_Byte-swap_Unix_fd_indexes_if_needed.patch
Patch4:         CVE-2020-12049.patch
Patch5:         CVE-2023-34969.patch

BuildRequires:  expat-devel
BuildRequires:  systemd-devel
BuildRequires:  xz-devel

Requires:       expat
Requires:       systemd
Requires:       xz

%description
The dbus package contains dbus.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
Requires:       expat-devel
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure                                   \
    --docdir=%{_datadir}/doc/dbus-1.11.12    \
    --enable-libaudit=no --enable-selinux=no \
    --with-console-auth-dir=/run/console

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -vdm755 %{buildroot}%{_lib}
#ln -sfv ../../lib/$(readlink %{buildroot}%{_libdir}/libdbus-1.so) %{buildroot}%{_libdir}/libdbus-1.so
#rm -f %{buildroot}%{_sharedstatedir}/dbus/machine-id
#ln -sv %{buildroot}%{_sysconfdir}/machine-id %{buildroot}%{_sharedstatedir}/dbus

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_sysconfdir}/dbus-1
%{_bindir}/*
%{_libdir}/libdbus-1.so.*
%{_libdir}/tmpfiles.d/dbus.conf
%exclude %{_libdir}/sysusers.d
/lib/*
%{_libexecdir}/*
%{_docdir}/*
%{_datadir}/dbus-1

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/xml/dbus-1
%{_libdir}/cmake/DBus1
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Tue Feb 06 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.13.8-4
- Fix CVE-2020-12049
* Thu Oct 13 2022 Ajay Kaher <akaher@vmware.com> 1.13.8-3
- Fix CVE-2022-42010, CVE-2022-42011, CVE-2022-42012
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.13.8-2
- Remove .la files
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 1.13.8-1
- Automatic Version Bump
* Fri Oct 18 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.13.6-2
- Fix CVE-2019-12749
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 1.13.6-1
- Update to 1.13.6
* Fri Apr 21 2017 Bo Gan <ganb@vmware.com> 1.11.12-1
- Update to 1.11.12
* Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.8-8
- Move all header files to devel subpackage.
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.8.8-7
- Change systemd dependency
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.8.8-6
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.8-5
- GA - Bump release of all rpms
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.8-4
- Created devel sub-package
* Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 1.8.8-3
- Remove debug files.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.8.8-2
- Update according to UsrMove.
* Sun Apr 06 2014 Sharath George <sharathg@vmware.com> 1.8.8
- Initial build. First version
