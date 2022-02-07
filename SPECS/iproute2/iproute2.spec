Summary:        Basic and advanced IPV4-based networking
Name:           iproute2
Version:        5.12.0
Release:        3%{?dist}
License:        GPLv2+
URL:            http://www.kernel.org/pub/linux/utils/net/iproute2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.kernel.org/pub/linux/utils/net/iproute2/%{name}-%{version}.tar.xz
%define sha512  %{name}=9249beb67b30ceef178b60b2b61a5e6c45277e747ae4c865e739b7ab84192549e8e94ebaee43c0a87c0291037746ffb6936346245220786e369201ee13d60fac

Patch0:         replace_killall_by_pkill.patch

Provides:       iproute

%description
The IPRoute2 package contains programs for basic and advanced
IPV4-based networking.

%package devel
Summary: Header files for building application using iproute2.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -p1
sed -i /ARPD/d Makefile
sed -i 's/arpd.8//' man/man8/Makefile
sed -i 's/m_ipt.o//' tc/Makefile

%build
%configure
%make_build %{?_smp_mflags}

%install
export SBINDIR='%{_sbindir}'
export LIBDIR='%{_libdir}'
%make_install %{?_smp_mflags}

%check
%if 0%{?with_check}
cd testsuite
# Fix linking issue in testsuite
sed -i 's/<libnetlink.h>/\"..\/..\/include\/libnetlink.h\"/g' tools/generate_nlmsg.c
sed -i 's/\"libnetlink.h\"/"..\/include\/libnetlink.h\"/g' ../lib/libnetlink.c
cd tools
make %{?_smp_mflags}
cd ..
make %{?_smp_mflags}
make alltests %{?_smp_mflags}
cd ..
%endif

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_sysconfdir}/%{name}/*
%{_sbindir}/*
%{_libdir}/tc/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_datadir}/bash-completion/completions/tc
%{_datadir}/bash-completion/completions/devlink

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/bpf_elf.h
%{_mandir}/man3/*

%changelog
* Sat Feb 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.12.0-3
- Drop libdb support
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 5.12.0-2
- Use autosetup and ldconfig scriptlets
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 5.12.0-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 5.11.0-1
- Automatic Version Bump
* Sat Jan 23 2021 Susant Sahani <ssahani@vmware.com> 5.10.0-1
- Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 5.8.0-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 5.5.0-1
- Automatic Version Bump
* Wed Jul 03 2019 Alexey Makhalov <amakhalov@vmware.com> 4.18.0-3
- Cross compilation support
* Fri Mar 08 2019 Fabio Rapposelli <fabio@vmware.com> 4.18.0-2
- Added "Provides: iproute" for better compatibility with other distributions
* Wed Sep 05 2018 Ankit Jain <ankitja@vmware.com> 4.18.0-1
- Updated to version 4.18.0
* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 4.10.0-3
- Fix compilation issue for glibc-2.26
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 4.10.0-2
- Move man3 to devel package.
* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.10.0-1
- Updated to version 4.10.0
* Thu Jun 16 2016 Nick Shi <nshi@vmware.com> 4.2.0-3
- Replace killall by pkill in ifcfg
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.0-2
- GA - Bump release of all rpms
* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 4.2.0-1
- Updated to version 4.2.0
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.12.0-1
- Initial build. First version
