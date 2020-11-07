%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
Summary:        A library for retrieving information onrunning processes and system utilization
Name:           python3-psutil
Version:        5.7.3
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/psutil
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/psutil/psutil-%{version}.tar.gz
%define sha1    psutil=0b093faed351cf89e930d1c3ba380831b068ebc1
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%if 0
%if %{with_check}
BuildRequires:  ncurses-terminfo
BuildRequires:  coreutils
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-six
BuildRequires:  python3-test
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pbr
%endif
%endif
Requires:       python3
Requires:       python3-libs

%description
psutil (process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python. It is useful mainly for system monitoring, profiling and limiting process resources and management of running processes. It implements many functionalities offered by command line tools such as: ps, top, lsof, netstat, ifconfig, who, df, kill, free, nice, ionice, iostat, iotop, uptime, pidof, tty, taskset, pmap. It currently supports Linux, Windows, OSX, Sun Solaris, FreeBSD, OpenBSD and NetBSD, both 32-bit and 64-bit architectures, with Python versions from 2.6 to 3.6 (users of Python 2.4 and 2.5 may use 2.1.3 version). PyPy is also known to work.

%prep
%setup -q -n psutil-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%if 0
%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 linecache2
$easy_install_3 pytest
$easy_install_3 mock
$easy_install_3 unittest2
pushd ../p3dir
LANG=en_US.UTF-8 make test PYTHON=python%{python3_version}
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 5.7.3-1
-   Automatic Version Bump
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.7.2-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.7.2-1
-   Automatic Version Bump
*   Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 5.4.7-4
-   Mass removal python2
*   Mon Sep 09 2019 Tapas Kundu <tkundu@vmware.com> 5.4.7-3
-   Disabled make check as it requires certain drivers to be
-   installed in /sys/class/power_supply
*   Fri Jan 11 2019 Tapas Kundu <tkundu@vmware.com> 5.4.7-2
-   Fix makecheck
*   Wed Sep 12 2018 Tapas Kundu <tkundu@vmware.com> 5.4.7-1
-   Updated to version 5.4.7
*   Fri Aug 10 2017 Xiaolin Li <xiaolinl@vmware.com> 5.2.2-2
-   Fixed make check error.
*   Wed Apr 26 2017 Xialin Li <xiaolinl@vmware.com> 5.2.2-1
-   Initial packaging for Photon
