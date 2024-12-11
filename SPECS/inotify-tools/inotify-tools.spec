Summary:        Command line utility for i-node notifications and management.
Name:           inotify-tools
Version:        3.13
Release:        4%{?dist}
URL:            http://sourceforge.net/projects/inotify-tools
Group:          Applications/Systems
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://sourceforge.net/projects/inotify-tools/files/latest/download/%{name}-%{version}.tar.gz
%define sha512  %{name}=e757ca5d3bac2b6b84e9435671107d6d695ff7d04cefd139590ab538d1be8f9a295eb9b0042406bdbfa60bb2b2545a428ec861e60f1cbf172050d47d0350bdb9

Source1: license.txt
%include %{SOURCE1}

Provides:       libinotifytools0

%description
inotify-tools is simple command line interface program for linux distributions
which is used to monitor inode specific filesystem events.

%package devel
Summary: Header files and libraries for building application using libinotify-tools.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%makeinstall %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}
%{_datadir}
%{_libdir}/libinotifytools.so.0.4.1

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}/libinotifytools.a
%{_libdir}/libinotifytools.so
%{_libdir}/libinotifytools.so.0
%exclude %{_libdir}/libinotifytools.la

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.13-4
- Release bump for SRP compliance
* Wed Jun 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.13-3
- Spec improvements
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.13-2
- GA - Bump release of all rpms
* Mon Dec 14 2015 Kumar Kaushik <kaushikk@vmware.com> 3.13-1
- Initial build.  First version
