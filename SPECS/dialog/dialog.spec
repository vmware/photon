%global dialogsubversion 20200327

Summary:       A utility for creating TTY dialog boxes
Name:          dialog
Version:       1.3
Release:       6.20200327%{?dist}
License:       LGPLv2
URL:           http://invisible-island.net/dialog/dialog.html
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       https://invisible-mirror.net/archives/dialog/%{name}-%{version}-%{dialogsubversion}.tar.gz
%define sha512  dialog=c8c7ccd86fa189a2b6739320f59f127512e53f908ed257280099f8c45754da98d2095835d0c14090cd071af0ed6e8ff95f9938f5ca8027b0b7001c7fd746fe59

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
Requires:      %{name} = %{version}-%{release} ncurses-devel

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
%defattr(-,root,root)
%doc COPYING dialog.lsm README _samples/samples
%{_bindir}/dialog
%{_libdir}/libdialog.so.*
%{_mandir}/man1/dialog.*

%files devel
%defattr(-,root,root)
%{_bindir}/dialog-config
%{_includedir}/*.h
%{_libdir}/libdialog.so
%exclude %{_libdir}/libdialog.a
%{_mandir}/man3/dialog.*

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3-6.20200327
- Remove .la files
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
