Summary:        snoopy is a tiny library that logs all executed commands
Name:           snoopy
Version:        2.4.15
Release:        1%{?dist}
License:        GNU GPLv2
URL:            https://github.com/a2o/snoopy/archive/snoopy-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha512  snoopy=2ef3e787ef9659e57e4f3f9961c5c865d887ab38f1a56d6dbec25e1efd2c3e8ceab938e7915a8cf92353f6a67bf530b0a5712b095f9b8a8a703411100fb2df95
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  socat
BuildRequires:  gzip

%description
Snoopy is a tiny library that logs all executed commands (+ arguments) on your system.

%prep
%autosetup -n %{name}-%{name}-%{version}

%build
mkdir -p build/m4
mkdir -p lib/iniparser/build/m4
autoreconf -i -v
rm -f config.h.in~
export CFLAGS="-O2 -g -Wno-error=stringop-truncation -Wno-error=stringop-overflow"
%configure \
     --enable-config-file
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
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
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 2.4.15-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.4.13-1
-   Automatic Version Bump
*   Tue Jan 19 2021 Vikash Bansal <bvikas@vmware.com> 2.4.10-1
-   Update to version 2.4.10
*   Fri Apr 03 2020 Alexey Makhalov <amakhalov@vmware.com> 2.4.6-2
-   Fix compilation issue with gcc-8.4.0
*   Wed Sep 18 2019 Ashwin H <ashwinh@vmware.com> 2.4.6-1
-   snoopy initial version
