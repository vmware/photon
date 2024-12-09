Summary:        fatrace reports file access events from all running processes.
Name:           fatrace
Version:        0.15
Release:        2%{?dist}
URL:            https://launchpad.net/fatrace
Source0:        https://launchpad.net/fatrace/trunk/%{version}/+download/%{name}-%{version}.tar.bz2
%define sha512 fatrace=f4c4c4054537c3ce6d99be7baa8a269c6aae74cd71ad5f43cc82dba6572979d4fd11c423254f661b7b83d958de4c50210820af865d16fd5c1ca0d5d8213b59ba

Source1: license.txt
%include %{SOURCE1}
Requires:       python3
Group:          Utilities
Vendor:         VMware, Inc.
Distribution:   Photon

%description
fatrace reports file access events from all running processes.
Its main purpose is to find processes which keep waking up the disk unnecessarily and thus prevent some power saving.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install %{_smp_mflags}

%check
make -k check %{_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/*

%changelog
*   Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.15-2
-   Release bump for SRP compliance
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 0.15-1
-   Automatic Version Bump
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 0.13-2
-   Require python3
*   Thu Sep 20 2018 Sujay G <gsujay@vmware.com> 0.13-1
-   Bump fatrace version to 0.13
*   Fri Mar 24 2017 Alexey Makhalov <amakhalov@vmware.com> 0.12-2
-   Added fatrace-sysmacros.patch to fix build issue with glibc-2.25
*   Mon Feb 6 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.12-1
-   initial version
