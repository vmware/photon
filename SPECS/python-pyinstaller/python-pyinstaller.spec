%define debug_package %{nil}
%define srcname PyInstaller

Summary:        PyInstaller bundles a Python application and all its dependencies into a single package.
Name:           python-pyinstaller
Version:        3.4
Release:        4%{?dist}
Url:            https://pypi.python.org/pypi/PyInstaller
License:        GPLv2+
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/source/P/PyInstaller/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=8a1e0065e8c7760ffcae906d3469914c98a69139658a3a85f1bb7b1a63265e33603314586897bf3b588400d2bdd48bb6ee06cef68c19232c4ec8a8df84e57330

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml
BuildRequires: zlib-devel

Requires: python2
Requires: python-setuptools
Requires: python-xml
Requires: python-altgraph
Requires: python-macholib
Requires: python-pefile
Requires: python-dis3

%description
PyInstaller bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules.
PyInstaller reads a Python script written by you. It analyzes your code to discover every other module and library your script needs in order to execute. Then it collects copies of all those files – including the active Python interpreter! – and puts them with your script in a single folder, or optionally in a single executable file.

PyInstaller is tested against Windows, Mac OS X, and Linux. However, it is not a cross-compiler: to make a Windows app you run PyInstaller in Windows; to make a Linux app you run it in Linux, etc. PyInstaller has been used successfully with AIX, Solaris, and FreeBSD, but is not tested against them.

%package -n     python3-pyinstaller
Summary:        Python 3 version
Requires:       python3
Requires:       zlib
Requires:       python3-setuptools
Requires:       python3-xml
Requires:       python3-altgraph
Requires:       python3-macholib
Requires:       python3-pefile
Conflicts:      python-pyinstalled < 3.4-4%{?dist}

%description -n python3-pyinstaller
Python 3 version.

%prep
%autosetup -p1 -n %{srcname}-%{version}
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
mv %{buildroot}%{_bindir}/pyi-archive_viewer %{buildroot}%{_bindir}/pyi-archive_viewer3
mv %{buildroot}%{_bindir}/pyi-bindepend      %{buildroot}%{_bindir}/pyi-bindepend3
mv %{buildroot}%{_bindir}/pyi-grab_version   %{buildroot}%{_bindir}/pyi-grab_version3
mv %{buildroot}%{_bindir}/pyi-makespec       %{buildroot}%{_bindir}/pyi-makespec3
mv %{buildroot}%{_bindir}/pyi-set_version    %{buildroot}%{_bindir}/pyi-set_version3
mv %{buildroot}%{_bindir}/pyinstaller        %{buildroot}%{_bindir}/pyinstaller3
popd

python2 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/pyi-archive_viewer
%{_bindir}/pyi-bindepend
%{_bindir}/pyi-grab_version
%{_bindir}/pyi-makespec
%{_bindir}/pyi-set_version
%{_bindir}/pyinstaller

%{python_sitelib}/*
%exclude %{python_sitelib}/%{srcname}/bootloader/Darwin-64bit
%exclude %{python_sitelib}/%{srcname}/bootloader/Linux-32bit
%ifarch aarch64
%exclude %{python_sitelib}/%{srcname}/bootloader/Linux-64bit
%endif
%exclude %{python_sitelib}/%{srcname}/bootloader/Windows-32bit
%exclude %{python_sitelib}/%{srcname}/bootloader/Windows-64bit

%files -n python3-pyinstaller
%defattr(-,root,root,-)
%{_bindir}/pyi-archive_viewer3
%{_bindir}/pyi-bindepend3
%{_bindir}/pyi-grab_version3
%{_bindir}/pyi-makespec3
%{_bindir}/pyi-set_version3
%{_bindir}/pyinstaller3
%{python3_sitelib}/*
%exclude %{python3_sitelib}/%{srcname}/bootloader/Darwin-64bit
%exclude %{python3_sitelib}/%{srcname}/bootloader/Linux-32bit
%ifarch aarch64
%exclude %{python3_sitelib}/%{srcname}/bootloader/Linux-64bit
%endif
%exclude %{python3_sitelib}/%{srcname}/bootloader/Windows-32bit
%exclude %{python3_sitelib}/%{srcname}/bootloader/Windows-64bit

%changelog
* Fri Aug 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.4-4
- Fix file packaging
* Thu Feb 11 2021 Ankit Jain <ankitja@vmware.com> 3.4-3
- Fix pyinstaller by adding requires
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
