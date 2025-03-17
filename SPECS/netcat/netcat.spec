Summary:    Netcat is a featured networking utility which reads and writes data across network connections, using the TCP/IP protocol.
Name:       netcat
Version:    0.7.1
Release:    6%{?dist}
URL:        http://netcat.sourceforge.net
Group:      Productivity/Networking/Other
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
Netcat is a featured networking utility which reads and writes data across network connections, using the TCP/IP protocol.
It is designed to be a reliable "back-end" tool that can be used directly or easily driven by other programs and scripts. At the same time, it is a feature-rich network debugging and exploration tool, since it can create almost any kind of connection you would need and has several interesting built-in capabilities.

%prep
%autosetup -p1

%build
%configure
%make_build %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}
%{_datadir}

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 0.7.1-6
- Release bump for SRP compliance
* Thu Oct 19 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-5
- Remove infodir
- Use standard build macros
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-4
- Use standard configure macros
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.7.1-3
- Removed packaging of debug files
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.1-2
- GA - Bump release of all rpms
* Tue Dec 08 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.7.1-1
- Initial build.    First version
