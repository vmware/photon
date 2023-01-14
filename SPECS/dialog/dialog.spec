%global dialogsubversion 20220728

Summary:       A utility for creating TTY dialog boxes
Name:          dialog
Version:       1.3
Release:       8.20220728%{?dist}
License:       LGPLv2
URL:           http://invisible-island.net/dialog/dialog.html
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       https://invisible-mirror.net/archives/dialog/%{name}-%{version}-%{dialogsubversion}.tgz
%define sha512 %{name}=dddceaf00bfec4b53f2cf67e51d4c54841d9db337536657c21bc8f324a0eb9c6d621f00e09bfb741bd263f171dde38cfea87568f86daf04a9e88575a0ed61218

BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: findutils
BuildRequires: libtool

%description
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces.  Dialog is called
from within a shell script.  The following dialog boxes are implemented:
yes/no, menu, input, message, text, info, checklist, radiolist, and
gauge.

Install dialog if you would like to create TTY dialog boxes.

%package       devel
Summary:       Development files for building applications with the dialog library
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      ncurses-devel

%description   devel
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces. This package
contains the files needed for developing applications, which use the
dialog library.

%prep
%autosetup -p1 -n %{name}-%{version}-%{dialogsubversion}

%build
%configure \
    --enable-nls \
    --with-libtool \
    --with-ncursesw
%make_build

%install
# prepare packaged samples
rm -rf _samples
mkdir _samples
cp -a samples _samples
rm -rf _samples/samples/install
find _samples -type f -print0 | xargs -0 chmod a-x
%make_install %{?_smp_mflags}

# configure incorrectly use '-m 644' for library, fix it
chmod +x %{buildroot}%{_libdir}/*
rm -rf %{buildroot}%{_libdir}/.libs

%find_lang %{name}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING dialog.lsm README _samples/samples
%{_bindir}/dialog
%{_libdir}/libdialog.so.*
%{_mandir}/man1/dialog.*

%files devel
%defattr(-,root,root,0755)
%{_bindir}/dialog-config
%{_includedir}/*.h
%{_libdir}/libdialog.so
%exclude %{_libdir}/libdialog.a
%{_mandir}/man3/dialog.*

%changelog
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3-8.20220728
- Bump version as a part of gettext upgrade
* Mon Oct 10 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3-7.20220728
- Update to 20220728
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3-7.20220526
- Remove .la files
* Wed Jun 01 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3-6.20220526
- Automatic Version Bump
* Fri Aug 28 2020 Michelle Wang <michellew@vmware.com> 1.3-5.20200327
- Update to 20200327
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 1.3-4.20180621
- Fix library permission.
* Wed Sep 19 2018 Bo Gan <ganb@vmware.com> 1.3-3.20180621
- Update to 20180621
* Wed Apr 19 2017 Bo Gan <ganb@vmware.com> 1.3-2.20170131
- update to 20170131
* Mon May 30 2016 Nick Shi <nshi@vmware.com> 1.3-1.20160209
- Initial version
