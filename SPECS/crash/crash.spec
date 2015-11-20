Name:          crash
Version:       7.1.3
Release:       1%{?dist}
Summary:       kernel crash analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles
Group:         Development/Tools
Vendor:	       VMware, Inc.
Distribution:  Photon
URL:           http://people.redhat.com/anderson/
Source:        http://people.redhat.com/anderson/crash-%{version}.tar.gz
%define sha1 crash=bd303380711f2f832c3ed0f135d1ebe16e8802d2
License:       GPL
BuildRequires: binutils
BuildRequires: glibc-devel
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
Requires:      binutils
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

%package devel
Group:         Development/Libraries
Summary:       Libraries and headers for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
Requires:      zlib-devel

%description devel
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

This package contains libraries and header files need for development.

%prep
%setup -q -n %{name}-%{version}

%build
make RPMPKG=%{version}-%{release}

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
mkdir -p %{buildroot}%{_bindir}
%makeinstall
install -pm 644 crash %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man8
install -pm 644 crash.8 %{buildroot}%{_mandir}/man8/crash.8
mkdir -p %{buildroot}%{_includedir}/crash
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/crash

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%{_bindir}/crash
%{_mandir}/man8/crash.8.gz
%doc COPYING3 README

%files devel
%defattr(-,root,root)
%dir %{_includedir}/crash
%{_includedir}/crash/*.h

%changelog
*	Wed Nov 18 2015 Anish Swaminathan <anishs@vmware.com> 2.7-1
-	Initial build. First version
