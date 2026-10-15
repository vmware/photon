%global build_if %{photon_subrelease} >= 92

Summary:        A library for retrieving information onrunning processes and system utilization
Name:           python3-psutil
Version:        7.2.2
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/psutil
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0: https://github.com/giampaolo/psutil/archive/refs/tags/v%{version}.tar.gz#/psutil-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging

%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-requests
%endif

Requires:       python3

%description
psutil (process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python. It is useful mainly for system monitoring, profiling and limiting process resources and management of running processes. It implements many functionalities offered by command line tools such as: ps, top, lsof, netstat, ifconfig, who, df, kill, free, nice, ionice, iostat, iotop, uptime, pidof, tty, taskset, pmap. It currently supports Linux, Windows, OSX, Sun Solaris, FreeBSD, OpenBSD and NetBSD, both 32-bit and 64-bit architectures, with Python versions from 2.6 to 3.6 (users of Python 2.4 and 2.5 may use 2.1.3 version). PyPy is also known to work.

%prep
%autosetup -n psutil-%{version} -p1

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
PYTHONSAFEPATH=1 make test CI_TESTING=1 PYTHON=%{__python3} PYTHONPATH=%{buildroot}/%{python3_sitelib} ARGS='-o addopts= --import-mode=append' %{?_smp_mflags}
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Oct 15 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.2.2-1
- Upgrade to 7.2.2
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.9.1-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.9.1-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.9.1-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 5.9.1-1
- Automatic Version Bump
* Tue Oct 19 2021 Tapas Kundu <tkundu@vmware.com> 5.7.3-2
- Requires setuptools for building.
- Fixed makecheck
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 5.7.3-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.7.2-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.7.2-1
- Automatic Version Bump
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 5.4.7-4
- Mass removal python2
* Mon Sep 09 2019 Tapas Kundu <tkundu@vmware.com> 5.4.7-3
- Disabled make check as it requires certain drivers to be
- installed in /sys/class/power_supply
* Fri Jan 11 2019 Tapas Kundu <tkundu@vmware.com> 5.4.7-2
- Fix makecheck
* Wed Sep 12 2018 Tapas Kundu <tkundu@vmware.com> 5.4.7-1
- Updated to version 5.4.7
* Thu Aug 10 2017 Xiaolin Li <xiaolinl@vmware.com> 5.2.2-2
- Fixed make check error.
* Wed Apr 26 2017 Xialin Li <xiaolinl@vmware.com> 5.2.2-1
- Initial packaging for Photon
