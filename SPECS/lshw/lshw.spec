Summary:        Hardware lister
Name:           lshw
Version:        B.02.19
Release:        4%{?dist}
URL:            https://github.com/lyonel/lshw/releases
Source0:        http://www.ezix.org/software/files/%{name}-%{version}.tar.gz
Source1:        license.txt
%include        %{SOURCE1}
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

%description
lshw is a small tool to provide detailed informaton on the hardware
configuration of the machine. It can report exact memory configuration,
firmware version, mainboard configuration, CPU version and speed, cache
configuration, bus speed, etc. Information can be displayed in plain text,
XML or HTML.

%package        docs
Summary:        lshw docs
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description    docs
The package contains lshw doc files.

%prep
%autosetup -p1

%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_sbindir}/lshw

%files docs
%defattr(-,root,root)
/usr/share/*

%changelog
* Sat Aug 16 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> B.02.19-4
- Fix requires on doc sub package
* Thu Jul 31 2025 Michelle Wang <michelle.wang@broadcom.com> B.02.19-3
- Ignore copyleft license CC-BY-SA-3.0 for docs subpackage
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> B.02.19-2
- Release bump for SRP compliance
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> B.02.19-1
- Automatic Version Bump
* Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> B.02.18-1
- Initial version of lshw package for Photon.
