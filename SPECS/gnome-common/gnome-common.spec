Summary:        Common development macros for GNOME
Name:           gnome-common
Version:        3.18.0
Release:        3%{?dist}
License:        GPL
URL:            https://www.gnome.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{version}/%{name}-%{version}.tar.xz
%define sha1 gnome-common=332e514961374a54dc065b86032eaeb03d6d3cee
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

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
%{_datadir}/aclocal/*.m4

%changelog
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.18.0-3
-   Fix arch
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.18.0-2
-	GA - Bump release of all rpms
* 	Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  3.18.0-1
- 	Upgrade to 3.18.0
*       Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.14.0-1
-       Add gnome-common v3.14.0

