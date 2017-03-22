Summary:	fatrace reports file access events from all running processes.
Name:		fatrace
Version:	0.12
Release:	2%{?dist}
License:	GNU GPLv3
URL:		https://launchpad.net/fatrace
Source0:	https://launchpad.net/fatrace/trunk/0.12/+download/%{name}-%{version}.tar.bz2
%define sha1 fatrace=af7d1249307c2d24083a7d9395464e72601ad358
Patch0:		fatrace-sysmacros.patch
Requires:	python2
Group:		Utilities
Vendor:		VMware, Inc.
Distribution:   Photon

%description
fatrace reports file access events from all running processes.
Its main purpose is to find processes which keep waking up the disk unnecessarily and thus prevent some power saving.

%prep
%setup -q
%patch0 -p1

%build
make %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/*

%changelog
*   Fri Mar 24 2017 Alexey Makhalov <amakhalov@vmware.com> 0.12-2
-   Added fatrace-sysmacros.patch to fix build issue with glibc-2.25
*   Mon Feb 6 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.12-1
-   initial version
