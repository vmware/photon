%define debug_package %{nil}
Summary:        PyInstaller bundles a Python application and all its dependencies into a single package.
Name:           python3-pyinstaller
Version:        6.10.0
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/PyInstaller
License:        GPLv2+
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/P/PyInstaller/pyinstaller-%{version}.tar.gz
%define sha512  pyinstaller=3d7338c31b40468cece26eb294db046339bda09c1f195048503b386ab9da8d71546bcc50dd95b865403921007220b1e35f0ba4ccab6e96b9d9d40cebca028c47
Patch0:         pyinstaller-gcc-10.patch
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  zlib-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python3
Requires:       python3-libs
Requires:       zlib
Requires:       python3-setuptools
Requires:       python3-xml
Requires:       python3-pyinstaller-hooks-contrib >= 2024.8
Requires:       python3-altgraph
Requires:       python3-packaging >= 22.0

%description
PyInstaller bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules.
PyInstaller reads a Python script written by you. It analyzes your code to discover every other module and library your script needs in order to execute.
Then it collects copies of all those files – including the active Python interpreter! – and puts them with your script in a single folder, or optionally in a single executable file.
PyInstaller is tested against Windows, Mac OS X, and Linux. However, it is not a cross-compiler: to make a Windows app you run PyInstaller in Windows;
to make a Linux app you run it in Linux, etc. PyInstaller has been used successfully with AIX, Solaris, and FreeBSD, but is not tested against them.

%prep
%autosetup -p1 -n pyinstaller-%{version}

%build
pushd bootloader
python3 ./waf distclean all
popd
pip3 install wheel
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}

%check
# Skip python3 make check, as python3.6 is not supported by 3.2.1

%files
%defattr(-,root,root)
%{_bindir}/pyi-archive_viewer
%{_bindir}/pyi-bindepend
%{_bindir}/pyi-grab_version
%{_bindir}/pyi-makespec
%{_bindir}/pyi-set_version
%{_bindir}/pyinstaller
%{python3_sitelib}/*
%exclude %{python3_sitelib}/PyInstaller/bootloader/Darwin-64bit
%exclude %{python3_sitelib}/PyInstaller/bootloader/Linux-32bit
%ifarch aarch64
%exclude %{python3_sitelib}/PyInstaller/bootloader/Linux-64bit
%endif
%exclude %{python3_sitelib}/PyInstaller/bootloader/Windows-32bit
%exclude %{python3_sitelib}/PyInstaller/bootloader/Windows-64bit

%changelog
*   Tue Sep 30 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.10.0-2
-   Include dependent package version constraints
*   Tue Sep 23 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.10.0-1
-   Upgrade to fix CVE-2025-59042
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 4.7-1
-   Update to version 4.7 to compile with python 3.10
*   Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 4.0-4
-   GCC-10 support.
*   Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 4.0-3
-   Added Requires pyinstaller-hooks-contrib and altgraph
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.0-2
-   openssl 1.1.1
*   Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.6-1
-   Automatic Version Bump
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.4-4
-   Mass removal python2
*   Wed Apr 01 2020 Alexey Makhalov <amakhalov@vmware.com> 3.4-3
-   Fix compilation issue with gcc-8.4.0
*   Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 3.4-2
-   Fix makecheck.
*   Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 3.4-1
-   Updated to release 3.4
*   Tue Jan 02 2018 Alexey Makhalov <amakhalov@vmware.com> 3.3.1-1
-   Version update. Build bootloader from sources
*   Mon Sep 25 2017 Bo Gan <ganb@vmware.com> 3.2.1-2
-   Fix make check issues.
*   Tue Feb 14 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.1-1
-   Initial packaging for Photon
