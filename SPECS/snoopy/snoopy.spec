Summary:        snoopy is a tiny library that logs all executed commands
Name:           snoopy
Version:        2.4.10
Release:        1%{?dist}
License:        GNU GPLv2
URL:            https://github.com/a2o/snoopy/archive/snoopy-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1 snoopy=a3333484903f2600efd553b80df30866cb490ef7
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

%build

mkdir -p build/m4
mkdir -p lib/iniparser/build/m4
autoreconf -i -v
rm -f config.h.in~

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
*   Thu Jan 19 2021 Vikash Bansal <bvikas@vmware.com> 2.4.10-1
-   Update to version 2.4.10
*   Thu Sep 18 2019 Ashwin H <ashwinh@vmware.com> 2.4.6-1
-   snoopy initial version

