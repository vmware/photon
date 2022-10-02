Summary:        A library which allows userspace access to USB devices
Name:           libusb
Version:        1.0.23
Release:        2%{?dist}
License:        LGPLv2+
URL:            http://sourceforge.net/projects/libusb/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://downloads.sourceforge.net/libusb/libusb-%{version}.tar.bz2
%define sha512 %{name}=73430ad31dd405e76a9c6c55086961003989c44964e2735b5076f9ca849e3f6fe71d10a66b74b111f0c34a0d2cb744b9ca105863c552123fce4ec0bbdd2ec15b

BuildRequires:  systemd-devel

Requires:       systemd

%description
This package provides a way for applications to access USB devices.

%package        devel
Summary:        Development files for libusb
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains the header files, libraries and documentation needed to
develop applications that use libusb.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

%check
pushd tests
make %{?_smp_mflags} -k check
./stress
popd

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/libusb*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libusb*.so
%{_libdir}/pkgconfig/*

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.23-2
- Remove .la files
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.23-1
- Automatic Version Bump
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.0.22-1
- Update to version 1.0.22
* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com>  1.0.21-1
- Upgrading version to 1.0.21
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.0.20-4
- Change systemd dependency
* Tue Jul 12 2016 Xiaolin Li <xiaolinl@vmware.com>  1.0.20-3
- Build libusb single threaded.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.20-2
- GA - Bump release of all rpms
* Thu May 05 2016 Nick Shi <nshi@vmware.com> 1.0.20-1
- Initial version
