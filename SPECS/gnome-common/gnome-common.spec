Summary:        Common development macros for GNOME
Name:           gnome-common
Version:        3.14.0
Release:        1%{?dist}
License:        GPL
URL:            https://www.gnome.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{version}/%{name}-%{version}.tar.xz
%define sha1 gnome-common=555ac7de25821f243f1838faa4d602da50237303
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

%description
This provides Common development macros for GNOME.

%prep
%setup -q
./autogen.sh

%build
./configure \
        --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/gnome-autogen.sh
%{_bindir}/gnome-doc-common
/usr/share/aclocal/ax_check_enable_debug.m4
/usr/share/aclocal/ax_code_coverage.m4
/usr/share/aclocal/gnome-code-coverage.m4
/usr/share/aclocal/gnome-common.m4
/usr/share/aclocal/gnome-compiler-flags.m4
/usr/share/gnome-common/data/omf.make
/usr/share/gnome-common/data/xmldocs.make

%changelog
*       Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.14.0-1
-       Add gnome-common v3.14.0

