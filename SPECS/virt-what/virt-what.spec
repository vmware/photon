Summary:       Application to detect if running in virtual machine
Name:          virt-what
Version:       1.24
Release:       1%{?dist}
URL:           https://people.redhat.com/~rjones/virt-what/files/
Source0:       https://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz
License:       GPLv2
Group:         Applications/System
%define sha512 %{name}=f6d14ea402f737ce45e67637076a5c11d3fcdbc64a738851fd0ffabec374074c7a9cf857719e0c8cad87b41fc4e78b825ebedafa6fa14e414a4068fca4f5d99c
Vendor:        VMware, Inc.
Distribution:  Photon
BuildRequires: gcc

%description
virt-what is a shell script which can be used to detect if the program is running in a virtual machine

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} %{_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libexecdir}/virt-what-cpuid-helper
%{_sbindir}/virt-what
%{_mandir}/man1/virt-what.1.gz

%changelog
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.24-1
- Automatic Version Bump
* Thu Apr 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.22-1
- Automatic Version Bump
* Mon Apr 19 2021 Gerrit Photon <photon-checkins@vmware.com> 1.21-1
- Automatic Version Bump
* Tue Aug 18 2020 Him Kalyan Bordoloi <bordoloih@vmware.com>  1.20-1
- Initial release.
