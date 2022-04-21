Summary:       Application to detect if running in virtual machine
Name:          virt-what
Version:       1.22
Release:       1%{?dist}
URL:           https://people.redhat.com/~rjones/virt-what/files/
Source0:       https://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz
License:       GPLv2
Group:         Applications/System
%define sha512 %{name}=d430281edd9aaaa29f5475ab0a750ce0b2a3641fe5798769e38169e1c7879b2ee455f6c6c015cd069523045144ebcc3c4f58d205c4366b07721469a0aaa964d6
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
* Thu Apr 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.22-1
- Automatic Version Bump
* Mon Apr 19 2021 Gerrit Photon <photon-checkins@vmware.com> 1.21-1
- Automatic Version Bump
* Tue Aug 18 2020 Him Kalyan Bordoloi <bordoloih@vmware.com>  1.20-1
- Initial release.
