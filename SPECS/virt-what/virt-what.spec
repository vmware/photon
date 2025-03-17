Summary:       Application to detect if running in virtual machine
Name:          virt-what
Version:       1.25
Release:       2%{?dist}
URL:           https://people.redhat.com/~rjones/virt-what/files/
Source0:       https://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Group:         Applications/System
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
* Wed Dec 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 1.25-2
- Release bump for SRP compliance
* Thu Aug 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.25-1
- Automatic Version Bump
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.24-1
- Automatic Version Bump
* Thu Apr 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.22-1
- Automatic Version Bump
* Mon Apr 19 2021 Gerrit Photon <photon-checkins@vmware.com> 1.21-1
- Automatic Version Bump
* Tue Aug 18 2020 Him Kalyan Bordoloi <bordoloih@vmware.com>  1.20-1
- Initial release.
