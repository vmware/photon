%define debug_package %{nil}
Summary:        PyInstaller bundles a Python application and all its dependencies into a single package.
Name:           python3-pyinstaller
Version:        5.5
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/PyInstaller
License:        GPLv2+
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/1e/d7/214b25c912d5f7d9c31d266821a8be6a35df80535056fe83997688721927/pyinstaller-%{version}.tar.gz
%define sha512  pyinstaller=aaff7fe272d70b597691d398344289333b11343f9ef37cd797a264310db140e8ec391c8aef7a0661f18487222fb945a5f797f31e21c932585277335f5c30ace6
BuildRequires:  cmocka-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-xml
BuildRequires:  zlib-devel
%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python3
Requires:       python3-libs
Requires:       zlib
Requires:       python3-setuptools
Requires:       python3-xml
Requires:       python3-pyinstaller-hooks-contrib
Requires:       python3-altgraph

%description
PyInstaller bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules.
PyInstaller reads a Python script written by you. It analyzes your code to discover every other module and library your script needs in order to execute.
Then it collects copies of all those files – including the active Python interpreter! – and puts them with your script in a single folder, or optionally in a single executable file.
PyInstaller is tested against Windows, Mac OS X, and Linux. However, it is not a cross-compiler: to make a Windows app you run PyInstaller in Windows;
to make a Linux app you run it in Linux, etc. PyInstaller has been used successfully with AIX, Solaris, and FreeBSD, but is not tested against them.

%prep
%autosetup -n pyinstaller-%{version}

%build
pushd bootloader
python3 ./waf distclean all
popd
%py3_build

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
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.5-3
- Bump version as a part of openssl upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.5-2
- Bump version as a part of zlib upgrade
* Wed Nov 30 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.5-1
- Update to 5.5
* Tue Nov 29 2022 Ankit Jain <ankitja@vmware.com> 4.0-5
- Release Bump-up to build with updated pyOpenSSL version
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 4.0-4
- GCC-10 support.
* Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 4.0-3
- Added Requires pyinstaller-hooks-contrib and altgraph
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.0-2
- openssl 1.1.1
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.6-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.4-4
- Mass removal python2
* Wed Apr 01 2020 Alexey Makhalov <amakhalov@vmware.com> 3.4-3
- Fix compilation issue with gcc-8.4.0
* Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 3.4-2
- Fix makecheck.
* Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 3.4-1
- Updated to release 3.4
* Tue Jan 02 2018 Alexey Makhalov <amakhalov@vmware.com> 3.3.1-1
- Version update. Build bootloader from sources
* Mon Sep 25 2017 Bo Gan <ganb@vmware.com> 3.2.1-2
- Fix make check issues.
* Tue Feb 14 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.1-1
- Initial packaging for Photon
