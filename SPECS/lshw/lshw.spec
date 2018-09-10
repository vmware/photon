Summary:        Hardware lister
Name:           lshw
Version:        T.00.07
Release:        1%{?dist}
License:        GPLv2
URL:            http://ezix.org/project/wiki/HardwareLiSter
Source0:        http://www.ezix.org/software/files/%{name}-%{version}.tar.gz
%define sha1 lshw=e38265948e0be98c02dbc84939d6c6da1c86ea10
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
*    Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> T.00.07-1
-    Update version to T.00.07.
*    Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> B.02.18-1
-    Initial version of lshw package for Photon.
