Name:           traceroute
Summary:        Traces the route taken by packets over an IPv4/IPv6 network
Version:        2.1.3
Release:        2%{?dist}
Group:          Applications/Internet
Url:            http://traceroute.sourceforge.net
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://downloads.sourceforge.net/project/traceroute/traceroute/traceroute-%{version}/traceroute-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.

%prep
%autosetup -p1

%build
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS=""

%install
install -d %{buildroot}%{_bindir}
install -m755 %{name}/%{name} %{buildroot}%{_bindir}

install -m755 wrappers/tcptraceroute %{buildroot}%{_bindir}

install -d %{buildroot}%{_mandir}/man8
install -p -m644 traceroute/traceroute.8 %{buildroot}%{_mandir}/man8
pushd %{buildroot}%{_mandir}/man8
ln -sv traceroute.8 tcptraceroute.8
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README TODO CREDITS
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2.1.3-2
- Release bump for SRP compliance
* Fri Nov 03 2023 Mukul Sikka <msikka@vmware.com> 2.1.3-1
- Version Update to fix CVE-2023-46316
* Fri Mar 10 2023 Michelle Wang <michellew@vmware.com> 2.1.0-5
- remove duplicate _bindir in files
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.1.0-4
- Fix binary path
* Fri Nov 30 2018 Ashwin H <ashwinh@vmware.com> 2.1.0-3
- Remove traceroute6 softlink as iputils provides traceroute6
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
- Ensure non empty debuginfo
* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.0-1
- Updated to version 2.1.0.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.22-2
- GA - Bump release of all rpms
* Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com>  2.0.22-1
- Initial version
