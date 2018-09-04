Name:           makedumpfile
Summary:        Tool to make a small dumpfile of kdump
Version:        1.6.4
Release:        1%{?dist}
License:        GPLv2
Group:          Applications/System
Url:            https://www.kernel.org/doc/Documentation/kdump/kdump.txt
Source0:        https://sourceforge.net/projects/makedumpfile/files/makedumpfile/%{version}/%{name}-%{version}.tar.gz
%define sha1 makedumpfile=2ec04ae267c7a216193c1c7a227aca78fe40a3fd
Vendor:		VMware, Inc.
Distribution:	Photon

BuildRequires:  elfutils-devel-static
BuildRequires:	bzip2-devel-static
BuildRequires:  elfutils-libelf-devel-static
Requires:       kexec-tools
%description

%prep
%setup -q

%build
make

%install
install -D -m 0755 makedumpfile %{buildroot}%{_sbindir}/makedumpfile
install -D -m 0755 makedumpfile-R.pl %{buildroot}%{_sbindir}/makedumpfile-R.pl
install -D -m 0644 makedumpfile.8 %{buildroot}%{_mandir}/man8/makedumpfile.8
install -D -m 0644 makedumpfile.conf.5 %{buildroot}%{_mandir}/man5/makedumpfile.conf.5
install -d -m 0755 %{buildroot}%{_datadir}/%{name}-%{version}/eppic_scripts
install -m 0644 -t %{buildroot}%{_datadir}/%{name}-%{version}/eppic_scripts/ eppic_scripts/*

%files
%defattr(-,root,root)
%doc README COPYING IMPLEMENTATION
%{_mandir}/man?/*
%{_sbindir}/*
%dir %{_datadir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}/eppic_scripts/

%changelog
*   Fri Aug 24 2018 Him Kalyan Bordoloi <bordoloih@vmware.com>  1.6.4-1
-   Initial version
