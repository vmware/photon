Summary:        snoopy is a tiny library that logs all executed commands
Name:           snoopy
Version:        2.5.1
Release:        2%{?dist}
URL:            https://github.com/a2o/snoopy/archive/snoopy-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha512  snoopy=2c0cde306ff58fe7f19c4df9aecab2c6936d71b77471bbb363ca660254b780a6874163988ebc6882b75d18319891bd1d5b5ef524f158f7645466c93e4dbe987f

Source1: license.txt
%include %{SOURCE1}
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
*   Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 2.5.1-2
-   Release bump for SRP compliance
*   Tue Nov 01 2022 Gerrit Photon <photon-checkins@vmware.com> 2.5.1-1
-   Automatic Version Bump
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
