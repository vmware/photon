Summary:        Hardware lister
Name:           lshw
Version:        B.02.19
Release:        1%{?dist}
License:        GPLv2
URL:            https://github.com/lyonel/lshw/releases
Source0:        http://www.ezix.org/software/files/%{name}-%{version}.tar.gz
%define sha1 lshw=c4751be7292e8f2d8f5d82ba25acaebf24d9e7d7
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

%description
lshw is a small tool to provide detailed informaton on the hardware
configuration of the machine. It can report exact memory configuration,
firmware version, mainboard configuration, CPU version and speed, cache
configuration, bus speed, etc. Information can be displayed in plain text,
XML or HTML.

%package docs
Summary:        lshw docs
Group:          Applications/System
%description docs
The package contains lshw doc files.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_sbindir}/lshw

%files docs
%defattr(-,root,root)
/usr/share/*

%changelog
*    Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> B.02.19-1
-    Automatic Version Bump
*    Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> B.02.18-1
-    Initial version of lshw package for Photon.
