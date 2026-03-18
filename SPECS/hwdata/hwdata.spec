%global build_if %{photon_subrelease} >= 92

Summary:        Hardware identification and configuration data
Name:           hwdata
Version:        0.405
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Base
BuildArch:      noarch
URL:            https://github.com/vcrhonek/hwdata
Source0:        https://github.com/vcrhonek/hwdata/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  make

%description
hwdata contains various hardware identification and configuration data,
such as the pci.ids, usb.ids, and pnp.ids databases.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains the pkgconfig file for %{name}.

%prep
%autosetup -p1

%build
%configure
# It's just text files, so there is nothing to actually compile here.

%install
%make_install libdir=%{_libdir}

%files
%defattr(-,root,root)
%license COPYING
%doc LICENSE
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_libdir}/modprobe.d/dist-blacklist.conf

%files devel
%defattr(-,root,root)
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Sat Mar 28 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 0.405-1
- Initial build to support libdisplay-info
