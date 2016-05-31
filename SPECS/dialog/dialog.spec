Summary:       A utility for creating TTY dialog boxes
Name:          dialog
%global dialogsubversion 20160209
Version:       1.3
Release:       1.%{dialogsubversion}%{?dist}
License:       LGPLv2
URL:           http://invisible-island.net/dialog/dialog.html
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       ftp://invisible-island.net/dialog/dialog-%{version}-20160209.tgz
%define sha1 dialog=e52ac488c792697f0f6af8b41134ba2337fdf261
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
%setup -q -n %{name}-%{version}-%{dialogsubversion}
%patch1 -p1 -b .incdir
%patch2 -p1 -b .multilib
%patch3 -p1 -b .libs

%build
%configure \
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

make DESTDIR=%{buildroot} install

chmod 755 %{buildroot}/%{_libdir}/libdialog.so.*.*.*
rm -f %{buildroot}/%{_libdir}/libdialog.{,l}a

%find_lang %{name}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc COPYING dialog.lsm README _samples/samples
%{_bindir}/dialog
%{_libdir}/libdialog.so.13*
%{_mandir}/man1/dialog.*

%files devel
%{_bindir}/dialog-config
%{_includedir}/dialog
%{_libdir}/libdialog.so
%{_mandir}/man3/dialog.*

%changelog
*	Fri May 30 2016 Nick Shi <nshi@vmware.com> - 1.3-1.20160209
-	Initial version
