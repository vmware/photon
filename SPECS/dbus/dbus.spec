Summary:	DBus for systemd
Name:		dbus
Version:	1.13.6
Release:	2%{?dist}
License:	GPLv2+ or AFL
URL:		http://www.freedesktop.org/wiki/Software/dbus
Group:		Applications/File
Source0:	http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
%define sha1 dbus=368c14e3dde9524dd9d0775227ebf3932802c023
Patch0:         CVE-2019-12749.patch
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	expat
BuildRequires:	systemd
BuildRequires:	xz-devel
Requires:	expat
Requires:	systemd
Requires:	xz
%description
The dbus package contains dbus.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications

%prep
%setup -q
%patch0 -p1

%build
./configure --prefix=%{_prefix}                 \
            --sysconfdir=%{_sysconfdir}         \
            --localstatedir=%{_var}             \
            --docdir=%{_datadir}/doc/dbus-1.13.6  \
            --with-console-auth-dir=/run/console

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm755 %{buildroot}%{_lib}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
/etc/*
%{_bindir}/*
%{_lib}/*
/lib/*
%{_libexecdir}/*
%{_docdir}/*
%{_datadir}/dbus-1

%files	devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/xml/dbus-1
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
*   Mon Jan 06 2020 Sujay G <gsujay@vmware.com> 1.13.6-2
-   Fix CVE-2019-12749
*   Wed Jun 19 2019 Sujay G <gsujay@vmware.com> 1.13.6-1
-   Version bump to 1.13.6 to fix CVE-2014-7824 & CVE-2015-0245
*   Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 1.8.8-6
-   Release bump for expat version update
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.8-5
-   GA - Bump release of all rpms
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.8-4
-   Created devel sub-package
*   Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 1.8.8-3
-   Remove debug files.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.8.8-2
-   Update according to UsrMove.
*   Sun Apr 06 2014 Sharath George <sharathg@vmware.com> 1.8.8
-   Initial build. First version
