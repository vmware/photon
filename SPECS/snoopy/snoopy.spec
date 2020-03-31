Summary:        snoopy is a tiny library that logs all executed commands
Name:           snoopy
Version:        2.4.6
Release:        2%{?dist}
License:        GNU GPLv2
URL:            https://github.com/a2o/snoopy/archive/snoopy-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         snoopy_64bit.patch
%define sha1 snoopy=a5d59431baff5eab90305c32aa3cc25f725ae5a8
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  socat
BuildRequires:  gzip

%description
Snoopy is a tiny library that logs all executed commands
(+ arguments) on your system.


%prep
%setup -n %{name}-%{name}-%{version}
%patch0 -p1

%build

mkdir -p build/m4
mkdir -p lib/iniparser/build/m4
autoreconf -i -v
rm -f config.h.in~
export CFLAGS="-O2 -g -Wno-error=stringop-truncation -Wno-error=stringop-overflow"
%configure \
     --enable-config-file
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete

%preun
#snoopy-enable adds entry to /etc/ld.so.preload
#call snoopy-disable incase it was missed calling
#before uninstall
cat /etc/ld.so.preload | grep snoopy
if [ $? -eq 0 ] ; then
   snoopy-disable
fi

%files
%defattr(-,root,root)
%{_libdir}/*.*
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/snoopy.ini

%changelog
*   Fri Apr 03 2020 Alexey Makhalov <amakhalov@vmware.com> 2.4.6-2
-   Fix compilation issue with gcc-8.4.0
*   Wed Sep 18 2019 Ashwin H <ashwinh@vmware.com> 2.4.6-1
-   snoopy initial version

