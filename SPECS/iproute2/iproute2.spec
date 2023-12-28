Summary:        Basic and advanced IPV4-based networking
Name:           iproute2
Version:        4.19.0
Release:        2%{?dist}
License:        GPLv2+
URL:            https://wiki.linuxfoundation.org/networking/iproute2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.kernel.org/pub/linux/utils/net/iproute2/%{name}-%{version}.tar.xz
%define sha512 %{name}=47c750da2247705b1b1d1621f58987333e54370d0fff2f24106194022de793ff35dfd67fd1be127ce019008705702092d31dac49abf930a7c0dc5c7e7c0665b8

Patch0: replace_killall_by_pkill.patch
Patch1: CVE-2019-20795.patch

# Add Support for HCX patches
Patch2: 0001-add-hcx-helper-modules.patch
Patch3: 0002-iptrunk.patch
Patch4: 0003-mss-clamp.patch
Patch5: 0004-sinkport.patch

BuildRequires: bison
BuildRequires: libmnl-devel

Requires: elfutils-libelf
Requires: glibc
Requires: libmnl

Provides: iproute

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
%make_build

%install
export SBINDIR=%{_sbindir}

%make_install %{?_smp_mflags}

rm -rvf %{buildroot}%{_docdir}/%{name}

%if 0%{?with_check}
%check
# tests need to be run on an actual host,
# because of kernel module dependency
#make check %%{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}/*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/%{name}/*
%{_sbindir}/*
%{_libdir}/tc/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_datadir}/bash-completion/completions/*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/bpf_elf.h
%{_mandir}/man3/*

%changelog
* Thu Dec 28 2023 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.19.0-2
- Fix mss-clamp value setting issue
* Mon Oct 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.19.0-1
- Upgrade to v4.19.0
* Wed Feb 16 2022 Sharan Turlapati <sturlapati@vmware.com> 4.18.0-4
- Add support for HCX patches
* Wed May 13 2020 Vikash Bansal <bvikas@vmware.com> 4.18.0-3
- Fix for CVE-2019-20795
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
