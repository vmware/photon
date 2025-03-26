Summary:       IPTraf-ng is a console-based network statistics utility
Name:          iptraf-ng
Version:       1.2.1
Release:       3%{?dist}
URL:           https://github.com/iptraf-ng/iptraf-ng
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/iptraf-ng/iptraf-ng/archive/%{name}-v%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ncurses-devel

Provides: iptraf
Obsoletes: iptraf

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
%make_build prefix=%{_prefix}

%install
%make_install prefix=%{_prefix} %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sbindir}/iptraf-ng
%{_mandir}/man8/iptraf-ng.8.gz

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.2.1-3
- Release bump for SRP compliance
* Tue Dec 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.1-2
- Add provies & obsoletes iptraf
* Mon Oct 19 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.2.1-1
- Initial build; first version.
