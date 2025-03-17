Summary:        Hardware lister
Name:           lshw
Version:        B.02.19
Release:        2%{?dist}
URL:            https://github.com/lyonel/lshw/releases
Source0:        http://www.ezix.org/software/files/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
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
%autosetup -p1

%build
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_sbindir}/lshw

%files docs
%defattr(-,root,root)
/usr/share/*

%changelog
*    Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> B.02.19-2
-    Release bump for SRP compliance
*    Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> B.02.19-1
-    Automatic Version Bump
*    Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> B.02.18-1
-    Initial version of lshw package for Photon.
