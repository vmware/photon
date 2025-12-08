Summary:       IPTraf-ng is a console-based network statistics utility
Name:          iptraf-ng
Version:       1.2.2
Release:       1%{?dist}
License:       GPLv2
URL:           https://github.com/iptraf-ng/iptraf-ng
Source:        https://github.com/iptraf-ng/iptraf-ng/archive/%{name}-v%{version}.tar.gz
%define sha512 iptraf-ng=275a345ffd3ab9578c4d159c3a8667326224b4a58b2e7787c4db518b81973d87c04b4b6c5275a721858d01a9b44a0200f8defc06c6f88655aa38d4fa6146ea1d
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon

BuildRequires: ncurses-devel

%description
IPTraf-ng is a console-based network monitoring program for Linux that
displays information about IP traffic. It returns information such as:
- Current TCP connections
- UDP, ICMP, OSPF, and other types of IP packets
- Packet and byte counts on TCP connections
- IP, TCP, UDP, ICMP, non-IP, and other packet and byte counts
- TCP/UDP counts by ports
- Packet counts by packet sizes
- Packet and byte counts by IP address
- Interface activity
- Flag statuses on TCP packets
- LAN station statistics

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sbindir}/iptraf-ng
%{_mandir}/man8/iptraf-ng.8.gz

%changelog
* Mon Dec 08 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 1.2.2-1
- Upgrade version
* Mon Oct 19 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.2.1-1
- Initial build; first version.
