Summary:        Common development macros for GNOME
Name:           gnome-common
Version:        3.18.0
Release:        2%{?dist}
License:        GPL
URL:            https://www.gnome.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{version}/%{name}-%{version}.tar.xz
%define sha1 gnome-common=332e514961374a54dc065b86032eaeb03d6d3cee
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
make %{?_smp_mflags} check 

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/gnome-autogen.sh
/usr/share/aclocal/ax_check_enable_debug.m4
/usr/share/aclocal/ax_code_coverage.m4
/usr/share/aclocal/gnome-code-coverage.m4
/usr/share/aclocal/gnome-common.m4
/usr/share/aclocal/gnome-compiler-flags.m4

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.18.0-2
-	GA - Bump release of all rpms
* 	Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  3.18.0-1
- 	Upgrade to 3.18.0
*       Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.14.0-1
-       Add gnome-common v3.14.0

