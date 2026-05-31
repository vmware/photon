%global build_if %{photon_subrelease} >= 91

Summary:        Command line utility for i-node notifications and management.
Name:           inotify-tools
Version:        4.25.9.0
Release:        2%{?dist}
URL:            https://github.com/inotify-tools/inotify-tools
Group:          Applications/Systems
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/inotify-tools/inotify-tools/archive/refs/tags/4.25.9.0.tar.gz#/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Requires:%{name}-libs = %{version}-%{release}

%description
inotify-tools is a library and a set of command-line programs providing a
simple interface to inotify.

%package devel
Summary: Header files and libraries for building application using libinotify-tools.
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package libs
Summary: %{name} libraries
Conflicts: %{name} < 4.25.9.0-2

%description libs
%{summary}

%package doc
Summary: Documentation for %{name}
Conflicts: %{name} < 4.25.9.0-2

%description doc
%{summary}

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
%make_build check
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*

%files libs
%defattr(-,root,root)
%{_libdir}/libinotifytools.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libinotifytools.so

%files doc
%defattr(-,root,root)
%{_mandir}/*

%changelog
* Sun May 31 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.25.9.0-2
- Split package to libs and doc
- Disable building static library
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
