%global dialogsubversion 20180621

Summary:       A utility for creating TTY dialog boxes
Name:          dialog
Version:       1.3
Release:       5.20180621%{?dist}
License:       LGPLv2
URL:           http://invisible-island.net/dialog/dialog.html
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       ftp://invisible-island.net/dialog/%{name}-%{version}-20180621.tar.gz
%define sha512 dialog=1c6d794af50a12294e32b99fd9d3eb9451ac4a2f21c5567848b59c7a316b3058463c41fb8f9eb0bce68edbbe463234a6ec893f7a013ceb953eb5da0effe0d274
BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: findutils
BuildRequires: libtool
Patch1:        dialog-incdir.patch
Patch2:        dialog-multilib.patch
Patch3:        dialog-libs.patch

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
sh ./configure --host=%{_host} --build=%{_build} \
    --disable-dependency-tracking \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-nls \
    --with-libtool \
    --with-ncursesw \
    --includedir=%{_includedir}/dialog

make %{?_smp_mflags}

%install
# prepare packaged samples
rm -rf _samples
mkdir _samples
cp -a samples _samples
rm -rf _samples/samples/install
find _samples -type f -print0 | xargs -0 chmod a-x

make DESTDIR=%{buildroot} install %{?_smp_mflags}

# configure incorrectly use '-m 644' for library, fix it
chmod +x %{buildroot}%{_libdir}/*

%find_lang %{name}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc COPYING dialog.lsm README _samples/samples
%{_bindir}/dialog
%{_libdir}/libdialog.so.*
%{_mandir}/man1/dialog.*

%files devel
%{_bindir}/dialog-config
%{_includedir}/dialog
%{_libdir}/libdialog.so
%exclude %{_libdir}/libdialog.a
%{_mandir}/man3/dialog.*

%changelog
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3-5.20180621
- Remove .la files
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 1.3-4.20180621
- Fix library permission.
* Wed Sep 19 2018 Bo Gan <ganb@vmware.com> 1.3-3.20180621
- Update to 20180621
* Wed Apr 19 2017 Bo Gan <ganb@vmware.com> 1.3-2.20170131
- update to 20170131
* Mon May 30 2016 Nick Shi <nshi@vmware.com> 1.3-1.20160209
- Initial version
