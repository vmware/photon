%global build_if %{photon_subrelease} >= 91

Summary:        Command line utility for i-node notifications and management.
Name:           inotify-tools
Version:        4.25.9.0
Release:        1%{?dist}
URL:            https://github.com/inotify-tools/inotify-tools
Group:          Applications/Systems
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/inotify-tools/inotify-tools/archive/refs/tags/4.25.9.0.tar.gz#/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
inotify-tools is a library and a set of command-line programs providing a
simple interface to inotify.

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
sh ./autogen.sh
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
* Fri May 29 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 4.25.9.0-1
- New repo, newer version
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.13-4
- Release bump for SRP compliance
* Wed Jun 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.13-3
- Spec improvements
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.13-2
- GA - Bump release of all rpms
* Mon Dec 14 2015 Kumar Kaushik <kaushikk@vmware.com> 3.13-1
- Initial build.  First version
