%define debug_package %{nil}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        PyInstaller bundles a Python application and all its dependencies into a single package.
Name:           python-pyinstaller
Version:        3.4
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/PyInstaller
License:        GPLv2+
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/P/PyInstaller/PyInstaller-%{version}.tar.gz
%define sha1    PyInstaller=218c99be6886c6fddfb10f9892b19df906821652
Patch0:         make-check-fix-pyinstaller.patch
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  zlib-devel
%if %{with_check}
BuildRequires:  python-six
BuildRequires:  python-pytest
BuildRequires:  python-psutil
BuildRequires:  python-pip
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python-atomicwrites
BuildRequires:  python-attrs
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
Requires:       python-xml

%description
PyInstaller bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules.
PyInstaller reads a Python script written by you. It analyzes your code to discover every other module and library your script needs in order to execute. Then it collects copies of all those files – including the active Python interpreter! – and puts them with your script in a single folder, or optionally in a single executable file.

PyInstaller is tested against Windows, Mac OS X, and Linux. However, it is not a cross-compiler: to make a Windows app you run PyInstaller in Windows; to make a Linux app you run it in Linux, etc. PyInstaller has been used successfully with AIX, Solaris, and FreeBSD, but is not tested against them.
%package -n     python3-pyinstaller
Summary:        Python 3 version
Requires:       python3
Requires:       python3-libs
Requires:       zlib
Requires:       python3-setuptools
Requires:       python3-xml

%description -n python3-pyinstaller
Python 3 version.

%prep
%setup -q -n PyInstaller-%{version}
%patch0 -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
pushd bootloader
python ./waf distclean all
popd

python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
mv %{buildroot}/%{_bindir}/pyi-archive_viewer %{buildroot}/%{_bindir}/pyi-archive_viewer3
mv %{buildroot}/%{_bindir}/pyi-bindepend      %{buildroot}/%{_bindir}/pyi-bindepend3
mv %{buildroot}/%{_bindir}/pyi-grab_version   %{buildroot}/%{_bindir}/pyi-grab_version3
mv %{buildroot}/%{_bindir}/pyi-makespec       %{buildroot}/%{_bindir}/pyi-makespec3
mv %{buildroot}/%{_bindir}/pyi-set_version    %{buildroot}/%{_bindir}/pyi-set_version3
mv %{buildroot}/%{_bindir}/pyinstaller        %{buildroot}/%{_bindir}/pyinstaller3

popd
python2 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}

%check
# future is required for python2 make check
pip2 install -U future
pip2 install -U pathlib2
pip2 install -U funcsigs
pip2 install -U pluggy
pip2 install -U more-itertools
pip2 install -U dis3
pip2 install -U altgraph
pip2 install -U subprocess32
# Skip tkinter and idlelib related test
# as our python is not compiled with Tcl/Tk.
# We don't have Tk.
LANG=en_US.UTF-8 py.test2 tests/unit tests/functional \
    -k "not test_tkinter and not test_idlelib"

# Skip python3 make check, as python3.6 is not supported by 3.2.1

%files
%defattr(-,root,root)
%{_bindir}/pyi-archive_viewer
%{_bindir}/pyi-bindepend
%{_bindir}/pyi-grab_version
%{_bindir}/pyi-makespec
%{_bindir}/pyi-set_version
%{_bindir}/pyinstaller

%{python2_sitelib}/*
%{_bindir}/pyi-archive_viewer3
%{_bindir}/pyi-bindepend3
%{_bindir}/pyi-grab_version3
%{_bindir}/pyi-makespec3
%{_bindir}/pyi-set_version3
%{_bindir}/pyinstaller3
%exclude %{python2_sitelib}/PyInstaller/bootloader/Darwin-64bit
%exclude %{python2_sitelib}/PyInstaller/bootloader/Linux-32bit
%ifarch aarch64
%exclude %{python2_sitelib}/PyInstaller/bootloader/Linux-64bit
%endif
%exclude %{python2_sitelib}/PyInstaller/bootloader/Windows-32bit
%exclude %{python2_sitelib}/PyInstaller/bootloader/Windows-64bit

%files -n python3-pyinstaller
%defattr(-,root,root,-)
%{_bindir}/*
%{python3_sitelib}/*
%exclude %{python3_sitelib}/PyInstaller/bootloader/Darwin-64bit
%exclude %{python3_sitelib}/PyInstaller/bootloader/Linux-32bit
%ifarch aarch64
%exclude %{python3_sitelib}/PyInstaller/bootloader/Linux-64bit
%endif
%exclude %{python3_sitelib}/PyInstaller/bootloader/Windows-32bit
%exclude %{python3_sitelib}/PyInstaller/bootloader/Windows-64bit

%changelog
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
