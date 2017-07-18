%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A library for retrieving information onrunning processes and system utilization
Name:           python-psutil
Version:        5.2.2
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/psutil
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/psutil/psutil-%{version}.tar.gz
%define sha1    psutil=e22e2f6abdff051d438626f9a59a8782ace1a63e

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

%description
psutil (process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python. It is useful mainly for system monitoring, profiling and limiting process resources and management of running processes. It implements many functionalities offered by command line tools such as: ps, top, lsof, netstat, ifconfig, who, df, kill, free, nice, ionice, iostat, iotop, uptime, pidof, tty, taskset, pmap. It currently supports Linux, Windows, OSX, Sun Solaris, FreeBSD, OpenBSD and NetBSD, both 32-bit and 64-bit architectures, with Python versions from 2.6 to 3.6 (users of Python 2.4 and 2.5 may use 2.1.3 version). PyPy is also known to work.

%package -n     python3-psutil
Summary:        python-psutil
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs

%description -n python3-psutil
Python 3 version.

%prep
%setup -q -n psutil-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
export TRAVIS=1
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 ipaddress mock unittest2
make test-system test-misc test-posix test-memleaks
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 ipaddress mock unittest2
make test-system test-misc test-posix test-memleaks
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-psutil
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Jul 18 2017 Chang Lee <changlee@vmware.com> 5.2.2-2
-   Updated %check with removing test-process and test-platform
*   Wed Apr 26 2017 Xialin Li <xiaolinl@vmware.com> 5.2.2-1
-   Initial packaging for Photon
